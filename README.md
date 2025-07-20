# CLI_Commander

A simple process manager for interactive shell sessions on Linux.

## Overview

CLI_Commander is a Python tool for managing persistent interactive shell processes using tmux. It allows you to open, manage, and communicate with shell or REPL sessions, and view their output in real time.

## Command Line Options

| Option | Description |
|--------|-------------|
| `--new` | Create a new named process |
| `--name NAME` | Specify the process name |
| `--run` | Run a command in a named process (starts a new session if not running) |
| `--command COMMAND` | The command to execute or send |
| `--wait SECONDS` | Wait time after command execution (default: 0.2) |
| `--close` | Close a named process |
| `--close_all` | Close all active processes |
| `--list` | List all active processes |
(default: 0.2) |
| `-h, --help` | Show help message |
| `--test` | Run tests |
## Example

```bash
# Create a new process and run a command
python CLI_Commander.py --new --name demo
python CLI_Commander.py --run --name demo --command "echo Hello! CLI Commander"
python CLI_Commander.py --list
python CLI_Commander.py --close --name demo
```

## Output Format

CLI_Commander prints output in the following format:
Example output:
```
[2025-07-20 12:00:00] [demo] [INFO] Created new process entry: demo
[2025-07-20 12:00:01] [demo] [COMMAND] echo Hello! CLI Commander
[2025-07-20 12:00:01] [demo] [RESPONSE] Hello! CLI Commander
[2025-07-20 12:00:02] [demo] [INFO] Process demo closed (PID: 5268)
```