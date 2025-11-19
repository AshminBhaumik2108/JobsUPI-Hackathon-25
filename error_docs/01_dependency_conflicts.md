# Problem: LangChain Dependency Conflicts

## Context
When we first ran `pip install -r requirements.txt`, the installation failed. The error mentioned conflicting versions of the LangChain packages (`langchain`, `langchain-core`, and `langchain-community`). Because each of these packages pins versions of the others, mixing releases from different dates often breaks the dependency resolver.

## Error Message
```
ERROR: Cannot install -r requirements.txt (line 3) and langchain-community==0.0.29 because these package versions have conflicting dependencies.
```

## Root Cause
Our `requirements.txt` originally mixed a newer `langchain-core==0.3.39` with an older `langchain-community==0.0.29` (and later with `langchain==0.2.16`). These packages belong to the same suite. When their versions are out of sync, pip refuses to continue because one package requires a different range than what another demands.

## Step-by-Step Solution
1. **Clear the virtual environment (optional but helpful):**
   ```bash
   rm -rf .venv
   ```
2. **Create a fresh Python 3.12 environment (see the Python version note in another doc):**
   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate
   ```
3. **Align LangChain package versions:**
   - Update `requirements.txt` so that `langchain`, `langchain-core`, and `langchain-community` come from the same release family.
   - We settled on:
     ```
     langchain-core==0.3.39
     langchain==0.3.6
     langchain-community==0.3.4
     ```
4. **Reinstall dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
5. **Confirm the versions:**
   ```bash
   pip show langchain langchain-core langchain-community
   ```

If these steps succeed without errors, the conflict is resolved.

## Prevention Tips
- When upgrading any LangChain package, update the entire trio (`langchain`, `langchain-core`, `langchain-community`).
- Consider pinning versions together in the requirements file or using LangChain’s official compatibility table when available.
- Run `pip check` after installations to catch broken dependency trees early.

## Validation Steps
- Run `pip install -r requirements.txt` without errors.
- Start the FastAPI server: `uvicorn api.main:app --reload`.
- Hit `/health` in Postman or browser. A success response indicates that the dependency tree is sane.
