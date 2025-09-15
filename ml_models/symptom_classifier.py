"""
Symptom Classification ML Model
Trained to classify symptoms and predict possible conditions
"""
import numpy as np
import pandas as pd
import joblib
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import LabelEncoder
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import logging
from typing import List, Dict, Tuple, Any
import os

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

logger = logging.getLogger(__name__)

class SymptomClassifier:
    def __init__(self, model_path: str = "ml_models/trained_models/"):
        self.model_path = model_path
        self.vectorizer = None
        self.label_encoder = None
        self.model = None
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
        # Medical condition categories
        self.condition_categories = {
            'respiratory': [
                'common_cold', 'flu', 'sinusitis', 'bronchitis', 'pneumonia', 
                'asthma', 'allergic_rhinitis', 'cough', 'sore_throat'
            ],
            'gastrointestinal': [
                'food_poisoning', 'gastroenteritis', 'indigestion', 'acid_reflux',
                'constipation', 'diarrhea', 'nausea', 'stomach_ulcer'
            ],
            'dermatological': [
                'acne', 'eczema', 'psoriasis', 'contact_dermatitis', 'rash',
                'hives', 'fungal_infection', 'bacterial_skin_infection'
            ],
            'musculoskeletal': [
                'back_pain', 'neck_pain', 'joint_pain', 'muscle_strain',
                'arthritis', 'fibromyalgia', 'tendonitis'
            ],
            'neurological': [
                'headache', 'migraine', 'dizziness', 'vertigo', 'tension_headache'
            ],
            'cardiovascular': [
                'chest_pain', 'heart_palpitations', 'hypertension', 'angina'
            ],
            'mental_health': [
                'anxiety', 'depression', 'stress', 'panic_attack', 'insomnia'
            ],
            'general': [
                'fatigue', 'fever', 'dehydration', 'vitamin_deficiency', 'anemia'
            ]
        }
        
        # Symptom to condition mapping
        self.symptom_condition_mapping = self._create_symptom_mapping()
        
    def _create_symptom_mapping(self) -> Dict[str, List[str]]:
        """Create mapping from symptoms to possible conditions"""
        mapping = {
            # Respiratory symptoms
            'cough': ['common_cold', 'flu', 'bronchitis', 'pneumonia', 'asthma'],
            'sore_throat': ['common_cold', 'flu', 'strep_throat', 'tonsillitis'],
            'runny_nose': ['common_cold', 'flu', 'allergic_rhinitis', 'sinusitis'],
            'congestion': ['common_cold', 'flu', 'sinusitis', 'allergic_rhinitis'],
            'shortness_of_breath': ['asthma', 'pneumonia', 'anxiety', 'heart_condition'],
            
            # Gastrointestinal symptoms
            'nausea': ['food_poisoning', 'gastroenteritis', 'migraine', 'pregnancy'],
            'vomiting': ['food_poisoning', 'gastroenteritis', 'migraine'],
            'diarrhea': ['food_poisoning', 'gastroenteritis', 'ibs', 'infection'],
            'stomach_pain': ['food_poisoning', 'gastroenteritis', 'indigestion', 'ulcer'],
            'abdominal_cramps': ['food_poisoning', 'gastroenteritis', 'ibs', 'menstrual'],
            
            # Dermatological symptoms
            'rash': ['allergic_reaction', 'eczema', 'psoriasis', 'viral_rash'],
            'itching': ['allergic_reaction', 'eczema', 'fungal_infection', 'dry_skin'],
            'redness': ['allergic_reaction', 'infection', 'irritation', 'sunburn'],
            'swelling': ['allergic_reaction', 'infection', 'injury', 'inflammation'],
            
            # Neurological symptoms
            'headache': ['tension_headache', 'migraine', 'sinusitis', 'dehydration'],
            'dizziness': ['dehydration', 'low_blood_pressure', 'vertigo', 'anxiety'],
            'fatigue': ['anemia', 'depression', 'thyroid_issue', 'sleep_disorder'],
            
            # Musculoskeletal symptoms
            'back_pain': ['muscle_strain', 'poor_posture', 'herniated_disc', 'arthritis'],
            'joint_pain': ['arthritis', 'injury', 'overuse', 'inflammatory_condition'],
            'muscle_ache': ['flu', 'overexertion', 'fibromyalgia', 'dehydration'],
            
            # General symptoms
            'fever': ['infection', 'flu', 'cold', 'inflammatory_condition'],
            'chills': ['fever', 'infection', 'flu', 'anxiety'],
            'sweating': ['fever', 'anxiety', 'menopause', 'infection']
        }
        return mapping
    
    def preprocess_text(self, text: str) -> str:
        """Preprocess text for ML model"""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Tokenize and lemmatize
        words = nltk.word_tokenize(text)
        words = [self.lemmatizer.lemmatize(word) for word in words if word not in self.stop_words]
        
        return ' '.join(words)
    
    def create_synthetic_data(self) -> Tuple[List[str], List[str]]:
        """Create synthetic training data for symptom classification"""
        symptoms = []
        conditions = []
        
        # Generate synthetic data based on symptom-condition mapping
        for symptom, possible_conditions in self.symptom_condition_mapping.items():
            for condition in possible_conditions:
                # Create multiple variations of symptom descriptions
                variations = [
                    f"I have {symptom.replace('_', ' ')}",
                    f"I'm experiencing {symptom.replace('_', ' ')}",
                    f"I feel {symptom.replace('_', ' ')}",
                    f"I've been having {symptom.replace('_', ' ')}",
                    f"{symptom.replace('_', ' ')} is bothering me",
                    f"I have severe {symptom.replace('_', ' ')}",
                    f"I have mild {symptom.replace('_', ' ')}",
                    f"I have chronic {symptom.replace('_', ' ')}"
                ]
                
                symptoms.extend(variations)
                conditions.extend([condition] * len(variations))
        
        # Add some general health complaints
        general_symptoms = [
            "I don't feel well", "I'm sick", "I feel unwell", "I'm not feeling good",
            "I feel terrible", "I feel awful", "I'm under the weather"
        ]
        symptoms.extend(general_symptoms)
        conditions.extend(['general_malaise'] * len(general_symptoms))
        
        return symptoms, conditions
    
    def train_model(self, X: List[str], y: List[str]) -> Dict[str, Any]:
        """Train the symptom classification model"""
        logger.info("Starting model training...")
        
        # Preprocess the text data
        X_processed = [self.preprocess_text(text) for text in X]
        
        # Create TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.95
        )
        
        # Fit and transform the data
        X_tfidf = self.vectorizer.fit_transform(X_processed)
        
        # Encode labels
        self.label_encoder = LabelEncoder()
        y_encoded = self.label_encoder.fit_transform(y)
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X_tfidf, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
        )
        
        # Train multiple models and select the best one
        models = {
            'random_forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'gradient_boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
            'logistic_regression': LogisticRegression(random_state=42, max_iter=1000)
        }
        
        best_model = None
        best_score = 0
        best_model_name = ""
        
        for name, model in models.items():
            # Cross-validation score
            cv_scores = cross_val_score(model, X_train, y_train, cv=5)
            mean_score = cv_scores.mean()
            
            logger.info(f"{name} CV Score: {mean_score:.4f}")
            
            if mean_score > best_score:
                best_score = mean_score
                best_model = model
                best_model_name = name
        
        # Train the best model
        best_model.fit(X_train, y_train)
        self.model = best_model
        
        # Evaluate on test set
        y_pred = best_model.predict(X_test)
        test_accuracy = accuracy_score(y_test, y_pred)
        
        logger.info(f"Best model: {best_model_name}")
        logger.info(f"Test accuracy: {test_accuracy:.4f}")
        
        # Save the model
        self.save_model()
        
        return {
            'model_name': best_model_name,
            'cv_score': best_score,
            'test_accuracy': test_accuracy,
            'classification_report': classification_report(y_test, y_pred, output_dict=True)
        }
    
    def predict_condition(self, symptoms: List[str], additional_info: str = "") -> Dict[str, Any]:
        """Predict possible conditions based on symptoms"""
        if not self.model or not self.vectorizer or not self.label_encoder:
            self.load_model()
        
        # Combine symptoms and additional info
        combined_text = ' '.join(symptoms)
        if additional_info:
            combined_text += ' ' + additional_info
        
        # Preprocess the text
        processed_text = self.preprocess_text(combined_text)
        
        # Transform using the trained vectorizer
        X_tfidf = self.vectorizer.transform([processed_text])
        
        # Get predictions
        prediction_proba = self.model.predict_proba(X_tfidf)[0]
        prediction = self.model.predict(X_tfidf)[0]
        
        # Get top 3 predictions
        top_indices = np.argsort(prediction_proba)[-3:][::-1]
        
        results = []
        for idx in top_indices:
            condition = self.label_encoder.inverse_transform([idx])[0]
            probability = prediction_proba[idx]
            
            # Get condition category
            category = self._get_condition_category(condition)
            
            results.append({
                'condition_name': condition.replace('_', ' ').title(),
                'probability': float(probability),
                'category': category,
                'description': self._get_condition_description(condition),
                'severity': self._get_condition_severity(condition)
            })
        
        return {
            'possible_conditions': results,
            'confidence_score': float(max(prediction_proba)),
            'primary_condition': results[0] if results else None
        }
    
    def _get_condition_category(self, condition: str) -> str:
        """Get the category for a condition"""
        for category, conditions in self.condition_categories.items():
            if condition in conditions:
                return category
        return 'general'
    
    def _get_condition_description(self, condition: str) -> str:
        """Get description for a condition"""
        descriptions = {
            'common_cold': 'Viral infection of the upper respiratory tract',
            'flu': 'Influenza viral infection affecting the respiratory system',
            'headache': 'Pain or discomfort in the head or neck area',
            'migraine': 'Severe headache often accompanied by nausea and sensitivity to light',
            'food_poisoning': 'Illness caused by consuming contaminated food',
            'gastroenteritis': 'Inflammation of the stomach and intestines',
            'rash': 'Change in skin appearance, often red, itchy, or irritated',
            'eczema': 'Chronic skin condition causing inflammation and irritation',
            'back_pain': 'Pain in the back, often in the lower back region',
            'anxiety': 'Feeling of worry, nervousness, or unease',
            'fatigue': 'Extreme tiredness or lack of energy',
            'fever': 'Elevated body temperature, often indicating infection'
        }
        return descriptions.get(condition, f'Medical condition: {condition.replace("_", " ")}')
    
    def _get_condition_severity(self, condition: str) -> str:
        """Get severity level for a condition"""
        high_severity = ['pneumonia', 'heart_condition', 'severe_allergic_reaction']
        moderate_severity = ['flu', 'migraine', 'gastroenteritis', 'asthma']
        
        if condition in high_severity:
            return 'high'
        elif condition in moderate_severity:
            return 'moderate'
        else:
            return 'low'
    
    def save_model(self):
        """Save the trained model and components"""
        os.makedirs(self.model_path, exist_ok=True)
        
        # Save model components
        joblib.dump(self.model, os.path.join(self.model_path, 'symptom_model.pkl'))
        joblib.dump(self.vectorizer, os.path.join(self.model_path, 'vectorizer.pkl'))
        joblib.dump(self.label_encoder, os.path.join(self.model_path, 'label_encoder.pkl'))
        
        logger.info(f"Model saved to {self.model_path}")
    
    def load_model(self):
        """Load the trained model and components"""
        try:
            self.model = joblib.load(os.path.join(self.model_path, 'symptom_model.pkl'))
            self.vectorizer = joblib.load(os.path.join(self.model_path, 'vectorizer.pkl'))
            self.label_encoder = joblib.load(os.path.join(self.model_path, 'label_encoder.pkl'))
            logger.info("Model loaded successfully")
        except FileNotFoundError:
            logger.warning("Model files not found. Training new model...")
            self.train_from_scratch()
    
    def train_from_scratch(self):
        """Train a new model from scratch"""
        symptoms, conditions = self.create_synthetic_data()
        self.train_model(symptoms, conditions)

# Training script
if __name__ == "__main__":
    classifier = SymptomClassifier()
    
    # Create and train the model
    symptoms, conditions = classifier.create_synthetic_data()
    results = classifier.train_model(symptoms, conditions)
    
    print("Training completed!")
    print(f"Best model: {results['model_name']}")
    print(f"Test accuracy: {results['test_accuracy']:.4f}")
    
    # Test the model
    test_symptoms = ["I have a headache and feel tired", "I have a rash on my arm"]
    for symptom in test_symptoms:
        prediction = classifier.predict_condition([symptom])
        print(f"\nSymptoms: {symptom}")
        print(f"Prediction: {prediction}")
