#!/usr/bin/env python3
"""
Enhanced Health Platform Test Script
Tests all new features: nutrition, physio, and blood bank services
"""
import requests
import json
import time
import logging
import sys
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class HealthPlatformTester:
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = {}
    
    def test_health_check(self) -> bool:
        """Test basic health check endpoint"""
        logger.info("Testing health check endpoint...")
        try:
            response = self.session.get(f"{self.base_url}/api/health")
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ Health check passed: {data.get('message', 'OK')}")
                return True
            else:
                logger.error(f"❌ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ Health check error: {e}")
            return False
    
    def test_user_registration(self) -> str:
        """Test user registration"""
        logger.info("Testing user registration...")
        try:
            user_data = {
                "user_id": "test_user_123",
                "name": "Test User",
                "age": 30,
                "gender": "male",
                "location": "delhi",
                "consent": True
            }
            
            response = self.session.post(
                f"{self.base_url}/api/user/register",
                json=user_data
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ User registration passed: {data.get('message', 'OK')}")
                return user_data["user_id"]
            else:
                logger.error(f"❌ User registration failed: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"❌ User registration error: {e}")
            return None
    
    def test_symptom_analysis(self, user_id: str) -> bool:
        """Test symptom analysis"""
        logger.info("Testing symptom analysis...")
        try:
            symptom_data = {
                "user_id": user_id,
                "symptoms": ["headache", "fever"],
                "duration": "1-3 days",
                "severity": "moderate",
                "age": 30,
                "gender": "male"
            }
            
            response = self.session.post(
                f"{self.base_url}/api/symptoms/analyze",
                json=symptom_data
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ Symptom analysis passed: Found {len(data.get('possible_conditions', []))} conditions")
                return True
            else:
                logger.error(f"❌ Symptom analysis failed: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ Symptom analysis error: {e}")
            return False
    
    def test_nutrition_consultation(self, user_id: str) -> bool:
        """Test nutrition consultation"""
        logger.info("Testing nutrition consultation...")
        try:
            nutrition_data = {
                "user_id": user_id,
                "query": "I want to lose weight, what should I eat?",
                "user_context": {
                    "age": 30,
                    "gender": "male",
                    "location": "delhi"
                }
            }
            
            response = self.session.post(
                f"{self.base_url}/api/nutrition/consult",
                json=nutrition_data
            )
            
            if response.status_code == 200:
                data = response.json()
                prediction = data.get('prediction', {})
                logger.info(f"✅ Nutrition consultation passed: Category {prediction.get('category', 'unknown')}")
                return True
            else:
                logger.error(f"❌ Nutrition consultation failed: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ Nutrition consultation error: {e}")
            return False
    
    def test_physio_consultation(self, user_id: str) -> bool:
        """Test physiotherapy consultation"""
        logger.info("Testing physiotherapy consultation...")
        try:
            physio_data = {
                "user_id": user_id,
                "query": "I have lower back pain, what exercises can help?",
                "user_context": {
                    "age": 30,
                    "gender": "male",
                    "location": "delhi"
                }
            }
            
            response = self.session.post(
                f"{self.base_url}/api/physio/consult",
                json=physio_data
            )
            
            if response.status_code == 200:
                data = response.json()
                prediction = data.get('prediction', {})
                logger.info(f"✅ Physiotherapy consultation passed: Category {prediction.get('category', 'unknown')}")
                return True
            else:
                logger.error(f"❌ Physiotherapy consultation failed: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ Physiotherapy consultation error: {e}")
            return False
    
    def test_blood_bank_request(self, user_id: str) -> bool:
        """Test blood bank request"""
        logger.info("Testing blood bank request...")
        try:
            blood_data = {
                "user_id": user_id,
                "blood_type": "O+",
                "request_type": "urgent_blood_request",
                "urgency_level": "high",
                "city": "Delhi",
                "state": "Delhi",
                "contact_number": "+91-9876543210",
                "additional_info": "Emergency surgery"
            }
            
            response = self.session.post(
                f"{self.base_url}/api/blood-bank/request",
                json=blood_data
            )
            
            if response.status_code == 200:
                data = response.json()
                availability = data.get('availability', {})
                donors = data.get('compatible_donors', [])
                logger.info(f"✅ Blood bank request passed: {availability.get('total_units_available', 0)} units, {len(donors)} donors")
                return True
            else:
                logger.error(f"❌ Blood bank request failed: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ Blood bank request error: {e}")
            return False
    
    def test_donor_registration(self, user_id: str) -> bool:
        """Test blood donor registration"""
        logger.info("Testing blood donor registration...")
        try:
            donor_data = {
                "user_id": user_id,
                "name": "Test Donor",
                "age": 25,
                "gender": "female",
                "blood_type": "O+",
                "city": "Mumbai",
                "state": "Maharashtra",
                "contact_number": "+91-9876543211",
                "email": "test.donor@example.com",
                "medical_conditions": ["None"]
            }
            
            response = self.session.post(
                f"{self.base_url}/api/blood-bank/donor-register",
                json=donor_data
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ Donor registration passed: {data.get('message', 'OK')}")
                return True
            else:
                logger.error(f"❌ Donor registration failed: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ Donor registration error: {e}")
            return False
    
    def test_nearby_hospitals(self) -> bool:
        """Test nearby hospitals endpoint"""
        logger.info("Testing nearby hospitals...")
        try:
            params = {
                "lat": 28.7041,  # Delhi coordinates
                "lon": 77.1025,
                "radius": 50
            }
            
            response = self.session.get(
                f"{self.base_url}/api/blood-bank/hospitals",
                params=params
            )
            
            if response.status_code == 200:
                data = response.json()
                hospitals = data.get('hospitals', [])
                logger.info(f"✅ Nearby hospitals passed: Found {len(hospitals)} hospitals")
                return True
            else:
                logger.error(f"❌ Nearby hospitals failed: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ Nearby hospitals error: {e}")
            return False
    
    def test_service_chat(self, user_id: str) -> bool:
        """Test multi-service chat"""
        logger.info("Testing multi-service chat...")
        try:
            chat_data = {
                "user_id": user_id,
                "message": "I need help with my diet",
                "service_type": "nutrition",
                "user_context": {
                    "age": 30,
                    "gender": "male"
                }
            }
            
            response = self.session.post(
                f"{self.base_url}/api/services/chat",
                json=chat_data
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ Service chat passed: {data.get('service_type', 'unknown')} service")
                return True
            else:
                logger.error(f"❌ Service chat failed: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ Service chat error: {e}")
            return False
    
    def test_general_chat(self, user_id: str) -> bool:
        """Test general chat"""
        logger.info("Testing general chat...")
        try:
            chat_data = {
                "user_id": user_id,
                "message": "I have a headache",
                "session_id": f"test_session_{int(time.time())}"
            }
            
            response = self.session.post(
                f"{self.base_url}/api/chat",
                json=chat_data
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ General chat passed: Response received")
                return True
            else:
                logger.error(f"❌ General chat failed: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ General chat error: {e}")
            return False
    
    def run_all_tests(self) -> Dict[str, bool]:
        """Run all tests"""
        logger.info("🧪 Starting Enhanced Health Platform Tests")
        logger.info("=" * 60)
        
        # Test basic connectivity
        if not self.test_health_check():
            logger.error("❌ Health check failed. Is the server running?")
            return {"health_check": False}
        
        # Register test user
        user_id = self.test_user_registration()
        if not user_id:
            logger.error("❌ User registration failed")
            return {"user_registration": False}
        
        # Run all tests
        tests = [
            ("symptom_analysis", lambda: self.test_symptom_analysis(user_id)),
            ("nutrition_consultation", lambda: self.test_nutrition_consultation(user_id)),
            ("physio_consultation", lambda: self.test_physio_consultation(user_id)),
            ("blood_bank_request", lambda: self.test_blood_bank_request(user_id)),
            ("donor_registration", lambda: self.test_donor_registration(user_id)),
            ("nearby_hospitals", lambda: self.test_nearby_hospitals()),
            ("service_chat", lambda: self.test_service_chat(user_id)),
            ("general_chat", lambda: self.test_general_chat(user_id))
        ]
        
        results = {"health_check": True, "user_registration": True}
        
        for test_name, test_function in tests:
            logger.info(f"\n📋 Testing {test_name}...")
            try:
                result = test_function()
                results[test_name] = result
                if result:
                    logger.info(f"✅ {test_name} passed")
                else:
                    logger.error(f"❌ {test_name} failed")
            except Exception as e:
                logger.error(f"❌ {test_name} error: {e}")
                results[test_name] = False
        
        return results
    
    def print_summary(self, results: Dict[str, bool]):
        """Print test summary"""
        logger.info("\n" + "=" * 60)
        logger.info("📊 TEST SUMMARY")
        logger.info("=" * 60)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            logger.info(f"{test_name.replace('_', ' ').title()}: {status}")
        
        logger.info(f"\nOverall: {passed}/{total} tests passed")
        
        if passed == total:
            logger.info("🎉 All tests passed! The Enhanced Health Platform is working correctly.")
        else:
            logger.error(f"⚠️  {total - passed} tests failed. Please check the logs above.")
        
        return passed == total

def main():
    """Main test function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Test Enhanced Health Platform')
    parser.add_argument('--url', default='http://localhost:5000', help='Base URL of the platform')
    parser.add_argument('--wait', type=int, default=5, help='Wait time before starting tests (seconds)')
    
    args = parser.parse_args()
    
    logger.info(f"Waiting {args.wait} seconds for server to be ready...")
    time.sleep(args.wait)
    
    tester = HealthPlatformTester(args.url)
    results = tester.run_all_tests()
    success = tester.print_summary(results)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
