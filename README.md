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

```bash
git clone <repository>
cd CLI_Test
```

## Usage

### Basic Commands

#### Open a named process
```bash
python CLI_Commander.py --open --process_name demo
```

#### Run a command in an existing process
```bash
python CLI_Commander.py --process_name demo --command "echo Hello World"
```

#### List all active processes
```bash
python CLI_Commander.py --list
```

#### Close a named process
```bash
python CLI_Commander.py --close --process_name demo
```

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
- `RESPONSE`: Confirmation that command was sent to process

Example output:
```
19:09:26 INFO: demo opened
19:09:26 COMMAND: demo echo Hello CLI_Commander
19:09:26 RESPONSE: Command sent to demo
19:09:26 INFO: Command executed in demo
19:09:26 INFO: Active processes:
19:09:26 INFO: demo RUNNING (PID: 5268)
19:09:26 INFO: Total active processes: 1
19:09:26 INFO: demo closed (PID: 5268)
```

## Architecture

### Core Components

1. **Process Registry**: Global dictionary tracking all managed processes
2. **Output Streaming**: Background threads for real-time output monitoring
3. **Command Interface**: Argument parsing and command dispatch
4. **Process Lifecycle**: Creation, monitoring, and termination management

### Key Functions

- `open_process(process_name)`: Create and register a new shell process
- `run_command(process_name, command)`: Send commands to existing processes
- `list_processes()`: Display status of all managed processes
- `close_process(process_name)`: Terminate and cleanup processes
- `_stream_output()`: Background thread for output monitoring

## Error Handling

CLI_Commander handles various error conditions:

- **Process not found**: When trying to use non-existent process names
- **Process termination**: Automatic cleanup of terminated processes
- **Command execution failures**: Graceful error reporting
- **Resource cleanup**: Proper process termination and resource management

## Limitations

- **Platform-specific shells**: Uses `cmd` on Windows, `bash` on Unix-like systems
- **Output buffering**: Some applications may buffer output differently
- **Process persistence**: Processes don't persist across CLI_Commander restarts
- **Encoding**: May have issues with non-ASCII characters in some environments

## Use Cases

- **Interactive development**: Managing Python/Node.js REPL sessions
- **System administration**: Running multiple shell sessions for different tasks
- **Testing and automation**: Scripted interaction with command-line tools
- **Educational purposes**: Demonstrating process management concepts

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Specify your license here]

## Support

For issues and questions:
- Check the examples in this README
- Review the source code comments
- Open an issue in the repository

---

*CLI_Commander - Simple, effective process management for interactive shells.*
