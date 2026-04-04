import sys
import os
import argparse
import stat
from datetime import datetime

# The expanded Shebang Map
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
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

def unlock_and_exec(filepath):
    """Handles cross-platform file permissions/blocks."""
    try:
        if os.name != 'nt': # Linux/WSL
            st = os.stat(filepath)
            os.chmod(filepath, st.st_mode | stat.S_IEXEC)
        else: # Windows
            os.chmod(filepath, stat.S_IWRITE)
            zone_file = f"{filepath}:Zone.Identifier"
            if os.path.exists(zone_file):
                os.remove(zone_file)
        return True
    except:
        return False

def process_file(filepath, user_desc="", dry_run=False):
    filename = os.path.basename(filepath)
    ext = os.path.splitext(filename)[1].lower()
    
    if ext not in SHEBANGS:
        return 

    if dry_run:
        print(f"[DRY RUN] Would Bang & Unlock: {filepath}")
        return

    try:
        os.chmod(filepath, stat.S_IWRITE) 
        
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        clean_body = [
            line for line in lines 
            if not (line.startswith('#!') or line.startswith(f"# {filename}") or line.startswith('#####'))
        ]

        desc_line = user_desc if user_desc else "ADD DESCRIPTION HERE"
        header = [
            f"{SHEBANGS[ext]}\n",
            f"# {filename}\n",
            f"##### {desc_line}\n\n"
        ]

        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(header + clean_body)
        
        unlocked = unlock_and_exec(filepath)
        status = "Success" if unlocked else "Success (Perms Failed)"
        
        print(f"✔ {status}: {filepath}")
        write_log(f"{status}: {filepath} (Ext: {ext})")

    except Exception as e:
        error_msg = f"Error: {filepath} -> {e}"
        print(f"✘ {error_msg}")
        write_log(error_msg)

def main():
    parser = argparse.ArgumentParser(description="Bangit: The Ultimate Script Janitor.")
    parser.add_argument("path", help="File or directory to process")
    parser.add_argument("-d", "--desc", help="Description for the ##### block", default="")
    parser.add_argument("-r", "--recursive", action="store_true", help="Recurse subfolders")
    parser.add_argument("--dry-run", action="store_true", help="Preview mode")

    args = parser.parse_args()

    if not args.dry_run:
        write_log(f"--- STARTING SESSION: {args.path} ---")

    if os.path.isfile(args.path):
        process_file(args.path, args.desc, args.dry_run)
    elif os.path.isdir(args.path):
        for root, _, files in (os.walk(args.path) if args.recursive else [(args.path, [], os.listdir(args.path))]):
            for file in files:
                process_file(os.path.join(root, file), args.desc, args.dry_run)
    else:
        print(f"Error: {args.path} not found.")

    if not args.dry_run:
        write_log("--- SESSION COMPLETE ---")

if __name__ == "__main__":
    main()
