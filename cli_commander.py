#!/usr/bin/env python3
"""
CLI_Commander - Command Line Process Management Tool
Command-line tool for managing persistent processes for Linux platforms.


Usage Examples:
    # Create a new process entry
    python cli_commander.py --new --name my_process
    # Start Python with interactive communication
    python cli_commander.py --run --name py_repl --command "python"
    # Send commands to Python process
    python cli_commander.py --send --name py_repl --command "s = 'Hello World'"
    python cli_commander.py --send --name py_repl --command "print(s)"
    # Send a simple echo command
    python cli_commander.py --run --name my_process --command "echo Hello! CLI Commander"
    # List all processes
    python cli_commander.py --list
    # Close all processes
    python cli_commander.py --close_all
    
    # Run test demonstration
    python cli_commander.py --test

"""

import argparse
import subprocess
import os
import sys
import time
import tempfile
import threading
import signal
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Tuple, Any
import re


class UnifiedProcessManager:
    """Unified process manager for Linux only (tmux-based REPL)."""

    @staticmethod
    def start_detached_process(command: str) -> subprocess.Popen:
        """Start detached process (Linux only)."""
        return subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            preexec_fn=os.setsid
        )

    @staticmethod
    def terminate_process(pid: int) -> bool:
        """Terminate process (Linux only)."""
        if not pid:
            return False
        try:
            os.kill(pid, signal.SIGTERM)
            time.sleep(0.1)
            try:
                os.kill(pid, 0)
                os.kill(pid, signal.SIGKILL)
            except OSError:
                pass
            return True
        except Exception:
            return False

    @staticmethod
    def is_process_running(pid: int) -> bool:
        """Check if process is running (Linux only)."""
        if not pid:
            return False
        try:
            os.kill(pid, 0)
            return True
        except:
            return False





class CLI_Commander:
    """Linux only: tmux-based REPL process manager"""

    def __init__(self):
        self.process_file = "unified_process_info.json"
        self.processes = {}
        self.process_manager = UnifiedProcessManager()
        self.load_processes()

    def log(self, message: str, process_name: str = "CLI_Commander", log_type: str = "INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{process_name}] [{log_type}] {message}")

    def save_processes(self):
        try:
            with open(self.process_file, 'w', encoding='utf-8') as f:
                json.dump(self.processes, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.log(f"Failed to save processes: {e}", log_type="ERROR")

    def load_processes(self):
        if not os.path.exists(self.process_file):
            return
        try:
            with open(self.process_file, 'r', encoding='utf-8') as f:
                self.processes = json.load(f)
        except Exception as e:
            self.log(f"Failed to load processes: {e}", log_type="WARNING")
            self.processes = {}

    def send_to_process(self, name: str, command: str) -> bool:
        """Send command to tmux session. For REPL (python, bash), use send-keys directly. For others, use output redirection."""
        if name not in self.processes:
            self.log(f"Process '{name}' not found", log_type="ERROR")
            return False
        info = self.processes[name]
        if not info.get('tmux_session'):
            self.log(f"Process '{name}' is not a tmux session", log_type="ERROR")
            return False
        session = info['tmux_session']
        # REPL detection: command is python, python3, bash, sh, zsh, etc.
        repl_keywords = ["python", "python3", "bash", "sh", "zsh"]
        is_repl = False
        proc_cmd = info.get('command', '') or ''
        for kw in repl_keywords:
            if proc_cmd.strip().startswith(kw):
                is_repl = True
                break
        try:
            if is_repl:
                # Send command
                send_cmd = f"tmux send-keys -t {session} '{command}' Enter"
                subprocess.run(send_cmd, shell=True, check=True)
                time.sleep(0.2)

                # Get output after sending command (capture all)
                capture_cmd = f"tmux capture-pane -pt {session}"
                result = subprocess.run(capture_cmd, shell=True, check=True, stdout=subprocess.PIPE, text=True)
                output = result.stdout.strip()
                if not output:
                    output = "(No output)"
                # Show only diff: keep previous RESPONSE and output only the diff
                prev_output = info.get('last_repl_output', '')
                if prev_output and output != prev_output:
                    # Extract diff (only new part)
                    prev_lines = prev_output.splitlines()
                    curr_lines = output.splitlines()
                    # Find start position of diff
                    diff_start = 0
                    for i in range(min(len(prev_lines), len(curr_lines))):
                        if prev_lines[i] != curr_lines[i]:
                            break
                        diff_start = i + 1
                    diff_lines = curr_lines[diff_start:]
                    diff_str = '\n'.join(diff_lines).strip()
                    if not diff_str:
                        diff_str = "(No output)"
                    self.log(f"{diff_str}", process_name=name, log_type="RESPONSE")
                else:
                    # On first run or if all lines match, output all
                    self.log(f"{output}", process_name=name, log_type="RESPONSE")
                # Save current output
                info['last_repl_output'] = output
                self.save_processes()
                return True
            else:
                # Non-REPL: use existing temp file method
                tmpfile = f"/tmp/cli_commander_{name}_output.txt"
                safe_command = command.strip()
                wrapped_cmd = f"({safe_command}) > {tmpfile} 2>&1"
                send_cmd = f"tmux send-keys -t {session} \"{wrapped_cmd}\" Enter"
                subprocess.run(send_cmd, shell=True, check=True)
                time.sleep(0.2)
                output = ""
                if os.path.exists(tmpfile):
                    with open(tmpfile, 'r', encoding='utf-8', errors='replace') as f:
                        output = f.read().strip()
                    os.remove(tmpfile)
                self.log(f"{output}", process_name=name, log_type="RESPONSE")
                return True
        except Exception as e:
            self.log(f"tmux send error: {e}", log_type="ERROR")
            return False

    def execute_command(self, action: str, name: Optional[str] = None, command: Optional[str] = None, wait_time: float = 0.2) -> bool:
        """Unified command executor for all actions."""
        if action == "send":
            # Only sleep after sending command, handled inside send_to_process
            return self.send_to_process(name, command)

        if action == "new":
            if name in self.processes:
                info = self.processes[name]
                status = "running" if self.process_manager.is_process_running(info.get('pid')) else "not running"
                self.log(f"Process '{name}' already exists and is {status}")
                return True
            # Start bash when creating a new process
            self.processes[name] = {'pid': None, 'command': None, 'start_time': None}
            self.save_processes()
            self.log(f"Created new process entry: {name}")
            # Start bash as run
            return self.execute_command("run", name, "bash", wait_time)

        if action == "run":
            if name not in self.processes:
                self.log(f"Process '{name}' not found", log_type="ERROR")
                return False
            safe_command = command.strip()
            self.log(f"{safe_command}", process_name=name, log_type="COMMAND")
            session = f"cli_{name}"
            # Check if tmux session exists
            check_cmd = f"tmux has-session -t {session}"
            session_exists = subprocess.run(check_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
            try:
                if not session_exists:
                    # Create new session
                    tmux_cmd = f"tmux new-session -d -s {session} '{safe_command}'"
                    subprocess.run(tmux_cmd, shell=True, check=True)
                    get_pid_cmd = f"tmux list-panes -t {session} -F '#{{pane_pid}}'"
                    result = subprocess.run(get_pid_cmd, shell=True, check=True, stdout=subprocess.PIPE, text=True)
                    pid = int(result.stdout.strip().splitlines()[0])
                    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.processes[name].update({
                        'pid': pid,
                        'command': safe_command,
                        'start_time': start_time,
                        'tmux_session': session
                    })
                    self.save_processes()
                    self.log(f"tmux session started (PID: {pid}, session: {session})", process_name=name, log_type="RESPONSE")
                    return True
                else:
                    # Send command to existing session (sleep handled in send_to_process)
                    return self.send_to_process(name, command)
            except Exception as e:
                self.log(f"Failed to run command: {e}", log_type="ERROR")
                return False

        if action == "close":
            if not name or name not in self.processes:
                self.log(f"Process '{name}' not found", log_type="ERROR")
                return False
            info = self.processes[name]
            session = info.get('tmux_session')
            pid = info.get('pid')
            # Kill tmux session if exists
            if session:
                kill_cmd = f"tmux kill-session -t {session}"
                subprocess.run(kill_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            # Kill process if still running
            if pid and self.process_manager.is_process_running(pid):
                self.process_manager.terminate_process(pid)
            self.log(f"Closed process: {name}")
            del self.processes[name]
            self.save_processes()
            return True

        if action == "close_all":
            names = list(self.processes.keys())
            for pname in names:
                self.execute_command("close", pname, None, 0)
            self.log("All processes closed.")
            return True

        if action == "list":
            if name:
                info = self.processes.get(name)
                if not info:
                    self.log(f"Process '{name}' not found", log_type="ERROR")
                    return False
                self.log(f"Process '{name}': {json.dumps(info, ensure_ascii=False, indent=2)}")
            else:
                if not self.processes:
                    self.log("No processes found.")
                for pname, info in self.processes.items():
                    self.log(f"Process '{pname}': {json.dumps(info, ensure_ascii=False, indent=2)}")
            return True

        self.log(f"Unknown action: {action}", log_type="ERROR")
        return False



def run_test():
    """Test function demonstrating unified CLI_Commander commands."""
    commander = CLI_Commander()
    
    commander.log("Starting Unified CLI_Commander test...")
    commander.execute_command("new", "test_process")
    

    test_cmd = "echo 'Hello Unified CLI_Commander'"
    commander.execute_command("run", "test_process", test_cmd, 1.0)

    # Additional echo test as requested
    echo_cmd = "echo Hello! CLI Commander"
    commander.execute_command("run", "test_process", echo_cmd, 1.0)
    
    commander.execute_command("list")
    commander.execute_command("close_all")
    commander.log("Unified test completed!")


def main():
    """Main function to parse arguments and execute unified CLI_Commander actions."""
    parser = argparse.ArgumentParser(description="CLI_Commander - Unified Process Manager")
    parser.add_argument('--new', action='store_true', help='Create new process')
    parser.add_argument('--run', action='store_true', help='Run command in tmux session (create or send)')
    parser.add_argument('--close', action='store_true', help='Close specific process')
    parser.add_argument('--close_all', action='store_true', help='Close all processes')
    parser.add_argument('--list', action='store_true', help='List processes')
    parser.add_argument('--test', action='store_true', help='Run test function')
    parser.add_argument('--name', type=str, help='Process name')
    parser.add_argument('--command', type=str, help='Command to execute')
    parser.add_argument('--wait', type=float, default=0, help='Wait time in seconds')
    
    args = parser.parse_args()
    commander = CLI_Commander()
    
    if args.new:
        if not args.name:
            commander.log("--name required for --new", log_type="ERROR")
            return 1
        commander.execute_command('new', args.name, None, args.wait)
        return 0
    if args.run:
        if not args.name or not args.command:
            commander.log("--name and --command required for --run", log_type="ERROR")
            return 1
        commander.execute_command('run', args.name, args.command, args.wait)
        return 0
    if args.close:
        if not args.name:
            commander.log("--name required for --close", log_type="ERROR")
            return 1
        commander.execute_command('close', args.name, None, args.wait)
        return 0
    if args.close_all:
        commander.execute_command('close_all', None, None, args.wait)
        return 0
    if args.list:
        commander.execute_command('list', args.name, None, args.wait)
        return 0
    if args.test:
        run_test()
        return 0
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
