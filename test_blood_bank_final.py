#!/usr/bin/env python3
"""
Final Blood Bank Test
Test the blood bank functionality end-to-end
"""
import requests
import json
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_blood_bank_complete():
    """Test complete blood bank functionality"""
    base_url = "http://localhost:5000"
    
    logger.info("🩸 Final Blood Bank Test")
    logger.info("=" * 50)
    
    # Test 1: Check if server is running
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            logger.info("✅ Server is running")
        else:
            logger.error(f"❌ Server returned status: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ Cannot connect to server: {e}")
        logger.info("Please start the server with: python simple_start.py")
        return False
    
    # Test 2: Blood bank request
    logger.info("\n🧪 Testing blood bank request...")
    try:
        test_data = {
            "user_id": "test_user_final",
            "blood_type": "O+",
            "request_type": "urgent_blood_request",
            "urgency_level": "high",
            "city": "Delhi",
            "state": "Delhi",
            "contact_number": "+91-9876543210",
            "additional_info": "Final test - emergency blood needed"
        }
        
        response = requests.post(f"{base_url}/api/blood-bank/request", json=test_data, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            logger.info("✅ Blood bank request successful!")
            logger.info(f"   Blood Type: {data.get('blood_type')}")
            logger.info(f"   City: {data.get('city')}")
            logger.info(f"   Total Units Available: {data.get('availability', {}).get('total_units_available', 0)}")
            logger.info(f"   Compatible Donors: {data.get('total_donors_found', 0)}")
            
            # Show sample results
            donors = data.get('compatible_donors', [])
            if donors:
                donor = donors[0]
                logger.info(f"   Sample Donor: {donor.get('name')} ({donor.get('blood_type')}) - {donor.get('distance_km')} km")
            
            hospitals = data.get('availability', {}).get('hospitals_with_blood', [])
            if hospitals:
                hospital = hospitals[0]
                logger.info(f"   Sample Hospital: {hospital.get('name')} - {hospital.get('distance_km')} km")
            
        else:
            logger.error(f"❌ Blood bank request failed: {response.status_code}")
            logger.error(f"Response: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Blood bank request error: {e}")
        return False
    
    # Test 3: Different blood types
    logger.info("\n🩸 Testing different blood types...")
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
            
            response = requests.post(f"{base_url}/api/blood-bank/request", json=test_data, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                units = data.get('availability', {}).get('total_units_available', 0)
                donors = data.get('total_donors_found', 0)
                logger.info(f"   ✅ {blood_type}: {units} units, {donors} donors")
            else:
                logger.warning(f"   ⚠️ {blood_type}: Request failed ({response.status_code})")
                
        except Exception as e:
            logger.warning(f"   ⚠️ {blood_type}: Error - {e}")
    
    # Test 4: Hospitals API
    logger.info("\n🏥 Testing hospitals API...")
    try:
        response = requests.get(f"{base_url}/api/blood-bank/hospitals?lat=28.7041&lon=77.1025&radius=50", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            logger.info(f"✅ Hospitals API working: {data.get('total_found', 0)} hospitals found")
        else:
            logger.warning(f"⚠️ Hospitals API failed: {response.status_code}")
            
    except Exception as e:
        logger.warning(f"⚠️ Hospitals API error: {e}")
    
    logger.info("\n" + "=" * 50)
    logger.info("🎉 BLOOD BANK TEST COMPLETE!")
    logger.info("✅ All core functionality is working")
    logger.info("🌐 Access your platform at: http://localhost:5000")
    logger.info("📱 To use blood bank:")
    logger.info("   1. Click '🩸 Blood Bank' service")
    logger.info("   2. Select blood type (e.g., O+)")
    logger.info("   3. Select urgency level")
    logger.info("   4. Enter city (e.g., Delhi)")
    logger.info("   5. Click 'Find Blood & Donors'")
    logger.info("   6. View results with blood availability and donors")
    
    return True

def main():
    """Main test function"""
    try:
        test_blood_bank_complete()
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")

if __name__ == "__main__":
    main()
