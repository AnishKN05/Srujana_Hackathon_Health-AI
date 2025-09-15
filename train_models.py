#!/usr/bin/env python3
"""
Training script for ML models
Trains both symptom classification and image classification models
"""
import os
import sys
import logging
import argparse
from pathlib import Path

# Add ml_models to path
sys.path.append('ml_models')

from symptom_classifier import SymptomClassifier
from image_classifier import SkinConditionClassifier
from nutrition_classifier import NutritionClassifier
from physio_classifier import PhysioClassifier
from blood_bank_system import BloodBankSystem

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def train_symptom_classifier():
    """Train the symptom classification model"""
    logger.info("Starting symptom classifier training...")
    
    try:
        classifier = SymptomClassifier()
        
        # Create synthetic training data
        symptoms, conditions = classifier.create_synthetic_data()
        logger.info(f"Created {len(symptoms)} training samples")
        
        # Train the model
        results = classifier.train_model(symptoms, conditions)
        
        logger.info("Symptom classifier training completed!")
        logger.info(f"Best model: {results['model_name']}")
        logger.info(f"Test accuracy: {results['test_accuracy']:.4f}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error training symptom classifier: {str(e)}")
        return False

def train_image_classifier():
    """Train the image classification model"""
    logger.info("Starting image classifier training...")
    
    try:
        classifier = SkinConditionClassifier()
        
        # Create synthetic training data
        X, y = classifier.create_synthetic_data(num_samples_per_class=200)
        logger.info(f"Created {len(X)} training images")
        
        # Train the model
        results = classifier.train_model(X, y)
        
        logger.info("Image classifier training completed!")
        logger.info(f"Test accuracy: {results['test_accuracy']:.4f}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error training image classifier: {str(e)}")
        return False

def train_nutrition_classifier():
    """Train the nutrition classification model"""
    logger.info("Starting nutrition classifier training...")
    
    try:
        classifier = NutritionClassifier()
        
        # Create synthetic training data
        queries, categories = classifier.create_synthetic_data()
        logger.info(f"Created {len(queries)} training samples")
        
        # Train the model
        results = classifier.train_model(queries, categories)
        
        logger.info("Nutrition classifier training completed!")
        logger.info(f"Best model: {results['model_name']}")
        logger.info(f"Test accuracy: {results['test_accuracy']:.4f}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error training nutrition classifier: {str(e)}")
        return False

def train_physio_classifier():
    """Train the physiotherapy classification model"""
    logger.info("Starting physiotherapy classifier training...")
    
    try:
        classifier = PhysioClassifier()
        
        # Create synthetic training data
        queries, categories = classifier.create_synthetic_data()
        logger.info(f"Created {len(queries)} training samples")
        
        # Train the model
        results = classifier.train_model(queries, categories)
        
        logger.info("Physiotherapy classifier training completed!")
        logger.info(f"Best model: {results['model_name']}")
        logger.info(f"Test accuracy: {results['test_accuracy']:.4f}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error training physiotherapy classifier: {str(e)}")
        return False

def train_blood_bank_system():
    """Train the blood bank system"""
    logger.info("Starting blood bank system training...")
    
    try:
        system = BloodBankSystem()
        
        # Create synthetic training data
        queries, categories = system.create_synthetic_data()
        logger.info(f"Created {len(queries)} training samples")
        
        # Train the model
        results = system.train_model(queries, categories)
        
        logger.info("Blood bank system training completed!")
        logger.info(f"Test accuracy: {results['test_accuracy']:.4f}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error training blood bank system: {str(e)}")
        return False

def test_models():
    """Test the trained models"""
    logger.info("Testing trained models...")
    
    try:
        # Test symptom classifier
        symptom_classifier = SymptomClassifier()
        symptom_classifier.load_model()
        
        test_symptoms = [
            "I have a headache and feel tired",
            "I have a rash on my arm",
            "I'm experiencing chest pain",
            "I have a fever and sore throat"
        ]
        
        logger.info("Testing symptom classifier:")
        for symptom in test_symptoms:
            prediction = symptom_classifier.predict_condition([symptom])
            logger.info(f"Symptoms: {symptom}")
            logger.info(f"Prediction: {prediction['primary_condition']['condition_name']} "
                       f"(confidence: {prediction['confidence_score']:.3f})")
        
        # Test image classifier
        image_classifier = SkinConditionClassifier()
        image_classifier.load_model()
        
        test_conditions = ['acne', 'rash', 'wound', 'normal_skin']
        
        logger.info("\nTesting image classifier:")
        for condition in test_conditions:
            test_image = image_classifier._generate_synthetic_image(condition)
            prediction = image_classifier.predict_condition(test_image)
            logger.info(f"Test condition: {condition}")
            logger.info(f"Prediction: {prediction['primary_condition']['condition_name']} "
                       f"(confidence: {prediction['confidence_score']:.3f})")
        
        logger.info("Model testing completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Error testing models: {str(e)}")
        return False

def main():
    """Main training function"""
    parser = argparse.ArgumentParser(description='Train ML models for health assessment')
    parser.add_argument('--symptom', action='store_true', help='Train symptom classifier')
    parser.add_argument('--image', action='store_true', help='Train image classifier')
    parser.add_argument('--nutrition', action='store_true', help='Train nutrition classifier')
    parser.add_argument('--physio', action='store_true', help='Train physiotherapy classifier')
    parser.add_argument('--blood', action='store_true', help='Train blood bank system')
    parser.add_argument('--all', action='store_true', help='Train all models')
    parser.add_argument('--test', action='store_true', help='Test trained models')
    
    args = parser.parse_args()
    
    # Create models directory
    os.makedirs('ml_models/trained_models', exist_ok=True)
    
    success = True
    
    if args.test:
        success = test_models()
    elif args.all or (not args.symptom and not args.image and not args.nutrition and not args.physio and not args.blood):
        # Train all models by default
        logger.info("Training all models...")
        success = (train_symptom_classifier() and 
                  train_image_classifier() and 
                  train_nutrition_classifier() and 
                  train_physio_classifier() and 
                  train_blood_bank_system())
    else:
        if args.symptom:
            success = train_symptom_classifier()
        if args.image:
            success = train_image_classifier() and success
        if args.nutrition:
            success = train_nutrition_classifier() and success
        if args.physio:
            success = train_physio_classifier() and success
        if args.blood:
            success = train_blood_bank_system() and success
    
    if success:
        logger.info("All operations completed successfully!")
        logger.info("Models are ready for use in the health assessment platform.")
    else:
        logger.error("Some operations failed. Check the logs for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()
