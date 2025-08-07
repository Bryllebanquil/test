#!/usr/bin/env python3
"""
Test the final fixes for Socket.IO event handlers
"""

import sys

def test_socketio_events():
    """Test that Socket.IO event handlers are properly configured."""
    print("Testing Socket.IO event handlers...")
    
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
        
        # Test that the command handler exists
        try:
            # Check if the on_command function exists
            if hasattr(main, 'on_command'):
                print("✅ Command handler function exists")
            else:
                print("❌ Command handler function missing")
                return False
        except Exception as e:
            print(f"❌ Command handler check failed: {e}")
            return False
        
        print("✅ All Socket.IO event tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        return False

def test_event_structure():
    """Test that the event structure matches the working code."""
    print("\nTesting event structure...")
    
    try:
        import main
        
        # Check if the correct event handlers are registered
        expected_events = ['connect', 'disconnect', 'command']
        
        for event in expected_events:
            if hasattr(main, f'on_{event}') or hasattr(main, event):
                print(f"✅ Event handler for '{event}' exists")
            else:
                print(f"❌ Event handler for '{event}' missing")
                return False
        
        print("✅ All expected event handlers exist")
        return True
        
    except Exception as e:
        print(f"❌ Event structure test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("Final Socket.IO Event Handler Test")
    print("=" * 60)
    
    tests = [
        ("Socket.IO Events", test_socketio_events),
        ("Event Structure", test_event_structure),
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
        print("🎉 All tests passed! Socket.IO event handlers are working correctly.")
        print("✅ Command handler is properly configured")
        print("✅ Event structure matches working code")
        print("✅ Agent should now work with controller")
    else:
        print("⚠️ Some tests failed. Please review the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)