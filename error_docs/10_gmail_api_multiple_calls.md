# Problem: Excessive Gmail API Calls on Server Startup

## Context
After launching `uvicorn`, Gmail’s activity dashboard showed 8–12 API calls before we invoked any endpoint. This is undesirable because it consumes quota and may throttle the account. The calls were traced to the background pipeline runner in `api/main.py`.

## Root Cause
The background task was configured to run immediately at startup. When it fired, it called `run_notification_pipeline()`, which performs:
1. `messages.list` (1 API call)
2. `messages.get` for up to `limit` messages (default 10 API calls)
3. Potential token refresh requests

Therefore a single startup triggered about a dozen Gmail requests. If the server restarts frequently, the quota is quickly exhausted.

## Step-by-Step Solution
We have two practical options:

### Option A: Disable the Runner for Local Testing
1. Set the poll interval to zero in `.env`:
   ```
   EMAIL_POLL_INTERVAL=0
   ```
2. Restart the FastAPI server. The startup hook checks this value and skips creating the background task.
3. Trigger the pipeline manually through `/agents/notification-preview` or `/agents/graph-preview` when you want to test.

### Option B: Add a Startup Delay (keep automatic polling)
1. Modify the background runner in `api/main.py` to wait before the first execution:
   ```python
   async def background_pipeline_runner() -> None:
       interval = max(settings.email_poll_interval, 60)
       await asyncio.sleep(10)  # wait 10 seconds before the first run
       # existing while loop follows...
   ```
2. Optionally reduce the default `limit` inside `run_notification_pipeline` to shrink the number of `messages.get` calls per run.

## Prevention Tips
- Expose controls in the API (e.g., `/system/pipeline/start` and `/system/pipeline/stop`) so you can toggle background polling without editing code.
- Log the total Gmail calls per run to monitor quota usage over time.
- Document the default poll interval in `README.md` and suggest testing with `EMAIL_POLL_INTERVAL=0`.

## Validation Steps
- After applying Option A, restart the server and check Gmail’s usage: there should be no calls until you hit an endpoint manually.
- After applying Option B, confirm the first automatic run happens only after the configured delay, and observe reduced call counts in Gmail’s dashboard.
