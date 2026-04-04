import sys
import os
import argparse
import stat
from datetime import datetime

# The Map
SHEBANGS = {
    '.py':  '#!/usr/bin/env python3',
    '.sh':  '#!/bin/bash',
    '.ps1': '#!/usr/bin/pwsh',
    '.rb':  '#!/usr/bin/env ruby',
    '.lua': '#!/usr/bin/env lua',
    '.pl':  '#!/usr/bin/env perl'
}

LOG_FILE = "bangit_log.txt"

def write_log(message):
    if os.path.exists(LOG_FILE) or "STARTING" in message:
        timestamp = datetime.now().strftime("%H:%M:%S")
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")

def process_file(filepath, user_desc="", dry_run=False):
    filename = os.path.basename(filepath)
    ext = os.path.splitext(filename)[1].lower()
    if ext not in SHEBANGS: return 

    if dry_run:
        print(f"[-] Would Bang: {filepath}")
        return

    try:
        # Unlock / Permissions
        os.chmod(filepath, stat.S_IWRITE) 
        
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        # Scrubbing old headers
        clean_body = [line for line in lines if not (line.startswith('#!') or line.startswith(f"# {filename}") or line.startswith('#####'))]

        header = [f"{SHEBANGS[ext]}\n", f"# {filename}\n", f"##### {user_desc if user_desc else 'ADD DESCRIPTION'}\n\n"]

        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(header + clean_body)
        
        # Make Executable / Unblock Windows
        if os.name != 'nt':
            os.chmod(filepath, os.stat(filepath).st_mode | stat.S_IEXEC)
        elif os.path.exists(f"{filepath}:Zone.Identifier"):
            os.remove(f"{filepath}:Zone.Identifier")

        write_log(f"FIXED: {filepath}")
        print(f"✔ {filename}")

    except Exception as e:
        write_log(f"FAIL: {filepath} ({e})")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", help="Target file/dir")
    parser.add_argument("-d", "--desc", default="")
    parser.add_argument("-r", "--recursive", action="store_true")
    parser.add_argument("--dry", action="store_true")
    parser.add_argument("--cleanup", action="store_true", help="Nuke the log file")

    args = parser.parse_args()

    if args.cleanup:
        if os.path.exists(LOG_FILE):
            os.remove(LOG_FILE)
            print("🧹 Log file nuked.")
        return

    if not args.path:
        parser.print_help()
        return

    write_log(f"--- SESSION START: {args.path} ---")

    if os.path.isfile(args.path):
        process_file(args.path, args.desc, args.dry)
    else:
        for root, _, files in (os.walk(args.path) if args.recursive else [(args.path, [], os.listdir(args.path))]):
            for f in files: process_file(os.path.join(root, f), args.desc, args.dry)

if __name__ == "__main__":
    main()
