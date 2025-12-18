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
REPO = os.environ.get("GITHUB_REPOSITORY", "") # e.g. ivanphz/my-custom-caddy

def get_current_modules():
    """运行 go list 获取当前所有依赖的详细信息（含时间）"""
    result = subprocess.run(['go', 'list', '-m', '-json', 'all'], capture_output=True, text=True)
    modules = {}
    
    # go list 输出的是多个 JSON 对象拼在一起，需要分割解析
    decoder = json.JSONDecoder()
    pos = 0
    while pos < len(result.stdout):
        obj, size = decoder.raw_decode(result.stdout[pos:])
        if 'Path' in obj:
            # 过滤掉主模块自己和无关模块，只保留 github.com 的插件
            if "github.com" in obj['Path']:
                modules[obj['Path']] = {
                    "Version": obj.get("Version", "unknown"),
                    "Time": obj.get("Time", "") # UTC Time string
                }
        pos += size
    return modules

def get_previous_manifest():
    """尝试从 Latest Release 下载上次的 manifest.json"""
    url = f"https://github.com/{REPO}/releases/latest/download/{MANIFEST_FILE}"
    try:
        print(f"Downloading previous manifest from {url}...")
        with urllib.request.urlopen(url) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Could not download previous manifest: {e}")
        return {}

def parse_time(iso_str):
    """解析 Go 的时间字符串并转为北京时间"""
    if not iso_str:
        return "N/A"
    try:
        # 格式示例: 2025-12-18T06:01:02Z
        dt = datetime.fromisoformat(iso_str.replace('Z', '+00:00'))
        return dt.astimezone(TZ_CN).strftime('%Y-%m-%d %H:%M:%S')
    except:
        return iso_str

def format_date_simple(iso_str):
    """用于对比日志的简化日期"""
    if not iso_str: return "N/A"
    try:
        dt = datetime.fromisoformat(iso_str.replace('Z', '+00:00'))
        return dt.astimezone(TZ_CN).strftime('%Y-%m-%d')
    except: return "N/A"

def generate_notes(current, previous):
    diff_lines = []
    
    # 1. 对比版本和时间差异
    # 优先检查 Caddy 核心
    caddy_pkg = "github.com/caddyserver/caddy"
    if caddy_pkg in current:
        curr_ver = current[caddy_pkg]['Version']
        prev_ver = previous.get(caddy_pkg, {}).get('Version', 'N/A')
        if curr_ver != prev_ver:
            diff_lines.append(f"### ⚠️ Core Update\n")
            diff_lines.append(f"- **CADDY**: `{prev_ver}` -> `{curr_ver}`\n")
    
    diff_lines.append(f"### 📦 Plugin Changes\n")
    has_changes = False
    
    for name, info in current.items():
        if name == caddy_pkg: continue
        
        prev_info = previous.get(name, {})
        curr_ver = info['Version']
        prev_ver = prev_info.get('Version', 'N/A')
        
        curr_date = format_date_simple(info['Time'])
        prev_date = format_date_simple(prev_info.get('Time', ''))
        
        # 逻辑：如果版本变了，或者日期变了
        if curr_ver != prev_ver:
            diff_lines.append(f"- **{name.split('/')[-1]}**: `{prev_ver}` -> `{curr_ver}`")
            has_changes = True
        elif curr_date != prev_date and prev_date != "N/A":
             diff_lines.append(f"- **{name.split('/')[-1]}**: Update from {prev_date} to {curr_date}")
             has_changes = True

    if not has_changes:
        diff_lines.append("- No plugin updates detected in this build.")

    # 2. 生成详细列表（带北京时间）
    table_lines = []
    table_lines.append("\n### 🔌 Installed Plugins Status\n")
    table_lines.append("| Plugin | Version | Last Commit (Beijing) |")
    table_lines.append("| :--- | :--- | :--- |")
    
    # 排除 caddy 核心，按名称排序
    sorted_keys = sorted([k for k in current.keys() if k != caddy_pkg])
    
    xcaddy_args = []
    
    for name in sorted_keys:
        info = current[name]
        ver = info['Version']
        time_bj = parse_time(info['Time'])
        link = f"[{name.split('/')[-1]}](https://{name})"
        table_lines.append(f"| {link} | `{ver}` | {time_bj} |")
        
        # 生成 xcaddy 参数: --with github.com/xxx@v1.2.3
        xcaddy_args.append(f"--with {name}@{ver}")

    return "\n".join(diff_lines + table_lines), " ".join(xcaddy_args)

def main():
    print("Gathering module info...")
    current_modules = get_current_modules()
    previous_modules = get_previous_manifest()
    
    print("Generating release notes...")
    notes, build_args = generate_notes(current_modules, previous_modules)
    
    # 写入 Release Note 文件
    with open(RELEASE_NOTE_FILE, 'w') as f:
        f.write(notes)
    
    # 写入 Manifest 文件 (供下次对比)
    with open(MANIFEST_FILE, 'w') as f:
        json.dump(current_modules, f, indent=2)
        
    # 输出 xcaddy 参数到环境变量
    # GitHub Actions 写入 $GITHUB_OUTPUT
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
             f.write(f"XCADDY_ARGS={build_args}\n")
    
    print("Done.")

if __name__ == "__main__":
    main()
