"""
Nutrition Classification ML Model
Trained to provide dietary recommendations, meal planning, and nutrition advice
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

class NutritionClassifier:
    def __init__(self, model_path: str = "ml_models/trained_models/"):
        self.model_path = model_path
        self.model = None
        self.vectorizer = None
        self.nutrition_categories = [
            'weight_loss',
            'weight_gain',
            'diabetes_management',
            'heart_health',
            'muscle_building',
            'general_health',
            'pregnancy_nutrition',
            'child_nutrition',
            'elderly_nutrition',
            'sports_nutrition',
            'vegetarian_vegan',
            'food_allergies',
            'digestive_health',
            'immune_support',
            'bone_health'
        ]
        
        self.nutrition_responses = {
            'weight_loss': {
                'description': 'Weight loss and healthy eating guidance',
                'recommendations': [
                    'Focus on whole foods: vegetables, fruits, lean proteins, and whole grains',
                    'Control portion sizes and eat mindfully',
                    'Stay hydrated with water throughout the day',
                    'Limit processed foods, sugary drinks, and high-calorie snacks',
                    'Include regular physical activity in your routine'
                ],
                'foods_to_include': [
                    'Leafy greens (spinach, kale, lettuce)',
                    'Lean proteins (chicken breast, fish, tofu)',
                    'Whole grains (brown rice, quinoa, oats)',
                    'Healthy fats (avocado, nuts, olive oil)',
                    'Low-calorie fruits (berries, apples, citrus)'
                ],
                'foods_to_avoid': [
                    'Processed foods and fast food',
                    'Sugary drinks and sodas',
                    'High-calorie snacks and desserts',
                    'Fried foods and excessive oils',
                    'Alcohol in excess'
                ]
            },
            'weight_gain': {
                'description': 'Healthy weight gain and muscle building nutrition',
                'recommendations': [
                    'Eat more frequent, nutrient-dense meals',
                    'Include healthy fats and proteins in each meal',
                    'Choose whole foods over processed options',
                    'Stay consistent with meal timing',
                    'Combine with strength training exercises'
                ],
                'foods_to_include': [
                    'Lean proteins (chicken, fish, eggs, dairy)',
                    'Healthy fats (nuts, seeds, olive oil, avocado)',
                    'Complex carbohydrates (sweet potatoes, brown rice, oats)',
                    'Dairy products (milk, yogurt, cheese)',
                    'Nutrient-dense snacks (trail mix, protein bars)'
                ],
                'foods_to_avoid': [
                    'Empty calories from junk food',
                    'Excessive processed foods',
                    'Too much sugar and refined carbs',
                    'Unhealthy fats and trans fats'
                ]
            },
            'diabetes_management': {
                'description': 'Blood sugar management and diabetes-friendly nutrition',
                'recommendations': [
                    'Monitor carbohydrate intake and timing',
                    'Choose low glycemic index foods',
                    'Eat regular, balanced meals',
                    'Include fiber-rich foods',
                    'Limit added sugars and refined carbohydrates'
                ],
                'foods_to_include': [
                    'Non-starchy vegetables (broccoli, spinach, peppers)',
                    'Lean proteins (fish, chicken, beans)',
                    'Whole grains (quinoa, brown rice, oats)',
                    'Healthy fats (nuts, olive oil, avocado)',
                    'Low-sugar fruits (berries, apples)'
                ],
                'foods_to_avoid': [
                    'Sugary drinks and desserts',
                    'White bread and refined grains',
                    'Processed foods with added sugars',
                    'High-carb snacks and candies',
                    'Excessive fruit juices'
                ]
            },
            'heart_health': {
                'description': 'Cardiovascular health and heart-friendly nutrition',
                'recommendations': [
                    'Reduce sodium intake',
                    'Include omega-3 fatty acids',
                    'Eat plenty of fruits and vegetables',
                    'Choose lean proteins',
                    'Limit saturated and trans fats'
                ],
                'foods_to_include': [
                    'Fatty fish (salmon, mackerel, sardines)',
                    'Nuts and seeds (walnuts, flaxseeds)',
                    'Leafy greens and colorful vegetables',
                    'Whole grains and legumes',
                    'Olive oil and avocado'
                ],
                'foods_to_avoid': [
                    'High-sodium processed foods',
                    'Saturated fats (red meat, butter)',
                    'Trans fats (fried foods, baked goods)',
                    'Excessive alcohol',
                    'High-sugar foods and drinks'
                ]
            },
            'muscle_building': {
                'description': 'Nutrition for muscle growth and strength training',
                'recommendations': [
                    'Consume adequate protein (1.6-2.2g per kg body weight)',
                    'Eat balanced meals with carbs and fats',
                    'Time protein intake around workouts',
                    'Stay hydrated throughout the day',
                    'Get enough calories for growth'
                ],
                'foods_to_include': [
                    'Lean proteins (chicken, fish, eggs, Greek yogurt)',
                    'Complex carbs (sweet potatoes, brown rice, oats)',
                    'Healthy fats (nuts, olive oil, avocado)',
                    'Dairy products (milk, cottage cheese)',
                    'Post-workout recovery foods'
                ],
                'foods_to_avoid': [
                    'Insufficient protein intake',
                    'Excessive processed foods',
                    'Too much alcohol',
                    'Inadequate hydration',
                    'Skipping post-workout nutrition'
                ]
            },
            'general_health': {
                'description': 'General health and wellness nutrition guidance',
                'recommendations': [
                    'Eat a variety of colorful fruits and vegetables',
                    'Include lean proteins and healthy fats',
                    'Choose whole grains over refined grains',
                    'Stay hydrated with water',
                    'Practice mindful eating habits'
                ],
                'foods_to_include': [
                    'Colorful fruits and vegetables',
                    'Lean proteins (fish, poultry, beans)',
                    'Whole grains (quinoa, brown rice, oats)',
                    'Healthy fats (nuts, seeds, olive oil)',
                    'Dairy or dairy alternatives'
                ],
                'foods_to_avoid': [
                    'Excessive processed foods',
                    'Too much added sugar',
                    'High sodium foods',
                    'Trans fats and excessive saturated fats',
                    'Overconsumption of alcohol'
                ]
            }
        }
        
        self.meal_plans = {
            'weight_loss': {
                'breakfast': 'Oatmeal with berries and nuts',
                'lunch': 'Grilled chicken salad with mixed vegetables',
                'dinner': 'Baked fish with steamed broccoli and quinoa',
                'snacks': 'Apple slices with almond butter, Greek yogurt'
            },
            'weight_gain': {
                'breakfast': 'Scrambled eggs with whole grain toast and avocado',
                'lunch': 'Chicken and rice bowl with vegetables',
                'dinner': 'Salmon with sweet potato and green beans',
                'snacks': 'Trail mix, protein smoothie, cheese and crackers'
            },
            'diabetes_management': {
                'breakfast': 'Greek yogurt with berries and nuts',
                'lunch': 'Grilled chicken with quinoa and vegetables',
                'dinner': 'Baked fish with roasted vegetables',
                'snacks': 'Raw vegetables with hummus, small apple'
            }
        }
    
    def create_synthetic_data(self, num_samples: int = 1000) -> Tuple[List[str], List[str]]:
        """Create synthetic training data for nutrition classification"""
        logger.info("Creating synthetic nutrition training data...")
        
        queries = []
        categories = []
        
        # Weight loss queries
        weight_loss_queries = [
            "I want to lose weight, what should I eat?",
            "How can I reduce my calorie intake?",
            "What foods help with weight loss?",
            "I need a diet plan for losing weight",
            "What should I avoid when trying to lose weight?",
            "How to eat healthy for weight loss?",
            "Best foods for weight reduction",
            "Low calorie meal ideas",
            "Weight loss nutrition tips",
            "Healthy eating for weight management"
        ]
        
        # Weight gain queries
        weight_gain_queries = [
            "I want to gain weight healthily",
            "What foods help with weight gain?",
            "How to increase calorie intake?",
            "Best foods for muscle building",
            "Healthy weight gain diet plan",
            "What to eat to gain weight?",
            "High calorie healthy foods",
            "Nutrition for weight gain",
            "How to bulk up with food?",
            "Healthy weight gain tips"
        ]
        
        # Diabetes management queries
        diabetes_queries = [
            "What should I eat if I have diabetes?",
            "How to manage blood sugar with diet?",
            "Diabetes-friendly foods",
            "What foods to avoid with diabetes?",
            "Low glycemic index foods",
            "Diabetes meal planning",
            "How to control blood sugar naturally?",
            "Best diet for diabetes",
            "Carbohydrate counting for diabetes",
            "Diabetes nutrition guidelines"
        ]
        
        # Heart health queries
        heart_health_queries = [
            "What foods are good for heart health?",
            "How to eat for cardiovascular health?",
            "Heart-healthy diet recommendations",
            "Foods to avoid for heart health",
            "Omega-3 rich foods",
            "Low sodium diet for heart",
            "Cholesterol-lowering foods",
            "Heart disease prevention diet",
            "Cardiovascular nutrition",
            "Healthy heart eating plan"
        ]
        
        # Muscle building queries
        muscle_building_queries = [
            "What should I eat to build muscle?",
            "Protein requirements for muscle growth",
            "Best foods for muscle building",
            "Pre and post workout nutrition",
            "How much protein do I need?",
            "Muscle building meal plan",
            "Sports nutrition for athletes",
            "Recovery nutrition after exercise",
            "Supplements for muscle growth",
            "High protein diet for athletes"
        ]
        
        # General health queries
        general_health_queries = [
            "What is a balanced diet?",
            "How to eat healthy?",
            "What are the best foods for health?",
            "Nutritional requirements for adults",
            "How to improve my diet?",
            "What vitamins do I need?",
            "Healthy eating guidelines",
            "How to get all nutrients?",
            "What makes a healthy meal?",
            "General nutrition advice"
        ]
        
        # Combine all queries
        all_queries = [
            (weight_loss_queries, 'weight_loss'),
            (weight_gain_queries, 'weight_gain'),
            (diabetes_queries, 'diabetes_management'),
            (heart_health_queries, 'heart_health'),
            (muscle_building_queries, 'muscle_building'),
            (general_health_queries, 'general_health')
        ]
        
        for query_list, category in all_queries:
            for query in query_list:
                queries.append(query)
                categories.append(category)
        
        # Add variations and additional samples
        for _ in range(num_samples - len(queries)):
            category = np.random.choice(self.nutrition_categories[:6])  # Use first 6 categories
            base_query = np.random.choice([
                "What should I eat for",
                "How to eat for",
                "Best foods for",
                "Nutrition advice for",
                "Diet plan for",
                "Meal ideas for"
            ])
            
            query = f"{base_query} {category.replace('_', ' ')}"
            queries.append(query)
            categories.append(category)
        
        return queries, categories
    
    def train_model(self, queries: List[str], categories: List[str]) -> Dict[str, Any]:
        """Train the nutrition classification model"""
        logger.info("Starting nutrition model training...")
        
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
    
    def predict_nutrition_category(self, query: str) -> Dict[str, Any]:
        """Predict nutrition category from user query"""
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
        category_info = self.nutrition_responses.get(prediction, {})
        
        return {
            'category': prediction,
            'confidence': float(confidence),
            'description': category_info.get('description', ''),
            'recommendations': category_info.get('recommendations', []),
            'foods_to_include': category_info.get('foods_to_include', []),
            'foods_to_avoid': category_info.get('foods_to_avoid', []),
            'meal_plan': self.meal_plans.get(prediction, {})
        }
    
    def generate_nutrition_response(self, query: str, user_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate comprehensive nutrition response"""
        prediction = self.predict_nutrition_category(query)
        
        # Customize response based on user context
        if user_context:
            age = user_context.get('age')
            gender = user_context.get('gender')
            medical_conditions = user_context.get('medical_conditions', [])
            
            # Add age-specific recommendations
            if age and age < 18:
                prediction['age_specific'] = "For teenagers, focus on balanced nutrition for growth and development."
            elif age and age > 65:
                prediction['age_specific'] = "For seniors, ensure adequate protein and calcium for bone health."
            
            # Add medical condition considerations
            if 'diabetes' in medical_conditions:
                prediction['medical_considerations'] = "Monitor blood sugar levels and consult with your healthcare provider."
            elif 'heart_disease' in medical_conditions:
                prediction['medical_considerations'] = "Focus on heart-healthy foods and limit sodium intake."
        
        return {
            'query': query,
            'prediction': prediction,
            'timestamp': pd.Timestamp.now().isoformat(),
            'disclaimer': 'This nutrition advice is for educational purposes only. Consult a registered dietitian for personalized nutrition guidance.'
        }
    
    def save_model(self):
        """Save the trained model and vectorizer"""
        os.makedirs(self.model_path, exist_ok=True)
        
        # Save the model
        joblib.dump(self.model, os.path.join(self.model_path, 'nutrition_classifier.pkl'))
        
        # Save the vectorizer
        joblib.dump(self.vectorizer, os.path.join(self.model_path, 'nutrition_vectorizer.pkl'))
        
        # Save metadata
        metadata = {
            'nutrition_categories': self.nutrition_categories,
            'nutrition_responses': self.nutrition_responses,
            'meal_plans': self.meal_plans
        }
        
        with open(os.path.join(self.model_path, 'nutrition_metadata.json'), 'w') as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"Nutrition model saved to {self.model_path}")
    
    def load_model(self):
        """Load the trained model and vectorizer"""
        try:
            self.model = joblib.load(os.path.join(self.model_path, 'nutrition_classifier.pkl'))
            self.vectorizer = joblib.load(os.path.join(self.model_path, 'nutrition_vectorizer.pkl'))
            
            # Load metadata
            with open(os.path.join(self.model_path, 'nutrition_metadata.json'), 'r') as f:
                metadata = json.load(f)
                self.nutrition_categories = metadata['nutrition_categories']
                self.nutrition_responses = metadata['nutrition_responses']
                self.meal_plans = metadata['meal_plans']
            
            logger.info("Nutrition model loaded successfully")
        except FileNotFoundError:
            logger.warning("Nutrition model files not found. Training new model...")
            self.train_from_scratch()
    
    def train_from_scratch(self):
        """Train a new model from scratch"""
        queries, categories = self.create_synthetic_data()
        self.train_model(queries, categories)

# Training script
if __name__ == "__main__":
    classifier = NutritionClassifier()
    
    # Create and train the model
    queries, categories = classifier.create_synthetic_data()
    results = classifier.train_model(queries, categories)
    
    print("Training completed!")
    print(f"Best model: {results['model_name']}")
    print(f"Test accuracy: {results['test_accuracy']:.4f}")
    
    # Test the model
    test_queries = [
        "I want to lose weight, what should I eat?",
        "What foods are good for heart health?",
        "How to build muscle with nutrition?",
        "What should I eat if I have diabetes?"
    ]
    
    print("\nTest predictions:")
    for query in test_queries:
        prediction = classifier.predict_nutrition_category(query)
        print(f"Query: {query}")
        print(f"Category: {prediction['category']} (confidence: {prediction['confidence']:.3f})")
        print()
