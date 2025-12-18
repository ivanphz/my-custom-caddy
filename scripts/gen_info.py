import json
import os
import subprocess
import re
import urllib.request
from datetime import datetime, timezone, timedelta

TZ_CN = timezone(timedelta(hours=8))
MANIFEST_FILE = "manifest.json"
RELEASE_NOTE_FILE = "release_notes.md"
REPO = os.environ.get("GITHUB_REPOSITORY", "") 

def get_modules_info():
    result = subprocess.run(['go', 'list', '-m', '-json', 'all'], capture_output=True, text=True)
    
    modules = {}
    caddy_core_info = None
    decoder = json.JSONDecoder()
    pos = 0
    while pos < len(result.stdout):
        try:
            obj, size = decoder.raw_decode(result.stdout[pos:])
            
            if (not obj.get('Main') 
                and 'Path' in obj 
                and "github.com" in obj['Path'] 
                and not obj.get('Indirect', False)):
                
                real_path = obj['Path']
                real_ver = obj.get('Version', 'unknown')
                real_time = obj.get('Time', '')
                is_replaced = False

                if obj.get('Replace'):
                    rep = obj['Replace']
                    if not rep.get('Path', '').startswith('.'):
                        real_path = rep['Path']
                        real_ver = rep.get('Version', 'unknown')
                        real_time = rep.get('Time', '')
                        is_replaced = True
                
                if obj['Path'].startswith("github.com/caddyserver/caddy"):
                    caddy_core_info = { "Version": real_ver, "Path": obj['Path'] }
                else:
                    modules[real_path] = {
                        "OriginalPath": obj['Path'],
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
    match = re.search(r'-([a-f0-9]{12})$', ver_str)
    if match: return f"Commit: {match.group(1)[:7]}"
    return ver_str

def parse_time_bj(iso_str):
    if not iso_str: return "N/A"
    try:
        dt = datetime.fromisoformat(iso_str.replace('Z', '+00:00'))
        return dt.astimezone(TZ_CN).strftime('%Y-%m-%d %H:%M:%S')
    except: return iso_str

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
        curr_ver_raw = info['Version']
        prev_ver_raw = prev_info.get('Version', 'N/A')
        
        curr_ver_disp = format_version_display(curr_ver_raw)
        prev_ver_disp = format_version_display(prev_ver_raw)
        curr_date = format_date_simple(info['Time'])
        prev_date = format_date_simple(prev_info.get('Time', ''))
        
        if curr_ver_raw != prev_ver_raw:
            diff_lines.append(f"- **{name.split('/')[-1]}**: `{prev_ver_disp}` -> `{curr_ver_disp}`")
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
    
    for name in sorted(current.keys()):
        info = current[name]
        ver_disp = format_version_display(info['Version'])
        time_bj = parse_time_bj(info['Time'])
        link = f"[{name.split('/')[-1]}](https://{name})"
        table_lines.append(f"| {link} | `{ver_disp}` | {time_bj} |")
        
    # 生成 XCaddy 参数 (必须基于解析后的 Version)
    xcaddy_args = []
    for name, info in sorted(current.items()):
        if info['IsReplaced']:
            xcaddy_args.append(f"--with {info['OriginalPath']}={name}@{info['Version']}")
        else:
            xcaddy_args.append(f"--with {name}@{info['Version']}")

    return "\n".join(diff_lines + table_lines), " ".join(xcaddy_args)

def main():
    current_plugins, caddy_core = get_modules_info()
    previous_manifest = get_previous_manifest()
    notes, build_args = generate_notes(current_plugins, previous_manifest)
    
    with open(RELEASE_NOTE_FILE, 'w') as f:
        f.write(notes)
    with open(MANIFEST_FILE, 'w') as f:
        json.dump(current_plugins, f, indent=2)
        
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
             f.write(f"XCADDY_ARGS={build_args}\n")
             f.write(f"CADDY_VERSION={caddy_core['Version'] if caddy_core else 'unknown'}\n")

if __name__ == "__main__":
    main()
