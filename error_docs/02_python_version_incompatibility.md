# Problem: Python Version Incompatibility with `pydantic-core`

## Context
During the initial dependency installation we executed `pip install -r requirements.txt` using the system default Python (3.13 at the time). The installation crashed while building `pydantic-core`, which is a compiled dependency used by Pydantic 2.

## Error Message
```
ERROR: Failed building wheel for pydantic-core
```
Pip would then roll back and abort the installation.

## Root Cause
`pydantic-core` did not yet provide pre-built wheels for Python 3.13 when we set up the project. Building from source requires Rust and additional configuration. Because we only need a stable, supported Python version, forcing the project to use Python 3.12 solves the issue instantly.

## Step-by-Step Solution
1. **Deactivate and remove the old virtual environment (if it exists):**
   ```bash
   deactivate  # only if your shell prompt shows (.venv)
   rm -rf .venv
   ```
2. **Install Python 3.12 if it is missing:**
   - With Homebrew: `brew install python@3.12`
   - Or with pyenv:
     ```bash
     pyenv install 3.12.2
     pyenv local 3.12.2
     ```
3. **Create a fresh virtual environment pinned to Python 3.12:**
   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate
   ```
4. **Reinstall the requirements:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
5. **Verify the Python version inside the venv:**
   ```bash
   python --version
   # Expected output: Python 3.12.x
   ```

## Prevention Tips
- Always check the project’s supported Python version (documented in `README.md`).
- Avoid mixing system Python with project Python; pin the version in the documentation and enforce it via tooling (e.g., pyenv, `.python-version`).
- For team members, share an installation script or note in README to prevent surpise upgrades.

## Validation Steps
- Run `python --version` inside `.venv` and confirm it shows 3.12.
- Run `pip install -r requirements.txt` with no compilation errors.
- Launch the server (`uvicorn api.main:app --reload`) and confirm `/health` returns success.
