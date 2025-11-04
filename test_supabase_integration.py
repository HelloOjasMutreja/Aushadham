#!/usr/bin/env python3
"""
Test script for Supabase integration
This script tests the Supabase service layer functionality
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_environment_variables():
    """Test if Supabase environment variables are set"""
    print("\n=== Testing Environment Variables ===")
    use_supabase = os.getenv('USE_SUPABASE', 'false').lower() == 'true'
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    print(f"USE_SUPABASE: {use_supabase}")
    print(f"SUPABASE_URL: {'Set' if supabase_url else 'Not Set'}")
    print(f"SUPABASE_KEY: {'Set' if supabase_key else 'Not Set'}")
    
    if use_supabase:
        if not supabase_url or not supabase_key:
            print("❌ Supabase is enabled but credentials are missing!")
            return False
        print("✅ Supabase credentials are configured")
        return True
    else:
        print("ℹ️  Supabase is not enabled (using SQLAlchemy)")
        return False

def test_supabase_connection():
    """Test if we can connect to Supabase"""
    print("\n=== Testing Supabase Connection ===")
    
    try:
        from supabase_service import get_supabase_service
        service = get_supabase_service()
        
        if service:
            print("✅ Supabase service initialized successfully")
            return True
        else:
            print("❌ Failed to initialize Supabase service")
            return False
    except Exception as e:
        print(f"❌ Error initializing Supabase: {e}")
        return False

def test_sqlalchemy_fallback():
    """Test if SQLAlchemy fallback works"""
    print("\n=== Testing SQLAlchemy Fallback ===")
    
    try:
        # Temporarily disable Supabase
        original_use_supabase = os.getenv('USE_SUPABASE')
        os.environ['USE_SUPABASE'] = 'false'
        
        from flask_sqlalchemy import SQLAlchemy
        print("✅ SQLAlchemy is available as fallback")
        
        # Restore original value
        if original_use_supabase:
            os.environ['USE_SUPABASE'] = original_use_supabase
        
        return True
    except Exception as e:
        print(f"❌ Error with SQLAlchemy fallback: {e}")
        return False

def test_schema_file():
    """Test if schema file exists"""
    print("\n=== Testing Schema File ===")
    
    schema_file = 'supabase_schema.sql'
    if os.path.exists(schema_file):
        with open(schema_file, 'r') as f:
            content = f.read()
            tables = ['users', 'saved_questionnaires', 'user_feedback']
            all_found = all(table in content for table in tables)
            
            if all_found:
                print(f"✅ Schema file exists and contains all required tables")
                return True
            else:
                print(f"❌ Schema file is missing some tables")
                return False
    else:
        print(f"❌ Schema file not found: {schema_file}")
        return False

def test_documentation():
    """Test if documentation exists"""
    print("\n=== Testing Documentation ===")
    
    docs = ['SUPABASE_SETUP.md', 'README.md', '.env.example']
    all_exist = True
    
    for doc in docs:
        if os.path.exists(doc):
            print(f"✅ {doc} exists")
        else:
            print(f"❌ {doc} not found")
            all_exist = False
    
    return all_exist

def main():
    """Run all tests"""
    print("=" * 60)
    print("Supabase Integration Test Suite")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Environment Variables", test_environment_variables()))
    results.append(("SQLAlchemy Fallback", test_sqlalchemy_fallback()))
    results.append(("Schema File", test_schema_file()))
    results.append(("Documentation", test_documentation()))
    
    # Try Supabase connection only if credentials are set
    if os.getenv('USE_SUPABASE', 'false').lower() == 'true':
        results.append(("Supabase Connection", test_supabase_connection()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
