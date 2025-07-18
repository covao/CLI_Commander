#!/usr/bin/env python3
"""CLI_Commander.py: A simple cross‑platform process manager.

Overview:
This tool manages interactive shell processes across different platforms.
It allows you to:
- Open named interactive shell sessions
- Send commands to running sessions 
- List all active sessions with their status
- Close sessions gracefully or forcefully

Key Features:
- Cross-platform support (Windows cmd, Linux/Mac bash)
- Real-time output streaming with timestamps
- Background thread management for output monitoring
- Process state tracking and error handling
- Graceful and forceful termination options

Usage examples:
  Open a named process:
    python CLI_Commander.py --open --process_name demo

  Run a command inside the named process:
    python CLI_Commander.py --process_name demo --command "echo Hello"

  List managed processes:
    python CLI_Commander.py --list

  Close the named process:
    python CLI_Commander.py --close --process_name demo
"""

import argparse
import platform
import subprocess
import threading
import time
from datetime import datetime
import sys

# Global registry of running subprocesses
PROCESSES = {}


def timestamp() -> str:
    """Return current time in HH:MM:SS format."""
    return datetime.now().strftime('%H:%M:%S')


def _stream_output(process_name: str, proc: subprocess.Popen):
    """Continuously read subprocess stdout and print with timestamp."""
    for line in iter(proc.stdout.readline, ''):
        if line:
            clean_line = line.rstrip()
            # Filter out Windows startup messages and prompts
            if clean_line and not _should_filter_output(clean_line):
                print(f"{timestamp()} RESPONSE: {process_name} {clean_line}")
        else:
            break


def _should_filter_output(line: str) -> bool:
    """Check if output line should be filtered out."""
    filters = [
        "Microsoft Windows",
        "(c) Microsoft Corporation",
        "All rights reserved"
    ]
    # Only filter Windows startup messages, keep Python prompts and output
    return any(filter_text in line for filter_text in filters)


def open_process(process_name: str):
    """Start an interactive shell process and register it."""
    try:
        if process_name in PROCESSES:
            print(f"{timestamp()} ERROR: {process_name} already open")
            return False

        shell_cmd = 'cmd' if platform.system() == 'Windows' else '/bin/bash'
        proc = subprocess.Popen(
            shell_cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        PROCESSES[process_name] = proc

        # Start background thread for stdout
        t = threading.Thread(target=_stream_output, args=(process_name, proc), daemon=True)
        t.start()

        print(f"{timestamp()} INFO: {process_name} opened")
        
        # Wait for shell to initialize and startup messages to complete
        time.sleep(0.1)
        return True
        
    except Exception as e:
        print(f"{timestamp()} ERROR: Failed to open {process_name} - {str(e)}")
        return False


def run_command(process_name: str, command: str):
    """Send a command to a running process with timestamp and response tracking."""
    try:
        proc = PROCESSES.get(process_name)
        if not proc:
            print(f"{timestamp()} ERROR: {process_name} not found")
            return False

        # Check if process is still alive
        if proc.poll() is not None:
            print(f"{timestamp()} ERROR: {process_name} process has terminated")
            del PROCESSES[process_name]
            return False

        print(f"{timestamp()} COMMAND: {command}")
        proc.stdin.write(command + "\n")
        proc.stdin.flush()
        # Brief wait to allow command to execute and output to be captured
        time.sleep(0.1)
        return True
        
    except Exception as e:
        print(f"{timestamp()} ERROR: Failed to execute command in {process_name} - {str(e)}")
        return False


def list_processes():
    """List all managed process names."""
    try:
        if not PROCESSES:
            print(f"{timestamp()} INFO: No active processes")
            return True
        
        print(f"{timestamp()} INFO: Active processes:")
        active_count = 0
        for process_name in list(PROCESSES.keys()):  # Use list() to avoid modification during iteration
            proc = PROCESSES[process_name]
            if proc.poll() is None:
                print(f"{timestamp()} INFO: {process_name} RUNNING (PID: {proc.pid})")
                active_count += 1
            else:
                print(f"{timestamp()} WARNING: {process_name} TERMINATED")
                del PROCESSES[process_name]
        
        print(f"{timestamp()} INFO: Total active processes: {active_count}")
        return True
        
    except Exception as e:
        print(f"{timestamp()} ERROR: Failed to list processes - {str(e)}")
        return False


def close_process(process_name: str):
    """Terminate a managed process."""
    try:
        proc = PROCESSES.pop(process_name, None)
        if not proc:
            print(f"{timestamp()} ERROR: {process_name} not found")
            return False

        pid = proc.pid  # Store PID before terminating

        # Check if process is already terminated
        if proc.poll() is not None:
            print(f"{timestamp()} WARNING: {process_name} already terminated (PID: {pid})")
            return True

        # Try graceful exit first
        try:
            proc.stdin.write("exit\n")
            proc.stdin.flush()
            time.sleep(0.1)
        except Exception as e:
            print(f"{timestamp()} WARNING: Could not send exit command to {process_name} - {str(e)}")

        # Force terminate if still running
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=2)
                print(f"{timestamp()} INFO: {process_name} closed (PID: {pid}) (terminated)")
            except subprocess.TimeoutExpired:
                proc.kill()
                print(f"{timestamp()} INFO: {process_name} closed (PID: {pid}) (killed)")
        else:
            print(f"{timestamp()} INFO: {process_name} closed (PID: {pid})")

        return True
        
    except Exception as e:
        print(f"{timestamp()} ERROR: Failed to close {process_name} - {str(e)}")
        return False


def parse_args():
    parser = argparse.ArgumentParser(description='CLI_Commander process manager')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--open', action='store_true', help='Open a named process')
    group.add_argument('--close', action='store_true', help='Close a named process')
    group.add_argument('--list', action='store_true', help='List processes')
    parser.add_argument('--process_name', default='default', help='Process name')
    parser.add_argument('--command', help='Command to run inside process')

    return parser.parse_args()


def main():
    args = parse_args()

    if len(sys.argv) == 1:
        # Self‑test when no arguments are provided
        demo = 'demo'
        open_process(demo)
        run_command(demo, 'echo Hello CLI_Commander')
        list_processes()
        close_process(demo)
        return

    if args.open:
        open_process(args.process_name)
    elif args.close:
        close_process(args.process_name)
    elif args.list:
        list_processes()
    elif args.command:
        run_command(args.process_name, args.command)
    else:
        print('No action specified. Use -h for help.')


if __name__ == '__main__':
    main()
