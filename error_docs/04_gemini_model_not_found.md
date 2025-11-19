# Problem: Gemini Model Not Found (`404 models/gemini-1.5-flash`)

## Context
When the content analysis agent attempted to call Gemini via the Google Generative AI SDK, the API responded with a 404 error indicating the requested model did not exist. This appeared after we updated dependencies and tried the endpoint `/agents/content-analysis`.

## Error Message
```
404 models/gemini-1.5-flash is not found for API version v1beta
```

## Root Cause
Two separate issues triggered this error:
1. The `google-ai-generativelanguage` dependency was outdated (`<0.7.0`), so it did not expose the newer Gemini model families.
2. The code referenced `gemini-1.5-flash-002`, which the free-tier API no longer served under the chosen package version. We needed to switch to `models/gemini-2.5-flash`, the latest free-tier-friendly model supported by `google-generativeai==0.8.5` plus the newer language package.

## Step-by-Step Solution
1. **Upgrade the Google Generative AI libraries:**
   ```bash
   pip install --upgrade --force-reinstall --no-deps "google-ai-generativelanguage>=0.7.0"
   pip install --upgrade google-generativeai==0.8.5
   ```
   Using `--no-deps` avoids downgrading other packages unexpectedly.

2. **Update the model name in the agent:**
   - Open `agents/content_analysis_agent.py`.
   - Use `model_name="models/gemini-2.5-flash"` in the `GenerativeModel` call.

3. **Restart the FastAPI server** so the new environment variables and dependency changes take effect.

4. **Retry the endpoint:**
   ```bash
   curl http://localhost:8000/agents/content-analysis
   ```
   or use Postman. The response should contain model-generated analyses instead of a 404 error.

## Prevention Tips
- Track Google’s official release notes for Gemini; model names and API versions evolve quickly.
- Keep the `requirements.txt` pinned to known-working pairs (`google-generativeai` and `google-ai-generativelanguage`).
- Whenever you modify dependency versions, rerun a quick smoke test hitting the Gemini endpoint to verify the model responds.

## Validation Steps
- Run `/agents/content-analysis` and confirm the response has `analysed_count > 0` with `is_placement_related` fields.
- Check the terminal logs: the 404 error should no longer appear.
- Confirm LangSmith traces (if configured) capture successful runs again.
