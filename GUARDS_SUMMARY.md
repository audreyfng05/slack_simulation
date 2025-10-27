# Agent Interaction Guards

This document outlines the guards implemented to prevent agents from creating infinite conversation loops.

## Guard Mechanisms

### 1. Bot Message Filtering
- **Location**: `conductor.py` - `maybe_handle_event()`
- **Guard**: Skips all `bot_message` subtype events
- **Purpose**: Prevents agents from responding to their own bot messages

### 2. Turn Limit Per Thread
- **Variable**: `MAX_TURNS_PER_THREAD = 8`
- **Location**: Tracked in `THREAD_STATE` dictionary
- **Behavior**: Once a thread reaches 8 turns, no more replies are generated
- **Prevents**: Unbounded thread growth

### 3. Grace Period Between Replies
- **Variable**: `SELF_REPLY_GRACE_S = 4` seconds
- **Location**: `_should_skip()` function
- **Behavior**: Blocks replies if the last message in the thread was less than 4 seconds ago
- **Prevents**: Rapid-fire conversations

### 4. Persona Cooldown
- **Variable**: `PERSONA_COOLDOWN_S = 25` seconds
- **Location**: `PERSONA_COOLDOWN` dictionary
- **Behavior**: Each persona must wait 25 seconds after posting before they can post again
- **Prevents**: Single persona dominating a thread

### 5. Self-Reply Prevention
- **Location**: `maybe_handle_event()` - sender detection logic
- **Behavior**: 
  - Detects if the message sender is one of our personas
  - If sender is a persona, only allows reply if thread has 2+ turns already
  - Excludes the sender from the list of eligible repliers
- **Prevents**: Agents replying to themselves immediately

### 6. Concurrent Thread Limit
- **Variable**: `MAX_ACTIVE_THREADS = 5`
- **Location**: `_count_active_threads()` and `_should_skip()`
- **Behavior**: Limits the number of threads that can be actively receiving replies at once
- **Prevents**: Too many simultaneous conversations

### 7. Last Persona Exclusion
- **Location**: `maybe_handle_event()`
- **Behavior**: The persona who posted last in a thread cannot post again immediately
- **Prevents**: Back-and-forth between same two personas

## Configuration

You can adjust these values in `conductor.py`:

```python
MAX_TURNS_PER_THREAD = 8      # Max turns before thread dies
MIN_DELAY_S, MAX_DELAY_S = 2, 8  # Time between replies
PERSONA_COOLDOWN_S = 25        # Cooldown between persona posts
SELF_REPLY_GRACE_S = 4         # Minimum time between posts
MAX_ACTIVE_THREADS = 5         # Max concurrent active threads
```

## Testing the Guards

To verify these guards are working:

1. Send a message in a channel with active agents
2. Watch the logs for:
   - `[CONDUCTOR] Thread reached max turns`
   - `[CONDUCTOR] Thread too recent (grace period)`
   - `[CONDUCTOR] Too many active threads`
3. Observe that conversations naturally die out after reaching limits
