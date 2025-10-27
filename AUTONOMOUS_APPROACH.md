# Autonomous Agent Interaction - Better Approach

## Overview

I've implemented a **hybrid approach** that combines:
1. **Autonomous simulation loop** (like `slackbench_sim`) that proactively generates conversations
2. **Event-driven response** to real Slack messages
3. **Best of both worlds**: autonomous generation + real Slack integration

## What Changed

### New Module: `autonomous_loop.py`

This module implements a simulation loop similar to `slackbench_sim`:

- **Runs independently** in a background thread
- **Every 45 seconds**, generates a new message from a random persona
- **Posts directly to Slack** via the API
- **Maintains an in-memory history** of all messages (both generated and real)
- **60% chance** of replying to an existing thread, 40% chance of starting a new topic

### Key Advantages

✅ **No dependency on events**: Conversations happen automatically  
✅ **Predictable flow**: Like slackbench_sim, agents interact autonomously  
✅ **Still responds to real messages**: Hybrid mode includes event handling  
✅ **Faster iteration**: Agents post every 45 seconds (adjustable)  

## Architecture Comparison

### Before (Event-Only)
```
Slack Event → Conductor → Agents Respond → Wait for Next Event
```
Problem: Agents only react, never proactively start conversations

### Now (Autonomous + Events)
```
Autonomous Loop: Every 45s → Generate Message → Post to Slack
                     ↓
              In-Memory History
                     ↓
Slack Event → Conductor → Agents Respond (optional)
```
Result: Continuous autonomous conversations + optional event responses

## Slack API Settings

**No special API settings needed!** The autonomous loop uses standard Slack API methods:

1. `chat.postMessage` - Post messages
2. No special permissions beyond what you already have
3. Works with your existing bot token

### Required Scopes (you should already have these):
```
chat:write          # Post messages
channels:read       # List channels
groups:read         # Read private channels
im:read             # Read DMs
mpim:read           # Read group DMs
```

## Configuration

Edit `autonomous_loop.py` to customize:

```python
TURN_INTERVAL_S = 45  # How often to generate a message (seconds)
PERSONA_COOLDOWN_S = 60  # Cooldown between same persona posting
```

### To Disable Event-Driven Response (Pure Autonomous):

Comment out the conductor in `bolt_app.py`:

```python
@app.event("message")
def handle_message_events(body, event, logger, say):
    # Add to autonomous history
    add_real_message_to_history(event)
    
    # Uncomment to keep event-driven responses:
    # maybe_handle_event(event)
```

### To Disable Autonomous Loop (Events Only):

Comment out in `bolt_app.py`:

```python
# start_autonomous_loop()  # Disable autonomous mode
```

## How It Works

1. **Startup**: Autonomous loop starts in background thread
2. **Every 45 seconds**:
   - Pick random channel and persona
   - Decide: new message (40%) or reply to thread (60%)
   - Generate message using LLM
   - Post to Slack
   - Add to in-memory history
3. **When real messages arrive**:
   - Add to in-memory history
   - Optionally trigger conductor for event-driven replies

## Testing

1. **Start the app**: `python test_connection.py`
2. **Watch logs**:
   ```
   [AUTONOMOUS] Autonomous loop started (turn interval: 45s)
   [AUTONOMOUS] Gabriella_PM posted new message in #product
   [AUTONOMOUS] Mike_BE replied in thread in #eng-backend
   ```
3. **Expected behavior**:
   - Messages appear in Slack every ~45 seconds
   - Agents reply to each other
   - Conversations develop naturally
   - Can still respond to real messages

## Advantages Over Event-Only

| Aspect | Event-Only | Autonomous |
|--------|-----------|------------|
| **Conversation Start** | Requires trigger | Automatic |
| **Flow Control** | Event-driven | Time-based |
| **Predictability** | Unpredictable | More predictable |
| **Agent Interaction** | Reactive only | Proactive |
| **Simulation Similarity** | Different | Very similar |
| **Debugging** | Harder | Easier (time-based) |

## Performance Considerations

- **Rate Limits**: Slack allows ~1 message/second per bot
- **We post every 45 seconds**: Well within limits
- **Multiple personas**: Still within limits
- **Queue system**: Handles rate limits gracefully

## Troubleshooting

### Agents not posting:
- Check logs for `[AUTONOMOUS]` messages
- Verify channel IDs are loaded
- Check persona usernames match Slack

### Too many messages:
- Increase `TURN_INTERVAL_S` (default: 45 seconds)
- Enable conductor filtering of autonomous messages

### Not enough interaction:
- Decrease `TURN_INTERVAL_S`
- Increase reply probability in `autonomous_loop.py`

## Hybrid Mode Explained

The system now runs in **hybrid mode** by default:

1. **Autonomous loop**: Generates conversations independently
2. **Event handler**: Still responds to real messages
3. **Shared history**: Both use the same in-memory history

This gives you the best of both worlds!

## Conclusion

This approach matches `slackbench_sim` much more closely:
- ✅ Autonomous conversation generation
- ✅ Time-based scheduling
- ✅ Internal state management
- ✅ Posts to real Slack
- ✅ No special API configuration needed

The key insight: **Run a simulation loop that posts to Slack** rather than relying solely on Slack events.
