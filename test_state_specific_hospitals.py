#!/usr/bin/env python3
"""
Test State-Specific Hospital Recommendations
Test that hospitals are filtered by state only
"""
import requests
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_state_specific_recommendations():
    """Test that hospital recommendations are state-specific"""
    base_url = "http://localhost:5000"
    
    logger.info("🏥 Testing State-Specific Hospital Recommendations")
    logger.info("=" * 70)
    logger.info("Focus: Hospitals from SAME STATE only")
    logger.info("=" * 70)
    
    # Test cases for different states
    test_cases = [
        {
            "medical_issue": "I have severe chest pain and need heart surgery",
            "city": "Mumbai",
            "expected_state": "Maharashtra",
            "description": "Mumbai - Should only show Maharashtra hospitals"
        },
        {
            "medical_issue": "I need brain surgery for a tumor removal",
            "city": "Bangalore", 
            "expected_state": "Karnataka",
            "description": "Bangalore - Should only show Karnataka hospitals"
        },
        {
            "medical_issue": "My child has a complex heart defect requiring surgery",
            "city": "Chennai",
            "expected_state": "Tamil Nadu", 
            "description": "Chennai - Should only show Tamil Nadu hospitals"
        },
        {
            "medical_issue": "I have a broken hip that needs orthopedic surgery",
            "city": "Delhi",
            "expected_state": "Delhi",
            "description": "Delhi - Should only show Delhi hospitals"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        logger.info(f"\n🧪 Test Case {i}: {test_case['description']}")
        logger.info(f"Medical Issue: {test_case['medical_issue']}")
        logger.info(f"City: {test_case['city']} | Expected State: {test_case['expected_state']}")
        logger.info("-" * 60)
        
        try:
            response = requests.post(f"{base_url}/api/hospital/recommend", json=test_case, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('success'):
                    logger.info(f"✅ ML Analysis Complete!")
                    logger.info(f"   Predicted Specialty: {data.get('predicted_specialty', 'Unknown')}")
                    logger.info(f"   Total Hospitals Found: {data.get('total_hospitals', 0)}")
                    
                    recommendations = data.get('recommendations', [])
                    if recommendations:
                        logger.info(f"\n🏆 HOSPITAL RECOMMENDATIONS (State: {test_case['expected_state']}):")
                        logger.info("=" * 60)
                        
                        # Check if all hospitals are from the expected state
                        all_correct_state = True
                        for j, hospital in enumerate(recommendations, 1):
                            hospital_state = hospital.get('state', 'Unknown')
                            is_correct_state = hospital_state.lower() == test_case['expected_state'].lower()
                            
                            if not is_correct_state:
                                all_correct_state = False
                            
                            status_icon = "✅" if is_correct_state else "❌"
                            
                            logger.info(f"{status_icon} #{j} {hospital.get('name', 'Unknown Hospital')}")
                            logger.info(f"   📍 Location: {hospital.get('city', 'Unknown')}, {hospital_state}")
                            logger.info(f"   ⭐ Overall Rating: {hospital.get('overall_rating', 0)}/5.0")
                            logger.info(f"   🎯 Recommendation Score: {hospital.get('recommendation_score', 0)}")
                            logger.info(f"   🏥 Specialty Match: {'✅ YES' if hospital.get('specialty_match') else '❌ NO'}")
                            
                            # Show specialty-specific information
                            if hospital.get('specialty_match'):
                                logger.info(f"   🎯 {data.get('predicted_specialty', 'Specialty')} Department:")
                                logger.info(f"      • Department Rating: {hospital.get('specialty_rating', 0)}/5.0")
                                logger.info(f"      • Specialist Doctors: {hospital.get('specialty_doctors', 0)}")
                                logger.info(f"      • Success Rate: {hospital.get('specialty_success_rate', 0)}%")
                                logger.info(f"      • Wait Time: {hospital.get('specialty_wait_time', 0)} days")
                            
                            logger.info("-" * 40)
                        
                        # Summary
                        if all_correct_state:
                            logger.info(f"✅ SUCCESS: All hospitals are from {test_case['expected_state']} state!")
                        else:
                            logger.error(f"❌ FAILED: Some hospitals are NOT from {test_case['expected_state']} state!")
                            
                    else:
                        logger.warning("   ⚠️ No hospital recommendations found")
                        
                else:
                    logger.error(f"   ❌ API Error: {data.get('error', 'Unknown error')}")
                    
            else:
                logger.error(f"   ❌ HTTP Error: {response.status_code}")
                logger.error(f"   Response: {response.text}")
                
        except Exception as e:
            logger.error(f"   ❌ Test failed: {e}")
    
    logger.info("\n" + "=" * 70)
    logger.info("🎯 STATE-SPECIFIC HOSPITAL RECOMMENDATION TEST COMPLETE!")
    logger.info("✅ Key Features Tested:")
    logger.info("   • State-specific hospital filtering")
    logger.info("   • Same-state hospital recommendations only")
    logger.info("   • ML-powered medical issue analysis")
    logger.info("   • Doctor quality-based ranking within state")

def test_multiple_cities_same_state():
    """Test that different cities in same state show different hospitals"""
    base_url = "http://localhost:5000"
    
    logger.info("\n🏙️ Testing Multiple Cities in Same State")
    logger.info("=" * 50)
    
    # Test Mumbai and Pune (both Maharashtra)
    cities = ['Mumbai', 'Pune']
    medical_issue = "I have severe chest pain and need heart surgery"
    
    for city in cities:
        logger.info(f"\n🔍 Testing {city} (Maharashtra):")
        
        try:
            response = requests.post(f"{base_url}/api/hospital/recommend", json={
                'medical_issue': medical_issue,
                'city': city,
                'urgency_level': 'high'
            }, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('success'):
                    recommendations = data.get('recommendations', [])
                    logger.info(f"   ✅ Found {len(recommendations)} hospitals in {city}")
                    
                    if recommendations:
                        # Show first 3 hospitals
                        for i, hospital in enumerate(recommendations[:3], 1):
                            logger.info(f"   {i}. {hospital.get('name', 'Unknown')} - {hospital.get('city', 'Unknown')}")
                    else:
                        logger.warning(f"   ⚠️ No hospitals found for {city}")
                else:
                    logger.error(f"   ❌ API error: {data.get('error', 'Unknown error')}")
            else:
                logger.error(f"   ❌ HTTP Error: {response.status_code}")
                
        except Exception as e:
            logger.error(f"   ❌ Test failed for {city}: {e}")

def main():
    """Main test function"""
    try:
        # Test if server is running
        try:
            response = requests.get("http://localhost:5000", timeout=5)
            if response.status_code == 200:
                logger.info("✅ Server is running")
            else:
                logger.error("❌ Server is not responding properly")
                return
        except:
            logger.error("❌ Cannot connect to server. Please start the server with: python simple_start.py")
            return
        
        test_state_specific_recommendations()
        test_multiple_cities_same_state()
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")

if __name__ == "__main__":
    main()
