#!/usr/bin/env python3
"""
Debug Blood Bank System
Test the blood bank system directly without the web server
"""
import sys
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_blood_bank_system():
    """Test blood bank system directly"""
    try:
        # Add ml_models to path
        sys.path.append('ml_models')
        
        logger.info("Testing Blood Bank System directly...")
        
        from blood_bank_system import BloodBankSystem
        
        # Initialize system
        system = BloodBankSystem()
        logger.info("✅ Blood bank system initialized")
        
        # Test blood availability
        logger.info("Testing blood availability...")
        availability = system.check_blood_availability('O+', 'Delhi')
        logger.info(f"✅ Blood availability test passed: {availability['total_units_available']} units")
        
        # Test donor finding
        logger.info("Testing donor finding...")
        donors = system.find_compatible_donors('O+', 'Delhi')
        logger.info(f"✅ Donor finding test passed: {len(donors)} donors found")
        
        # Test hospital finding
        logger.info("Testing hospital finding...")
        hospitals = system.find_nearby_hospitals(28.7041, 77.1025, 50)
        logger.info(f"✅ Hospital finding test passed: {len(hospitals)} hospitals found")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Blood bank system test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_blood_bank_api_simulation():
    """Simulate the API call without the web server"""
    try:
        sys.path.append('ml_models')
        from blood_bank_system import BloodBankSystem
        
        logger.info("Simulating blood bank API call...")
        
        # Simulate the API request data
        data = {
            'user_id': 'test_user',
            'blood_type': 'O+',
            'request_type': 'urgent_blood_request',
            'urgency_level': 'high',
            'city': 'Delhi',
            'state': 'Delhi',
            'contact_number': '+91-9876543210',
            'additional_info': 'Emergency surgery'
        }
        
        blood_type = data.get('blood_type', '')
        city = data.get('city', 'Delhi')
        
        if not blood_type:
            logger.error("❌ Blood type is required")
            return False
        
        system = BloodBankSystem()
        
        # Check blood availability
        availability = system.check_blood_availability(blood_type, city)
        logger.info(f"✅ Blood availability: {availability['total_units_available']} units")
        
        # Find compatible donors
        donors = system.find_compatible_donors(blood_type, city)
        logger.info(f"✅ Compatible donors: {len(donors)} found")
        
        # Create response
        response = {
            'blood_type': blood_type,
            'city': city,
            'availability': availability,
            'compatible_donors': donors[:10],  # Top 10 donors
            'total_donors_found': len(donors),
            'emergency_contacts': {
                'national_blood_bank': '+91-1800-180-1234',
                'red_cross_india': '+91-1800-180-1234',
                'emergency_services': '108'
            }
        }
        
        logger.info("✅ API simulation successful!")
        logger.info(f"Response keys: {list(response.keys())}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ API simulation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main debug function"""
    logger.info("🔍 Blood Bank Debug Test")
    logger.info("=" * 50)
    
    tests = [
        ("Blood Bank System", test_blood_bank_system),
        ("API Simulation", test_blood_bank_api_simulation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_function in tests:
        logger.info(f"\n📋 Testing {test_name}...")
        if test_function():
            passed += 1
        else:
            logger.error(f"❌ {test_name} failed")
    
    logger.info("\n" + "=" * 50)
    logger.info(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All blood bank tests passed!")
        logger.info("The issue might be in the web server or database connection.")
    else:
        logger.error("⚠️  Blood bank system has issues.")
        logger.info("Check the error messages above for details.")

if __name__ == "__main__":
    main()
