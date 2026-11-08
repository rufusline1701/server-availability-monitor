#!/usr/bin/env python3
"""A small server availability monitor for learning Python and networking."""

import argparse
import csv
import platform
import subprocess
import time
from datetime import datetime
from pathlib import Path

DEFAULT_HOSTS = ["1.1.1.1", "8.8.8.8", "github.com"]
LOG_FILE = Path("results.csv")


def ping(host: str, timeout: int = 2) -> tuple[bool, float | None]:
    """Ping one host. Returns (is_available, response_time_ms)."""
    system = platform.system().lower()

    if system == "windows":
        command = ["ping", "-n", "1", "-w", str(timeout * 1000), host]
    else:
        command = ["ping", "-c", "1", "-W", str(timeout), host]

    started = time.perf_counter()
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout + 2,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False, None

    elapsed_ms = (time.perf_counter() - started) * 1000
    if result.returncode == 0:
        return True, round(elapsed_ms, 2)
    return False, None


def save_result(host: str, status: str, response_ms: float | None) -> None:
    """Append one check result to a CSV file."""
    new_file = not LOG_FILE.exists()
    with LOG_FILE.open("a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if new_file:
            writer.writerow(["timestamp", "host", "status", "response_ms"])
        writer.writerow([
            datetime.now().astimezone().isoformat(timespec="seconds"),
            host,
            status,
            response_ms if response_ms is not None else "",
        ])


def check_hosts(hosts: list[str]) -> None:
    for host in hosts:
        available, response_ms = ping(host)
        status = "UP" if available else "DOWN"
        if available:
            print(f"[{status:4}] {host:25} {response_ms} ms")
        else:
            print(f"[{status:4}] {host:25} no response")
        save_result(host, status, response_ms)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check whether hosts respond to ping and log the results."
    )
    parser.add_argument(
        "hosts",
        nargs="*",
        help="Hosts or IP addresses to check. Defaults to 1.1.1.1, 8.8.8.8 and github.com.",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=0,
        help="Repeat checks every N seconds. 0 means run once.",
    )
    args = parser.parse_args()

    hosts = args.hosts or DEFAULT_HOSTS
    if args.interval < 0:
        parser.error("--interval must be zero or a positive number")

    print("Server availability monitor")
    print(f"Logging results to: {LOG_FILE.resolve()}")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            print(f"\nCheck time: {datetime.now().astimezone():%Y-%m-%d %H:%M:%S %Z}")
            check_hosts(hosts)
            if args.interval == 0:
                break
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")


if __name__ == "__main__":
    main()
