import os
import sys
import json
import winreg
import sqlite3
import subprocess
import urllib.request
from pathlib import Path
from datetime import datetime, timedelta

WEBHOOK_URL = "https://discord.com/api/webhooks/1544992006508642354/4JXoZqzMTR5To56f-cErDhBsLhtnU305fZiXlfbQMRyP9IygyRsMW7PF8jiN1zH5l5l6"

ASCII_LOGO = """
  ░▒▓███████▓▒░ ░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░ 
  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
  ░▒▓███████▓▒░░▒▓████████▓▒░▒▓█▓▒░      ░▒▓████████▓▒░ 
  ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
  ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
  ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░
"""

EXECUTORS = [
    "synapse", "synapseX", "synapse x", "syna x",
    "script-ware", "scriptware", "sw.exe",
    "krnl", "krnl.exe", "krnlss",
    "fluxus", "fluxus.exe",
    "hydrogen", "hydrogen executor",
    "delta", "delta executor", "delta.exe",
    "arceus x", "arceusX", "arceusx",
    "trigon", "trigon evo", "trigon.exe",
    "cactus", "cactus executor",
    "evon", "evon executor", "evon.exe",
    "codex", "codex executor", "codex.exe",
    "sentinel", "sentinel executor",
    "electron", "electron executor",
    "sirhurt", "sirhurt.exe",
    "proxo", "proxo executor",
    "jjsploit", "jjsploit.exe",
    "oxygen u", "oxygenu",
    "dansploit", "dansploit.exe",
    "vega x", "vegax", "vega.exe",
    "zaros", "zaros executor",
    "level 7", "level7",
    "exploit", "roblox exploit",
    "roblox hack", "roblox cheat",
    "inject", "injector", "dll inject",
    "getgenv", "hookfunction", "newcclosure",
    "readfile", "writefile", "loadstring",
    "workspace().FindFirstChild",
    "RunService", "Players.LocalPlayer",
    "remotespy", "remote spy",
    "dex explorer", "dex.exe",
    "solargraph", "solar graph",
    "bloxstrap", "bloxstrap exploit",
    "rbxcrash", "rbx crash",
    "rbxfps", "rbx fps unlocker",
    "fps unlocker", "rbxfpsunlocker",
    "namecheap", "executor download",
    "wearedevs", "we are devs",
    "lua executor", "luaexecutor",
    "bytecode", "bytecode converter",
    "auto clicker roblox",
]

EXECUTOR_DIRS = [
    r"C:\Synapse X", r"C:\SynapseX", r"C:\Users\Public\SynapseX",
    r"C:\KRNL", r"C:\krnl", r"C:\Users\Public\KRNL",
    r"C:\Script-Ware", r"C:\ScriptWare",
    r"C:\Fluxus", r"C:\Users\Public\Fluxus",
    r"C:\Hydrogen", r"C:\Delta", r"C:\DeltaExecutor",
    r"C:\ArceusX", r"C:\Arceus X",
    r"C:\Trigon", r"C:\Evon", r"C:\Cactus", r"C:\Codex",
    r"C:\Sentinel", r"C:\JJSploit", r"C:\WeAreDevs",
    r"C:\OxygenU", r"C:\VegaX", r"C:\Zaros",
    r"C:\Proxo", r"C:\Electron", r"C:\SirHurt", r"C:\Dansploit",
]

EXECUTOR_FILE_NAMES = [
    "synapse.exe", "synapseX.exe", "syna.exe",
    "sw.exe", "scriptware.exe",
    "krnl.exe", "krnlss.exe",
    "fluxus.exe", "flux.exe",
    "hydrogen.exe",
    "delta.exe", "deltaexecutor.exe",
    "arceusx.exe", "arceus.exe",
    "trigon.exe", "trigonevo.exe",
    "evon.exe", "cactus.exe", "codex.exe",
    "sentinel.exe", "jjsploit.exe", "dansploit.exe",
    "vegax.exe", "vega.exe", "zaros.exe",
    "proxo.exe", "sirhurt.exe", "electron.exe",
    "oxygenu.exe", "remotespy.exe", "dex.exe",
    "rbxfpsunlocker.exe", "injector.exe",
    "loader.exe", "launcher.exe",
    "bootstrapper.exe", "executor.exe",
]

EXECUTOR_PROCESS_NAMES = [
    "synapsex", "synapseX", "syna", "krnl", "krnlss",
    "fluxus", "hydrogen", "delta", "arceusx", "trigon",
    "evon", "cactus", "codex", "sentinel", "jjsploit",
    "scriptware", "sw", "dansploit", "vegax", "zaros",
    "proxo", "sirhurt", "electron_exec", "oxygenu",
    "rbxfpsunlocker", "injector", "remotespy",
]

FINDINGS = []
SCAN_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
MACHINE = os.environ.get("COMPUTERNAME", "unknown")
USER = os.environ.get("USERNAME", "unknown")

STEPS = [
    "Processes", "Filesystem", "Recent Files", "Prefetch",
    "Registry", "Browser History", "Event Logs", "Temp Folders",
]
TOTAL_STEPS = len(STEPS)
BAR_WIDTH = 60

def draw_progress(step_index, label):
    try:
        filled = int(BAR_WIDTH * step_index / TOTAL_STEPS)
        bar = "█" * filled + "░" * (BAR_WIDTH - filled)
        pct = int(100 * step_index / TOTAL_STEPS)
        sys.stdout.write(f"\r  [{bar}] {pct:>3}%  {label:<20}")
        sys.stdout.flush()
    except Exception:
        pass

def flag(category, detail, severity="HIGH"):
    FINDINGS.append({"category": category, "detail": detail, "severity": severity})

def send_webhook(payload: dict):
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            WEBHOOK_URL,
            data=data,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "DiscordBot (pc-checker, 1.0)",
            },
            method="POST",
        )
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        print(f"\n  [WEBHOOK] Failed to send: {e}")

def send_file_to_webhook(report_path):
    try:
        boundary = "----PachBoundary8z2m"
        with open(report_path, "rb") as fp:
            file_bytes = fp.read()
        filename = Path(report_path).name
        embed_json = json.dumps({
            "embeds": [{
                "title": "📄 Full Report",
                "description": "All findings are in the attached file.",
                "color": 0x2B2D31,
                "footer": {"text": "PC Checker — Executor Scanner"},
            }]
        }).encode("utf-8")
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="payload_json"\r\n'
            f"Content-Type: application/json\r\n\r\n"
        ).encode("utf-8") + embed_json + (
            f"\r\n--{boundary}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
            f"Content-Type: text/plain\r\n\r\n"
        ).encode("utf-8") + file_bytes + f"\r\n--{boundary}--\r\n".encode("utf-8")
        req = urllib.request.Request(
            WEBHOOK_URL,
            data=body,
            headers={
                "Content-Type": f"multipart/form-data; boundary={boundary}",
                "User-Agent": "DiscordBot (pc-checker, 1.0)",
            },
            method="POST",
        )
        urllib.request.urlopen(req, timeout=15)
    except Exception as e:
        print(f"\n  [WEBHOOK] Failed to upload report: {e}")

def send_start_ping():
    send_webhook({
        "embeds": [{
            "title": "🔍 PC Scan Started",
            "description": "A scan has been initiated on this machine.",
            "color": 0x5865F2,
            "fields": [
                {"name": "💻 Machine", "value": f"`{MACHINE}`", "inline": True},
                {"name": "👤 User", "value": f"`{USER}`", "inline": True},
                {"name": "🕐 Time", "value": f"`{SCAN_TIME}`", "inline": False},
            ],
            "footer": {"text": "PC Checker — Executor Scanner"},
        }]
    })

def send_final_report(report_path=None):
    high = [f for f in FINDINGS if f["severity"] == "HIGH"]
    med  = [f for f in FINDINGS if f["severity"] == "MEDIUM"]

    if not FINDINGS:
        send_webhook({
            "embeds": [{
                "title": "✅ Scan Complete — CLEAN",
                "description": "No executor traces were found on this machine.",
                "color": 0x57F287,
                "fields": [
                    {"name": "💻 Machine", "value": f"`{MACHINE}`", "inline": True},
                    {"name": "👤 User", "value": f"`{USER}`", "inline": True},
                    {"name": "🕐 Scanned At", "value": f"`{SCAN_TIME}`", "inline": False},
                ],
                "footer": {"text": "PC Checker — Executor Scanner"},
            }]
        })
        return

    color = 0xED4245 if high else 0xFEE75C
    desc = f"🔴 **{len(high)} HIGH**  🟡 **{len(med)} MEDIUM**\nFull details in the attached report."

    send_webhook({
        "embeds": [{
            "title": "🚨 Scan Complete — FINDINGS DETECTED",
            "description": desc,
            "color": color,
            "fields": [
                {"name": "💻 Machine", "value": f"`{MACHINE}`", "inline": True},
                {"name": "👤 User", "value": f"`{USER}`", "inline": True},
                {"name": "🕐 Scanned At", "value": f"`{SCAN_TIME}`", "inline": False},
            ],
            "footer": {"text": "PC Checker — Executor Scanner"},
        }]
    })

    if report_path and Path(report_path).exists():
        send_file_to_webhook(report_path)

def check_running_processes():
    try:
        result = subprocess.run(
            ["tasklist", "/FO", "CSV", "/NH"],
            capture_output=True, text=True, timeout=15
        )
        for line in result.stdout.strip().splitlines():
            parts = line.strip('"').split('","')
            if not parts:
                continue
            proc_name = parts[0].lower().replace(".exe", "")
            for ep in EXECUTOR_PROCESS_NAMES:
                if ep.lower() in proc_name:
                    flag("Running Process", f"{parts[0]} (PID: {parts[1] if len(parts) > 1 else 'unknown'})")
                    break
    except Exception:
        pass

def check_filesystem():
    for d in EXECUTOR_DIRS:
        p = Path(d)
        if p.exists():
            flag("Directory Found", str(p))
    scan_roots = [
        Path.home() / "Downloads",
        Path.home() / "Desktop",
        Path.home() / "Documents",
        Path("C:/Users/Public"),
        Path("C:/Temp"),
        Path(os.environ.get("TEMP", "")),
        Path(os.environ.get("APPDATA", "")),
        Path(os.environ.get("LOCALAPPDATA", "")),
    ]
    for root in scan_roots:
        if not root.exists():
            continue
        try:
            for f in root.rglob("*"):
                if f.is_file() and f.suffix.lower() == ".exe":
                    if f.name.lower() in [e.lower() for e in EXECUTOR_FILE_NAMES]:
                        flag("Executor File", str(f))
                    else:
                        for kw in EXECUTORS:
                            if kw.lower() in f.name.lower():
                                flag("Suspicious File", str(f), severity="MEDIUM")
                                break
        except (PermissionError, OSError):
            pass

def check_recent_files():
    recent_dir = Path(os.environ.get("APPDATA", "")) / "Microsoft" / "Windows" / "Recent"
    if not recent_dir.exists():
        return
    try:
        cutoff = datetime.now() - timedelta(days=30)
        for f in recent_dir.iterdir():
            try:
                mtime = datetime.fromtimestamp(f.stat().st_mtime)
                if mtime < cutoff:
                    continue
                for kw in EXECUTORS:
                    if kw.lower() in f.stem.lower():
                        flag("Recent File", f"{f.name} (modified {mtime.strftime('%Y-%m-%d')})", severity="MEDIUM")
                        break
            except OSError:
                pass
    except Exception:
        pass

def check_prefetch():
    prefetch_dir = Path("C:/Windows/Prefetch")
    if not prefetch_dir.exists():
        return
    try:
        for f in prefetch_dir.iterdir():
            if f.suffix.lower() != ".pf":
                continue
            for ep in EXECUTOR_FILE_NAMES:
                if ep.lower().replace(".exe", "") in f.stem.lower():
                    try:
                        mtime = datetime.fromtimestamp(f.stat().st_mtime)
                        flag("Prefetch Entry", f"{f.name} (last run ~{mtime.strftime('%Y-%m-%d')})")
                    except OSError:
                        flag("Prefetch Entry", f.name)
                    break
    except PermissionError:
        pass

def check_registry():
    hives = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
    ]
    for hive, path in hives:
        try:
            key = winreg.OpenKey(hive, path)
            i = 0
            while True:
                try:
                    subkey_name = winreg.EnumKey(key, i)
                    subkey = winreg.OpenKey(key, subkey_name)
                    try:
                        display_name, _ = winreg.QueryValueEx(subkey, "DisplayName")
                        for kw in EXECUTORS:
                            if kw.lower() in display_name.lower():
                                try:
                                    install_loc, _ = winreg.QueryValueEx(subkey, "InstallLocation")
                                except:
                                    install_loc = "unknown"
                                flag("Registry Uninstall", f"{display_name} @ {install_loc}")
                                break
                    except FileNotFoundError:
                        pass
                    winreg.CloseKey(subkey)
                    i += 1
                except OSError:
                    break
            winreg.CloseKey(key)
        except Exception:
            pass
    run_keys = [
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"),
    ]
    for hive, path in run_keys:
        try:
            key = winreg.OpenKey(hive, path)
            i = 0
            while True:
                try:
                    name, value, _ = winreg.EnumValue(key, i)
                    for kw in EXECUTORS:
                        if kw.lower() in (name + value).lower():
                            flag("Registry Run Key", f"{name} = {value}")
                            break
                    i += 1
                except OSError:
                    break
            winreg.CloseKey(key)
        except Exception:
            pass

def check_browser_history():
    suspicious_domains = [
        "wearedevs.net", "synapsex.to", "krnl.ca",
        "fluxteam.net", "scriptware.io",
        "arceusx.net", "trigon.to", "evon.to", "codex.to",
        "hydrogen.lat", "deltarblx.com", "jjsploit.net",
        "sirhurt.xyz", "dansploit.xyz", "vegax.to",
        "zaros.io", "proxo.xyz", "electron-executor.xyz",
        "executor", "roblox+exploit", "roblox+hack",
        "roblox+cheat", "roblox+executor", "roblox+script",
        "buy+executor", "free+executor",
        "lua+executor", "download+executor",
    ]
    lad = os.environ.get("LOCALAPPDATA", "")
    browsers = [
        ("Chrome", Path(lad) / "Google" / "Chrome" / "User Data" / "Default" / "History"),
        ("Edge",   Path(lad) / "Microsoft" / "Edge" / "User Data" / "Default" / "History"),
        ("Brave",  Path(lad) / "BraveSoftware" / "Brave-Browser" / "User Data" / "Default" / "History"),
    ]
    for browser_name, history_path in browsers:
        if not history_path.exists():
            continue
        tmp = Path(os.environ.get("TEMP", "C:/Temp")) / f"_pchk_{browser_name}_hist"
        try:
            import shutil
            shutil.copy2(history_path, tmp)
            conn = sqlite3.connect(tmp)
            cur = conn.cursor()
            cutoff_ts = int(((datetime.now() - timedelta(days=90)) - datetime(1601, 1, 1)).total_seconds() * 1_000_000)
            cur.execute("SELECT url, title, last_visit_time FROM urls WHERE last_visit_time > ? ORDER BY last_visit_time DESC", (cutoff_ts,))
            rows = cur.fetchall()
            conn.close()
            tmp.unlink(missing_ok=True)
            for url, title, ts in rows:
                combined = (url or "").lower() + " " + (title or "").lower()
                for domain in suspicious_domains:
                    if domain.lower() in combined:
                        try:
                            visit_str = (datetime(1601, 1, 1) + timedelta(microseconds=ts)).strftime("%Y-%m-%d")
                        except:
                            visit_str = "unknown"
                        flag("Browser History", f"[{browser_name}] {url[:100]} ({visit_str})", severity="MEDIUM")
                        break
        except Exception:
            pass

def check_event_logs():
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "Get-EventLog -LogName Application -Source msiinstaller -Newest 200 2>$null | "
             "Select-Object TimeGenerated,Message | ConvertTo-Json"],
            capture_output=True, text=True, timeout=20
        )
        if result.stdout.strip():
            try:
                events = json.loads(result.stdout)
                if isinstance(events, dict):
                    events = [events]
                for ev in events:
                    msg = str(ev.get("Message", "")).lower()
                    for kw in EXECUTORS:
                        if kw.lower() in msg:
                            flag("Event Log Install", msg[:120])
                            break
            except json.JSONDecodeError:
                pass
    except Exception:
        pass

def check_temp_folders():
    temp_paths = [
        Path(os.environ.get("TEMP", "")),
        Path(os.environ.get("TMP", "")),
        Path("C:/Windows/Temp"),
    ]
    for tp in temp_paths:
        if not tp.exists():
            continue
        try:
            for f in tp.iterdir():
                fname_lower = f.name.lower()
                for kw in EXECUTORS + EXECUTOR_FILE_NAMES:
                    if kw.lower().replace(".exe", "") in fname_lower:
                        flag("Temp Artifact", str(f), severity="MEDIUM")
                        break
        except (PermissionError, OSError):
            pass

def get_desktop_path():
    """Return the real Desktop path, even if it's redirected to OneDrive."""
    # Try Windows shell API first (handles OneDrive redirection)
    try:
        import ctypes
        CSIDL_DESKTOPDIRECTORY = 0x0010
        buf = ctypes.create_unicode_buffer(32768)
        ctypes.windll.shell32.SHGetFolderPathW(0, CSIDL_DESKTOPDIRECTORY, 0, 0, buf)
        desktop = Path(buf.value)
        if desktop.exists():
            return desktop
    except Exception:
        pass
    # Fallback 1: standard home/Desktop
    desktop = Path.home() / "Desktop"
    if desktop.exists():
        return desktop
    # Fallback 2: OneDrive Desktop
    onedrive = os.environ.get("OneDrive", "")
    if onedrive:
        od_desktop = Path(onedrive) / "Desktop"
        if od_desktop.exists():
            return od_desktop
    # Fallback 3: save next to the exe / script itself
    try:
        exe_dir = Path(sys.executable).parent
        if exe_dir.exists():
            return exe_dir
    except Exception:
        pass
    # Last resort: TEMP folder
    return Path(os.environ.get("TEMP", "C:/Temp"))

def save_report():
    report_path = get_desktop_path() / f"pc_check_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    lines = [
        "PC CHECKER — EXECUTOR SCAN REPORT",
        f"Scan Time : {SCAN_TIME}",
        f"Machine   : {MACHINE}",
        f"User      : {USER}",
        "",
    ]
    if not FINDINGS:
        lines.append("RESULT: CLEAN — No executor traces found.")
    else:
        lines.append(f"RESULT: {len(FINDINGS)} finding(s) detected.\n")
        for i, f in enumerate(FINDINGS, 1):
            lines.append(f"[{i}] [{f['severity']}] {f['category']}")
            lines.append(f"    {f['detail']}")
            lines.append("")
    with open(report_path, "w", encoding="utf-8") as fp:
        fp.write("\n".join(lines))
    print(f"\n  Report saved to: {report_path}")
    return report_path

def main():
    if sys.platform != "win32":
        print("[ERROR] This scanner only runs on Windows.")
        sys.exit(1)

    try:
        print(ASCII_LOGO)
        print("  =========================================================")
    except Exception:
        pass

    draw_progress(0, "Starting...")
    send_start_ping()

    checks = [
        check_running_processes,
        check_filesystem,
        check_recent_files,
        check_prefetch,
        check_registry,
        check_browser_history,
        check_event_logs,
        check_temp_folders,
    ]

    report_path = None
    try:
        for i, (check_fn, label) in enumerate(zip(checks, STEPS), start=1):
            draw_progress(i - 1, label)
            check_fn()
            draw_progress(i, label)
    finally:
        draw_progress(TOTAL_STEPS, "Done")
        try:
            print()
            print("  =========================================================")
            if not FINDINGS:
                print("\n  RESULT  CLEAN — no executor traces found.")
            else:
                high = sum(1 for f in FINDINGS if f["severity"] == "HIGH")
                med  = sum(1 for f in FINDINGS if f["severity"] == "MEDIUM")
                print(f"\n  RESULT  {len(FINDINGS)} finding(s)  —  HIGH: {high}  MEDIUM: {med}")
        except Exception:
            pass
        report_path = save_report()
        send_final_report(report_path)

    input("\n  Press Enter to exit...")

if __name__ == "__main__":
    main()