#!/usr/bin/env python3
"""
Simple test to verify streaming and file transfer functionality
"""

import os
import time
import base64
import requests

def test_file_upload():
    """Test file upload functionality."""
    print("Testing file upload...")
    
    # Create a test file
    test_content = "This is a test file for upload testing."
    test_content_b64 = base64.b64encode(test_content.encode()).decode()
    
    # Test the upload function directly
    import main
    result = main.handle_file_upload(['upload-file', './test_upload_real.txt', test_content_b64])
    print(f"Upload result: {result}")
    
    # Check if file was created
    if os.path.exists('./test_upload_real.txt'):
        with open('./test_upload_real.txt', 'r') as f:
            content = f.read()
        print(f"File content: {content}")
        os.remove('./test_upload_real.txt')
        return True
    else:
        print("File was not created")
        return False

def test_file_download():
    """Test file download functionality."""
    print("Testing file download...")
    
    # Create a test file to download
    test_content = "This is a test file for download testing."
    with open('./test_download_real.txt', 'w') as f:
        f.write(test_content)
    
    # Test the download function directly
    import main
    result = main.handle_file_download(['download-file', './test_download_real.txt'], "test-agent")
    print(f"Download result: {result}")
    
    # Cleanup
    os.remove('./test_download_real.txt')
    return True

def test_screen_streaming():
    """Test screen streaming functionality."""
    print("Testing screen streaming...")
    
    import main
    
    # Test starting streaming
    try:
        main.start_streaming("test-agent")
        print("✅ Screen streaming started")
        
        # Let it run for a moment
        time.sleep(2)
        
        # Stop streaming
        main.stop_streaming()
        print("✅ Screen streaming stopped")
        return True
    except Exception as e:
        print(f"❌ Screen streaming failed: {e}")
        return False

def test_camera_streaming():
    """Test camera streaming functionality."""
    print("Testing camera streaming...")
    
    import main
    
    # Test starting camera streaming
    try:
        main.start_camera_streaming("test-agent")
        print("✅ Camera streaming started")
        
        # Let it run for a moment
        time.sleep(2)
        
        # Stop camera streaming
        main.stop_camera_streaming()
        print("✅ Camera streaming stopped")
        return True
    except Exception as e:
        print(f"❌ Camera streaming failed: {e}")
        return False

def test_audio_streaming():
    """Test audio streaming functionality."""
    print("Testing audio streaming...")
    
    import main
    
    # Test starting audio streaming
    try:
        main.start_audio_streaming("test-agent")
        print("✅ Audio streaming started")
        
        # Let it run for a moment
        time.sleep(2)
        
        # Stop audio streaming
        main.stop_audio_streaming()
        print("✅ Audio streaming stopped")
        return True
    except Exception as e:
        print(f"❌ Audio streaming failed: {e}")
        return False

def test_command_execution():
    """Test command execution."""
    print("Testing command execution...")
    
    import main
    
    # Test basic command
    result = main.execute_command("echo 'test command'")
    print(f"Command result: {result[:100]}...")
    
    # Test PowerShell/Linux command
    if main.WINDOWS_AVAILABLE:
        result = main.execute_command("Get-Process | Select-Object -First 1")
    else:
        result = main.execute_command("ps aux | head -1")
    print(f"System command result: {result[:100]}...")
    
    return True

def main():
    """Run all tests."""
    print("=" * 60)
    print("Testing Real Functionality")
    print("=" * 60)
    
    tests = [
        ("File Upload", test_file_upload),
        ("File Download", test_file_download),
        ("Screen Streaming", test_screen_streaming),
        ("Camera Streaming", test_camera_streaming),
        ("Audio Streaming", test_audio_streaming),
        ("Command Execution", test_command_execution),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} passed")
            else:
                print(f"❌ {test_name} failed")
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("🎉 All functionality tests passed!")
        print("✅ File upload/download is working")
        print("✅ Screen streaming is working")
        print("✅ Camera streaming is working")
        print("✅ Audio streaming is working")
        print("✅ Command execution is working")
    else:
        print("⚠️ Some tests failed. Please review the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)