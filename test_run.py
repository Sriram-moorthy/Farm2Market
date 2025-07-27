#!/usr/bin/env python3
"""
Simple test to verify Farm2Market can start without errors
"""

import sys
import traceback

def test_imports():
    """Test if all required modules can be imported"""
    try:
        print("Testing imports...")
        
        # Test FastAPI imports
        from fastapi import FastAPI, Request, Form, File, UploadFile, HTTPException, WebSocket, WebSocketDisconnect
        print("✅ FastAPI imports successful")
        
        # Test other imports
        from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
        from fastapi.staticfiles import StaticFiles
        from fastapi.templating import Jinja2Templates
        print("✅ FastAPI components imports successful")
        
        # Test Pydantic
        from pydantic import BaseModel
        print("✅ Pydantic import successful")
        
        # Test Google AI
        import google.generativeai as genai
        print("✅ Google Generative AI import successful")
        
        # Test other dependencies
        import json
        import os
        import uuid
        import shutil
        from datetime import datetime
        import asyncio
        print("✅ Standard library imports successful")
        
        # Test config
        from config import settings
        print("✅ Config import successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        traceback.print_exc()
        return False

def test_app_creation():
    """Test if the FastAPI app can be created"""
    try:
        print("\nTesting app creation...")
        
        # Import the main module
        import main
        print("✅ Main module imported successfully")
        
        # Check if app is created
        if hasattr(main, 'app'):
            print("✅ FastAPI app created successfully")
            return True
        else:
            print("❌ FastAPI app not found")
            return False
            
    except Exception as e:
        print(f"❌ App creation failed: {e}")
        traceback.print_exc()
        return False

def test_static_files():
    """Test if static files exist"""
    try:
        print("\nTesting static files...")
        
        import os
        
        # Check CSS
        if os.path.exists("static/css/main.css"):
            print("✅ CSS file exists")
        else:
            print("❌ CSS file missing")
            return False
            
        # Check JS
        if os.path.exists("static/js/main.js"):
            print("✅ JavaScript file exists")
        else:
            print("❌ JavaScript file missing")
            return False
            
        # Check directories
        if os.path.exists("static/uploads"):
            print("✅ Uploads directory exists")
        else:
            print("❌ Uploads directory missing")
            
        if os.path.exists("templates"):
            print("✅ Templates directory exists")
        else:
            print("❌ Templates directory missing")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Static files check failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🌾 Farm2Market Application Test")
    print("=" * 40)
    
    tests = [
        ("Import Test", test_imports),
        ("App Creation Test", test_app_creation),
        ("Static Files Test", test_static_files)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        if test_func():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application should run correctly.")
        print("\n🚀 To start the application:")
        print("   python main.py")
        print("\n🌐 Then visit: http://localhost:8000")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 