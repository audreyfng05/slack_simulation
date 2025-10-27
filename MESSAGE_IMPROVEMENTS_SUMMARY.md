# Message Quality Improvements

## Changes Made to Match slackbench_sim Quality

### 1. **Removed Citation Requirements** ✅
**Before:** Forced `[[ref:TIMESTAMP]]` citations made messages awkward
**After:** Natural flow without forced citations

### 2. **Simplified Context Formatting** ✅
**Before:** `"[ 1761519740.989239 ] Mike_BE: Fetching logs..."`
**After:** `"Mike_BE: Fetching logs from prod..."`

### 3. **Added Role-Specific Guidance** ✅
**Before:** Generic prompts for all roles
**After:** Each role gets specific guidance:
- Backend Engineer: "Provide technical analysis from a systems perspective"
- Product Manager: "Focus on business impact and stakeholder communication"
- QA Tester: "Share testing insights or verification steps"
- etc.

### 4. **Better Prompts** ✅
**Before:** "Rules: Use 1–2 specific context lines as evidence..."
**After:** "Guidance: Respond naturally based on your role..."
**Before:** "Incoming message: ..."
**After:** "Goal: ..." (more natural)

### 5. **Improved Temperature & Tokens** ✅
**Before:** `temperature=0.6, max_tokens=140`
**After:** `temperature=0.7, max_tokens=180` (more natural length)

### 6. **Enhanced Persona System Prompts** ✅
Now includes:
- Role-specific personality hints
- Expertise areas
- Typical contributions
- Communication style phrases
- Example messages (seed snippets)

## Key Differences Fixed

| Issue | slackbench_sim | slackbench_real_sim (Before) | slackbench_real_sim (After) |
|-------|---------------|------------------------------|----------------------------|
| Citations | ❌ None | ❌ Required | ✅ None |
| Context format | ✅ Simple | ❌ Technical | ✅ Simple |
| Role guidance | ✅ Specific | ❌ Generic | ✅ Specific |
| Prompts | ✅ Natural | ❌ Formal | ✅ Natural |
| Max tokens | ✅ 180 | ❌ 140 | ✅ 180 |
| Temperature | ✅ 0.7 | ❌ 0.6 | ✅ 0.7 |

## Expected Results

Your messages should now be:
- ✅ More natural and conversational
- ✅ Role-appropriate (each agent sounds like their role)
- ✅ Less formulaic
- ✅ More varied in content and style
- ✅ Closer to slackbench_sim quality

## Testing

Restart your app and you should see:
1. Mike_BE sounds technical and direct
2. Gabriella_PM mentions business impact naturally
3. Sarah_FE focuses on UX naturally
4. Messages flow without awkward citations
5. More variety in responses

The improvements focus on making the LLM prompts more natural, which should result in more natural-sounding agent messages! 🎯

