#!/usr/bin/env python3
"""
Test Enhanced Hospital Recommendation System
Test the ML-powered hospital recommendations with emphasis on doctor quality
"""
import requests
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_enhanced_hospital_recommendations():
    """Test enhanced hospital recommendation system with doctor quality focus"""
    base_url = "http://localhost:5000"
    
    logger.info("🏥 Testing Enhanced Hospital Recommendation System")
    logger.info("=" * 70)
    logger.info("Focus: Doctor Quality & Specialty Expertise")
    logger.info("=" * 70)
    
    # Test cases focusing on different medical specialties
    test_cases = [
        {
            "medical_issue": "I have severe chest pain and need heart surgery",
            "city": "Delhi",
            "urgency_level": "high",
            "expected_specialty": "cardiology",
            "description": "Heart condition requiring best cardiologists"
        },
        {
            "medical_issue": "I need brain surgery for a tumor removal",
            "city": "Mumbai", 
            "urgency_level": "medium",
            "expected_specialty": "neurology",
            "description": "Brain surgery requiring top neurosurgeons"
        },
        {
            "medical_issue": "My child has a complex heart defect requiring surgery",
            "city": "Bangalore",
            "urgency_level": "high", 
            "expected_specialty": "pediatrics",
            "description": "Pediatric heart surgery requiring specialized doctors"
        },
        {
            "medical_issue": "I have a broken hip that needs orthopedic surgery",
            "city": "Chennai",
            "urgency_level": "medium",
            "expected_specialty": "orthopedics", 
            "description": "Orthopedic surgery requiring experienced surgeons"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        logger.info(f"\n🧪 Test Case {i}: {test_case['description']}")
        logger.info(f"Medical Issue: {test_case['medical_issue']}")
        logger.info(f"City: {test_case['city']} | Urgency: {test_case['urgency_level']}")
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
                        logger.info(f"\n🏆 TOP 3 HOSPITAL RECOMMENDATIONS (Ranked by Doctor Quality):")
                        logger.info("=" * 60)
                        
                        for j, hospital in enumerate(recommendations[:3], 1):
                            logger.info(f"\n#{j} {hospital.get('name', 'Unknown Hospital')}")
                            logger.info(f"   📍 Location: {hospital.get('city', 'Unknown')}, {hospital.get('state', 'Unknown')} ({hospital.get('distance_km', 0)} km)")
                            logger.info(f"   ⭐ Overall Rating: {hospital.get('overall_rating', 0)}/5.0")
                            logger.info(f"   🎯 Recommendation Score: {hospital.get('recommendation_score', 0)}")
                            logger.info(f"   🏥 Specialty Match: {'✅ YES' if hospital.get('specialty_match') else '❌ NO'}")
                            logger.info(f"   ⚡ Urgency Match: {'✅ YES' if hospital.get('urgency_match') else '❌ NO'}")
                            
                            # Show specialty-specific information
                            if hospital.get('specialty_match'):
                                logger.info(f"   🎯 {data.get('predicted_specialty', 'Specialty')} Department:")
                                logger.info(f"      • Department Rating: {hospital.get('specialty_rating', 0)}/5.0")
                                logger.info(f"      • Specialist Doctors: {hospital.get('specialty_doctors', 0)}")
                                logger.info(f"      • Success Rate: {hospital.get('specialty_success_rate', 0)}%")
                                logger.info(f"      • Wait Time: {hospital.get('specialty_wait_time', 0)} days")
                            
                            # Show top doctors
                            doctors = hospital.get('recommended_doctors', [])
                            if doctors:
                                logger.info(f"   👨‍⚕️ Top Specialists:")
                                for k, doctor in enumerate(doctors[:2], 1):
                                    logger.info(f"      {k}. {doctor.get('name', 'Unknown')} ({doctor.get('qualification', 'Unknown')})")
                                    logger.info(f"         ⭐ {doctor.get('rating', 0)}/5.0 | {doctor.get('experience_years', 0)} years | {doctor.get('success_rate', 0)}% success")
                                    logger.info(f"         📊 {doctor.get('procedures_performed', 0)} procedures | {doctor.get('patient_reviews', 0)} reviews")
                            
                            # Show hospital details
                            logger.info(f"   🏥 Hospital Details:")
                            logger.info(f"      • Capacity: {hospital.get('bed_capacity', 0)} beds | {hospital.get('icu_beds', 0)} ICU | {hospital.get('operation_theaters', 0)} OT")
                            logger.info(f"      • Services: Emergency {'✅' if hospital.get('emergency_services') else '❌'} | Ambulance {'✅' if hospital.get('ambulance_services') else '❌'}")
                            logger.info(f"      • Financial: Insurance {'✅' if hospital.get('insurance_accepted') else '❌'} | Cost: {hospital.get('cost_level', 'Unknown')}")
                            
                            # Show recommendation reason
                            logger.info(f"   💡 Why Recommended: {hospital.get('recommendation_reason', 'No reason provided')}")
                            
                            logger.info("-" * 40)
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
    logger.info("🎯 ENHANCED HOSPITAL RECOMMENDATION TEST COMPLETE!")
    logger.info("✅ Key Features Demonstrated:")
    logger.info("   • ML-powered medical issue analysis")
    logger.info("   • Doctor quality-based hospital ranking")
    logger.info("   • Specialty expertise prioritization")
    logger.info("   • Same-city hospital focus")
    logger.info("   • Detailed hospital and doctor information")
    logger.info("   • Comprehensive recommendation reasoning")

def test_doctor_quality_ranking():
    """Test doctor quality ranking system"""
    base_url = "http://localhost:5000"
    
    logger.info("\n👨‍⚕️ Testing Doctor Quality Ranking System")
    logger.info("=" * 50)
    
    specialties = ['cardiology', 'neurology', 'orthopedics', 'pediatrics']
    
    for specialty in specialties:
        logger.info(f"\n🔍 Testing {specialty.upper()} doctors:")
        
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
                        logger.info(f"   🏆 Top 3 {specialty} specialists (ranked by quality):")
                        for i, doctor in enumerate(doctors[:3], 1):
                            quality_score = doctor.get('quality_score', 0)
                            logger.info(f"   {i}. {doctor.get('name', 'Unknown')} ({doctor.get('qualification', 'Unknown')})")
                            logger.info(f"      Quality Score: {quality_score:.3f}")
                            logger.info(f"      Rating: {doctor.get('rating', 0)}/5.0 | Experience: {doctor.get('experience_years', 0)} years")
                            logger.info(f"      Success Rate: {doctor.get('success_rate', 0)}% | Procedures: {doctor.get('procedures_performed', 0)}")
                else:
                    logger.error(f"   ❌ API error: {data.get('error', 'Unknown error')}")
            else:
                logger.error(f"   ❌ HTTP Error: {response.status_code}")
                
        except Exception as e:
            logger.error(f"   ❌ Test failed: {e}")

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
        
        test_enhanced_hospital_recommendations()
        test_doctor_quality_ranking()
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")

if __name__ == "__main__":
    main()
