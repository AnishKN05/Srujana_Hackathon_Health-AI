"""
Physiotherapy Classification ML Model
Trained to provide exercise recommendations, injury assessment, and rehabilitation guidance
"""
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, accuracy_score
import joblib
import json
import os
import logging
from typing import List, Dict, Tuple, Any
import re

logger = logging.getLogger(__name__)

class PhysioClassifier:
    def __init__(self, model_path: str = "ml_models/trained_models/"):
        self.model_path = model_path
        self.model = None
        self.vectorizer = None
        self.physio_categories = [
            'back_pain',
            'neck_pain',
            'knee_pain',
            'shoulder_pain',
            'ankle_injury',
            'wrist_injury',
            'posture_correction',
            'strength_training',
            'flexibility',
            'balance_training',
            'cardio_fitness',
            'sports_injury',
            'rehabilitation',
            'prevention',
            'ergonomics'
        ]
        
        self.physio_responses = {
            'back_pain': {
                'description': 'Back pain management and strengthening exercises',
                'recommendations': [
                    'Practice gentle stretching exercises daily',
                    'Strengthen core muscles with planks and bridges',
                    'Maintain proper posture throughout the day',
                    'Avoid prolonged sitting - take breaks every hour',
                    'Use proper lifting techniques'
                ],
                'exercises': [
                    'Cat-cow stretches',
                    'Child\'s pose',
                    'Pelvic tilts',
                    'Bird-dog exercise',
                    'Dead bug exercise',
                    'Glute bridges',
                    'Wall sits'
                ],
                'precautions': [
                    'Avoid heavy lifting during acute pain',
                    'Stop exercises if pain increases',
                    'Consult healthcare provider for severe pain',
                    'Use ice/heat therapy as needed'
                ]
            },
            'neck_pain': {
                'description': 'Neck pain relief and posture improvement',
                'recommendations': [
                    'Practice neck stretches and range of motion exercises',
                    'Strengthen neck and upper back muscles',
                    'Improve workstation ergonomics',
                    'Use proper pillow support while sleeping',
                    'Take frequent breaks from computer work'
                ],
                'exercises': [
                    'Neck rotations',
                    'Chin tucks',
                    'Shoulder blade squeezes',
                    'Upper trapezius stretches',
                    'Levator scapulae stretches',
                    'Cervical retraction',
                    'Neck side bends'
                ],
                'precautions': [
                    'Move slowly and gently',
                    'Stop if dizziness occurs',
                    'Avoid sudden jerky movements',
                    'Consult if pain radiates to arms'
                ]
            },
            'knee_pain': {
                'description': 'Knee pain management and joint strengthening',
                'recommendations': [
                    'Strengthen quadriceps and hamstrings',
                    'Improve flexibility in hip and ankle',
                    'Use proper footwear and orthotics if needed',
                    'Maintain healthy weight to reduce joint stress',
                    'Avoid high-impact activities during pain'
                ],
                'exercises': [
                    'Straight leg raises',
                    'Wall sits',
                    'Clamshells',
                    'Heel slides',
                    'Quad sets',
                    'Hamstring stretches',
                    'Calf raises'
                ],
                'precautions': [
                    'Avoid deep squats during acute pain',
                    'Use pain as a guide for exercise intensity',
                    'Consider low-impact alternatives',
                    'Consult for severe swelling or instability'
                ]
            },
            'shoulder_pain': {
                'description': 'Shoulder pain relief and rotator cuff strengthening',
                'recommendations': [
                    'Strengthen rotator cuff muscles',
                    'Improve shoulder blade stability',
                    'Maintain proper shoulder posture',
                    'Avoid overhead activities during pain',
                    'Use ice therapy for inflammation'
                ],
                'exercises': [
                    'Pendulum exercises',
                    'Wall slides',
                    'External rotation with band',
                    'Internal rotation with band',
                    'Scapular retraction',
                    'Doorway chest stretch',
                    'Sleeper stretch'
                ],
                'precautions': [
                    'Avoid overhead lifting during pain',
                    'Stop if pain increases significantly',
                    'Use proper form for all exercises',
                    'Consult for severe pain or weakness'
                ]
            },
            'ankle_injury': {
                'description': 'Ankle injury rehabilitation and strengthening',
                'recommendations': [
                    'Follow RICE protocol (Rest, Ice, Compression, Elevation)',
                    'Gradually restore range of motion',
                    'Strengthen ankle stabilizers',
                    'Improve balance and proprioception',
                    'Use proper footwear and support'
                ],
                'exercises': [
                    'Ankle alphabet exercises',
                    'Calf raises',
                    'Single leg balance',
                    'Ankle circles',
                    'Resistance band exercises',
                    'Heel and toe walks',
                    'Balance board training'
                ],
                'precautions': [
                    'Follow medical clearance for weight-bearing',
                    'Progress gradually with exercises',
                    'Stop if pain increases',
                    'Use ankle support as recommended'
                ]
            },
            'wrist_injury': {
                'description': 'Wrist pain management and strengthening',
                'recommendations': [
                    'Rest and protect the injured wrist',
                    'Gradually restore range of motion',
                    'Strengthen forearm muscles',
                    'Improve ergonomics at work',
                    'Use proper typing and mouse techniques'
                ],
                'exercises': [
                    'Wrist flexion and extension',
                    'Wrist circles',
                    'Grip strengthening',
                    'Finger stretches',
                    'Tendon gliding exercises',
                    'Wrist pronation/supination',
                    'Resistance band exercises'
                ],
                'precautions': [
                    'Avoid repetitive strain activities',
                    'Use ergonomic equipment',
                    'Take frequent breaks',
                    'Consult for severe pain or numbness'
                ]
            },
            'posture_correction': {
                'description': 'Posture improvement and ergonomic guidance',
                'recommendations': [
                    'Strengthen core and back muscles',
                    'Stretch tight chest and hip flexors',
                    'Set up ergonomic workstation',
                    'Practice good posture habits',
                    'Take regular movement breaks'
                ],
                'exercises': [
                    'Wall angels',
                    'Chest stretches',
                    'Hip flexor stretches',
                    'Plank variations',
                    'Bird-dog exercise',
                    'Thoracic spine mobility',
                    'Glute bridges'
                ],
                'precautions': [
                    'Progress gradually with exercises',
                    'Maintain neutral spine position',
                    'Use proper ergonomic setup',
                    'Listen to your body'
                ]
            },
            'strength_training': {
                'description': 'General strength training and muscle building',
                'recommendations': [
                    'Start with bodyweight exercises',
                    'Focus on proper form over weight',
                    'Progressive overload principle',
                    'Include all major muscle groups',
                    'Allow adequate rest between sessions'
                ],
                'exercises': [
                    'Push-ups',
                    'Squats',
                    'Lunges',
                    'Planks',
                    'Pull-ups or rows',
                    'Deadlifts (with proper form)',
                    'Overhead press'
                ],
                'precautions': [
                    'Warm up before exercising',
                    'Use proper lifting techniques',
                    'Start with lighter weights',
                    'Consult trainer for proper form'
                ]
            },
            'flexibility': {
                'description': 'Flexibility training and mobility improvement',
                'recommendations': [
                    'Stretch after warming up',
                    'Hold stretches for 30-60 seconds',
                    'Focus on major muscle groups',
                    'Include dynamic and static stretching',
                    'Practice regularly for best results'
                ],
                'exercises': [
                    'Hamstring stretches',
                    'Quad stretches',
                    'Calf stretches',
                    'Hip flexor stretches',
                    'Shoulder stretches',
                    'Spinal twists',
                    'Neck and back stretches'
                ],
                'precautions': [
                    'Warm up before stretching',
                    'Avoid bouncing in stretches',
                    'Stop if you feel sharp pain',
                    'Breathe deeply during stretches'
                ]
            },
            'balance_training': {
                'description': 'Balance improvement and fall prevention',
                'recommendations': [
                    'Start with simple balance exercises',
                    'Progress to more challenging positions',
                    'Include single-leg exercises',
                    'Practice on different surfaces',
                    'Use support initially if needed'
                ],
                'exercises': [
                    'Single leg stand',
                    'Tandem walking',
                    'Heel-to-toe walk',
                    'Standing on one foot',
                    'Balance board exercises',
                    'Yoga tree pose',
                    'Tai chi movements'
                ],
                'precautions': [
                    'Use support for safety',
                    'Progress gradually',
                    'Stop if you feel unsteady',
                    'Practice in safe environment'
                ]
            }
        }
        
        self.exercise_programs = {
            'beginner': {
                'duration': '20-30 minutes',
                'frequency': '3-4 times per week',
                'intensity': 'Low to moderate',
                'focus': 'Basic movements and form'
            },
            'intermediate': {
                'duration': '30-45 minutes',
                'frequency': '4-5 times per week',
                'intensity': 'Moderate',
                'focus': 'Increased strength and endurance'
            },
            'advanced': {
                'duration': '45-60 minutes',
                'frequency': '5-6 times per week',
                'intensity': 'Moderate to high',
                'focus': 'Performance and skill development'
            }
        }
    
    def create_synthetic_data(self, num_samples: int = 1000) -> Tuple[List[str], List[str]]:
        """Create synthetic training data for physiotherapy classification"""
        logger.info("Creating synthetic physiotherapy training data...")
        
        queries = []
        categories = []
        
        # Back pain queries
        back_pain_queries = [
            "I have lower back pain, what exercises can help?",
            "How to relieve back pain?",
            "Best exercises for back pain",
            "Back strengthening exercises",
            "Lower back pain relief",
            "Core exercises for back pain",
            "Stretches for back pain",
            "Back pain management",
            "How to prevent back pain?",
            "Back pain exercises at home"
        ]
        
        # Neck pain queries
        neck_pain_queries = [
            "I have neck pain, what can I do?",
            "Neck pain relief exercises",
            "How to fix neck pain?",
            "Neck strengthening exercises",
            "Stretches for neck pain",
            "Computer neck pain relief",
            "Neck pain from poor posture",
            "Cervical spine exercises",
            "Neck pain management",
            "Upper back and neck exercises"
        ]
        
        # Knee pain queries
        knee_pain_queries = [
            "I have knee pain, what exercises help?",
            "Knee strengthening exercises",
            "How to reduce knee pain?",
            "Knee rehabilitation exercises",
            "Quad strengthening for knees",
            "Knee pain relief exercises",
            "Low impact knee exercises",
            "Knee joint strengthening",
            "Knee pain management",
            "Exercises for knee injury"
        ]
        
        # Shoulder pain queries
        shoulder_pain_queries = [
            "I have shoulder pain, what exercises?",
            "Shoulder strengthening exercises",
            "Rotator cuff exercises",
            "Shoulder pain relief",
            "Shoulder rehabilitation",
            "Frozen shoulder exercises",
            "Shoulder impingement exercises",
            "Shoulder mobility exercises",
            "Shoulder pain management",
            "Upper body strengthening"
        ]
        
        # Ankle injury queries
        ankle_injury_queries = [
            "I sprained my ankle, what exercises?",
            "Ankle strengthening exercises",
            "Ankle rehabilitation program",
            "Balance exercises for ankle",
            "Ankle mobility exercises",
            "Ankle injury recovery",
            "Ankle stability exercises",
            "Foot and ankle strengthening",
            "Ankle pain relief",
            "Post-ankle injury exercises"
        ]
        
        # Posture correction queries
        posture_queries = [
            "How to improve my posture?",
            "Posture correction exercises",
            "Exercises for better posture",
            "Back strengthening for posture",
            "Posture improvement program",
            "Ergonomic exercises",
            "Posture awareness exercises",
            "Core exercises for posture",
            "Posture correction stretches",
            "How to fix rounded shoulders?"
        ]
        
        # Strength training queries
        strength_queries = [
            "What are good strength training exercises?",
            "How to build muscle strength?",
            "Bodyweight strength exercises",
            "Strength training for beginners",
            "Muscle building exercises",
            "Functional strength training",
            "Strength training program",
            "Progressive strength training",
            "Strength exercises at home",
            "How to get stronger?"
        ]
        
        # Flexibility queries
        flexibility_queries = [
            "How to improve flexibility?",
            "Best stretching exercises",
            "Flexibility training program",
            "Mobility exercises",
            "Stretching routine",
            "How to become more flexible?",
            "Flexibility exercises for beginners",
            "Daily stretching routine",
            "Flexibility improvement",
            "Stretching for tight muscles"
        ]
        
        # Balance training queries
        balance_queries = [
            "How to improve balance?",
            "Balance training exercises",
            "Fall prevention exercises",
            "Balance improvement program",
            "Single leg balance exercises",
            "Balance exercises for seniors",
            "Proprioception training",
            "Balance and coordination",
            "Stability exercises",
            "How to prevent falls?"
        ]
        
        # Combine all queries
        all_queries = [
            (back_pain_queries, 'back_pain'),
            (neck_pain_queries, 'neck_pain'),
            (knee_pain_queries, 'knee_pain'),
            (shoulder_pain_queries, 'shoulder_pain'),
            (ankle_injury_queries, 'ankle_injury'),
            (posture_queries, 'posture_correction'),
            (strength_queries, 'strength_training'),
            (flexibility_queries, 'flexibility'),
            (balance_queries, 'balance_training')
        ]
        
        for query_list, category in all_queries:
            for query in query_list:
                queries.append(query)
                categories.append(category)
        
        # Add variations and additional samples
        for _ in range(num_samples - len(queries)):
            category = np.random.choice(self.physio_categories[:9])  # Use first 9 categories
            base_query = np.random.choice([
                "What exercises help with",
                "How to treat",
                "Best exercises for",
                "Rehabilitation for",
                "Strengthening exercises for",
                "Pain relief for"
            ])
            
            query = f"{base_query} {category.replace('_', ' ')}"
            queries.append(query)
            categories.append(category)
        
        return queries, categories
    
    def train_model(self, queries: List[str], categories: List[str]) -> Dict[str, Any]:
        """Train the physiotherapy classification model"""
        logger.info("Starting physiotherapy model training...")
        
        # Vectorize the text data
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2),
            lowercase=True
        )
        
        X = self.vectorizer.fit_transform(queries)
        y = categories
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Try different models
        models = {
            'random_forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'gradient_boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
            'logistic_regression': LogisticRegression(random_state=42, max_iter=1000)
        }
        
        best_model = None
        best_score = 0
        best_model_name = ''
        
        for name, model in models.items():
            # Cross-validation
            cv_scores = cross_val_score(model, X_train, y_train, cv=5)
            mean_score = cv_scores.mean()
            
            logger.info(f"{name} CV score: {mean_score:.4f}")
            
            if mean_score > best_score:
                best_score = mean_score
                best_model = model
                best_model_name = name
        
        # Train the best model
        best_model.fit(X_train, y_train)
        
        # Test the model
        y_pred = best_model.predict(X_test)
        test_accuracy = accuracy_score(y_test, y_pred)
        
        logger.info(f"Best model: {best_model_name}")
        logger.info(f"Test accuracy: {test_accuracy:.4f}")
        
        # Save the model
        self.model = best_model
        self.save_model()
        
        return {
            'model_name': best_model_name,
            'test_accuracy': test_accuracy,
            'cv_score': best_score,
            'classification_report': classification_report(y_test, y_pred, output_dict=True)
        }
    
    def predict_physio_category(self, query: str) -> Dict[str, Any]:
        """Predict physiotherapy category from user query"""
        if self.model is None or self.vectorizer is None:
            self.load_model()
        
        # Preprocess the query
        processed_query = self.vectorizer.transform([query])
        
        # Make prediction
        prediction = self.model.predict(processed_query)[0]
        probabilities = self.model.predict_proba(processed_query)[0]
        
        # Get confidence score
        confidence = max(probabilities)
        
        # Get category information
        category_info = self.physio_responses.get(prediction, {})
        
        return {
            'category': prediction,
            'confidence': float(confidence),
            'description': category_info.get('description', ''),
            'recommendations': category_info.get('recommendations', []),
            'exercises': category_info.get('exercises', []),
            'precautions': category_info.get('precautions', [])
        }
    
    def generate_physio_response(self, query: str, user_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate comprehensive physiotherapy response"""
        prediction = self.predict_physio_category(query)
        
        # Customize response based on user context
        if user_context:
            age = user_context.get('age')
            fitness_level = user_context.get('fitness_level', 'beginner')
            medical_conditions = user_context.get('medical_conditions', [])
            
            # Add age-specific recommendations
            if age and age < 18:
                prediction['age_specific'] = "For teenagers, focus on proper form and gradual progression."
            elif age and age > 65:
                prediction['age_specific'] = "For seniors, prioritize safety and balance exercises."
            
            # Add fitness level considerations
            if fitness_level in self.exercise_programs:
                prediction['exercise_program'] = self.exercise_programs[fitness_level]
            
            # Add medical condition considerations
            if 'heart_disease' in medical_conditions:
                prediction['medical_considerations'] = "Consult your healthcare provider before starting any exercise program."
            elif 'diabetes' in medical_conditions:
                prediction['medical_considerations'] = "Monitor blood sugar levels during exercise."
        
        return {
            'query': query,
            'prediction': prediction,
            'timestamp': pd.Timestamp.now().isoformat(),
            'disclaimer': 'This physiotherapy advice is for educational purposes only. Consult a licensed physiotherapist for personalized treatment and exercise prescription.'
        }
    
    def save_model(self):
        """Save the trained model and vectorizer"""
        os.makedirs(self.model_path, exist_ok=True)
        
        # Save the model
        joblib.dump(self.model, os.path.join(self.model_path, 'physio_classifier.pkl'))
        
        # Save the vectorizer
        joblib.dump(self.vectorizer, os.path.join(self.model_path, 'physio_vectorizer.pkl'))
        
        # Save metadata
        metadata = {
            'physio_categories': self.physio_categories,
            'physio_responses': self.physio_responses,
            'exercise_programs': self.exercise_programs
        }
        
        with open(os.path.join(self.model_path, 'physio_metadata.json'), 'w') as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"Physiotherapy model saved to {self.model_path}")
    
    def load_model(self):
        """Load the trained model and vectorizer"""
        try:
            self.model = joblib.load(os.path.join(self.model_path, 'physio_classifier.pkl'))
            self.vectorizer = joblib.load(os.path.join(self.model_path, 'physio_vectorizer.pkl'))
            
            # Load metadata
            with open(os.path.join(self.model_path, 'physio_metadata.json'), 'r') as f:
                metadata = json.load(f)
                self.physio_categories = metadata['physio_categories']
                self.physio_responses = metadata['physio_responses']
                self.exercise_programs = metadata['exercise_programs']
            
            logger.info("Physiotherapy model loaded successfully")
        except FileNotFoundError:
            logger.warning("Physiotherapy model files not found. Training new model...")
            self.train_from_scratch()
    
    def train_from_scratch(self):
        """Train a new model from scratch"""
        queries, categories = self.create_synthetic_data()
        self.train_model(queries, categories)

# Training script
if __name__ == "__main__":
    classifier = PhysioClassifier()
    
    # Create and train the model
    queries, categories = classifier.create_synthetic_data()
    results = classifier.train_model(queries, categories)
    
    print("Training completed!")
    print(f"Best model: {results['model_name']}")
    print(f"Test accuracy: {results['test_accuracy']:.4f}")
    
    # Test the model
    test_queries = [
        "I have lower back pain, what exercises can help?",
        "How to improve my posture?",
        "What are good strength training exercises?",
        "I sprained my ankle, what exercises?"
    ]
    
    print("\nTest predictions:")
    for query in test_queries:
        prediction = classifier.predict_physio_category(query)
        print(f"Query: {query}")
        print(f"Category: {prediction['category']} (confidence: {prediction['confidence']:.3f})")
        print()
