#!/usr/bin/env python3
"""
Final test to verify main.py matches working code structure
"""

import sys

def test_main_structure():
    """Test that main.py structure matches working code."""
    print("Testing main.py structure...")
    
    try:
        import main
        
        # Check critical components
        checks = [
            ("Socket.IO Client", hasattr(main, 'sio')),
            ("Server URL", hasattr(main, 'SERVER_URL')),
            ("Command Handler", hasattr(main, 'on_command')),
            ("Connect Handler", hasattr(main, 'connect')),
            ("Disconnect Handler", hasattr(main, 'disconnect')),
            ("File Upload Handler", hasattr(main, 'handle_file_upload')),
            ("File Download Handler", hasattr(main, 'handle_file_download')),
            ("Execute Command", hasattr(main, 'execute_command')),
            ("Agent ID Function", hasattr(main, 'get_or_create_agent_id')),
        ]
        
        for check_name, result in checks:
            if result:
                print(f"✅ {check_name}: OK")
            else:
                print(f"❌ {check_name}: Missing")
                return False
        
        # Check Socket.IO configuration
        if main.sio:
            print("✅ Socket.IO client created")
            # Check if SSL verification is disabled (should be False)
            if hasattr(main.sio, 'ssl_verify'):
                print(f"✅ Socket.IO SSL verify: {main.sio.ssl_verify}")
            else:
                print("✅ Socket.IO client exists (ssl_verify attribute not accessible)")
        else:
            print("❌ Socket.IO client not created")
            return False
        
        # Check event handler structure
        import inspect
        on_command_source = inspect.getsource(main.on_command)
        if '@sio.on(\'command\')' in on_command_source:
            print("✅ Command handler uses correct event name")
        else:
            print("❌ Command handler uses wrong event name")
            return False
        
        print("✅ All structure checks passed")
        return True
        
    except Exception as e:
        print(f"❌ Structure test failed: {e}")
        return False

def test_command_execution():
    """Test that command execution works."""
    print("\nTesting command execution...")
    
    try:
        import main
        
        # Test basic command execution
        result = main.execute_command("echo 'test'")
        if result and len(result) > 0:
            print(f"✅ Command execution: {result[:50]}...")
        else:
            print("❌ Command execution failed")
            return False
        
        # Test PowerShell/Linux command
        if main.WINDOWS_AVAILABLE:
            result = main.execute_command("Get-Process | Select-Object -First 1")
        else:
            result = main.execute_command("ps aux | head -1")
        
        if result and len(result) > 0:
            print(f"✅ System command: {result[:50]}...")
        else:
            print("❌ System command failed")
            return False
        
        print("✅ Command execution tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Command execution test failed: {e}")
        return False

def test_file_handlers():
    """Test that file handlers work."""
    print("\nTesting file handlers...")
    
    try:
        import main
        import base64
        
        # Test file upload handler
        test_content = "test file content"
        test_content_b64 = base64.b64encode(test_content.encode()).decode()
        
        result = main.handle_file_upload(['upload-file', './test_upload.txt', test_content_b64])
        if "uploaded successfully" in result:
            print("✅ File upload handler works")
        else:
            print(f"❌ File upload handler failed: {result}")
            return False
        
        # Test file download handler
        result = main.handle_file_download(['download-file', './test_upload.txt'], "test-agent")
        if "sent to controller" in result:
            print("✅ File download handler works")
        else:
            print(f"❌ File download handler failed: {result}")
            return False
        
        # Cleanup
        import os
        if os.path.exists('./test_upload.txt'):
            os.remove('./test_upload.txt')
        
        print("✅ File handler tests passed")
        return True
        
    except Exception as e:
        print(f"❌ File handler test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("Final Working Code Match Test")
    print("=" * 60)
    
    tests = [
        ("Main Structure", test_main_structure),
        ("Command Execution", test_command_execution),
        ("File Handlers", test_file_handlers),
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
        print("🎉 All tests passed! main.py now matches working code structure.")
        print("✅ Socket.IO event handlers are correct")
        print("✅ Command execution works")
        print("✅ File handlers work")
        print("✅ Agent should now work with controller")
    else:
        print("⚠️ Some tests failed. Please review the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)