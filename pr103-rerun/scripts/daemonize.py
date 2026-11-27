#!/usr/bin/env python3
"""Daemonize a command: double-fork + setsid so parent session/server restarts and
process-group kills cannot reach it. stdout/stderr -> logfile."""
import os
import sys


def main():
    if len(sys.argv) < 3:
        sys.exit("usage: daemonize.py <logfile> <cmd> [args...]")
    logfile, cmd = sys.argv[1], sys.argv[2:]
    if os.fork() > 0:
        return  # grandchild is re-parented; nothing to reap reliably here
    os.setsid()
    if os.fork() > 0:
        os._exit(0)
    fd = os.open(logfile, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o644)
    os.dup2(fd, 1)
    os.dup2(fd, 2)
    devnull = os.open(os.devnull, os.O_RDONLY)
    os.dup2(devnull, 0)
    os.environ["PATH"] = "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
    os.execvp(cmd[0], cmd)


if __name__ == "__main__":
    main()
