#!/usr/bin/env python3
"""
Test Blood Bank Functionality
Tests the blood bank API endpoint directly
"""
import requests
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_blood_bank_api():
    """Test blood bank API endpoint"""
    base_url = "http://localhost:5000"
    
    logger.info("🧪 Testing Blood Bank API")
    logger.info("=" * 40)
    
    # Test data
    test_data = {
        "user_id": "test_user_123",
        "blood_type": "O+",
        "request_type": "urgent_blood_request",
        "urgency_level": "high",
        "city": "Delhi",
        "state": "Delhi",
        "contact_number": "+91-9876543210",
        "additional_info": "Emergency surgery"
    }
    
    try:
        logger.info("Sending blood bank request...")
        response = requests.post(
            f"{base_url}/api/blood-bank/request",
            json=test_data,
            timeout=10
        )
        
        logger.info(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            logger.info("✅ Blood bank API test passed!")
            logger.info(f"Blood type: {data.get('blood_type', 'N/A')}")
            logger.info(f"City: {data.get('city', 'N/A')}")
            
            availability = data.get('availability', {})
            logger.info(f"Total units available: {availability.get('total_units_available', 0)}")
            
            donors = data.get('compatible_donors', [])
            logger.info(f"Compatible donors found: {len(donors)}")
            
            if donors:
                logger.info("Sample donor:")
                donor = donors[0]
                logger.info(f"  Name: {donor.get('name', 'N/A')}")
                logger.info(f"  Blood Type: {donor.get('blood_type', 'N/A')}")
                logger.info(f"  Distance: {donor.get('distance_km', 'N/A')} km")
            
            return True
        else:
            logger.error(f"❌ Blood bank API test failed: {response.status_code}")
            logger.error(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        logger.error("❌ Cannot connect to server. Is it running?")
        logger.info("Start the server with: python simple_start.py")
        return False
    except Exception as e:
        logger.error(f"❌ Blood bank API test error: {e}")
        return False

def test_nearby_hospitals():
    """Test nearby hospitals endpoint"""
    base_url = "http://localhost:5000"
    
    logger.info("\n🏥 Testing Nearby Hospitals API")
    logger.info("=" * 40)
    
    try:
        params = {
            "lat": 28.7041,  # Delhi coordinates
            "lon": 77.1025,
            "radius": 50
        }
        
        response = requests.get(
            f"{base_url}/api/blood-bank/hospitals",
            params=params,
            timeout=10
        )
        
        logger.info(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            hospitals = data.get('hospitals', [])
            logger.info(f"✅ Nearby hospitals test passed!")
            logger.info(f"Hospitals found: {len(hospitals)}")
            
            if hospitals:
                hospital = hospitals[0]
                logger.info("Sample hospital:")
                logger.info(f"  Name: {hospital.get('name', 'N/A')}")
                logger.info(f"  City: {hospital.get('city', 'N/A')}")
                logger.info(f"  Distance: {hospital.get('distance_km', 'N/A')} km")
            
            return True
        else:
            logger.error(f"❌ Nearby hospitals test failed: {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Nearby hospitals test error: {e}")
        return False

def main():
    """Main test function"""
    logger.info("🩸 Blood Bank Functionality Test")
    logger.info("=" * 50)
    
    tests = [
        ("Blood Bank Request", test_blood_bank_api),
        ("Nearby Hospitals", test_nearby_hospitals)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_function in tests:
        if test_function():
            passed += 1
        else:
            logger.error(f"❌ {test_name} failed")
    
    logger.info("\n" + "=" * 50)
    logger.info(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All blood bank tests passed!")
        logger.info("The blood bank functionality is working correctly.")
    else:
        logger.error("⚠️  Some blood bank tests failed.")
        logger.info("Check the server logs for more details.")

if __name__ == "__main__":
    main()
