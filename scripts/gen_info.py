import json
import os
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone, timedelta

# 配置
TZ_CN = timezone(timedelta(hours=8))
MANIFEST_FILE = "manifest.json"
RELEASE_NOTE_FILE = "release_notes.md"
REPO = os.environ.get("GITHUB_REPOSITORY", "") 

def get_current_modules():
    """获取当前所有 Direct 依赖（即 tools.go 里引用的插件）"""
    # 关键修改：通过 Go 命令获取详细 JSON，包含 Replace 信息
    result = subprocess.run(['go', 'list', '-m', '-json', 'all'], capture_output=True, text=True)
    modules = {}
    
    decoder = json.JSONDecoder()
    pos = 0
    while pos < len(result.stdout):
        try:
            obj, size = decoder.raw_decode(result.stdout[pos:])
            
            # 过滤逻辑：
            # 1. 必须是 github.com 开头
            # 2. 不能是 Indirect (间接依赖)，只看我们在 tools.go 里显式引入的
            # 3. 排除 caddy 主程序自己
            if ('Path' in obj 
                and "github.com" in obj['Path'] 
                and not obj.get('Indirect', False)
                and obj['Path'] != "github.com/caddyserver/caddy"):
                
                # 记录详细信息，包括是否被 Replace
                modules[obj['Path']] = {
                    "Version": obj.get("Version", "unknown"),
                    "Time": obj.get("Time", ""),
                    "Replace": obj.get("Replace", None) # 捕获 Replace 字段
                }
            pos += size
        except Exception as e:
            # 容错处理
            pos += 1
            
    return modules

def get_previous_manifest():
    url = f"https://github.com/{REPO}/releases/latest/download/{MANIFEST_FILE}"
    try:
        # print(f"Downloading previous manifest from {url}...")
        with urllib.request.urlopen(url) as response:
            return json.loads(response.read().decode())
    except Exception:
        return {}

def parse_time(iso_str):
    if not iso_str: return "N/A"
    try:
        dt = datetime.fromisoformat(iso_str.replace('Z', '+00:00'))
        return dt.astimezone(TZ_CN).strftime('%Y-%m-%d %H:%M:%S')
    except:
        return iso_str

def format_date_simple(iso_str):
    if not iso_str: return "N/A"
    try:
        dt = datetime.fromisoformat(iso_str.replace('Z', '+00:00'))
        return dt.astimezone(TZ_CN).strftime('%Y-%m-%d')
    except: return "N/A"

def generate_notes(current, previous):
    diff_lines = []
    
    # 既然 current 里过滤掉了 caddy 核心，我们需要单独拿一下 caddy 核心版本
    # 这里简单处理，只对比插件变动
    
    diff_lines.append(f"### 📦 Plugin Changes\n")
    has_changes = False
    
    for name, info in current.items():
        prev_info = previous.get(name, {})
        curr_ver = info['Version']
        
        # 如果有 Replace，版本号可能在 Replace 对象里，这里为了日志简洁，
        # 我们优先显示 Replace 里的版本，如果都在，显示原始版本也行。
        # 这里维持原样，通常 info['Version'] 是最终解析版本
        
        prev_ver = prev_info.get('Version', 'N/A')
        curr_date = format_date_simple(info['Time'])
        prev_date = format_date_simple(prev_info.get('Time', ''))
        
        if curr_ver != prev_ver:
            diff_lines.append(f"- **{name.split('/')[-1]}**: `{prev_ver}` -> `{curr_ver}`")
            has_changes = True
        elif curr_date != prev_date and prev_date != "N/A":
             diff_lines.append(f"- **{name.split('/')[-1]}**: Update from {prev_date} to {curr_date}")
             has_changes = True

    if not has_changes:
        diff_lines.append("- No plugin updates detected in this build.")

    table_lines = []
    table_lines.append("\n### 🔌 Installed Plugins Status\n")
    table_lines.append("| Plugin | Version | Last Commit (Beijing) |")
    table_lines.append("| :--- | :--- | :--- |")
    
    sorted_keys = sorted(current.keys())
    xcaddy_args = []
    
    for name in sorted_keys:
        info = current[name]
        ver = info['Version']
        time_bj = parse_time(info['Time'])
        
        # 生成表格链接
        link = f"[{name.split('/')[-1]}](https://{name})"
        table_lines.append(f"| {link} | `{ver}` | {time_bj} |")
        
        # === 核心修复逻辑 ===
        # 如果存在 Replace (例如 forwardproxy)，生成特殊的 xcaddy 参数
        # 格式: --with github.com/A=github.com/B@version
        if info.get('Replace'):
            rep = info['Replace']
            rep_path = rep['Path']
            rep_ver = rep['Version']
            # 这里生成: --with github.com/old=github.com/new@v1.2.3
            xcaddy_args.append(f"--with {name}={rep_path}@{rep_ver}")
        else:
            # 普通插件: --with github.com/A@v1.2.3
            xcaddy_args.append(f"--with {name}@{ver}")

    return "\n".join(diff_lines + table_lines), " ".join(xcaddy_args)

def main():
    current_modules = get_current_modules()
    previous_modules = get_previous_manifest()
    
    notes, build_args = generate_notes(current_modules, previous_modules)
    
    # 打印生成的参数，方便在 Actions 日志里调试
    print(f"Generated xcaddy args: {build_args}")

    with open(RELEASE_NOTE_FILE, 'w') as f:
        f.write(notes)
    with open(MANIFEST_FILE, 'w') as f:
        json.dump(current_modules, f, indent=2)
        
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
             f.write(f"XCADDY_ARGS={build_args}\n")

if __name__ == "__main__":
    main()
