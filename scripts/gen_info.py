import json
import os
import subprocess
import re
import urllib.request
from datetime import datetime, timezone, timedelta

# 配置：严格定义北京时间
TZ_CN = timezone(timedelta(hours=8))
MANIFEST_FILE = "manifest.json"
RELEASE_NOTE_FILE = "release_notes.md"
REPO = os.environ.get("GITHUB_REPOSITORY", "") 

def get_modules_info():
    """获取模块信息，包含处理 Replace 和版本美化"""
    # 获取详细依赖 JSON
    result = subprocess.run(['go', 'list', '-m', '-json', 'all'], capture_output=True, text=True)
    
    modules = {}
    caddy_core_info = None

    decoder = json.JSONDecoder()
    pos = 0
    while pos < len(result.stdout):
        try:
            obj, size = decoder.raw_decode(result.stdout[pos:])
            
            # 基础过滤：排除 Main(自己)、排除非 github.com、排除 Indirect(间接依赖)
            if (not obj.get('Main') 
                and 'Path' in obj 
                and "github.com" in obj['Path'] 
                and not obj.get('Indirect', False)):
                
                # === 核心逻辑：处理 Replace (如 forwardproxy) ===
                # 如果有 Replace，我们只关心替换后的那个包的信息
                real_path = obj['Path']
                real_ver = obj.get('Version', 'unknown')
                real_time = obj.get('Time', '')
                is_replaced = False

                if obj.get('Replace'):
                    rep = obj['Replace']
                    # 如果是本地路径替换(path=>./xxx)，忽略
                    if not rep.get('Path', '').startswith('.'):
                        real_path = rep['Path']
                        real_ver = rep.get('Version', 'unknown')
                        real_time = rep.get('Time', '')
                        is_replaced = True
                
                # === 核心逻辑：分离 Caddy 主程序 ===
                # 凡是以 github.com/caddyserver/caddy 开头的（包括 v2），都算核心
                if obj['Path'].startswith("github.com/caddyserver/caddy"):
                    caddy_core_info = {
                        "Version": real_ver,
                        "Path": obj['Path'] # 核心通常不replace，保留原path方便后续处理
                    }
                else:
                    # 普通插件
                    modules[real_path] = {
                        "OriginalPath": obj['Path'], # xcaddy 需要原始 import 路径
                        "Version": real_ver,
                        "Time": real_time,
                        "IsReplaced": is_replaced,
                        "ReplacePath": real_path if is_replaced else None
                    }

            pos += size
        except Exception:
            pos += 1
            
    return modules, caddy_core_info

def get_previous_manifest():
    url = f"https://github.com/{REPO}/releases/latest/download/{MANIFEST_FILE}"
    try:
        with urllib.request.urlopen(url) as response:
            return json.loads(response.read().decode())
    except Exception:
        return {}

def format_version_display(ver_str):
    """美化版本号显示"""
    # 匹配伪版本号 v0.0.0-20231130002422-f53b62aa13cb
    # 提取最后的 hash (12位) 并截取前7位
    match = re.search(r'-([a-f0-9]{12})$', ver_str)
    if match:
        short_hash = match.group(1)[:7]
        return f"Commit: {short_hash}"
    return ver_str

def parse_time_bj(iso_str):
    """转北京时间详细"""
    if not iso_str: return "N/A"
    try:
        dt = datetime.fromisoformat(iso_str.replace('Z', '+00:00'))
        return dt.astimezone(TZ_CN).strftime('%Y-%m-%d %H:%M:%S')
    except: return iso_str

def format_date_simple(iso_str):
    """转北京时间简略 (用于对比)"""
    if not iso_str: return "N/A"
    try:
        dt = datetime.fromisoformat(iso_str.replace('Z', '+00:00'))
        return dt.astimezone(TZ_CN).strftime('%Y-%m-%d')
    except: return "N/A"

def generate_notes(current, previous):
    diff_lines = []
    
    # 1. 生成变更日志 (Diff)
    diff_lines.append(f"### 📦 Plugin Changes\n")
    has_changes = False
    
    for name, info in current.items():
        # previous 的 key 可能是 real_path
        prev_info = previous.get(name, {})
        
        curr_ver_raw = info['Version']
        prev_ver_raw = prev_info.get('Version', 'N/A')
        
        curr_ver_disp = format_version_display(curr_ver_raw)
        prev_ver_disp = format_version_display(prev_ver_raw)
        
        curr_date = format_date_simple(info['Time'])
        prev_date = format_date_simple(prev_info.get('Time', ''))
        
        # 逻辑：版本号变了，或者版本号没变但日期变了(极端情况)
        if curr_ver_raw != prev_ver_raw:
            diff_lines.append(f"- **{name.split('/')[-1]}**: `{prev_ver_disp}` -> `{curr_ver_disp}`")
            has_changes = True
        elif curr_date != prev_date and prev_date != "N/A":
             diff_lines.append(f"- **{name.split('/')[-1]}**: Update from {prev_date} to {curr_date}")
             has_changes = True

    if not has_changes:
        diff_lines.append("- No plugin updates detected in this build.")

    # 2. 生成详细表格 (Table)
    table_lines = []
    table_lines.append("\n### 🔌 Installed Plugins Status\n")
    table_lines.append("| Plugin | Version | Last Commit (Beijing) |")
    table_lines.append("| :--- | :--- | :--- |")
    
    sorted_keys = sorted(current.keys())
    xcaddy_args = []
    
    for name in sorted_keys:
        info = current[name]
        
        # 显示用的数据
        ver_disp = format_version_display(info['Version'])
        time_bj = parse_time_bj(info['Time'])
        link = f"[{name.split('/')[-1]}](https://{name})"
        
        table_lines.append(f"| {link} | `{ver_disp}` | {time_bj} |")
        
        # 构建 xcaddy 参数
        # 如果是 Replace 过来的，格式: --with github.com/Original=github.com/Replaced@Version
        if info['IsReplaced']:
            xcaddy_args.append(f"--with {info['OriginalPath']}={name}@{info['Version']}")
        else:
            xcaddy_args.append(f"--with {name}@{info['Version']}")

    return "\n".join(diff_lines + table_lines), " ".join(xcaddy_args)

def main():
    current_plugins, caddy_core = get_modules_info()
    previous_manifest = get_previous_manifest()
    
    notes, build_args = generate_notes(current_plugins, previous_manifest)
    
    # 写入 Note 和 Manifest
    with open(RELEASE_NOTE_FILE, 'w') as f:
        f.write(notes)
    
    # Manifest 保存全量信息方便下次对比
    with open(MANIFEST_FILE, 'w') as f:
        json.dump(current_plugins, f, indent=2)
        
    # 输出到 GitHub Actions 环境变量
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
             # 1. 传递 xcaddy 参数
             f.write(f"XCADDY_ARGS={build_args}\n")
             # 2. 传递 Caddy 核心版本 (如果有)
             if caddy_core:
                 f.write(f"CADDY_VERSION={caddy_core['Version']}\n")
             else:
                 f.write(f"CADDY_VERSION=unknown\n")

if __name__ == "__main__":
    main()
