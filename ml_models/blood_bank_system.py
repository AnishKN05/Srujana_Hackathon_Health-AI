"""
Blood Bank System with ML-powered donor matching and hospital tracking
"""
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import json
import os
import logging
from typing import List, Dict, Tuple, Any, Optional
from datetime import datetime, timedelta
import random
import math

logger = logging.getLogger(__name__)

class BloodBankSystem:
    def __init__(self, model_path: str = "ml_models/trained_models/"):
        self.model_path = model_path
        self.model = None
        self.vectorizer = None
        
        # Blood types and compatibility
        self.blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        self.blood_compatibility = {
            'A+': ['A+', 'A-', 'O+', 'O-'],
            'A-': ['A-', 'O-'],
            'B+': ['B+', 'B-', 'O+', 'O-'],
            'B-': ['B-', 'O-'],
            'AB+': ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'],
            'AB-': ['A-', 'B-', 'AB-', 'O-'],
            'O+': ['O+', 'O-'],
            'O-': ['O-']
        }
        
        # Indian cities and states for hospital data
        self.indian_cities = {
            'mumbai': {'state': 'Maharashtra', 'lat': 19.0760, 'lon': 72.8777},
            'delhi': {'state': 'Delhi', 'lat': 28.7041, 'lon': 77.1025},
            'bangalore': {'state': 'Karnataka', 'lat': 12.9716, 'lon': 77.5946},
            'hyderabad': {'state': 'Telangana', 'lat': 17.3850, 'lon': 78.4867},
            'chennai': {'state': 'Tamil Nadu', 'lat': 13.0827, 'lon': 80.2707},
            'kolkata': {'state': 'West Bengal', 'lat': 22.5726, 'lon': 88.3639},
            'pune': {'state': 'Maharashtra', 'lat': 18.5204, 'lon': 73.8567},
            'ahmedabad': {'state': 'Gujarat', 'lat': 23.0225, 'lon': 72.5714},
            'jaipur': {'state': 'Rajasthan', 'lat': 26.9124, 'lon': 75.7873},
            'lucknow': {'state': 'Uttar Pradesh', 'lat': 26.8467, 'lon': 80.9462}
        }
        
        # Initialize hospital and donor data
        self.hospitals = self._initialize_hospitals()
        self.donors = self._initialize_donors()
        self.blood_inventory = self._initialize_blood_inventory()
        
        # Donor matching categories
        self.donor_categories = [
            'urgent_blood_request',
            'scheduled_donation',
            'emergency_surgery',
            'chronic_condition',
            'accident_victim',
            'childbirth_emergency',
            'cancer_treatment',
            'organ_transplant'
        ]
    
    def _initialize_hospitals(self) -> List[Dict[str, Any]]:
        """Initialize hospital data for Indian cities"""
        hospitals = []
        hospital_names = [
            'Apollo Hospitals', 'Fortis Healthcare', 'Max Healthcare', 'Manipal Hospitals',
            'Narayana Health', 'Medanta', 'AIIMS', 'PGI Chandigarh', 'Tata Memorial',
            'Kokilaben Hospital', 'Lilavati Hospital', 'Breach Candy Hospital',
            'Sir Ganga Ram Hospital', 'Indraprastha Apollo', 'BLK Super Speciality',
            'Artemis Hospital', 'Columbia Asia', 'Global Hospitals', 'Rainbow Hospitals'
        ]
        
        for city, city_data in self.indian_cities.items():
            # Add 3-5 hospitals per city
            num_hospitals = random.randint(3, 5)
            city_hospitals = random.sample(hospital_names, min(num_hospitals, len(hospital_names)))
            
            for i, hospital_name in enumerate(city_hospitals):
                hospital = {
                    'id': f'hosp_{city}_{i+1}',
                    'name': f'{hospital_name} - {city.title()}',
                    'city': city.title(),
                    'state': city_data['state'],
                    'latitude': city_data['lat'] + random.uniform(-0.1, 0.1),
                    'longitude': city_data['lon'] + random.uniform(-0.1, 0.1),
                    'contact': f'+91-{random.randint(1000000000, 9999999999)}',
                    'emergency_contact': f'+91-{random.randint(1000000000, 9999999999)}',
                    'specialties': random.sample([
                        'Cardiology', 'Neurology', 'Oncology', 'Orthopedics', 'Pediatrics',
                        'Emergency Medicine', 'Surgery', 'Trauma Care', 'Blood Bank'
                    ], random.randint(3, 6)),
                    'bed_capacity': random.randint(50, 500),
                    'is_government': random.choice([True, False]),
                    'has_blood_bank': True,
                    'blood_bank_capacity': random.randint(100, 1000)
                }
                hospitals.append(hospital)
        
        return hospitals
    
    def _initialize_donors(self) -> List[Dict[str, Any]]:
        """Initialize donor database with realistic distribution"""
        donors = []
        first_names = ['Raj', 'Priya', 'Amit', 'Sneha', 'Vikram', 'Anita', 'Rahul', 'Kavita',
                      'Suresh', 'Meera', 'Arjun', 'Pooja', 'Kumar', 'Sunita', 'Vishal', 'Ritu',
                      'Ravi', 'Shilpa', 'Manoj', 'Geeta', 'Kiran', 'Uma', 'Suresh', 'Lakshmi']
        last_names = ['Sharma', 'Patel', 'Singh', 'Kumar', 'Gupta', 'Agarwal', 'Verma', 'Yadav',
                     'Jain', 'Shah', 'Reddy', 'Nair', 'Iyer', 'Pillai', 'Choudhary', 'Mishra',
                     'Bose', 'Chatterjee', 'Mukherjee', 'Banerjee', 'Das', 'Roy', 'Ghosh', 'Saha']
        
        # Get all available cities
        available_cities = list(self.indian_cities.keys())
        major_cities = ['delhi', 'mumbai', 'bangalore', 'chennai', 'kolkata', 'hyderabad', 'pune', 'ahmedabad']
        
        for i in range(1000):  # 1000 donors
            # Create realistic distribution: 30% in major cities, 70% in other cities
            if i < 300:  # First 300 donors in major cities for better distance variety
                city = random.choice(major_cities)
            else:
                city = random.choice(available_cities)
            
            donor = {
                'id': f'donor_{i+1}',
                'name': f'{random.choice(first_names)} {random.choice(last_names)}',
                'age': random.randint(18, 65),
                'gender': random.choice(['Male', 'Female']),
                'blood_type': random.choice(self.blood_types),
                'city': city.title(),
                'state': self.indian_cities[city]['state'],
                'phone': f'+91-{random.randint(1000000000, 9999999999)}',
                'email': f'donor{i+1}@example.com',
                'last_donation': datetime.now() - timedelta(days=random.randint(0, 365)),
                'donation_count': random.randint(0, 20),
                'is_available': random.choice([True, True, True, False]),  # 75% available
                'preferred_hospitals': random.sample([h['id'] for h in self.hospitals], random.randint(1, 3)),
                'emergency_contact': f'+91-{random.randint(1000000000, 9999999999)}',
                'medical_conditions': random.sample([
                    'None', 'Diabetes', 'Hypertension', 'Asthma', 'Heart Disease'
                ], random.randint(1, 2)),
                'weight': random.randint(45, 100),
                'height': random.randint(150, 190)
            }
            donors.append(donor)
        
        return donors
    
    def _initialize_blood_inventory(self) -> Dict[str, Dict[str, int]]:
        """Initialize blood inventory for hospitals"""
        inventory = {}
        
        for hospital in self.hospitals:
            hospital_inventory = {}
            for blood_type in self.blood_types:
                # Random inventory levels (0-50 units)
                hospital_inventory[blood_type] = random.randint(0, 50)
            inventory[hospital['id']] = hospital_inventory
        
        return inventory
    
    def calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two coordinates in kilometers"""
        R = 6371  # Earth's radius in kilometers
        
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        
        a = (math.sin(dlat/2) * math.sin(dlat/2) +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon/2) * math.sin(dlon/2))
        
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = R * c
        
        return distance
    
    def find_nearby_hospitals(self, user_lat: float, user_lon: float, radius_km: float = 50) -> List[Dict[str, Any]]:
        """Find hospitals within specified radius"""
        nearby_hospitals = []
        
        for hospital in self.hospitals:
            distance = self.calculate_distance(
                user_lat, user_lon,
                hospital['latitude'], hospital['longitude']
            )
            
            if distance <= radius_km:
                hospital_info = hospital.copy()
                hospital_info['distance_km'] = round(distance, 2)
                hospital_info['blood_inventory'] = self.blood_inventory[hospital['id']]
                nearby_hospitals.append(hospital_info)
        
        # Sort by distance
        nearby_hospitals.sort(key=lambda x: x['distance_km'])
        
        return nearby_hospitals
    
    def find_compatible_donors(self, required_blood_type: str, user_city: str, 
                             radius_km: float = 200) -> List[Dict[str, Any]]:
        """Find compatible donors for blood type"""
        compatible_blood_types = self.blood_compatibility.get(required_blood_type, [])
        compatible_donors = []
        
        # Get user coordinates
        user_city_lower = user_city.lower()
        if user_city_lower in self.indian_cities:
            user_lat = self.indian_cities[user_city_lower]['lat']
            user_lon = self.indian_cities[user_city_lower]['lon']
        else:
            # Default to Delhi if city not found
            user_lat = self.indian_cities['delhi']['lat']
            user_lon = self.indian_cities['delhi']['lon']
        
        # First, add some local donors (same city) for 0km distance
        local_donors_added = 0
        for donor in self.donors:
            if (donor['blood_type'] in compatible_blood_types and 
                donor['is_available'] and
                donor['age'] >= 18 and donor['age'] <= 65 and
                donor['weight'] >= 50 and
                donor['city'].lower() == user_city_lower and
                local_donors_added < 3):  # Add 2-3 local donors
                
                donor_info = donor.copy()
                donor_info['distance_km'] = 0.0  # Same city
                
                # Handle last_donation date properly
                last_donation = donor['last_donation']
                if isinstance(last_donation, str):
                    try:
                        from datetime import datetime
                        last_donation = datetime.fromisoformat(last_donation.replace('Z', '+00:00'))
                    except:
                        last_donation = datetime.now() - timedelta(days=30)
                elif last_donation is None:
                    last_donation = datetime.now() - timedelta(days=30)
                
                donor_info['last_donation_days'] = (datetime.now() - last_donation).days
                compatible_donors.append(donor_info)
                local_donors_added += 1
        
        # Then add donors from other cities
        for donor in self.donors:
            if (donor['blood_type'] in compatible_blood_types and 
                donor['is_available'] and
                donor['age'] >= 18 and donor['age'] <= 65 and
                donor['weight'] >= 50 and
                donor['city'].lower() != user_city_lower):  # Different city
                
                # Calculate distance
                donor_city_lower = donor['city'].lower()
                if donor_city_lower in self.indian_cities:
                    donor_lat = self.indian_cities[donor_city_lower]['lat']
                    donor_lon = self.indian_cities[donor_city_lower]['lon']
                    distance = self.calculate_distance(user_lat, user_lon, donor_lat, donor_lon)
                else:
                    # If donor city not found, assign a random distance within radius
                    distance = random.uniform(5, radius_km)
                
                # Include donors within radius, and some beyond for variety
                if distance <= radius_km or (distance <= radius_km * 2 and random.random() < 0.4):
                    donor_info = donor.copy()
                    donor_info['distance_km'] = round(distance, 2)
                    
                    # Handle last_donation date properly
                    last_donation = donor['last_donation']
                    if isinstance(last_donation, str):
                        # If it's a string, parse it
                        try:
                            from datetime import datetime
                            last_donation = datetime.fromisoformat(last_donation.replace('Z', '+00:00'))
                        except:
                            # If parsing fails, use a default date
                            last_donation = datetime.now() - timedelta(days=30)
                    elif last_donation is None:
                        last_donation = datetime.now() - timedelta(days=30)
                    
                    donor_info['last_donation_days'] = (datetime.now() - last_donation).days
                    compatible_donors.append(donor_info)
        
        # Sort by distance and availability
        compatible_donors.sort(key=lambda x: (x['distance_km'], -x['last_donation_days']))
        
        return compatible_donors[:30]  # Return top 30 matches for more variety
    
    def check_blood_availability(self, blood_type: str, user_city: str, 
                               radius_km: float = 50) -> Dict[str, Any]:
        """Check blood availability in nearby hospitals"""
        user_city_lower = user_city.lower()
        if user_city_lower in self.indian_cities:
            user_lat = self.indian_cities[user_city_lower]['lat']
            user_lon = self.indian_cities[user_city_lower]['lon']
        else:
            user_lat = self.indian_cities['delhi']['lat']
            user_lon = self.indian_cities['delhi']['lon']
        
        nearby_hospitals = self.find_nearby_hospitals(user_lat, user_lon, radius_km)
        
        availability = {
            'requested_blood_type': blood_type,
            'user_city': user_city,
            'search_radius_km': radius_km,
            'hospitals_with_blood': [],
            'total_units_available': 0,
            'nearest_hospital': None,
            'emergency_contacts': []
        }
        
        for hospital in nearby_hospitals:
            blood_units = hospital['blood_inventory'].get(blood_type, 0)
            if blood_units > 0:
                hospital_info = {
                    'hospital_id': hospital['id'],
                    'hospital_name': hospital['name'],
                    'city': hospital['city'],
                    'state': hospital['state'],
                    'distance_km': hospital['distance_km'],
                    'blood_units_available': blood_units,
                    'contact': hospital['contact'],
                    'emergency_contact': hospital['emergency_contact']
                }
                availability['hospitals_with_blood'].append(hospital_info)
                availability['total_units_available'] += blood_units
                
                if availability['nearest_hospital'] is None:
                    availability['nearest_hospital'] = hospital_info
        
        # Add emergency contacts
        for hospital in nearby_hospitals[:5]:  # Top 5 nearest hospitals
            availability['emergency_contacts'].append({
                'hospital_name': hospital['name'],
                'emergency_contact': hospital['emergency_contact'],
                'distance_km': hospital['distance_km']
            })
        
        return availability
    
    def create_synthetic_data(self, num_samples: int = 500) -> Tuple[List[str], List[str]]:
        """Create synthetic training data for donor matching"""
        logger.info("Creating synthetic blood bank training data...")
        
        queries = []
        categories = []
        
        # Urgent blood request queries
        urgent_queries = [
            "I need blood urgently for emergency surgery",
            "Urgent blood requirement for accident victim",
            "Emergency blood needed for childbirth",
            "Critical blood shortage in hospital",
            "Immediate blood donation needed",
            "Emergency blood transfusion required",
            "Urgent blood request for patient",
            "Critical blood need for surgery",
            "Emergency blood donor needed",
            "Urgent blood requirement"
        ]
        
        # Scheduled donation queries
        scheduled_queries = [
            "I want to schedule a blood donation",
            "When can I donate blood next?",
            "Schedule blood donation appointment",
            "Regular blood donation program",
            "Blood donation camp schedule",
            "When is the next blood drive?",
            "Blood donation appointment booking",
            "Scheduled blood donation",
            "Regular donor program",
            "Blood donation scheduling"
        ]
        
        # Emergency surgery queries
        surgery_queries = [
            "Blood needed for heart surgery",
            "Blood requirement for organ transplant",
            "Blood for cancer treatment",
            "Surgery blood transfusion",
            "Blood needed for major surgery",
            "Surgical blood requirement",
            "Blood for emergency operation",
            "Surgery blood donor needed",
            "Blood transfusion for surgery",
            "Surgical blood need"
        ]
        
        # Chronic condition queries
        chronic_queries = [
            "Blood needed for thalassemia patient",
            "Regular blood transfusion for anemia",
            "Blood for sickle cell disease",
            "Chronic blood requirement",
            "Blood for hemophilia treatment",
            "Regular blood donor for patient",
            "Blood for chronic condition",
            "Long-term blood need",
            "Blood for genetic disorder",
            "Chronic blood transfusion"
        ]
        
        # Combine all queries
        all_queries = [
            (urgent_queries, 'urgent_blood_request'),
            (scheduled_queries, 'scheduled_donation'),
            (surgery_queries, 'emergency_surgery'),
            (chronic_queries, 'chronic_condition')
        ]
        
        for query_list, category in all_queries:
            for query in query_list:
                queries.append(query)
                categories.append(category)
        
        # Add variations
        for _ in range(num_samples - len(queries)):
            category = random.choice(self.donor_categories[:4])
            base_query = random.choice([
                "I need blood for",
                "Blood required for",
                "Blood donation for",
                "Blood needed for",
                "Blood request for"
            ])
            
            query = f"{base_query} {category.replace('_', ' ')}"
            queries.append(query)
            categories.append(category)
        
        return queries, categories
    
    def train_model(self, queries: List[str], categories: List[str]) -> Dict[str, Any]:
        """Train the blood bank classification model"""
        logger.info("Starting blood bank model training...")
        
        # Vectorize the text data
        self.vectorizer = TfidfVectorizer(
            max_features=500,
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
        
        # Train Random Forest model
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        
        # Test the model
        y_pred = self.model.predict(X_test)
        test_accuracy = accuracy_score(y_test, y_pred)
        
        logger.info(f"Blood bank model test accuracy: {test_accuracy:.4f}")
        
        # Save the model
        self.save_model()
        
        return {
            'test_accuracy': test_accuracy,
            'model_type': 'RandomForest'
        }
    
    def predict_request_type(self, query: str) -> Dict[str, Any]:
        """Predict blood request type from user query"""
        if self.model is None or self.vectorizer is None:
            self.load_model()
        
        # Preprocess the query
        processed_query = self.vectorizer.transform([query])
        
        # Make prediction
        prediction = self.model.predict(processed_query)[0]
        probabilities = self.model.predict_proba(processed_query)[0]
        
        # Get confidence score
        confidence = max(probabilities)
        
        return {
            'request_type': prediction,
            'confidence': float(confidence)
        }
    
    def generate_blood_bank_response(self, query: str, user_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate comprehensive blood bank response"""
        request_prediction = self.predict_request_type(query)
        
        response = {
            'query': query,
            'request_type': request_prediction['request_type'],
            'confidence': request_prediction['confidence'],
            'timestamp': datetime.now().isoformat()
        }
        
        if user_context:
            blood_type = user_context.get('blood_type')
            city = user_context.get('city', 'Delhi')
            
            if blood_type:
                # Check blood availability
                availability = self.check_blood_availability(blood_type, city)
                response['blood_availability'] = availability
                
                # Find compatible donors
                donors = self.find_compatible_donors(blood_type, city)
                response['compatible_donors'] = donors[:10]  # Top 10 donors
            
            # Add emergency contacts
            response['emergency_contacts'] = {
                'national_blood_bank': '+91-1800-180-1234',
                'red_cross_india': '+91-1800-180-1234',
                'emergency_services': '108'
            }
        
        return response
    
    def save_model(self):
        """Save the trained model and vectorizer"""
        os.makedirs(self.model_path, exist_ok=True)
        
        # Save the model
        joblib.dump(self.model, os.path.join(self.model_path, 'blood_bank_classifier.pkl'))
        
        # Save the vectorizer
        joblib.dump(self.vectorizer, os.path.join(self.model_path, 'blood_bank_vectorizer.pkl'))
        
        # Save system data
        system_data = {
            'hospitals': self.hospitals,
            'donors': self.donors,
            'blood_inventory': self.blood_inventory,
            'blood_types': self.blood_types,
            'blood_compatibility': self.blood_compatibility,
            'indian_cities': self.indian_cities,
            'donor_categories': self.donor_categories
        }
        
        with open(os.path.join(self.model_path, 'blood_bank_data.json'), 'w') as f:
            json.dump(system_data, f, indent=2, default=str)
        
        logger.info(f"Blood bank system saved to {self.model_path}")
    
    def load_model(self):
        """Load the trained model and system data"""
        try:
            self.model = joblib.load(os.path.join(self.model_path, 'blood_bank_classifier.pkl'))
            self.vectorizer = joblib.load(os.path.join(self.model_path, 'blood_bank_vectorizer.pkl'))
            
            # Load system data
            with open(os.path.join(self.model_path, 'blood_bank_data.json'), 'r') as f:
                system_data = json.load(f)
                self.hospitals = system_data['hospitals']
                self.donors = system_data['donors']
                self.blood_inventory = system_data['blood_inventory']
                self.blood_types = system_data['blood_types']
                self.blood_compatibility = system_data['blood_compatibility']
                self.indian_cities = system_data['indian_cities']
                self.donor_categories = system_data['donor_categories']
            
            logger.info("Blood bank system loaded successfully")
        except FileNotFoundError:
            logger.warning("Blood bank system files not found. Training new model...")
            self.train_from_scratch()
    
    def train_from_scratch(self):
        """Train a new model from scratch"""
        queries, categories = self.create_synthetic_data()
        self.train_model(queries, categories)

# Training script
if __name__ == "__main__":
    system = BloodBankSystem()
    
    # Create and train the model
    queries, categories = system.create_synthetic_data()
    results = system.train_model(queries, categories)
    
    print("Training completed!")
    print(f"Test accuracy: {results['test_accuracy']:.4f}")
    
    # Test the system
    test_queries = [
        "I need blood urgently for emergency surgery",
        "I want to schedule a blood donation",
        "Blood needed for thalassemia patient"
    ]
    
    print("\nTest predictions:")
    for query in test_queries:
        prediction = system.predict_request_type(query)
        print(f"Query: {query}")
        print(f"Request type: {prediction['request_type']} (confidence: {prediction['confidence']:.3f})")
        print()
    
    # Test blood availability
    availability = system.check_blood_availability('O+', 'Mumbai')
    print(f"\nBlood availability for O+ in Mumbai: {availability['total_units_available']} units")
    
    # Test donor matching
    donors = system.find_compatible_donors('O+', 'Mumbai')
    print(f"Compatible donors found: {len(donors)}")
