# How to Start the App

## Method 1: Using test_connection.py
```bash
python test_connection.py
```

## Method 2: Using the module directly
```bash
python -m src.slack_io.bolt_app
```

## Method 3: Using the shell script
```bash
./run_app.sh
```

## What to Look For

Once running, you should see:
1. Environment variable loading messages
2. Channel loading messages
3. "⚡️ Bolt app is running!"
4. Event logs when messages arrive

## Testing

1. Send a message in a configured channel (like #product or #eng-backend)
2. Watch the logs for `[CONDUCTOR]` messages
3. You should see messages like:
   - `[CONDUCTOR] NEW EVENT RECEIVED`
   - `[CONDUCTOR] Processing event from...`
   - `[CONDUCTOR] Scheduling X replies`
   - `[CONDUCTOR] persona_name posting reply`

## Troubleshooting

If you don't see logs:
1. Make sure the app is actually running (check the process)
2. Check that you're sending messages in a configured channel
3. Verify your .env file has SLACK_APP_TOKEN and SLACK_BOT_TOKEN

If logs appear but no replies:
- Check the conductor logs to see why messages are being skipped
- Look for cooldown messages
- Check if personas are in cooldown
