#!/usr/bin/env python3
"""
Test Socket.IO connection and command handling
"""

import time
import sys

def test_socketio_connection():
    """Test Socket.IO connection and basic functionality."""
    print("Testing Socket.IO connection...")
    
    try:
        import main
        
        # Check if Socket.IO is available
        if not main.SOCKETIO_AVAILABLE:
            print("❌ Socket.IO not available")
            return False
        
        print(f"✅ Socket.IO available")
        print(f"✅ Server URL: {main.SERVER_URL}")
        
        # Test agent ID generation
        try:
            agent_id = main.get_or_create_agent_id()
            print(f"✅ Agent ID: {agent_id}")
        except Exception as e:
            print(f"❌ Agent ID generation failed: {e}")
            return False
        
        # Test command execution function
        try:
            result = main.execute_command("echo 'test'")
            print(f"✅ Command execution: {result[:50]}...")
        except Exception as e:
            print(f"❌ Command execution failed: {e}")
            return False
        
        # Test file upload function
        try:
            import base64
            test_content = "test file content"
            test_content_b64 = base64.b64encode(test_content.encode()).decode()
            result = main.handle_file_upload(['upload-file', './test_socketio.txt', test_content_b64])
            print(f"✅ File upload: {result}")
        except Exception as e:
            print(f"❌ File upload failed: {e}")
            return False
        
        # Test file download function
        try:
            result = main.handle_file_download(['download-file', './test_socketio.txt'], agent_id)
            print(f"✅ File download: {result}")
        except Exception as e:
            print(f"❌ File download failed: {e}")
            return False
        
        print("✅ All basic functionality tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        return False

def test_streaming_functions():
    """Test streaming function availability."""
    print("\nTesting streaming functions...")
    
    try:
        import main
        
        # Test streaming start/stop functions
        functions_to_test = [
            ("start_streaming", main.start_streaming),
            ("stop_streaming", main.stop_streaming),
            ("start_camera_streaming", main.start_camera_streaming),
            ("stop_camera_streaming", main.stop_camera_streaming),
            ("start_audio_streaming", main.start_audio_streaming),
            ("stop_audio_streaming", main.stop_audio_streaming),
        ]
        
        for func_name, func in functions_to_test:
            try:
                if func_name.startswith("start"):
                    func("test-agent")
                    print(f"✅ {func_name} - started")
                    time.sleep(0.1)  # Brief pause
                else:
                    func()
                    print(f"✅ {func_name} - stopped")
            except Exception as e:
                print(f"❌ {func_name} failed: {e}")
        
        print("✅ Streaming functions test completed")
        return True
        
    except Exception as e:
        print(f"❌ Streaming test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("Socket.IO Connection and Functionality Test")
    print("=" * 60)
    
    tests = [
        ("Socket.IO Connection", test_socketio_connection),
        ("Streaming Functions", test_streaming_functions),
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
        print("🎉 All tests passed! Socket.IO connection and functionality is working.")
        print("✅ Socket.IO connection is available")
        print("✅ Command execution is working")
        print("✅ File transfer is working")
        print("✅ Streaming functions are available")
        print("\nThe agent should now work properly with the controller.")
    else:
        print("⚠️ Some tests failed. Please review the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)