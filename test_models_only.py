#!/usr/bin/env python3
"""
Test ML Models Only
Tests the ML models without requiring the server to be running
"""
import os
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_nutrition_model():
    """Test nutrition classifier"""
    try:
        sys.path.append('ml_models')
        from nutrition_classifier import NutritionClassifier
        
        logger.info("Testing Nutrition Classifier...")
        classifier = NutritionClassifier()
        
        # Test queries
        test_queries = [
            "I want to lose weight, what should I eat?",
            "What foods are good for heart health?",
            "How to build muscle with nutrition?"
        ]
        
        for query in test_queries:
            try:
                prediction = classifier.predict_nutrition_category(query)
                logger.info(f"✅ Query: '{query}' -> Category: {prediction['category']}")
            except Exception as e:
                logger.error(f"❌ Error with query '{query}': {e}")
                return False
        
        logger.info("✅ Nutrition model test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Nutrition model test failed: {e}")
        return False

def test_physio_model():
    """Test physiotherapy classifier"""
    try:
        sys.path.append('ml_models')
        from physio_classifier import PhysioClassifier
        
        logger.info("Testing Physiotherapy Classifier...")
        classifier = PhysioClassifier()
        
        # Test queries
        test_queries = [
            "I have lower back pain, what exercises can help?",
            "How to improve my posture?",
            "What are good strength training exercises?"
        ]
        
        for query in test_queries:
            try:
                prediction = classifier.predict_physio_category(query)
                logger.info(f"✅ Query: '{query}' -> Category: {prediction['category']}")
            except Exception as e:
                logger.error(f"❌ Error with query '{query}': {e}")
                return False
        
        logger.info("✅ Physiotherapy model test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Physiotherapy model test failed: {e}")
        return False

def test_blood_bank_system():
    """Test blood bank system"""
    try:
        sys.path.append('ml_models')
        from blood_bank_system import BloodBankSystem
        
        logger.info("Testing Blood Bank System...")
        system = BloodBankSystem()
        
        # Test blood availability
        try:
            availability = system.check_blood_availability('O+', 'Delhi')
            logger.info(f"✅ Blood availability test: {availability['total_units_available']} units found")
        except Exception as e:
            logger.error(f"❌ Blood availability test failed: {e}")
            return False
        
        # Test donor matching
        try:
            donors = system.find_compatible_donors('O+', 'Delhi')
            logger.info(f"✅ Donor matching test: {len(donors)} compatible donors found")
        except Exception as e:
            logger.error(f"❌ Donor matching test failed: {e}")
            return False
        
        logger.info("✅ Blood bank system test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Blood bank system test failed: {e}")
        return False

def main():
    """Main test function"""
    logger.info("🧪 Testing ML Models")
    logger.info("=" * 40)
    
    tests = [
        ("Nutrition Model", test_nutrition_model),
        ("Physiotherapy Model", test_physio_model),
        ("Blood Bank System", test_blood_bank_system)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_function in tests:
        logger.info(f"\n📋 Testing {test_name}...")
        if test_function():
            passed += 1
        else:
            logger.error(f"❌ {test_name} failed")
    
    logger.info("\n" + "=" * 40)
    logger.info(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All ML models are working correctly!")
        logger.info("You can now start the server with: python start_platform.py")
    else:
        logger.error("⚠️  Some tests failed. Please check the errors above.")
        return False
    
    return True

if __name__ == "__main__":
    main()
