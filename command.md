# Experiment 6 – Dropbox Cloud Storage Integration

## Prerequisites

- Python installed.
- VS Code installed.
- Internet connection.
- Valid Dropbox Access Token.
- Project files: `app.py` and `index.html`.

## 1. Open Project Folder

Open the `ex6` folder in VS Code. Select **Terminal → New Terminal** and make sure the terminal is inside the `ex6` folder.

## 2. Check Python Installation

```powershell
python --version
```

If Python is not recognized, try:

```powershell
py --version
```

## 3. Create Virtual Environment (First Time Only)

```powershell
python -m venv .venv
```

## 4. Activate Virtual Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, allow it for the current terminal session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Then activate the environment again.

## 5. Install Required Libraries

```powershell
python -m pip install flask dropbox
```

## 6. Configure Dropbox

Open `app.py` and replace the placeholder:

```python
ACCESS_TOKEN = "paste_your_dropbox_access_token_here"
```

with a valid Dropbox Access Token. Never publish or commit the actual token to GitHub.

## 7. Run Application

```powershell
python app.py
```

## 8. Open HTML Interface

Open this URL in your browser:

<http://127.0.0.1:5000>

## 9. Complete Commands for a New Computer

Run these commands inside the `ex6` project folder. Configure the Dropbox token in `app.py` before starting the app.

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install flask dropbox
python app.py
```

## 10. Daily Execution (After Initial Setup)

```powershell
.\.venv\Scripts\Activate.ps1
python app.py
```

## 11. Testing Procedure

1. Open the HTML interface in your browser.
2. Upload a PDF file and verify that it appears in Dropbox.
3. Upload a TXT file and verify that it appears in Dropbox.
4. Download an uploaded file.
5. Try an unsupported file type and verify that the app rejects it.

## 12. Additional Commands

| Command | Purpose |
| --- | --- |
| `python app.py` | Start the Flask server. |
| `Ctrl + C` | Stop the Flask server. |
| `deactivate` | Exit the virtual environment. |
| `cls` | Clear the terminal. |
| `python -m pip list` | Display installed packages. |

## Important Instructions

- Do not use computer-specific paths in commands.
- Do not modify the working Python or HTML code when setting up on another computer.
- Do not include or share the actual Dropbox Access Token in this file.
- Keep the token-filled `app.py` private; do not publish or commit it.
- Follow these steps from the `ex6` project folder.
