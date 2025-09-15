#!/usr/bin/env python3
"""
Hospital Recommendation System
Uses ML to recommend hospitals based on medical issue type, specialties, and real-time data
"""
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import random
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
import json
import math

logger = logging.getLogger(__name__)

class HospitalRecommender:
    """ML-powered hospital recommendation system"""
    
    def __init__(self):
        self.hospitals = []
        self.doctors = []
        self.specialties = []
        self.medical_issues = []
        self.recommendation_model = None
        self.specialty_vectorizer = None
        self.issue_classifier = None
        self._initialize_data()
        self._train_models()
    
    def _initialize_data(self):
        """Initialize hospital, doctor, and specialty data"""
        logger.info("Initializing hospital recommendation data...")
        
        # Medical specialties and their keywords
        self.specialties = {
            'cardiology': {
                'keywords': ['heart', 'cardiac', 'chest pain', 'heart attack', 'angina', 'arrhythmia', 'bypass', 'stent'],
                'procedures': ['angioplasty', 'bypass surgery', 'pacemaker', 'heart transplant', 'valve replacement'],
                'equipment': ['cath lab', 'ecg', 'echocardiogram', 'stress test', 'cardiac mri']
            },
            'neurology': {
                'keywords': ['brain', 'stroke', 'seizure', 'headache', 'migraine', 'epilepsy', 'parkinson', 'alzheimer'],
                'procedures': ['brain surgery', 'neurosurgery', 'deep brain stimulation', 'aneurysm repair'],
                'equipment': ['mri', 'ct scan', 'eeg', 'pet scan', 'neurosurgery suite']
            },
            'oncology': {
                'keywords': ['cancer', 'tumor', 'chemotherapy', 'radiation', 'oncology', 'malignancy', 'carcinoma'],
                'procedures': ['surgery', 'chemotherapy', 'radiation therapy', 'immunotherapy', 'bone marrow transplant'],
                'equipment': ['linear accelerator', 'pet-ct', 'mri', 'cyberknife', 'proton therapy']
            },
            'orthopedics': {
                'keywords': ['bone', 'fracture', 'joint', 'knee', 'hip', 'spine', 'arthritis', 'sports injury'],
                'procedures': ['joint replacement', 'arthroscopy', 'spinal surgery', 'fracture repair'],
                'equipment': ['x-ray', 'mri', 'surgical robots', 'rehabilitation center']
            },
            'pediatrics': {
                'keywords': ['child', 'baby', 'infant', 'pediatric', 'neonatal', 'adolescent', 'congenital'],
                'procedures': ['pediatric surgery', 'neonatal care', 'vaccination', 'developmental assessment'],
                'equipment': ['neonatal icu', 'pediatric mri', 'play therapy room', 'child-friendly facilities']
            },
            'emergency': {
                'keywords': ['emergency', 'trauma', 'accident', 'critical', 'urgent', 'ambulance', 'resuscitation'],
                'procedures': ['trauma surgery', 'emergency medicine', 'resuscitation', 'stabilization'],
                'equipment': ['trauma bay', 'emergency or', 'ambulance bay', 'critical care unit']
            }
        }
        
        # Create comprehensive hospital database
        self._create_hospital_database()
        self._create_doctor_database()
        self._create_medical_issues()
    
    def _create_hospital_database(self):
        """Create comprehensive hospital database with specialties and ratings"""
        major_cities = [
            {'name': 'Delhi', 'lat': 28.7041, 'lon': 77.1025, 'state': 'Delhi'},
            {'name': 'Mumbai', 'lat': 19.0760, 'lon': 72.8777, 'state': 'Maharashtra'},
            {'name': 'Bangalore', 'lat': 12.9716, 'lon': 77.5946, 'state': 'Karnataka'},
            {'name': 'Chennai', 'lat': 13.0827, 'lon': 77.2707, 'state': 'Tamil Nadu'},
            {'name': 'Kolkata', 'lat': 22.5726, 'lon': 88.3639, 'state': 'West Bengal'},
            {'name': 'Hyderabad', 'lat': 17.3850, 'lon': 78.4867, 'state': 'Telangana'},
            {'name': 'Pune', 'lat': 18.5204, 'lon': 73.8567, 'state': 'Maharashtra'},
            {'name': 'Ahmedabad', 'lat': 23.0225, 'lon': 72.5714, 'state': 'Gujarat'}
        ]
        
        hospital_names = [
            'Apollo Hospitals', 'Fortis Healthcare', 'Max Healthcare', 'Manipal Hospitals',
            'AIIMS', 'Tata Memorial Hospital', 'Narayana Health', 'Medanta',
            'Kokilaben Hospital', 'Lilavati Hospital', 'Breach Candy Hospital',
            'Sir Ganga Ram Hospital', 'Safdarjung Hospital', 'Ram Manohar Lohia Hospital',
            'KEM Hospital', 'Jaslok Hospital', 'Bombay Hospital', 'Wockhardt Hospital'
        ]
        
        for i, city in enumerate(major_cities):
            # Create 3-5 hospitals per city
            num_hospitals = random.randint(3, 5)
            for j in range(num_hospitals):
                hospital = {
                    'id': f'hospital_{i}_{j}',
                    'name': f'{random.choice(hospital_names)} - {city["name"]}',
                    'city': city['name'],
                    'state': city['state'],
                    'latitude': city['lat'] + random.uniform(-0.1, 0.1),
                    'longitude': city['lon'] + random.uniform(-0.1, 0.1),
                    'contact_number': f'+91-{random.randint(1000000000, 9999999999)}',
                    'emergency_contact': f'+91-{random.randint(1000000000, 9999999999)}',
                    'bed_capacity': random.randint(50, 500),
                    'is_government': random.choice([True, False]),
                    'has_blood_bank': random.choice([True, True, False]),
                    'blood_bank_capacity': random.randint(0, 200) if random.choice([True, True, False]) else 0,
                    'overall_rating': round(random.uniform(3.5, 5.0), 1),
                    'specialties': self._assign_specialties(),
                    'equipment_quality': round(random.uniform(3.0, 5.0), 1),
                    'doctor_expertise': round(random.uniform(3.0, 5.0), 1),
                    'infrastructure': round(random.uniform(3.0, 5.0), 1),
                    'patient_satisfaction': round(random.uniform(3.0, 5.0), 1),
                    'wait_time_minutes': random.randint(15, 120),
                    'cost_level': random.choice(['Low', 'Medium', 'High']),
                    'insurance_accepted': random.choice([True, True, False]),
                    'emergency_services': random.choice([True, True, True, False]),
                    'icu_beds': random.randint(5, 50),
                    'operation_theaters': random.randint(2, 15),
                    'ambulance_services': random.choice([True, True, False]),
                    'created_at': datetime.now() - timedelta(days=random.randint(1, 3650))
                }
                self.hospitals.append(hospital)
    
    def _assign_specialties(self):
        """Assign specialties to hospitals with realistic distribution"""
        all_specialties = list(self.specialties.keys())
        num_specialties = random.randint(2, 6)
        selected_specialties = random.sample(all_specialties, num_specialties)
        
        specialty_details = {}
        for specialty in selected_specialties:
            specialty_details[specialty] = {
                'rating': round(random.uniform(3.0, 5.0), 1),
                'doctors_count': random.randint(1, 10),
                'procedures_available': random.sample(
                    self.specialties[specialty]['procedures'], 
                    random.randint(1, len(self.specialties[specialty]['procedures']))
                ),
                'equipment_available': random.sample(
                    self.specialties[specialty]['equipment'],
                    random.randint(1, len(self.specialties[specialty]['equipment']))
                ),
                'wait_time_days': random.randint(1, 30),
                'success_rate': round(random.uniform(85, 99), 1)
            }
        
        return specialty_details
    
    def _create_doctor_database(self):
        """Create doctor database with specialties and expertise"""
        first_names = ['Dr. Rajesh', 'Dr. Priya', 'Dr. Amit', 'Dr. Sneha', 'Dr. Vikram', 'Dr. Kavya',
                      'Dr. Arjun', 'Dr. Pooja', 'Dr. Rahul', 'Dr. Anita', 'Dr. Suresh', 'Dr. Meera']
        last_names = ['Sharma', 'Patel', 'Singh', 'Kumar', 'Gupta', 'Agarwal', 'Verma', 'Yadav',
                     'Jain', 'Shah', 'Reddy', 'Nair', 'Iyer', 'Pillai', 'Choudhary', 'Mishra']
        
        for i in range(200):  # 200 doctors
            doctor = {
                'id': f'doctor_{i+1}',
                'name': f'{random.choice(first_names)} {random.choice(last_names)}',
                'specialty': random.choice(list(self.specialties.keys())),
                'subspecialty': random.choice(['General', 'Pediatric', 'Geriatric', 'Surgical', 'Medical']),
                'experience_years': random.randint(2, 40),
                'qualification': random.choice(['MBBS', 'MD', 'MS', 'DM', 'MCh', 'DNB']),
                'hospital_id': random.choice([h['id'] for h in self.hospitals]),
                'rating': round(random.uniform(3.5, 5.0), 1),
                'consultation_fee': random.randint(500, 5000),
                'availability': random.choice(['Available', 'Busy', 'On Leave']),
                'languages': random.sample(['English', 'Hindi', 'Tamil', 'Telugu', 'Bengali', 'Gujarati'], 
                                         random.randint(1, 3)),
                'procedures_performed': random.randint(50, 1000),
                'success_rate': round(random.uniform(85, 99), 1),
                'research_papers': random.randint(0, 50),
                'awards': random.randint(0, 10),
                'patient_reviews': random.randint(10, 500)
            }
            self.doctors.append(doctor)
    
    def _create_medical_issues(self):
        """Create medical issue database for training"""
        self.medical_issues = [
            # Heart/Cardiac issues
            {'issue': 'chest pain', 'specialty': 'cardiology', 'urgency': 'high', 'keywords': 'heart cardiac chest pain angina'},
            {'issue': 'heart attack', 'specialty': 'cardiology', 'urgency': 'critical', 'keywords': 'heart attack myocardial infarction cardiac emergency'},
            {'issue': 'irregular heartbeat', 'specialty': 'cardiology', 'urgency': 'high', 'keywords': 'arrhythmia irregular heartbeat palpitations'},
            {'issue': 'shortness of breath', 'specialty': 'cardiology', 'urgency': 'high', 'keywords': 'breathing difficulty dyspnea cardiac respiratory'},
            
            # Neurological issues
            {'issue': 'severe headache', 'specialty': 'neurology', 'urgency': 'high', 'keywords': 'headache migraine brain neurological'},
            {'issue': 'stroke symptoms', 'specialty': 'neurology', 'urgency': 'critical', 'keywords': 'stroke paralysis facial droop neurological emergency'},
            {'issue': 'seizure', 'specialty': 'neurology', 'urgency': 'high', 'keywords': 'seizure epilepsy convulsion neurological'},
            {'issue': 'memory problems', 'specialty': 'neurology', 'urgency': 'medium', 'keywords': 'memory dementia alzheimer cognitive'},
            
            # Cancer/Oncology issues
            {'issue': 'suspected cancer', 'specialty': 'oncology', 'urgency': 'high', 'keywords': 'cancer tumor malignancy oncology'},
            {'issue': 'lump in breast', 'specialty': 'oncology', 'urgency': 'high', 'keywords': 'breast cancer lump tumor oncology'},
            {'issue': 'unexplained weight loss', 'specialty': 'oncology', 'urgency': 'medium', 'keywords': 'weight loss cancer malignancy'},
            
            # Orthopedic issues
            {'issue': 'broken bone', 'specialty': 'orthopedics', 'urgency': 'high', 'keywords': 'fracture broken bone orthopedic trauma'},
            {'issue': 'severe back pain', 'specialty': 'orthopedics', 'urgency': 'medium', 'keywords': 'back pain spine orthopedic'},
            {'issue': 'joint pain', 'specialty': 'orthopedics', 'urgency': 'medium', 'keywords': 'joint pain arthritis orthopedic'},
            
            # Pediatric issues
            {'issue': 'child fever', 'specialty': 'pediatrics', 'urgency': 'high', 'keywords': 'child fever pediatric baby infant'},
            {'issue': 'child breathing problems', 'specialty': 'pediatrics', 'urgency': 'high', 'keywords': 'child breathing pediatric respiratory'},
            
            # Emergency issues
            {'issue': 'severe accident', 'specialty': 'emergency', 'urgency': 'critical', 'keywords': 'accident trauma emergency critical'},
            {'issue': 'unconscious', 'specialty': 'emergency', 'urgency': 'critical', 'keywords': 'unconscious emergency critical trauma'}
        ]
    
    def _train_models(self):
        """Train ML models for hospital recommendation"""
        logger.info("Training hospital recommendation models...")
        
        # Prepare training data
        X_text = []
        y_specialty = []
        
        for issue in self.medical_issues:
            X_text.append(issue['keywords'])
            y_specialty.append(issue['specialty'])
        
        # Train specialty classifier
        self.specialty_vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        X_vectorized = self.specialty_vectorizer.fit_transform(X_text)
        
        self.issue_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.issue_classifier.fit(X_vectorized, y_specialty)
        
        logger.info("Hospital recommendation models trained successfully")
    
    def recommend_hospitals(self, medical_issue: str, user_city: str, 
                          urgency_level: str = 'medium', max_hospitals: int = 10) -> List[Dict[str, Any]]:
        """Recommend hospitals based on medical issue using ML"""
        logger.info(f"Recommending hospitals for: {medical_issue} in {user_city}")
        
        # Classify the medical issue
        issue_vector = self.specialty_vectorizer.transform([medical_issue])
        predicted_specialty = self.issue_classifier.predict(issue_vector)[0]
        specialty_confidence = max(self.issue_classifier.predict_proba(issue_vector)[0])
        
        logger.info(f"Predicted specialty: {predicted_specialty} (confidence: {specialty_confidence:.2f})")
        
        # Get user coordinates and state
        user_lat, user_lon = self._get_city_coordinates(user_city)
        user_state = self._get_city_state(user_city)
        
        # Filter hospitals by STATE ONLY
        state_hospitals = [h for h in self.hospitals if h['state'].lower() == user_state.lower()]
        
        if not state_hospitals:
            logger.warning(f"No hospitals found in state: {user_state}")
            return []
        
        logger.info(f"Found {len(state_hospitals)} hospitals in {user_state} state")
        
        # Score and rank hospitals (only from the same state)
        scored_hospitals = []
        
        for hospital in state_hospitals:
            score = self._calculate_hospital_score(
                hospital, predicted_specialty, urgency_level, 
                user_lat, user_lon, medical_issue
            )
            
            if score > 0:  # Only include hospitals with positive scores
                hospital_info = hospital.copy()
                hospital_info['recommendation_score'] = round(score, 2)
                hospital_info['distance_km'] = round(
                    self._calculate_distance(user_lat, user_lon, 
                                           hospital['latitude'], hospital['longitude']), 2
                )
                hospital_info['specialty_match'] = predicted_specialty in hospital['specialties']
                hospital_info['urgency_match'] = self._check_urgency_match(hospital, urgency_level)
                
                # Add specialty-specific information
                if predicted_specialty in hospital['specialties']:
                    specialty_info = hospital['specialties'][predicted_specialty]
                    hospital_info['specialty_rating'] = specialty_info['rating']
                    hospital_info['specialty_doctors'] = specialty_info['doctors_count']
                    hospital_info['specialty_success_rate'] = specialty_info['success_rate']
                    hospital_info['specialty_wait_time'] = specialty_info['wait_time_days']
                else:
                    hospital_info['specialty_rating'] = 0
                    hospital_info['specialty_doctors'] = 0
                    hospital_info['specialty_success_rate'] = 0
                    hospital_info['specialty_wait_time'] = 999
                
                scored_hospitals.append(hospital_info)
        
        # Sort by recommendation score (descending)
        scored_hospitals.sort(key=lambda x: x['recommendation_score'], reverse=True)
        
        # Return top hospitals
        recommendations = scored_hospitals[:max_hospitals]
        
        # Add recommendation reasoning
        for i, hospital in enumerate(recommendations):
            hospital['rank'] = i + 1
            hospital['recommendation_reason'] = self._generate_recommendation_reason(
                hospital, predicted_specialty, medical_issue
            )
        
        logger.info(f"Generated {len(recommendations)} hospital recommendations")
        return recommendations
    
    def _calculate_hospital_score(self, hospital: Dict, specialty: str, urgency: str,
                                user_lat: float, user_lon: float, medical_issue: str) -> float:
        """Calculate comprehensive hospital recommendation score with emphasis on doctor quality"""
        score = 0.0
        
        # Doctor Quality and Specialty Expertise (50% - Most Important)
        if specialty in hospital['specialties']:
            specialty_data = hospital['specialties'][specialty]
            # Heavily weight doctor expertise and specialty quality
            doctor_quality_score = (
                specialty_data['rating'] * 0.5 +  # Specialty department rating
                (specialty_data['doctors_count'] / 10) * 0.3 +  # Number of specialists
                (specialty_data['success_rate'] / 100) * 0.4 +  # Success rate
                (1 - specialty_data['wait_time_days'] / 30) * 0.1  # Availability
            )
            score += doctor_quality_score * 0.5
        else:
            score += 0.05  # Heavy penalty for no specialty match
        
        # Base hospital quality (25%)
        base_score = (
            hospital['overall_rating'] * 0.3 +
            hospital['equipment_quality'] * 0.25 +
            hospital['doctor_expertise'] * 0.3 +  # Emphasize doctor expertise
            hospital['infrastructure'] * 0.1 +
            hospital['patient_satisfaction'] * 0.05
        )
        score += base_score * 0.25
        
        # Urgency match (15%)
        urgency_score = self._calculate_urgency_score(hospital, urgency)
        score += urgency_score * 0.15
        
        # Distance factor (10%) - Prioritize same city
        distance = self._calculate_distance(user_lat, user_lon, 
                                          hospital['latitude'], hospital['longitude'])
        if distance < 50:  # Same city or very close
            distance_score = 1.0
        elif distance < 100:  # Nearby city
            distance_score = 0.8
        else:  # Far away
            distance_score = max(0, 1 - (distance / 500))
        score += distance_score * 0.1
        
        # Emergency services bonus (5%)
        if urgency in ['critical', 'high'] and hospital['emergency_services']:
            score += 0.05
        
        return score
    
    def _calculate_urgency_score(self, hospital: Dict, urgency: str) -> float:
        """Calculate urgency match score"""
        if urgency == 'critical':
            return 1.0 if hospital['emergency_services'] and hospital['icu_beds'] > 10 else 0.5
        elif urgency == 'high':
            return 0.8 if hospital['emergency_services'] else 0.6
        elif urgency == 'medium':
            return 0.7 if hospital['wait_time_minutes'] < 60 else 0.5
        else:  # low
            return 0.6
    
    def _check_urgency_match(self, hospital: Dict, urgency: str) -> bool:
        """Check if hospital matches urgency requirements"""
        if urgency == 'critical':
            return hospital['emergency_services'] and hospital['icu_beds'] > 5
        elif urgency == 'high':
            return hospital['emergency_services'] or hospital['wait_time_minutes'] < 90
        else:
            return True
    
    def _generate_recommendation_reason(self, hospital: Dict, specialty: str, medical_issue: str) -> str:
        """Generate human-readable recommendation reason"""
        reasons = []
        
        if hospital['specialty_match']:
            reasons.append(f"Specialized in {specialty} with {hospital['specialty_doctors']} expert doctors")
            reasons.append(f"{specialty} success rate: {hospital['specialty_success_rate']}%")
        
        if hospital['overall_rating'] >= 4.5:
            reasons.append("Highly rated hospital")
        
        if hospital['emergency_services'] and 'emergency' in medical_issue.lower():
            reasons.append("24/7 emergency services available")
        
        if hospital['distance_km'] < 10:
            reasons.append("Close to your location")
        elif hospital['distance_km'] < 50:
            reasons.append("Within reasonable distance")
        
        if hospital['icu_beds'] > 20:
            reasons.append("Well-equipped ICU facilities")
        
        if hospital['insurance_accepted']:
            reasons.append("Accepts insurance")
        
        return "; ".join(reasons[:3])  # Top 3 reasons
    
    def _get_city_coordinates(self, city: str) -> Tuple[float, float]:
        """Get coordinates for a city"""
        city_coords = {
            'delhi': (28.7041, 77.1025),
            'mumbai': (19.0760, 72.8777),
            'bangalore': (12.9716, 77.5946),
            'chennai': (13.0827, 77.2707),
            'kolkata': (22.5726, 88.3639),
            'hyderabad': (17.3850, 78.4867),
            'pune': (18.5204, 73.8567),
            'ahmedabad': (23.0225, 72.5714)
        }
        
        city_lower = city.lower()
        return city_coords.get(city_lower, city_coords['delhi'])  # Default to Delhi
    
    def _get_city_state(self, city: str) -> str:
        """Get state for a city"""
        city_state_map = {
            'delhi': 'Delhi',
            'mumbai': 'Maharashtra',
            'bangalore': 'Karnataka',
            'chennai': 'Tamil Nadu',
            'kolkata': 'West Bengal',
            'hyderabad': 'Telangana',
            'pune': 'Maharashtra',
            'ahmedabad': 'Gujarat'
        }
        
        city_lower = city.lower()
        return city_state_map.get(city_lower, 'Delhi')  # Default to Delhi
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
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
    
    def get_doctor_recommendations(self, specialty: str, hospital_id: str = None) -> List[Dict[str, Any]]:
        """Get doctor recommendations for a specialty, prioritizing quality"""
        doctors = [d for d in self.doctors if d['specialty'] == specialty]
        
        if hospital_id:
            doctors = [d for d in doctors if d['hospital_id'] == hospital_id]
        
        # Enhanced sorting: prioritize by doctor quality score
        for doctor in doctors:
            # Calculate doctor quality score
            quality_score = (
                doctor['rating'] * 0.4 +  # Rating weight
                (doctor['experience_years'] / 40) * 0.3 +  # Experience weight
                (doctor['success_rate'] / 100) * 0.2 +  # Success rate weight
                (doctor['procedures_performed'] / 1000) * 0.1  # Procedure count weight
            )
            doctor['quality_score'] = quality_score
        
        # Sort by quality score, then by rating, then by experience
        doctors.sort(key=lambda x: (x['quality_score'], x['rating'], x['experience_years']), reverse=True)
        
        return doctors[:10]  # Top 10 doctors
    
    def save_models(self, filepath: str = 'ml_models/trained_models/'):
        """Save trained models"""
        import os
        os.makedirs(filepath, exist_ok=True)
        
        joblib.dump(self.issue_classifier, f'{filepath}/issue_classifier.pkl')
        joblib.dump(self.specialty_vectorizer, f'{filepath}/specialty_vectorizer.pkl')
        
        # Save data
        with open(f'{filepath}/hospitals.json', 'w') as f:
            json.dump(self.hospitals, f, default=str, indent=2)
        
        with open(f'{filepath}/doctors.json', 'w') as f:
            json.dump(self.doctors, f, default=str, indent=2)
        
        logger.info(f"Models saved to {filepath}")
    
    def load_models(self, filepath: str = 'ml_models/trained_models/'):
        """Load trained models"""
        try:
            self.issue_classifier = joblib.load(f'{filepath}/issue_classifier.pkl')
            self.specialty_vectorizer = joblib.load(f'{filepath}/specialty_vectorizer.pkl')
            
            with open(f'{filepath}/hospitals.json', 'r') as f:
                self.hospitals = json.load(f)
            
            with open(f'{filepath}/doctors.json', 'r') as f:
                self.doctors = json.load(f)
            
            logger.info("Hospital recommendation models loaded successfully")
            return True
        except Exception as e:
            logger.warning(f"Could not load models: {e}")
            return False
