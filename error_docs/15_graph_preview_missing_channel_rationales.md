# Problem: Graph Preview Endpoint Returns Empty Channels and Channel Rationales

## Status
**⚠️ NOT RESOLVED** - This issue has not been corrected yet because a solution could not be found. The problem persists where `/agents/graph-preview` returns empty `channels` and `channel_rationales` arrays, while `/agents/notification-preview` correctly returns populated values.

## Context
When calling the `/agents/graph-preview` endpoint, the response includes empty arrays for `channels` and `channel_rationales`, even though the `/agents/notification-preview` endpoint correctly returns populated values for the same data. Both endpoints should use the same pipeline logic and return identical response structures.

## Symptom
- **`/agents/graph-preview`** returns:
  ```json
  {
    "channels": [],
    "channel_rationales": []
  }
  ```

- **`/agents/notification-preview`** returns:
  ```json
  {
    "channels": ["api_response", "immediate_attention"],
    "channel_rationales": [
      "Included in API response; High priority message",
      "Included in API response; Standard placement update"
    ]
  }
  ```

## Root Cause
In `graph/notification_graph.py`, the `invoke_graph()` function incorrectly extracts `channel_rationales` from the wrong source. On line 156, it uses:

```python
"channel_rationales": final_state.get("channel_decisions", []),
```

This returns `ChannelDecision` objects (which are dataclass instances), not the actual rationale strings. The `DeliveryResult` object from `run_delivery()` already contains the correct `channel_rationales` as a list of strings, but this wasn't being used.

The `channels` field was correctly extracted from `delivery.channels`, but `channel_rationales` was not extracted from `delivery.channel_rationales`.

## Step-by-Step Solution

1. **Open `graph/notification_graph.py`** and locate the `invoke_graph()` function (around line 152-157).

2. **Fix the `channel_rationales` extraction**:
   ```python
   "delivery": {
       "delivered": bool(delivery.delivered) if delivery else False,
       "channels": delivery.channels if delivery else [],
       "details": delivery.details if delivery else "",
       "channel_rationales": delivery.channel_rationales if delivery else [],  # Fixed
   },
   ```

3. **Change line 156 from**:
   ```python
   "channel_rationales": final_state.get("channel_decisions", []),
   ```
   
   **To**:
   ```python
   "channel_rationales": delivery.channel_rationales if delivery else [],
   ```

4. **Restart the FastAPI server** to apply the changes.

5. **Test the endpoint**:
   ```bash
   curl "http://localhost:8000/agents/graph-preview?limit=5&query=Division%20of%20Career%20Services"
   ```
   
   Verify that `channels` and `channel_rationales` are now populated correctly.

## Prevention Tips
- When extracting data from state objects, always verify the data structure matches expectations.
- Use consistent patterns: if `delivery.channels` works, use `delivery.channel_rationales` for the same object.
- Add type hints and validation to catch these issues during development.
- Compare response structures between similar endpoints to ensure consistency.

## Validation Steps
1. Call `/agents/graph-preview` with a query that returns placement-related emails.
2. Verify the response includes:
   - Non-empty `channels` array (e.g., `["api_response", "immediate_attention"]`)
   - Non-empty `channel_rationales` array with string values
3. Compare the response structure with `/agents/notification-preview` - they should match.
4. Verify that the number of `channel_rationales` matches the number of notifications.

