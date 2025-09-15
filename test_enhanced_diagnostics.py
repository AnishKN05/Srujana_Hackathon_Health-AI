#!/usr/bin/env python3
"""
Test Enhanced Diagnostic Services
Test all the new diagnostic capabilities
"""
import requests
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_enhanced_diagnostics():
    """Test all enhanced diagnostic services"""
    base_url = "http://localhost:5000"
    
    logger.info("🔍 Testing Enhanced Diagnostic Services")
    logger.info("=" * 60)
    
    # Test 1: Vital Signs Analysis
    logger.info("\n📊 Test 1: Vital Signs Analysis")
    logger.info("-" * 40)
    
    try:
        response = requests.post(f"{base_url}/api/vitals/analyze", json={
            'systolic': 130,
            'diastolic': 85,
            'heartRate': 75,
            'temperature': 98.6,
            'respiratoryRate': 16,
            'oxygenSaturation': 98,
            'weight': 70,
            'height': 170
        }, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                logger.info("✅ Vital Signs Analysis - SUCCESS")
                results = data.get('results', {})
                
                if 'bloodPressure' in results:
                    bp = results['bloodPressure']
                    logger.info(f"   Blood Pressure: {bp['systolic']}/{bp['diastolic']} - {bp['status']}")
                
                if 'heartRate' in results:
                    hr = results['heartRate']
                    logger.info(f"   Heart Rate: {hr['value']} BPM - {hr['status']}")
                
                if 'temperature' in results:
                    temp = results['temperature']
                    logger.info(f"   Temperature: {temp['value']}°F - {temp['status']}")
                
                if 'bmi' in results:
                    bmi = results['bmi']
                    logger.info(f"   BMI: {bmi['value']} - {bmi['status']}")
            else:
                logger.error(f"   ❌ API Error: {data.get('error', 'Unknown error')}")
        else:
            logger.error(f"   ❌ HTTP Error: {response.status_code}")
    except Exception as e:
        logger.error(f"   ❌ Test failed: {e}")
    
    # Test 2: Body System Analysis
    logger.info("\n🫀 Test 2: Body System Analysis")
    logger.info("-" * 40)
    
    try:
        response = requests.post(f"{base_url}/api/body-system/analyze", json={
            'symptoms': ['chest_pain', 'shortness_breath', 'cough', 'headache']
        }, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                logger.info("✅ Body System Analysis - SUCCESS")
                systems = data.get('affectedSystems', [])
                
                for system in systems:
                    logger.info(f"   {system['name']}: {system['riskLevel']} risk")
                    logger.info(f"   Symptoms: {', '.join(system['symptoms'])}")
            else:
                logger.error(f"   ❌ API Error: {data.get('error', 'Unknown error')}")
        else:
            logger.error(f"   ❌ HTTP Error: {response.status_code}")
    except Exception as e:
        logger.error(f"   ❌ Test failed: {e}")
    
    # Test 3: Mental Health Assessment
    logger.info("\n🧠 Test 3: Mental Health Assessment")
    logger.info("-" * 40)
    
    try:
        response = requests.post(f"{base_url}/api/mental-health/analyze", json={
            'responses': {
                'anxiety': 'sometimes',
                'mood': 'good',
                'sleep': 'well',
                'concentration': 'rarely',
                'interest': 'slightly'
            }
        }, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                logger.info("✅ Mental Health Assessment - SUCCESS")
                logger.info(f"   Overall Score: {data.get('overallScore', 0)}/100")
                logger.info(f"   Risk Level: {data.get('riskLevel', 'Unknown')}")
                
                categories = data.get('categoryScores', [])
                for category in categories:
                    logger.info(f"   {category['name']}: {category['score']}/20 - {category['interpretation']}")
            else:
                logger.error(f"   ❌ API Error: {data.get('error', 'Unknown error')}")
        else:
            logger.error(f"   ❌ HTTP Error: {response.status_code}")
    except Exception as e:
        logger.error(f"   ❌ Test failed: {e}")
    
    # Test 4: Chronic Disease Risk Assessment
    logger.info("\n🩺 Test 4: Chronic Disease Risk Assessment")
    logger.info("-" * 40)
    
    try:
        response = requests.post(f"{base_url}/api/chronic-risk/analyze", json={
            'riskFactors': ['diabetes_family', 'obesity', 'sedentary', 'poor_diet'],
            'ageRange': '31-45'
        }, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                logger.info("✅ Chronic Disease Risk Assessment - SUCCESS")
                logger.info(f"   Overall Risk: {data.get('overallRisk', 'Unknown')}")
                
                diseases = data.get('diseaseRisks', [])
                for disease in diseases:
                    logger.info(f"   {disease['name']}: {disease['riskLevel']} risk (Score: {disease['riskScore']}/100)")
                    logger.info(f"   Key Factors: {', '.join(disease['keyFactors'])}")
            else:
                logger.error(f"   ❌ API Error: {data.get('error', 'Unknown error')}")
        else:
            logger.error(f"   ❌ HTTP Error: {response.status_code}")
    except Exception as e:
        logger.error(f"   ❌ Test failed: {e}")
    
    logger.info("\n" + "=" * 60)
    logger.info("🎯 ENHANCED DIAGNOSTIC SERVICES TEST COMPLETE!")
    logger.info("✅ New Diagnostic Features Added:")
    logger.info("   • Vital Signs Analysis (BP, HR, Temperature, BMI)")
    logger.info("   • Body System Assessment (Cardio, Respiratory, Digestive, etc.)")
    logger.info("   • Mental Health Assessment (Anxiety, Mood, Sleep, etc.)")
    logger.info("   • Chronic Disease Risk Assessment (Diabetes, Heart, Cancer)")
    logger.info("   • Comprehensive Health Analysis with Recommendations")

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
        
        test_enhanced_diagnostics()
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")

if __name__ == "__main__":
    main()
