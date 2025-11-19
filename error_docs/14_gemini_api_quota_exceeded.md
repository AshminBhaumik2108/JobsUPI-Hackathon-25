# Problem: Gemini API Quota Exceeded (429 Error)

## Context
When processing multiple email messages through the content analysis agent, the system encounters 429 (Quota Exceeded) errors from the Gemini API. The pipeline continues to execute and saves data successfully, but all content analyses fail with quota errors. This occurs when processing 5+ emails in rapid succession, especially when hitting the `/agents/notification-preview` endpoint with `limit=10`.

## Error Message
```
429 You exceeded your current quota, please check your plan and billing details. 
For more information on this error, head to: https://ai.google.dev/gemini-api/docs/rate-limits. 
To monitor your current usage, head to: https://ai.dev/usage?tab=rate-limit.

* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, 
  limit: 10, model: gemini-2.5-flash
Please retry in 44.182577601s.
```

## Root Cause
The Gemini API free tier has strict rate limits:
- **10 requests per minute** per model (`gemini-2.5-flash`)
- The `ContentAnalysisAgent.run()` method processes messages sequentially without any delay between API calls
- When processing multiple emails (e.g., 5-10 messages), the code makes rapid sequential calls that exceed the 10/minute limit
- After the 10th request, all subsequent requests fail with 429 errors until the quota resets

The pipeline continues successfully because:
1. The exception handler catches quota errors gracefully
2. Default `ContentAnalysis` objects are created with `is_placement_related=False` and `confidence=0.0`
3. These default analyses are still saved to the database
4. The HTTP response returns 200 OK because the pipeline completed (with failed analyses)

## Step-by-Step Solution

### Option A: Add Rate Limiting (Recommended)
1. **Add delays between requests** in `agents/content_analysis_agent.py`:
   - Import `time` module at the top
   - Add a 6-second delay between each API call (10 requests/minute = 6 seconds between requests)
   - This prevents hitting the quota limit in the first place

2. **Add retry logic with exponential backoff**:
   - Catch 429/quota errors specifically
   - Extract the retry delay from the error message (e.g., "Please retry in 44s")
   - Retry the request after waiting for the specified delay
   - Implement exponential backoff as a fallback if delay cannot be extracted

3. **Example implementation**:
   ```python
   import time
   import re
   from google.api_core import exceptions as google_exceptions
   
   # In the run() method, before the API call:
   if idx > 0:  # Skip delay for first request
       time.sleep(6.0)  # Rate limiting: 10 requests/minute
   
   # In the exception handler:
   if "429" in str(exc) or "quota" in str(exc).lower():
       retry_delay = extract_retry_delay(str(exc))  # Extract from error message
       if retry_delay:
           time.sleep(retry_delay)
           # Retry the request
   ```

### Option B: Reduce Batch Size
1. **Limit the number of messages processed per request**:
   - Modify endpoints to enforce a lower default `limit` (e.g., 5 instead of 10)
   - Process emails in smaller batches to stay under the quota

2. **Add pagination**:
   - Process emails in chunks of 5-8 messages
   - Wait 1 minute between chunks to allow quota reset

### Option C: Upgrade API Tier
1. **Upgrade to a paid Gemini API plan**:
   - Higher rate limits (e.g., 60 requests/minute or more)
   - Check Google Cloud Console for pricing and quota limits
   - Update API key to use the paid tier

## Prevention Tips
- **Always add rate limiting** when calling external APIs with quota limits
- **Monitor API usage** through Google Cloud Console to track quota consumption
- **Implement retry logic** with exponential backoff for transient errors (429, 503, etc.)
- **Batch processing**: Process emails in smaller batches with delays between batches
- **Cache results**: Consider caching content analyses for duplicate emails to avoid redundant API calls
- **Use async processing**: For production, consider processing emails asynchronously with proper rate limiting

## Validation Steps
1. **Test rate limiting**:
   - Process 10+ emails and verify no 429 errors occur
   - Check logs: requests should be spaced 6+ seconds apart
   - Verify all analyses complete successfully

2. **Test retry logic**:
   - Temporarily reduce delay to trigger quota errors
   - Verify the system retries after the specified delay
   - Confirm analyses eventually succeed after retry

3. **Monitor quota usage**:
   - Check Google Cloud Console usage dashboard
   - Verify requests stay under 10/minute limit
   - Confirm no quota exceeded errors in logs

4. **Verify graceful degradation**:
   - If quota is exceeded, verify default analyses are created
   - Confirm pipeline still completes and saves data
   - Check that HTTP response is 200 OK (not 500)

