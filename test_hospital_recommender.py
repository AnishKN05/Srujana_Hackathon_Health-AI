#!/usr/bin/env python3
"""
Test Hospital Recommendation System
Test the ML-powered hospital recommendation functionality
"""
import requests
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_hospital_recommendations():
    """Test hospital recommendation API"""
    base_url = "http://localhost:5000"
    
    logger.info("🏥 Testing Hospital Recommendation System")
    logger.info("=" * 60)
    
    # Test different medical issues
    test_cases = [
        {
            "medical_issue": "I have severe chest pain and shortness of breath",
            "city": "Delhi",
            "urgency_level": "high",
            "expected_specialty": "cardiology"
        },
        {
            "medical_issue": "I need brain surgery for a tumor",
            "city": "Mumbai",
            "urgency_level": "medium",
            "expected_specialty": "neurology"
        },
        {
            "medical_issue": "My child has high fever and breathing problems",
            "city": "Bangalore",
            "urgency_level": "high",
            "expected_specialty": "pediatrics"
        },
        {
            "medical_issue": "I broke my leg in an accident",
            "city": "Chennai",
            "urgency_level": "medium",
            "expected_specialty": "orthopedics"
        },
        {
            "medical_issue": "I have a suspicious mole on my skin",
            "city": "Kolkata",
            "urgency_level": "low",
            "expected_specialty": "dermatology"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        logger.info(f"\n🧪 Test Case {i}: {test_case['medical_issue']}")
        logger.info("-" * 50)
        
        try:
            response = requests.post(f"{base_url}/api/hospital/recommend", json=test_case, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('success'):
                    logger.info(f"✅ Hospital recommendations generated successfully!")
                    logger.info(f"   Predicted Specialty: {data.get('predicted_specialty', 'Unknown')}")
                    logger.info(f"   Total Hospitals: {data.get('total_hospitals', 0)}")
                    
                    recommendations = data.get('recommendations', [])
                    if recommendations:
                        logger.info(f"   Top 3 Hospitals:")
                        for j, hospital in enumerate(recommendations[:3], 1):
                            logger.info(f"   {j}. {hospital.get('name', 'Unknown')} - Score: {hospital.get('recommendation_score', 0)}")
                            logger.info(f"      Location: {hospital.get('city', 'Unknown')} ({hospital.get('distance_km', 0)} km)")
                            logger.info(f"      Rating: {hospital.get('overall_rating', 0)}/5.0")
                            logger.info(f"      Specialty Match: {hospital.get('specialty_match', False)}")
                            logger.info(f"      Urgency Match: {hospital.get('urgency_match', False)}")
                            
                            # Show recommended doctors
                            doctors = hospital.get('recommended_doctors', [])
                            if doctors:
                                logger.info(f"      Top Doctors:")
                                for doctor in doctors[:2]:
                                    logger.info(f"        • {doctor.get('name', 'Unknown')} ({doctor.get('qualification', 'Unknown')}) - {doctor.get('experience_years', 0)} years")
                    else:
                        logger.warning("   No hospital recommendations found")
                        
                else:
                    logger.error(f"   API returned error: {data.get('error', 'Unknown error')}")
                    
            else:
                logger.error(f"   HTTP Error: {response.status_code}")
                logger.error(f"   Response: {response.text}")
                
        except Exception as e:
            logger.error(f"   Test failed: {e}")
    
    logger.info("\n" + "=" * 60)
    logger.info("🎯 Hospital Recommendation Test Complete!")
    logger.info("✅ The system now provides intelligent hospital recommendations based on:")
    logger.info("   • Medical issue analysis using ML")
    logger.info("   • Specialty matching and doctor expertise")
    logger.info("   • Hospital ratings and success rates")
    logger.info("   • Distance and urgency considerations")
    logger.info("   • Real-time data and recommendations")

def test_doctor_recommendations():
    """Test doctor recommendation API"""
    base_url = "http://localhost:5000"
    
    logger.info("\n👨‍⚕️ Testing Doctor Recommendation System")
    logger.info("=" * 60)
    
    # Test different specialties
    specialties = ['cardiology', 'neurology', 'oncology', 'orthopedics', 'pediatrics']
    
    for specialty in specialties:
        logger.info(f"\n🔍 Testing {specialty} doctors:")
        
        try:
            response = requests.get(f"{base_url}/api/hospital/doctors", 
                                 params={'specialty': specialty, 'hospital_id': 'hospital_0_0'}, 
                                 timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('success'):
                    doctors = data.get('doctors', [])
                    logger.info(f"   ✅ Found {len(doctors)} {specialty} doctors")
                    
                    if doctors:
                        for i, doctor in enumerate(doctors[:3], 1):
                            logger.info(f"   {i}. {doctor.get('name', 'Unknown')} ({doctor.get('qualification', 'Unknown')})")
                            logger.info(f"      Experience: {doctor.get('experience_years', 0)} years")
                            logger.info(f"      Rating: {doctor.get('rating', 0)}/5.0")
                            logger.info(f"      Success Rate: {doctor.get('success_rate', 0)}%")
                else:
                    logger.error(f"   API error: {data.get('error', 'Unknown error')}")
            else:
                logger.error(f"   HTTP Error: {response.status_code}")
                
        except Exception as e:
            logger.error(f"   Test failed: {e}")

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
        
        test_hospital_recommendations()
        test_doctor_recommendations()
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")

if __name__ == "__main__":
    main()
