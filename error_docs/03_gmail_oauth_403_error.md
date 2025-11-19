# Problem: Gmail OAuth `403 access_denied`

## Context
When we tried to authorise Gmail access using the `/gmail/auth-url` endpoint and followed the Google consent screen, the browser showed:
```
Error 403: access_denied
Notification System has not completed the Google verification process...
```
This prevented us from obtaining the authorisation code required for `/gmail/authorize`.

## Root Cause
The Google Cloud project associated with our Gmail API credentials was still in **testing** mode and did not list the current Google account as an approved tester. Google blocks OAuth consent for unverified apps unless the user is explicitly added. Additionally, the Gmail API must be enabled inside the Google Cloud console.

## Step-by-Step Solution
1. **Ensure Gmail API is enabled:**
   - Visit <https://console.cloud.google.com/apis/dashboard>.
   - Pick the project that generated `GMAIL_CLIENT_ID` and `GMAIL_CLIENT_SECRET`.
   - Enable “Gmail API” if it is not already active.

2. **Add your Google account as a test user:**
   - Open <https://console.cloud.google.com/apis/credentials/consent>.
   - Verify the consent screen is in “Testing” mode.
   - Add the Gmail address you plan to authorise under “Test users”.

3. **Regenerate or confirm OAuth credentials (if needed):**
   - In the same Credentials page, ensure you created an OAuth client ID of type “Desktop app” or “Web application” with redirect URI `http://localhost` (matching `.env`).

4. **Repeat the OAuth flow:**
   - Call `/gmail/auth-url` again; open the URL in a browser.
   - Sign in using the approved tester account.
   - Copy the `code` parameter from the final redirect (e.g., `http://localhost/?code=...`).
   - Post it to `/gmail/authorize` to store tokens.

5. **Verify success:**
   - `/gmail/authorize` should respond with `Gmail credentials stored successfully`.
   - `/gmail/messages` should return recent messages without errors.

## Prevention Tips
- Keep a checklist in the README explaining how to configure the Google Cloud OAuth consent screen and add test users.
- For production deployment, complete Google’s verification process or restrict usage to internal accounts.
- If credentials stop working, check whether the access token expired and whether refresh tokens are being saved in `logs/gmail_token.json`.

## Validation Steps
- Hit `/gmail/auth-url` and confirm the consent screen loads without the 403 error.
- Complete `/gmail/authorize` and check that a new `logs/gmail_token.json` file appears.
- Call `/gmail/messages?limit=3` and ensure Gmail data is returned.
