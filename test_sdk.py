#!/usr/bin/env python3
"""
Test Python SDK - Verify it loads without errors
This does NOT make real API calls
"""

import sys
sys.path.insert(0, 'src')

print("=== Python SDK Test ===\n")

try:
    # Test 1: SDK can be imported
    print("1. Testing SDK import... ", end="")
    from touristesim import TouristEsim
    print("✓ PASS")
    
    # Test 2: SDK can be instantiated
    print("2. Testing SDK instantiation... ", end="")
    sdk = TouristEsim('test_client_id', 'test_client_secret')
    print("✓ PASS")
    
    # Test 3: Check SDK structure
    print("3. Testing SDK structure... ", end="")
    if hasattr(sdk, 'config') and hasattr(sdk, 'oauth'):
        print("✓ PASS")
    else:
        print("✗ FAIL: Missing expected attributes")
        sys.exit(1)
    
    # Test 4: Check resource modules exist
    print("4. Testing resource modules... ", end="")
    try:
        from touristesim.resources import Plans, Orders, Esims, Countries, Regions
        print("✓ PASS (5 resource classes)")
    except ImportError as e:
        print(f"✗ FAIL: {e}")
        sys.exit(1)
    
    print("\n=== All Basic Tests Passed ✓ ===")
    print("SDK is ready for PyPI publication!\n")
    
except Exception as e:
    print(f"\n✗ FAIL: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
