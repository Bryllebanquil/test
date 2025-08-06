#!/usr/bin/env python3
"""
PowerShell Download Fix Demonstration

This script demonstrates the fix for the PowerShell download issue mentioned by the user.
The original command was failing:
    Invoke-WebRequest "https://raw.githubusercontent.com/Bryllebanquil/test/main/main.py" -OutFile "C:/c.py"

This script shows the improved version that actually works.
"""

import subprocess
import os
import sys

def test_original_powershell_command():
    """Test the original failing PowerShell command."""
    print("=" * 60)
    print("TESTING ORIGINAL FAILING COMMAND")
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

def test_improved_powershell_command():
    """Test the improved PowerShell command with error handling."""
    print("\n" + "=" * 60)
    print("TESTING IMPROVED COMMAND")
    print("=" * 60)
    
    improved_command = '''
try {
    $ProgressPreference = 'SilentlyContinue'
    Invoke-WebRequest -Uri "https://raw.githubusercontent.com/Bryllebanquil/test/main/main.py" -OutFile "C:/c.py" -UseBasicParsing
    Write-Host "Download completed successfully to: C:/c.py"
} catch {
    Write-Host "Download failed: $($_.Exception.Message)"
    exit 1
}
'''
    
    print("Improved command:")
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
            if os.path.exists("C:/c.py"):
                file_size = os.path.getsize("C:/c.py")
                print(f"✓ Improved command worked! File size: {file_size} bytes")
                return True
            else:
                print("✗ Improved command appeared to succeed but file not found")
                return False
        else:
            print("✗ Improved command failed")
            return False
            
    except Exception as e:
        print(f"✗ Error executing improved command: {e}")
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
    print("4. No verification that the download actually succeeded")
    print()
    print("The improved command includes:")
    print("1. Try-catch error handling")
    print("2. ProgressPreference = 'SilentlyContinue'")
    print("3. UseBasicParsing flag")
    print("4. Proper error messages and exit codes")
    print("5. File existence verification")
    print()
    print("In the main.py file, you can now use:")
    print("1. test-specific-download - Tests the exact URL mentioned")
    print("2. download-url:url:destination - Downloads any file from URL")
    print("3. test-powershell-download - Tests general download functionality")

def main():
    print("PowerShell Download Fix Demonstration")
    print("This script demonstrates the fix for the failing PowerShell download command.")
    print()
    
    # Check if we're on Windows
    if os.name != 'nt':
        print("This test is designed for Windows systems.")
        print("The PowerShell commands won't work on Linux/Mac.")
        sys.exit(1)
    
    # Test the original command
    original_success = test_original_powershell_command()
    
    # Test the improved command
    improved_success = test_improved_powershell_command()
    
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
        print("\nCommands available in main.py:")
        print("  - test-specific-download")
        print("  - download-url:https://example.com/file.txt:C:/destination.txt")
    else:
        print("\n✗ The fix needs further investigation.")
        print("Check the error messages above for details.")

if __name__ == "__main__":
    main()