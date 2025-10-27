#!/usr/bin/env python3
"""Test script to verify Slack app connection"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check environment variables
app_token = os.getenv("SLACK_APP_TOKEN")
bot_token = os.getenv("SLACK_BOT_TOKEN")

print("=" * 50)
print("Environment Variables Check")
print("=" * 50)

if app_token:
    print(f"✓ SLACK_APP_TOKEN: {app_token[:15]}...")
else:
    print("✗ SLACK_APP_TOKEN: NOT FOUND")

if bot_token:
    print(f"✓ SLACK_BOT_TOKEN: {bot_token[:15]}...")
else:
    print("✗ SLACK_BOT_TOKEN: NOT FOUND")

print("\n" + "=" * 50)
print("Attempting to start Socket Mode handler...")
print("=" * 50)
print()

try:
    from src.slack_io.bolt_app import run_socket_mode
    run_socket_mode()
except KeyboardInterrupt:
    print("\n\nShutting down...")
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
