#!/usr/bin/env python3
"""
Farm2Market Application Test Script
This script tests the key functionalities of the Farm2Market application.
"""

import requests
import json
import time
import sys

BASE_URL = "http://localhost:8000"

def test_server_status():
    """Test if the server is running"""
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        return response.status_code == 200
    except Exception as e:
        print(f"Server not accessible: {e}")
        return False

def test_api_endpoints():
    """Test various API endpoints"""
    tests = []
    
    # Test AI Chat
    try:
        response = requests.post(f"{BASE_URL}/api/ai-chat", 
                               json={"message": "Hello", "context": {"language": "en"}},
                               timeout=10)
        tests.append(("AI Chat", response.status_code == 200))
    except Exception as e:
        tests.append(("AI Chat", False))
        print(f"AI Chat test failed: {e}")
    
    # Test Crops API
    try:
        response = requests.get(f"{BASE_URL}/api/crops", timeout=5)
        tests.append(("Crops API", response.status_code == 200))
    except Exception as e:
        tests.append(("Crops API", False))
        print(f"Crops API test failed: {e}")
    
    # Test Price Suggestion
    try:
        response = requests.get(f"{BASE_URL}/api/price-suggestion", 
                               params={"crop_name": "tomato", "location": "mumbai"},
                               timeout=10)
        tests.append(("Price Suggestion", response.status_code == 200))
        if response.status_code == 200:
            data = response.json()
            if "suggested_price" in data:
                print(f"Price suggestion for tomato in Mumbai: ₹{data['suggested_price']}")
    except Exception as e:
        tests.append(("Price Suggestion", False))
        print(f"Price suggestion test failed: {e}")
    
    return tests

def test_user_flow():
    """Test basic user flow"""
    tests = []
    
    # Test signup
    try:
        signup_data = {
            "full_name": "Test Buyer",
            "age": 25,
            "email": "test@example.com",
            "phone": "9876543210",
            "location": "Mumbai",
            "role": "buyer"
        }
        response = requests.post(f"{BASE_URL}/signup", data=signup_data, 
                               allow_redirects=False, timeout=5)
        tests.append(("User Signup", response.status_code in [302, 303]))
    except Exception as e:
        tests.append(("User Signup", False))
        print(f"User signup test failed: {e}")
    
    return tests

def main():
    """Run all tests"""
    print("🌾 Farm2Market Application Test Suite")
    print("=" * 50)
    
    # Test server status
    print("1. Testing server status...")
    if not test_server_status():
        print("❌ Server is not running. Please start the server first.")
        print("   Run: python main.py")
        sys.exit(1)
    else:
        print("✅ Server is running")
    
    # Test API endpoints
    print("\n2. Testing API endpoints...")
    api_tests = test_api_endpoints()
    for test_name, result in api_tests:
        status = "✅" if result else "❌"
        print(f"   {status} {test_name}")
    
    # Test user flow
    print("\n3. Testing user flow...")
    user_tests = test_user_flow()
    for test_name, result in user_tests:
        status = "✅" if result else "❌"
        print(f"   {status} {test_name}")
    
    # Summary
    all_tests = api_tests + user_tests
    passed = sum(1 for _, result in all_tests if result)
    total = len(all_tests)
    
    print(f"\n📊 Test Summary: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Farm2Market is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
    
    print("\n🌐 Access the application at: http://localhost:8000")
    print("\n🤖 Features to test manually:")
    print("   • Language switching (English/Hindi/Tamil)")
    print("   • AI Assistant chat")
    print("   • Crop search and filtering")
    print("   • Add to cart functionality")
    print("   • Price suggestions")
    print("   • Farmer and buyer registration")

if __name__ == "__main__":
    main() 