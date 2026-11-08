# Server Availability Monitor

A beginner-friendly Python project that checks whether hosts respond to `ping` and stores the results in a CSV file.

## What it does

- Checks one or more hostnames or IP addresses.
- Displays `UP` or `DOWN` and approximate response time.
- Saves every check to `results.csv`.
- Can repeat checks at a chosen interval.
- Uses only Python's standard library (no third-party packages).

## Requirements

- Python 3.10 or newer.
- The system `ping` utility must be available.
- Internet access is needed to check public hosts.

## Run

Open a terminal in this folder.

Run the default checks:

```bash
python monitor.py
```

Check specific hosts:

```bash
python monitor.py github.com 1.1.1.1
```

Repeat checks every 30 seconds:

```bash
python monitor.py --interval 30
```

Stop repeated checks with `Ctrl+C`.

On some Linux distributions, the `ping` command may need to be installed separately.

## Output

The program creates `results.csv` in the current working directory:

| timestamp | host | status | response_ms |
|---|---|---|---|
| local date and time | github.com | UP / DOWN | response time in milliseconds |

## Concepts demonstrated

- Running external system commands with `subprocess`.
- Measuring elapsed time.
- Working with command-line arguments (`argparse`).
- Writing structured data to CSV.
- Handling timeouts and keyboard interruption.

## Possible improvements

1. Add configurable timeout and host list in a config file.
2. Calculate uptime percentage.
3. Add log rotation.
4. Run the monitor as a Linux systemd service.
5. Package the project with Docker.

## Note

This is a learning project, not a production monitoring system. A failed ping does not always mean a server is down: some hosts block ICMP traffic.
