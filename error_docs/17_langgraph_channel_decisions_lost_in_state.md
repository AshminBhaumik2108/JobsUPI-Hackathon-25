# Problem: Channel Decisions Lost Between Graph Nodes (Empty Channels/Rationales)

## Context

When calling `/agents/graph-preview`, the response returned empty arrays for `channels` and `channel_rationales`, even though the `/agents/notification-preview` endpoint correctly returned populated values. Debug logging revealed that `channel_decisions` were being created successfully in the `channels` node but were lost before reaching the `delivery` node.

## Error Message

No explicit error message appeared, but the issue manifested as:

- `/agents/graph-preview` returns empty `channels: []` and `channel_rationales: []`
- `/agents/notification-preview` correctly returns populated channels and rationales
- Debug logs showed: `channel_decisions count: 5` in channels node, but `channel_decisions count: 0` in delivery node

## Root Cause

The `NotificationState` class in `graph/notification_graph.py` was missing the `channel_decisions` field in its schema definition. LangGraph's state management system only preserves fields that are explicitly defined in the state schema. When the `channels` node set `state["channel_decisions"]`, LangGraph filtered it out because it wasn't part of the schema, causing the data to be lost before the `delivery` node could access it.

**The Problem:**

```python
class NotificationState(dict):
    """State passed between nodes in the LangGraph workflow."""
    messages: List[EmailMessage]
    sender_result: Dict[str, Any]
    analyses: List[ContentAnalysis]
    decisions: List[Any]
    notifications: List[Any]
    delivery: Dict[str, Any]
    # ❌ channel_decisions was missing!
```

**What Happened:**

1. `run_channels` node successfully created 5 `channel_decisions` and stored them in `state["channel_decisions"]`
2. LangGraph filtered out `channel_decisions` because it wasn't in the schema
3. `run_delivery` node received `channel_decisions count: 0` (empty list)
4. `DeliveryAgent` returned empty channels and rationales because it had no channel decisions to process

## Step-by-Step Solution

### Step 1: Add `channel_decisions` to NotificationState Schema

1. **Open `graph/notification_graph.py`** and locate the `NotificationState` class (around line 20-28).

2. **Add `channel_decisions` field to the schema:**

   ```python
   class NotificationState(dict):
       """State passed between nodes in the LangGraph workflow."""
       messages: List[EmailMessage]
       sender_result: Dict[str, Any]
       analyses: List[ContentAnalysis]
       decisions: List[Any]
       notifications: List[Any]
       channel_decisions: List[Any]  # ← Add this line
       delivery: Dict[str, Any]
   ```

3. **Verify the initial state in `invoke_graph()` already includes it:**
   ```python
   initial_state: NotificationState = {
       "messages": messages,
       "sender_result": {},
       "analyses": [],
       "decisions": [],
       "notifications": [],
       "channel_decisions": [],  # ← Should already be here
       "delivery": {},
   }
   ```

### Step 2: Restart the Server

```bash
uvicorn api.main:app --reload
```

### Step 3: Test the Fix

1. **Call the graph preview endpoint:**

   ```bash
   curl "http://localhost:8000/agents/graph-preview?limit=5&query=Division%20of%20Career%20Services"
   ```

2. **Verify the response now includes:**

   ```json
   {
     "channels": ["api_response"],
     "channel_rationales": [
       "Included in API response; Standard placement update",
       ...
     ]
   }
   ```

3. **Check debug logs** (if still enabled):
   - Should show: `channel_decisions count: 5` in both channels and delivery nodes
   - Should show: `delivery.channels: ['api_response']` and `channel_rationales count: 5`

## Prevention Tips

- **Always include all state fields in the schema**: When adding new data to state, ensure it's defined in the `NotificationState` class
- **Use debug logging during development**: Add temporary logging to verify data flows correctly between nodes
- **Compare with working implementations**: The direct pipeline (`/agents/notification-preview`) worked because it doesn't use LangGraph's state filtering
- **Test both endpoints**: Always verify that `/agents/graph-preview` and `/agents/notification-preview` return consistent results
- **Document state schema**: Keep the state schema well-documented to avoid missing fields

## Validation Steps

1. **Verify channels are populated:**

   - Call `/agents/graph-preview` with a query that returns placement emails
   - Check that `channels` array is not empty
   - Verify `channel_rationales` array has the same count as notifications

2. **Compare with notification-preview:**

   - Call both endpoints with the same parameters
   - Verify they return identical `channels` and `channel_rationales` values
   - Both should have the same structure and content

3. **Check debug logs (if enabled):**

   - Verify `channel_decisions count` is the same in both channels and delivery nodes
   - Confirm no errors are logged in the channels or delivery nodes

4. **Test edge cases:**
   - Test with `limit=0` or no matching emails
   - Verify the response handles empty cases gracefully
   - Ensure no KeyError or AttributeError occurs

## Additional Notes

- **LangGraph State Management**: LangGraph uses the state schema to validate and filter state data. Any field not in the schema will be silently dropped when state is passed between nodes.
- **Type Safety**: The `NotificationState` class uses type hints, but LangGraph treats it as a dictionary. Always ensure all keys used in state are defined in the schema.
- **Debug Logging**: The debug logging added to diagnose this issue can be removed once the problem is confirmed fixed, or kept for future debugging.
