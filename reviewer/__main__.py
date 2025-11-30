import argparse
import asyncio
import sys

from reviewer.src.read_app import run_read_app
from reviewer.src.write_app import run_write_app

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Run ReadApp (FastAPI) or WriteApp (FastStream)"
    )
    parser.add_argument(
        "mode",
        choices=["read", "write"],
        help="Choose which app to run"
    )
    args = parser.parse_args()

    if args.mode == "read":
        run_read_app()
    elif args.mode == "write":
        asyncio.run(
            run_write_app()
        )
    else:
        print(
            "ERROR: Invalid mode specified. "
            "Please choose 'read' or 'write'.\n"
        )
        parser.print_help()
        sys.exit(1)
