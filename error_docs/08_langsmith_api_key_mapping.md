# Problem: LangSmith Run Creation Failed (API Key Mapping)

## Context
While running the content-analysis agent, the logs repeatedly showed a warning:
```
LangSmith run creation failed; skipping trace logging.
```
This meant our LangSmith dashboard stayed empty even though the agent executed.

## Root Cause
Our settings model (`config/settings.py`) still mapped the LangSmith key to the environment variable `LANGCHAIN_API_KEY`. After we switched to the more explicit `LANGSMITH_API_KEY` in `.env`, the settings object returned `None`, so `Client(api_key=settings.langsmith_api_key)` received a null value. LangSmith silently rejected the request, resulting in `create_run()` returning `None`.

## Step-by-Step Solution
You have two equivalent options:

### Option A: Keep Both Environment Variables
1. Edit `.env`:
   ```
   LANGSMITH_API_KEY=lsv2_pt_...
   LANGCHAIN_API_KEY=lsv2_pt_...
   ```
   Using the same value for both ensures backwards compatibility.
2. Restart the FastAPI server so environment variables reload.
3. Trigger `/agents/content-analysis` and confirm the warning disappears.

### Option B: Update the Settings Alias (preferred long-term)
1. Open `config/settings.py` and change:
   ```python
   langsmith_api_key: str | None = Field(default=None, alias="LANGSMITH_API_KEY")
   ```
2. Adjust `config/langsmith_config.py` to set both env vars for compatibility:
   ```python
   os.environ.setdefault("LANGSMITH_API_KEY", settings.langsmith_api_key or "")
   os.environ.setdefault("LANGCHAIN_API_KEY", settings.langsmith_api_key or "")
   ```
3. Restart the server.
4. Run `/agents/content-analysis`; the log should now confirm the key is loaded.

## Prevention Tips
- Document the expected environment variable names in `README.md` to avoid confusion.
- Whenever you rename an env var, audit the settings module and all spots that read it.
- Add assertions in startup code to warn if critical keys are missing (e.g., log a fatal message if `settings.langsmith_api_key` is falsy).

## Validation Steps
- After applying the fix, hit `/agents/content-analysis` or `/agents/notification-preview`.
- Observe the terminal log: the warning should disappear, replaced by debug logs showing the key is loaded.
- Visit the LangSmith dashboard; new runs should now appear for `content_analysis`.
