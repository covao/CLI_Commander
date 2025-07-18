# CLI_Commander

A simple cross-platform process manager for interactive shell sessions.

## Overview

CLI_Commander is a Python tool that manages interactive shell processes across different platforms. It provides a simple interface to open, manage, and communicate with shell sessions while maintaining real-time output monitoring.

## Key Features

- **Cross-platform support**: Works on Windows (cmd), Linux, and macOS (bash)
- **Real-time output streaming**: Monitor process output with timestamps
- **Background thread management**: Non-blocking output monitoring
- **Process state tracking**: Track and manage multiple named sessions
- **Graceful termination**: Supports both graceful exit and forced termination
- **Error handling**: Comprehensive error detection and reporting

## Installation

No additional dependencies required beyond Python 3.6+. The tool uses only standard library modules:


### Self-test Demo

Run without arguments to see a quick demonstration:

```bash
python CLI_Commander.py
```

This will:
1. Open a process named 'demo'
2. Execute an echo command
3. List active processes
4. Close the demo process

## Command Line Options

| Option | Description |
|--------|-------------|
| `--open` | Open a new named process |
| `--close` | Close an existing named process |
| `--list` | List all active processes with status |
| `--process_name NAME` | Specify the process name (default: 'default') |
| `--command CMD` | Execute a command in the specified process |
| `-h, --help` | Show help message |

## Examples

### Example 1: Basic Shell Interaction
```bash
# Start a new shell session
python CLI_Commander.py --open --process_name myshell

# Run commands in the session
python CLI_Commander.py --process_name myshell --command "dir"
python CLI_Commander.py --process_name myshell --command "cd .."
python CLI_Commander.py --process_name myshell --command "echo Current directory changed"

# Close the session
python CLI_Commander.py --close --process_name myshell
```

### Example 2: Python Interactive Session
```bash
# Start a session for Python
python CLI_Commander.py --open --process_name python_session

# Start Python interpreter
python CLI_Commander.py --process_name python_session --command "python"

# Execute Python commands
python CLI_Commander.py --process_name python_session --command "print('Hello from Python')"
python CLI_Commander.py --process_name python_session --command "2 + 2"

# Exit Python and close session
python CLI_Commander.py --process_name python_session --command "exit()"
python CLI_Commander.py --close --process_name python_session
```

### Example 3: Managing Multiple Sessions
```bash
# Open multiple sessions
python CLI_Commander.py --open --process_name session1
python CLI_Commander.py --open --process_name session2
python CLI_Commander.py --open --process_name session3

# Check all active sessions
python CLI_Commander.py --list

# Work with different sessions
python CLI_Commander.py --process_name session1 --command "echo Working in session 1"
python CLI_Commander.py --process_name session2 --command "echo Working in session 2"

# Close all sessions
python CLI_Commander.py --close --process_name session1
python CLI_Commander.py --close --process_name session2
python CLI_Commander.py --close --process_name session3
```

## Output Format

CLI_Commander provides timestamped output with clear status indicators:

- `ERROR`: Operation failed
- `WARNING`: Non-fatal issues
- `INFO`: Informational messages
- `COMMAND`: Command being executed

Example output:
```
19:09:26 SUCCESS: demo opened
19:09:26 COMMAND: demo echo Hello CLI_Commander
19:09:26 demo Hello CLI_Commander
19:09:26 SUCCESS: Command executed in demo
19:09:26 INFO: Active processes:
19:09:26 SUCCESS: demo RUNNING (PID: 5268)
19:09:26 INFO: Total active processes: 1
19:09:26 INFO: demo closed (PID: 5268)
```

## Architecture

### Key Functions

- `open_process(process_name)`: Create and register a new shell process
- `run_command(process_name, command)`: Send commands to existing processes
- `list_processes()`: Display status of all managed processes
- `close_process(process_name)`: Terminate and cleanup processes
- `_stream_output()`: Background thread for output monitoring

