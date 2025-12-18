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
    result = subprocess.run(['go', 'list', '-m', '-json', 'all'], capture_output=True, text=True)
    modules = {}
    
    decoder = json.JSONDecoder()
    pos = 0
    while pos < len(result.stdout):
        try:
            obj, size = decoder.raw_decode(result.stdout[pos:])
            
            # 过滤逻辑：
            # 1. 排除主模块自身 (Main: true) -> 这就是之前报错的原因！
            # 2. 必须是 github.com 开头
            # 3. 不能是 Indirect (间接依赖)
            # 4. 排除 caddy 主程序
            if (not obj.get('Main') 
                and 'Path' in obj 
                and "github.com" in obj['Path'] 
                and not obj.get('Indirect', False)
                and obj['Path'] != "github.com/caddyserver/caddy"):
                
                modules[obj['Path']] = {
                    "Version": obj.get("Version", "unknown"),
                    "Time": obj.get("Time", ""),
                    "Replace": obj.get("Replace", None)
                }
            pos += size
        except Exception as e:
            pos += 1
            
    return modules

def get_previous_manifest():
    url = f"https://github.com/{REPO}/releases/latest/download/{MANIFEST_FILE}"
    try:
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
    
    diff_lines.append(f"### 📦 Plugin Changes\n")
    has_changes = False
    
    for name, info in current.items():
        prev_info = previous.get(name, {})
        curr_ver = info['Version']
        
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
        
        link = f"[{name.split('/')[-1]}](https://{name})"
        table_lines.append(f"| {link} | `{ver}` | {time_bj} |")
        
        # 处理 Replace 指令
        if info.get('Replace'):
            rep = info['Replace']
            rep_path = rep['Path']
            rep_ver = rep['Version']
            xcaddy_args.append(f"--with {name}={rep_path}@{rep_ver}")
        else:
            xcaddy_args.append(f"--with {name}@{ver}")

    return "\n".join(diff_lines + table_lines), " ".join(xcaddy_args)

def main():
    current_modules = get_current_modules()
    previous_modules = get_previous_manifest()
    
    notes, build_args = generate_notes(current_modules, previous_modules)
    
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
