import os
import sys
import argparse
from colony_client import ColonyClient, LoggerService

def parse_user_input():
    parser = argparse.ArgumentParser(prog='Colony Sandbox Start')
    parser.add_argument("sandbox_id", type=str, help="The name of sandbox")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_user_input()

    client = ColonyClient(
        space=os.environ.get("COLONY_SPACE", ""),
        token=os.environ.get("COLONY_TOKEN", "")
    )
    sandbox_id = args.sandbox_id

    if not sandbox_id:
        LoggerService.error("Sandbox Id cannot be empty.")

    try:
        client.end_sandbox(sandbox_id)
        LoggerService.success(f"End request has been sent.")
    except Exception as e:
        LoggerService.error(f"Unable to stop Sandbox {sandbox_id}; reason: {e}")
