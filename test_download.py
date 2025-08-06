#!/usr/bin/env python3
"""
Test script to demonstrate the download functionality fix.
This script shows how to properly download files from URLs using multiple methods.
"""

import requests
import subprocess
import os
import sys

def download_file_from_url(url, destination_path):
    """Download a file from a URL to a local path using Python requests."""
    try:
        print(f"Downloading file from: {url}")
        print(f"Destination: {destination_path}")
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        
        # Download the file
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Write the file
        with open(destination_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        print(f"File downloaded successfully to: {destination_path}")
        return f"File downloaded successfully to: {destination_path}"
        
    except requests.exceptions.RequestException as e:
        error_msg = f"Failed to download file: {e}"
        print(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"Error downloading file: {e}"
        print(error_msg)
        return error_msg

def execute_powershell_download(url, destination_path):
    """Execute PowerShell download command with better error handling."""
    try:
        # Use PowerShell with better error handling
        powershell_cmd = f'''
try {{
    $ProgressPreference = 'SilentlyContinue'
    Invoke-WebRequest -Uri "{url}" -OutFile "{destination_path}" -UseBasicParsing
    Write-Host "Download completed successfully to: {destination_path}"
}} catch {{
    Write-Host "Download failed: $($_.Exception.Message)"
    exit 1
}}
'''
        
        result = subprocess.run(
            ["powershell.exe", "-NoProfile", "-Command", powershell_cmd],
            capture_output=True,
            text=True,
            timeout=60,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        
        if result.returncode == 0:
            return f"PowerShell download successful: {result.stdout.strip()}"
        else:
            return f"PowerShell download failed: {result.stderr.strip()}"
            
    except Exception as e:
        return f"Download execution failed: {e}"

def test_download_functionality():
    """Test the download functionality with the specific URL mentioned."""
    url = "https://raw.githubusercontent.com/Bryllebanquil/test/main/main.py"
    destination = "C:/c.py"
    
    print("=" * 60)
    print("Testing Download Functionality Fix")
    print("=" * 60)
    print(f"URL: {url}")
    print(f"Destination: {destination}")
    print()
    
    # Try multiple download methods
    methods = [
        ("Python requests", lambda: download_file_from_url(url, destination)),
        ("PowerShell", lambda: execute_powershell_download(url, destination))
    ]
    
    for method_name, method_func in methods:
        try:
            print(f"Trying {method_name} method...")
            result = method_func()
            print(f"Result: {result}")
            
            if "successful" in result.lower() or "completed" in result.lower():
                # Check if file was actually created
                if os.path.exists(destination):
                    file_size = os.path.getsize(destination)
                    print(f"✓ File successfully downloaded! Size: {file_size} bytes")
                    print(f"✓ File location: {os.path.abspath(destination)}")
                    return True
                else:
                    print(f"✗ File not found at destination: {destination}")
            else:
                print(f"✗ {method_name} failed: {result}")
                
        except Exception as e:
            print(f"✗ {method_name} error: {e}")
            continue
    
    print("✗ All download methods failed")
    return False

def test_original_powershell_command():
    """Test the original PowerShell command that was failing."""
    print("\n" + "=" * 60)
    print("Testing Original PowerShell Command")
    print("=" * 60)
    
    original_command = 'Invoke-WebRequest "https://raw.githubusercontent.com/Bryllebanquil/test/main/main.py" -OutFile "C:/c.py"'
    
    print(f"Original command: {original_command}")
    print()
    
    try:
        result = subprocess.run(
            ["powershell.exe", "-NoProfile", "-Command", original_command],
            capture_output=True,
            text=True,
            timeout=30,
            creationflags=subprocess.CREATE_NO_WINDOW
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

if __name__ == "__main__":
    print("Download Functionality Test Script")
    print("This script tests the fix for the PowerShell download issue.")
    print()
    
    # Test the original failing command
    original_success = test_original_powershell_command()
    
    # Test the improved download functionality
    improved_success = test_download_functionality()
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    print(f"Original PowerShell command: {'✓ PASSED' if original_success else '✗ FAILED'}")
    print(f"Improved download methods: {'✓ PASSED' if improved_success else '✗ FAILED'}")
    
    if improved_success:
        print("\n✓ The download functionality fix is working!")
        print("You can now use the following commands in your agent:")
        print("  - test-powershell-download")
        print("  - download-url:https://example.com/file.txt:C:/destination.txt")
    else:
        print("\n✗ The download functionality still needs work.")
        print("Check the error messages above for details.")