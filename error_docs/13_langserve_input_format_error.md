# Problem: LangServe Input Format Error (422 Unprocessable Entity)

## Context
When testing the LangServe endpoint `/serve/graph/invoke` via Postman, the request returned a 422 Unprocessable Entity error. However, the same endpoint worked correctly when tested through the LangServe Playground UI. This indicated a format mismatch between what was being sent and what LangServe expected.

## Error Message

**HTTP Status:** `422 Unprocessable Entity`

**Error Response:**
```json
{
    "detail": [
        {
            "type": "missing",
            "loc": [
                "input"
            ],
            "msg": "Field required",
            "input": {
                "messages": [...]
            },
            "url": "https://errors.pydantic.dev/2.7/v/missing"
        }
    ]
}
```

**Key Error Details:**
- `"type": "missing"` - A required field is missing
- `"loc": ["input"]` - The missing field is `input`
- `"msg": "Field required"` - The `input` field is required but not provided
- The error shows that `messages` was sent, but it wasn't wrapped in an `input` field

## Root Cause

**LangServe's Input Format Requirement:**

LangServe expects all graph inputs to be wrapped in an `input` field. This is different from:
1. **FastAPI endpoints** - Which accept data directly (e.g., `{"messages": [...]}`)
2. **LangServe endpoints** - Which require the state wrapped in `input` (e.g., `{"input": {"messages": [...]}}`)

**Why Playground Works but Postman Doesn't:**

- The **Playground UI** automatically handles the `input` wrapper - it accepts simplified input and wraps it correctly
- **Direct API calls** (Postman, curl) require you to provide the full format including the `input` wrapper

**State Schema Understanding:**

The graph uses a `NotificationState` which includes:
- `messages` - List of email messages (required)
- `sender_result` - Filter results (can be empty object)
- `analyses` - Content analysis results (can be empty array)
- `decisions` - Priority decisions (can be empty array)
- `notifications` - Generated notifications (can be empty array)
- `delivery` - Delivery information (can be empty object)

LangServe requires the **entire state structure** in the `input` field, even if most fields are empty.

## Step-by-Step Solution

### Step 1: Understand the Correct Format

LangServe expects:
```json
{
  "input": {
    "messages": [...],
    "sender_result": {},
    "analyses": [],
    "decisions": [],
    "notifications": [],
    "delivery": {}
  }
}
```

**Not:**
```json
{
  "messages": [...]
}
```

### Step 2: Check Swagger UI Schema

1. Open Swagger UI: `http://localhost:8000/docs/`
2. Find `/serve/graph/invoke` endpoint
3. Click "Try it out"
4. Review the request body schema shown
5. The schema will show the exact format required

### Step 3: Use the Correct Postman Format

**Request:**
```
POST http://localhost:8000/serve/graph/invoke
```

**Headers:**
- Key: `Content-Type`
- Value: `application/json`

**Body (JSON) - Complete Format:**
```json
{
  "input": {
    "messages": [
      {
        "id": "19a5db62d9a262e6",
        "sender": "Division of Career Services <placement@lpu.co.in>",
        "subject": "Registration process of TCS IN.8266.2026.54524.",
        "snippet": "Dear Student, You are required to register in the below mentioned link for the further process of TCS IN.8266.2026.54524.",
        "body": "Registration process of TCS IN.8266.2026.54524.\n\nDear Student,\n\nYou are required to register in the below mentioned link for the further process of TCS IN.8266.2026.54524.\n\nCompetition Type: Catch the Flag (CTF)\n\nRegistration Start Date: 16th September 2025\n\nLast date to register: 18th November 2025",
        "received_at": "Fri, 07 Nov 2025 09:46:51 +0000 (UTC)"
      }
    ],
    "sender_result": {},
    "analyses": [],
    "decisions": [],
    "notifications": [],
    "delivery": {}
  }
}
```

**Body (JSON) - Minimal Format (also works):**
```json
{
  "input": {
    "messages": [
      {
        "id": "19a5db62d9a262e6",
        "sender": "Division of Career Services <placement@lpu.co.in>",
        "subject": "Test Subject",
        "snippet": "Test snippet",
        "body": "Test body",
        "received_at": "Fri, 07 Nov 2025 09:46:51 +0000 (UTC)"
      }
    ],
    "sender_result": {},
    "analyses": [],
    "decisions": [],
    "notifications": [],
    "delivery": {}
  }
}
```

### Step 4: Optional Fields

The `config` and `kwargs` fields are optional and can be omitted:

```json
{
  "input": {...},
  "config": {},    // Optional
  "kwargs": {}     // Optional
}
```

You can send just:
```json
{
  "input": {...}
}
```

## Understanding the Input Schema

### Required Fields in `input`

| Field | Type | Required | Default Value |
|-------|------|----------|---------------|
| `messages` | `List[EmailMessage]` | ✅ Yes | Must provide |
| `sender_result` | `Dict` | ✅ Yes | `{}` (empty object) |
| `analyses` | `List` | ✅ Yes | `[]` (empty array) |
| `decisions` | `List` | ✅ Yes | `[]` (empty array) |
| `notifications` | `List` | ✅ Yes | `[]` (empty array) |
| `delivery` | `Dict` | ✅ Yes | `{}` (empty object) |

### EmailMessage Structure

Each message in the `messages` array must have:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string` | ✅ Yes | Unique message ID |
| `sender` | `string` | ✅ Yes | Sender email address |
| `subject` | `string` | ✅ Yes | Email subject |
| `snippet` | `string` | ✅ Yes | Email preview text |
| `body` | `string` | ⚠️ Optional | Full email body (can be `null`) |
| `received_at` | `string` | ⚠️ Optional | Timestamp (can be `null`) |

## How to Verify the Fix

### Method 1: Test in Postman

1. Use the correct format with `input` wrapper
2. Send the request
3. Should receive `200 OK` with response in `output` field
4. Response structure:
   ```json
   {
     "output": {
       "matched_messages": [...],
       "skipped_messages": [],
       "analyses": [...],
       "decisions": [...],
       "notifications": [...],
       "delivery": {...},
       "matched_count": 1,
       "skipped_count": 0
     }
   }
   ```

### Method 2: Compare with Playground

1. Open Playground: `http://localhost:8000/serve/graph/playground/`
2. Enter your test data
3. Open browser DevTools → Network tab
4. Click "Invoke" in Playground
5. Check the actual request payload sent
6. Compare with your Postman request

### Method 3: Use Swagger UI

1. Open Swagger UI: `http://localhost:8000/docs/`
2. Find `/serve/graph/invoke`
3. Click "Try it out"
4. Use the example format provided
5. Modify with your data
6. Execute and verify it works
7. Copy the exact format to Postman

## Prevention Tips

### 1. Always Check Swagger UI First

Before writing Postman requests:
- Open Swagger UI at `/docs/`
- Find your endpoint
- Review the request schema
- Use "Try it out" to test
- Copy the working format

### 2. Understand LangServe Format

Remember:
- **LangServe** = Requires `input` wrapper
- **FastAPI** = Direct format, no wrapper
- **Playground** = Handles wrapper automatically

### 3. Use Playground to Learn Format

- Test in Playground first
- Check browser DevTools to see actual request
- Copy the format to Postman

### 4. Validate JSON Structure

- Ensure all required fields in `input` are present
- Use empty objects `{}` for dict fields
- Use empty arrays `[]` for list fields
- Verify JSON syntax (no trailing commas)

### 5. Compare Endpoints

Keep in mind the format differences:

**FastAPI Endpoint (`/agents/graph-preview`):**
```json
// Query parameters or direct JSON
GET /agents/graph-preview?limit=4
```

**LangServe Endpoint (`/serve/graph/invoke`):**
```json
POST /serve/graph/invoke
{
  "input": {
    "messages": [...],
    // ... other state fields
  }
}
```

## Additional Notes

### Why This Format Exists

LangServe uses a standardized format for all LangChain/LangGraph workflows:
- **Consistency** - Same format across all LangServe endpoints
- **State Management** - Preserves full graph state structure
- **Ecosystem Compatibility** - Works with LangSmith, LangChain tools
- **Type Safety** - Validates against the graph's state schema

### Difference from FastAPI Endpoints

| Aspect | FastAPI Endpoint | LangServe Endpoint |
|--------|------------------|-------------------|
| **Format** | Direct data | Wrapped in `input` |
| **State** | Partial (only messages) | Full state structure |
| **Response** | Custom wrapper | `output` wrapper |
| **Use Case** | Quick testing | Ecosystem integration |

### Getting Sample Data

To get real email data for testing:

1. Call `/gmail/messages?limit=2` first
2. Copy the `data` array from response
3. Wrap it in the LangServe format:
   ```json
   {
     "input": {
       "messages": [/* paste data array here */],
       "sender_result": {},
       "analyses": [],
       "decisions": [],
       "notifications": [],
       "delivery": {}
     }
   }
   ```

## Troubleshooting

### Still Getting 422?

1. **Check the `input` wrapper** - Must be present
2. **Verify all required fields** - `sender_result`, `analyses`, etc. must be included
3. **Check JSON syntax** - No trailing commas, valid JSON
4. **Compare with Swagger UI** - Use the exact format from Swagger
5. **Test in Playground** - If Playground works, check what format it uses

### Getting Different Errors?

- **404 Not Found** - Check URL, ensure server is running
- **500 Internal Server Error** - Check server logs for graph execution errors
- **401 Unauthorized** - Check Gmail credentials (if using Gmail endpoints)

### Format Confusion?

Remember the key difference:
- **Wrong**: `{"messages": [...]}`
- **Correct**: `{"input": {"messages": [...]}}`

The `input` field is the wrapper that LangServe requires.

## Validation Steps

After applying the fix:

1. ✅ **Postman request succeeds** - Returns 200 OK
2. ✅ **Response has `output` field** - Contains graph results
3. ✅ **All pipeline results present** - matched_messages, analyses, etc.
4. ✅ **Format matches Swagger UI** - Same structure as Swagger example
5. ✅ **Playground format matches** - Consistent with Playground behavior

## Related Documentation

- `dev_docs/swagger_ui_langserve_guide.md` - How to use Swagger UI and Playground
- `dev_docs/api_endpoints_guide.md` - Complete API endpoint documentation
- `error_docs/12_langserve_pydantic_conflict.md` - LangServe installation issues

