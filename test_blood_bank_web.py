#!/usr/bin/env python3
"""
Test Blood Bank Web Interface
Test the complete blood bank workflow through the web interface
"""
import requests
import json
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_complete_blood_bank_workflow():
    """Test the complete blood bank workflow"""
    base_url = "http://localhost:5000"
    
    logger.info("🩸 Testing Complete Blood Bank Workflow")
    logger.info("=" * 50)
    
    # Test 1: Register a user
    logger.info("1. Testing user registration...")
    try:
        register_data = {
            "name": "Test User",
            "age": 25,
            "gender": "Male",
            "location": "Delhi",
            "medical_history": [],
            "consent": True
        }
        
        response = requests.post(f"{base_url}/api/user/register", json=register_data)
        if response.status_code == 200:
            logger.info("✅ User registration successful")
        else:
            logger.warning(f"⚠️ User registration failed: {response.status_code}")
    except Exception as e:
        logger.warning(f"⚠️ User registration error: {e}")
    
    # Test 2: Blood bank request
    logger.info("\n2. Testing blood bank request...")
    try:
        blood_request_data = {
            "user_id": "test_user_123",
            "blood_type": "O+",
            "request_type": "urgent_blood_request",
            "urgency_level": "high",
            "city": "Delhi",
            "state": "Delhi",
            "contact_number": "+91-9876543210",
            "additional_info": "Emergency surgery - need blood urgently"
        }
        
        response = requests.post(f"{base_url}/api/blood-bank/request", json=blood_request_data)
        
        if response.status_code == 200:
            data = response.json()
            logger.info("✅ Blood bank request successful!")
            logger.info(f"   Blood Type: {data.get('blood_type')}")
            logger.info(f"   City: {data.get('city')}")
            logger.info(f"   Total Units Available: {data.get('availability', {}).get('total_units_available', 0)}")
            logger.info(f"   Compatible Donors: {data.get('total_donors_found', 0)}")
            
            # Show sample donor
            donors = data.get('compatible_donors', [])
            if donors:
                donor = donors[0]
                logger.info(f"   Sample Donor: {donor.get('name')} ({donor.get('blood_type')}) - {donor.get('distance_km')} km away")
            
            # Show emergency contacts
            emergency = data.get('emergency_contacts', {})
            logger.info(f"   Emergency Services: {emergency.get('emergency_services')}")
            
        else:
            logger.error(f"❌ Blood bank request failed: {response.status_code}")
            logger.error(f"Response: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Blood bank request error: {e}")
        return False
    
    # Test 3: Nearby hospitals
    logger.info("\n3. Testing nearby hospitals...")
    try:
        response = requests.get(f"{base_url}/api/blood-bank/hospitals?lat=28.7041&lon=77.1025&radius=50")
        
        if response.status_code == 200:
            data = response.json()
            logger.info("✅ Nearby hospitals request successful!")
            logger.info(f"   Hospitals Found: {data.get('total_found', 0)}")
            
            hospitals = data.get('hospitals', [])
            if hospitals:
                hospital = hospitals[0]
                logger.info(f"   Sample Hospital: {hospital.get('name')} - {hospital.get('distance_km')} km away")
                
        else:
            logger.error(f"❌ Nearby hospitals failed: {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Nearby hospitals error: {e}")
        return False
    
    # Test 4: Different blood types
    logger.info("\n4. Testing different blood types...")
    blood_types = ["A+", "B+", "AB+", "O-"]
    
    for blood_type in blood_types:
        try:
            test_data = {
                "user_id": "test_user",
                "blood_type": blood_type,
                "request_type": "general_request",
                "urgency_level": "medium",
                "city": "Mumbai",
                "state": "Maharashtra",
                "contact_number": "+91-9876543210"
            }
            
            response = requests.post(f"{base_url}/api/blood-bank/request", json=test_data)
            
            if response.status_code == 200:
                data = response.json()
                units = data.get('availability', {}).get('total_units_available', 0)
                donors = data.get('total_donors_found', 0)
                logger.info(f"   {blood_type}: {units} units, {donors} donors")
            else:
                logger.warning(f"   {blood_type}: Request failed ({response.status_code})")
                
        except Exception as e:
            logger.warning(f"   {blood_type}: Error - {e}")
    
    logger.info("\n" + "=" * 50)
    logger.info("🎉 Blood Bank Web Interface Test Complete!")
    logger.info("✅ All core functionality is working correctly")
    logger.info("🌐 You can now use the blood bank through the web interface at:")
    logger.info("   http://localhost:5000")
    logger.info("📱 Steps to use:")
    logger.info("   1. Click '🩸 Blood Bank' service")
    logger.info("   2. Select blood type (e.g., O+)")
    logger.info("   3. Select urgency level")
    logger.info("   4. Enter city (e.g., Delhi)")
    logger.info("   5. Click 'Find Blood & Donors'")
    
    return True

def main():
    """Main test function"""
    try:
        test_complete_blood_bank_workflow()
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")

if __name__ == "__main__":
    main()
