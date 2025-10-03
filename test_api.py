import requests
import json

# Test the API endpoints
BASE_URL = "http://localhost:8000/api"

def test_api():
    print("🏥 Healthcare Management System - API Testing")
    print("=" * 50)
    
    # Test if server is running by checking a simple endpoint
    try:
        response = requests.get(f"{BASE_URL}/users/", timeout=5)
        print(f"✅ Server is running! Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Total users: {len(data.get('results', data))}")
        
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running. Please start the Django server first.")
        print("🚀 Run: python manage.py runserver")
        return False
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_api()