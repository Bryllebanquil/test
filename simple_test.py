#!/usr/bin/env python3
"""
Simple test script to demonstrate the PowerShell download fix.
This script shows the improved PowerShell command structure.
"""

import subprocess
import os
import sys

def test_improved_powershell_download():
    """Test the improved PowerShell download command."""
    url = "https://raw.githubusercontent.com/Bryllebanquil/test/main/main.py"
    destination = "C:/c.py"
    
    print("=" * 60)
    print("Testing Improved PowerShell Download")
    print("=" * 60)
    print(f"URL: {url}")
    print(f"Destination: {destination}")
    print()
    
    # Improved PowerShell command with better error handling
    improved_command = f'''
try {{
    $ProgressPreference = 'SilentlyContinue'
    Invoke-WebRequest -Uri "{url}" -OutFile "{destination}" -UseBasicParsing
    Write-Host "Download completed successfully to: {destination}"
}} catch {{
    Write-Host "Download failed: $($_.Exception.Message)"
    exit 1
}}
'''
    
    print("Improved PowerShell command:")
    print(improved_command)
    print()
    
    try:
        result = subprocess.run(
            ["powershell.exe", "-NoProfile", "-Command", improved_command],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        print(f"Return code: {result.returncode}")
        print(f"Stdout: {result.stdout}")
        print(f"Stderr: {result.stderr}")
        
        if result.returncode == 0:
            if os.path.exists(destination):
                file_size = os.path.getsize(destination)
                print(f"✓ Download successful! File size: {file_size} bytes")
                print(f"✓ File location: {os.path.abspath(destination)}")
                return True
            else:
                print("✗ Download appeared to succeed but file not found")
                return False
        else:
            print("✗ Download failed")
            return False
            
    except Exception as e:
        print(f"✗ Error executing command: {e}")
        return False

def test_original_command():
    """Test the original failing command."""
    print("\n" + "=" * 60)
    print("Testing Original Command")
    print("=" * 60)
    
    original_command = 'Invoke-WebRequest "https://raw.githubusercontent.com/Bryllebanquil/test/main/main.py" -OutFile "C:/c.py"'
    
    print(f"Original command: {original_command}")
    print()
    
    try:
        result = subprocess.run(
            ["powershell.exe", "-NoProfile", "-Command", original_command],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        print(f"Return code: {result.returncode}")
        print(f"Stdout: {result.stdout}")
        print(f"Stderr: {result.stderr}")
        
        if result.returncode == 0:
            if os.path.exists("C:/c.py"):
                file_size = os.path.getsize("C:/c.py")
                print(f"✓ Original command worked! File size: {file_size} bytes")
                return True
            else:
                print("✗ Original command appeared to succeed but file not found")
                return False
        else:
            print("✗ Original command failed")
            return False
            
    except Exception as e:
        print(f"✗ Error executing original command: {e}")
        return False

def show_fix_explanation():
    """Show explanation of the fix."""
    print("\n" + "=" * 60)
    print("FIX EXPLANATION")
    print("=" * 60)
    print("The original PowerShell command was failing because:")
    print("1. No error handling - if the URL doesn't exist or network fails, it just hangs")
    print("2. No progress preference setting - can cause issues with some PowerShell versions")
    print("3. No UseBasicParsing flag - can cause issues in some environments")
    print()
    print("The improved command includes:")
    print("1. Try-catch error handling")
    print("2. ProgressPreference = 'SilentlyContinue'")
    print("3. UseBasicParsing flag")
    print("4. Proper error messages and exit codes")
    print()
    print("Additionally, the main.py file now includes:")
    print("1. Multiple download methods (Python requests + PowerShell)")
    print("2. Better error handling and reporting")
    print("3. File existence verification")
    print("4. New commands: test-powershell-download and download-url:url:path")

if __name__ == "__main__":
    print("PowerShell Download Fix Test")
    print("This script demonstrates the fix for the failing PowerShell download command.")
    print()
    
    # Check if we're on Windows
    if os.name != 'nt':
        print("This test is designed for Windows systems.")
        print("The PowerShell commands won't work on Linux/Mac.")
        sys.exit(1)
    
    # Test the original command
    original_success = test_original_command()
    
    # Test the improved command
    improved_success = test_improved_powershell_download()
    
    # Show explanation
    show_fix_explanation()
    
    print("\n" + "=" * 60)
    print("TEST RESULTS")
    print("=" * 60)
    print(f"Original command: {'✓ PASSED' if original_success else '✗ FAILED'}")
    print(f"Improved command: {'✓ PASSED' if improved_success else '✗ FAILED'}")
    
    if improved_success:
        print("\n✓ The fix is working!")
        print("You can now use the improved download functionality in your agent.")
    else:
        print("\n✗ The fix needs further investigation.")
        print("Check the error messages above for details.")