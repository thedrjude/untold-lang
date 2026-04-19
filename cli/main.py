import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from cli.build import cmd_build, cmd_run_binary
from cli.commands import (
    VERSION,
    cmd_check,
    cmd_help,
    cmd_info,
    cmd_init,
    cmd_install,
    cmd_list_packages,
    cmd_new,
    cmd_remove,
    cmd_run,
    cmd_search,
    cmd_version,
)


def main():
    args    = sys.argv[1:]
    command = args[0] if args else None
    rest    = args[1:] if len(args) > 1 else []

    if not command:
        print(f"Untold Lang v{VERSION} — type 'untold help' for commands")
        return

    if command == "run":
        cmd_run(rest[0] if rest else None)
    elif command == "build":
        cmd_build(rest)
    elif command == "run-build":
        cmd_run_binary(rest)
    elif command == "check":
        cmd_check(rest[0] if rest else None)
    elif command == "new":
        cmd_new(rest)
    elif command == "init":
        cmd_init(rest)
    elif command == "install":
        cmd_install(rest)
    elif command == "remove":
        cmd_remove(rest)
    elif command == "list":
        cmd_list_packages()
    elif command == "search":
        cmd_search(rest)
    elif command == "info":
        cmd_info()
    elif command == "version":
        cmd_version()
    elif command == "help":
        cmd_help()
    else:
        print(f"[Untold] Unknown command '{command}'. Run 'untold help'.")
        sys.exit(1)

if __name__ == "__main__":
    main()
