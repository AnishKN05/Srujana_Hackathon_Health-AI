from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import mysql.connector
import json
import os
import sys
from datetime import datetime
import logging

# Add ml_models to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ml_models'))

try:
    from nutrition_classifier import NutritionClassifier
    from physio_classifier import PhysioClassifier
    from blood_bank_system import BloodBankSystem
    from hospital_recommender import HospitalRecommender
except ImportError as e:
    logger.warning(f"Could not import ML models: {e}")
    NutritionClassifier = None
    PhysioClassifier = None
    BloodBankSystem = None
    HospitalRecommender = None

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize ML models
nutrition_classifier = None
physio_classifier = None
blood_bank_system = None
hospital_recommender = None

def initialize_ml_models():
    """Initialize ML models"""
    global nutrition_classifier, physio_classifier, blood_bank_system, hospital_recommender
    
    try:
        if NutritionClassifier:
            nutrition_classifier = NutritionClassifier()
            nutrition_classifier.load_model()
            logger.info("Nutrition classifier loaded successfully")
        
        if PhysioClassifier:
            physio_classifier = PhysioClassifier()
            physio_classifier.load_model()
            logger.info("Physiotherapy classifier loaded successfully")
        
        if BloodBankSystem:
            blood_bank_system = BloodBankSystem()
            blood_bank_system.load_model()
            logger.info("Blood bank system loaded successfully")
        
        if HospitalRecommender:
            hospital_recommender = HospitalRecommender()
            if not hospital_recommender.load_models():
                # Train new models if loading fails
                hospital_recommender = HospitalRecommender()
                hospital_recommender.save_models()
            logger.info("Hospital recommender loaded successfully")
            
    except Exception as e:
        logger.error(f"Error initializing ML models: {e}")

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'cse123',  # Change this to your MySQL password
    'database': 'health_ai_db',
    'port': 3306
}

def get_db_connection():
    """Get MySQL database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as err:
        logger.error(f"Database connection error: {err}")
        return None

def init_database():
    """Initialize database and create tables"""
    try:
        connection = get_db_connection()
        if not connection:
            return False
        
        cursor = connection.cursor()
        
        # Create database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS health_ai_db")
        cursor.execute("USE health_ai_db")
        
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(255) UNIQUE,
                name VARCHAR(255),
                age INT,
                gender VARCHAR(50),
                location VARCHAR(100),
                consent BOOLEAN,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create symptoms table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS symptoms (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(255),
                symptoms TEXT,
                duration VARCHAR(255),
                severity VARCHAR(50),
                age INT,
                gender VARCHAR(50),
                medical_history TEXT,
                additional_info TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create image_analysis table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS image_analysis (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(255),
                filename VARCHAR(255),
                description TEXT,
                analysis_result TEXT,
                confidence_score FLOAT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create chat_messages table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(255),
                session_id VARCHAR(255),
                message TEXT,
                response TEXT,
                message_type ENUM('user', 'assistant'),
                service_type ENUM('general', 'nutrition', 'physio', 'blood_bank'),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create nutrition_consultations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS nutrition_consultations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(255),
                query TEXT,
                category VARCHAR(100),
                recommendations TEXT,
                meal_plan TEXT,
                confidence_score FLOAT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create physio_consultations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS physio_consultations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(255),
                query TEXT,
                category VARCHAR(100),
                exercises TEXT,
                recommendations TEXT,
                precautions TEXT,
                confidence_score FLOAT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create blood_requests table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS blood_requests (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(255),
                blood_type VARCHAR(10),
                request_type VARCHAR(100),
                urgency_level ENUM('low', 'medium', 'high', 'critical'),
                city VARCHAR(100),
                state VARCHAR(100),
                contact_number VARCHAR(20),
                additional_info TEXT,
                status ENUM('pending', 'matched', 'fulfilled', 'cancelled'),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create blood_donors table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS blood_donors (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(255),
                name VARCHAR(255),
                age INT,
                gender VARCHAR(20),
                blood_type VARCHAR(10),
                city VARCHAR(100),
                state VARCHAR(100),
                contact_number VARCHAR(20),
                email VARCHAR(255),
                last_donation_date DATE,
                donation_count INT DEFAULT 0,
                is_available BOOLEAN DEFAULT TRUE,
                medical_conditions TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create hospitals table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS hospitals (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                city VARCHAR(100),
                state VARCHAR(100),
                latitude DECIMAL(10, 8),
                longitude DECIMAL(11, 8),
                contact_number VARCHAR(20),
                emergency_contact VARCHAR(20),
                specialties TEXT,
                bed_capacity INT,
                is_government BOOLEAN DEFAULT FALSE,
                has_blood_bank BOOLEAN DEFAULT FALSE,
                blood_bank_capacity INT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create blood_inventory table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS blood_inventory (
                id INT AUTO_INCREMENT PRIMARY KEY,
                hospital_id INT,
                blood_type VARCHAR(10),
                units_available INT DEFAULT 0,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (hospital_id) REFERENCES hospitals(id) ON DELETE CASCADE
            )
        """)
        
        connection.commit()
        cursor.close()
        connection.close()
        
        logger.info("Database initialized successfully")
        return True
        
    except mysql.connector.Error as err:
        logger.error(f"Database initialization error: {err}")
        return False

# Indian healthcare-specific symptom analysis
def analyze_symptoms(symptoms, duration=None, severity=None, age=None, gender=None, medical_history=None):
    """Indian healthcare-focused symptom analysis"""
    
    symptoms_lower = [s.lower() for s in symptoms]
    
    # Common conditions in India
    conditions = []
    
    # Dengue symptoms (common in India)
    if any(s in symptoms_lower for s in ['fever', 'high temperature']) and any(s in symptoms_lower for s in ['headache', 'body pain', 'joint pain', 'muscle pain']):
        conditions.append({
            'name': 'Possible Dengue Fever',
            'probability': 0.7,
            'description': 'Viral infection transmitted by mosquitoes, common in India',
            'severity': 'high',
            'indian_context': 'Dengue is endemic in many parts of India. Seek immediate medical attention.'
        })
    
    # Malaria symptoms
    if any(s in symptoms_lower for s in ['fever', 'chills', 'sweating']) and any(s in symptoms_lower for s in ['headache', 'nausea', 'vomiting']):
        conditions.append({
            'name': 'Possible Malaria',
            'probability': 0.6,
            'description': 'Parasitic infection transmitted by mosquitoes',
            'severity': 'high',
            'indian_context': 'Malaria is prevalent in many Indian states. Immediate medical care required.'
        })
    
    # Typhoid symptoms
    if any(s in symptoms_lower for s in ['fever', 'headache', 'weakness']) and any(s in symptoms_lower for s in ['stomach pain', 'diarrhea', 'constipation']):
        conditions.append({
            'name': 'Possible Typhoid',
            'probability': 0.65,
            'description': 'Bacterial infection affecting the digestive system',
            'severity': 'high',
            'indian_context': 'Typhoid is common in India due to contaminated food/water. Seek medical help.'
        })
    
    # Heat-related illnesses (common in Indian summers)
    if any(s in symptoms_lower for s in ['fever', 'dizziness', 'nausea']) and any(s in symptoms_lower for s in ['headache', 'weakness', 'fatigue']):
        conditions.append({
            'name': 'Heat Exhaustion/Heat Stroke',
            'probability': 0.7,
            'description': 'Heat-related illness due to high temperatures',
            'severity': 'high',
            'indian_context': 'Common during Indian summers. Move to cool place and hydrate immediately.'
        })
    
    # Respiratory conditions
    if any(s in symptoms_lower for s in ['cough', 'sore throat', 'runny nose', 'congestion']):
        if 'fever' in symptoms_lower:
            conditions.append({
                'name': 'Common Cold or Flu',
                'probability': 0.8,
                'description': 'Viral infection of the upper respiratory tract',
                'severity': 'moderate',
                'indian_context': 'Common in India, especially during monsoon season.'
            })
        else:
            conditions.append({
                'name': 'Common Cold',
                'probability': 0.7,
                'description': 'Mild viral infection',
                'severity': 'low',
                'indian_context': 'Usually resolves with rest and home remedies.'
            })
    
    # Gastrointestinal conditions (common in India)
    if any(s in symptoms_lower for s in ['nausea', 'vomiting', 'diarrhea', 'stomach pain']):
        conditions.append({
            'name': 'Gastroenteritis/Food Poisoning',
            'probability': 0.75,
            'description': 'Inflammation of the stomach and intestines',
            'severity': 'moderate',
            'indian_context': 'Common in India due to contaminated food/water. Stay hydrated.'
        })
    
    # Headache conditions
    if 'headache' in symptoms_lower:
        if 'fever' in symptoms_lower:
            conditions.append({
                'name': 'Viral Infection with Headache',
                'probability': 0.6,
                'description': 'Headache associated with viral infection',
                'severity': 'moderate',
                'indian_context': 'Could be related to seasonal infections common in India.'
            })
        else:
            conditions.append({
                'name': 'Tension Headache',
                'probability': 0.7,
                'description': 'Common headache often caused by stress or tension',
                'severity': 'low',
                'indian_context': 'Common in urban areas due to stress and pollution.'
            })
    
    # Skin conditions (common in Indian climate)
    if any(s in symptoms_lower for s in ['rash', 'itching', 'redness', 'swelling']):
        conditions.append({
            'name': 'Skin Irritation or Allergic Reaction',
            'probability': 0.65,
            'description': 'Skin condition that may be allergic or irritant-related',
            'severity': 'low',
            'indian_context': 'Common due to heat, humidity, and environmental factors in India.'
        })
    
    # If no specific conditions found, add general
    if not conditions:
        conditions.append({
            'name': 'General Health Concern',
            'probability': 0.5,
            'description': 'Please provide more specific symptoms for better analysis',
            'severity': 'low',
            'indian_context': 'Consult a local healthcare provider for proper evaluation.'
        })
    
    return conditions

def get_first_aid_advice(condition_name):
    """Get Indian healthcare-specific first aid advice"""
    advice_db = {
        'Possible Dengue Fever': {
            'immediate_actions': [
                'Call 108 immediately - this is a medical emergency',
                'Rest in a cool, well-ventilated room',
                'Stay hydrated with ORS (Oral Rehydration Solution)',
                'Use paracetamol for fever (avoid aspirin/ibuprofen)',
                'Apply cool compresses to reduce fever'
            ],
            'do_not_do': [
                'Do not take aspirin or ibuprofen',
                'Do not delay seeking medical help',
                'Do not ignore warning signs'
            ],
            'when_to_seek_help': [
                'Immediately - dengue requires hospital care',
                'If you have severe abdominal pain',
                'If you have persistent vomiting',
                'If you have bleeding from nose/gums'
            ],
            'emergency_signs': [
                'Severe abdominal pain',
                'Persistent vomiting',
                'Bleeding from nose, gums, or under skin',
                'Difficulty breathing',
                'Restlessness or confusion'
            ],
            'indian_context': 'Dengue is endemic in India. Government hospitals provide free treatment.'
        },
        'Possible Malaria': {
            'immediate_actions': [
                'Call 108 for immediate medical care',
                'Rest in a cool environment',
                'Stay hydrated with clean water',
                'Use paracetamol for fever',
                'Keep mosquito nets around bed'
            ],
            'do_not_do': [
                'Do not delay medical treatment',
                'Do not take anti-malarial drugs without prescription',
                'Do not ignore fever cycles'
            ],
            'when_to_seek_help': [
                'Immediately - malaria requires urgent treatment',
                'If fever comes in cycles (every 2-3 days)',
                'If you have severe chills and sweating'
            ],
            'emergency_signs': [
                'High fever with chills',
                'Severe headache',
                'Confusion or altered consciousness',
                'Difficulty breathing',
                'Severe anemia symptoms'
            ],
            'indian_context': 'Malaria is common in many Indian states. Free treatment available at government hospitals.'
        },
        'Possible Typhoid': {
            'immediate_actions': [
                'Call 108 for medical assistance',
                'Rest completely',
                'Stay hydrated with clean, boiled water',
                'Eat light, easily digestible foods',
                'Use paracetamol for fever'
            ],
            'do_not_do': [
                'Do not eat street food or unhygienic food',
                'Do not drink untreated water',
                'Do not delay medical treatment'
            ],
            'when_to_seek_help': [
                'Immediately - typhoid requires antibiotic treatment',
                'If you have persistent high fever',
                'If you have severe abdominal pain'
            ],
            'emergency_signs': [
                'High fever (103-104°F)',
                'Severe abdominal pain',
                'Persistent diarrhea or constipation',
                'Rose-colored spots on chest/abdomen',
                'Confusion or delirium'
            ],
            'indian_context': 'Typhoid is common in India. Prevention through clean water and food hygiene is crucial.'
        },
        'Heat Exhaustion/Heat Stroke': {
            'immediate_actions': [
                'Move to a cool, shaded area immediately',
                'Remove excess clothing',
                'Apply cool water or ice packs to body',
                'Drink cool water or ORS',
                'Fan the person to increase cooling'
            ],
            'do_not_do': [
                'Do not give alcohol or caffeine',
                'Do not leave person alone',
                'Do not ignore symptoms'
            ],
            'when_to_seek_help': [
                'Call 108 if symptoms are severe',
                'If person becomes unconscious',
                'If body temperature is very high'
            ],
            'emergency_signs': [
                'Body temperature above 104°F',
                'Loss of consciousness',
                'Seizures',
                'Difficulty breathing',
                'Confusion or disorientation'
            ],
            'indian_context': 'Common during Indian summers (April-June). Stay indoors during peak heat hours.'
        },
        'Common Cold': {
            'immediate_actions': [
                'Get plenty of rest',
                'Stay hydrated with warm water, herbal teas',
                'Use steam inhalation with eucalyptus oil',
                'Gargle with warm salt water',
                'Use honey and ginger for cough'
            ],
            'do_not_do': [
                'Do not take antibiotics unless prescribed',
                'Avoid cold drinks and ice cream',
                'Do not smoke or be around smoke'
            ],
            'when_to_seek_help': [
                'If symptoms persist for more than 10 days',
                'If you develop high fever',
                'If you have difficulty breathing'
            ],
            'emergency_signs': [
                'Severe difficulty breathing',
                'Chest pain',
                'High fever with confusion'
            ],
            'indian_context': 'Common during monsoon season. Traditional remedies like turmeric milk can help.'
        },
        'Gastroenteritis': {
            'immediate_actions': [
                'Stay hydrated with clear fluids',
                'Rest and avoid solid foods until vomiting stops',
                'Gradually reintroduce bland foods',
                'Wash hands frequently'
            ],
            'do_not_do': [
                'Do not eat solid foods while vomiting',
                'Avoid dairy products and caffeine'
            ],
            'when_to_seek_help': [
                'If symptoms persist for more than 2-3 days',
                'If you cannot keep fluids down',
                'If you have signs of dehydration'
            ],
            'emergency_signs': [
                'Severe dehydration',
                'Blood in vomit or stool',
                'High fever'
            ]
        },
        'Tension Headache': {
            'immediate_actions': [
                'Rest in a quiet, dark room',
                'Apply a cold or warm compress',
                'Stay hydrated',
                'Try gentle neck stretches'
            ],
            'do_not_do': [
                'Do not take more than recommended pain medication',
                'Avoid bright lights and loud noises'
            ],
            'when_to_seek_help': [
                'If headache is severe and sudden',
                'If headache is accompanied by fever',
                'If headache worsens with movement'
            ],
            'emergency_signs': [
                'Sudden, severe headache',
                'Headache with fever and stiff neck',
                'Headache after head injury'
            ]
        }
    }
    
    # Default advice
    default_advice = {
        'immediate_actions': [
            'Monitor your symptoms closely',
            'Get plenty of rest',
            'Stay hydrated'
        ],
        'do_not_do': [
            'Do not ignore persistent symptoms',
            'Do not self-medicate without medical advice'
        ],
        'when_to_seek_help': [
            'If symptoms worsen or persist',
            'If you develop new symptoms'
        ],
        'emergency_signs': [
            'Severe pain',
            'Difficulty breathing',
            'Chest pain'
        ]
    }
    
    return advice_db.get(condition_name, default_advice)

# Routes
@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('index.html')

@app.route('/firstaid.html')
def firstaid():
    """Serve the first aid page"""
    return render_template('firstaid.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Health AI Platform API is running',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/user/register', methods=['POST'])
def register_user():
    """Register a new user"""
    try:
        data = request.get_json()
        
        user_id = data.get('user_id')
        name = data.get('name')
        age = data.get('age')
        gender = data.get('gender')
        location = data.get('location')
        consent = data.get('consent')
        
        if not all([user_id, name, age, gender, location, consent]):
            return jsonify({'error': 'All fields are required'}), 400
        
        # Save user to database
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO users (user_id, name, age, gender, location, consent)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                name = VALUES(name),
                age = VALUES(age),
                gender = VALUES(gender),
                location = VALUES(location),
                consent = VALUES(consent)
            """, (user_id, name, age, gender, location, consent))
            connection.commit()
            cursor.close()
            connection.close()
        
        return jsonify({
            'status': 'success',
            'message': 'User registered successfully',
            'user_id': user_id
        })
        
    except Exception as e:
        logger.error(f"Error registering user: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/symptoms/analyze', methods=['POST'])
def analyze_symptoms_endpoint():
    """Analyze symptoms endpoint"""
    try:
        data = request.get_json()
        
        # Extract data
        user_id = data.get('user_id', 'anonymous')
        symptoms = data.get('symptoms', [])
        duration = data.get('duration')
        severity = data.get('severity')
        age = data.get('age')
        gender = data.get('gender')
        medical_history = data.get('medical_history', [])
        additional_info = data.get('additional_info')
        
        # Validate input
        if not symptoms:
            return jsonify({'error': 'Symptoms are required'}), 400
        
        # Analyze symptoms
        possible_conditions = analyze_symptoms(
            symptoms, duration, severity, age, gender, medical_history
        )
        
        # Get first aid advice for primary condition
        primary_condition = possible_conditions[0] if possible_conditions else None
        first_aid_advice = get_first_aid_advice(primary_condition['name']) if primary_condition else {}
        
        # Save to database
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO symptoms (user_id, symptoms, duration, severity, age, gender, medical_history, additional_info)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (user_id, json.dumps(symptoms), duration, severity, age, gender, 
                  json.dumps(medical_history), additional_info))
            connection.commit()
            cursor.close()
            connection.close()
        
        # Prepare response
        response = {
            'user_id': user_id,
            'possible_conditions': possible_conditions,
            'first_aid_advice': first_aid_advice,
            'confidence_score': primary_condition['probability'] if primary_condition else 0.5,
            'follow_up_questions': [
                'How long have you been experiencing these symptoms?',
                'Have you tried any treatments so far?',
                'Are there any factors that make your symptoms better or worse?'
            ],
            'timestamp': datetime.now().isoformat(),
            'disclaimer': 'This analysis is for educational purposes only and is not a substitute for professional medical advice.'
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error analyzing symptoms: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/chat', methods=['POST'])
def chat_endpoint():
    """Chat endpoint for conversational interaction"""
    try:
        data = request.get_json()
        
        user_id = data.get('user_id', 'anonymous')
        message = data.get('message', '')
        session_id = data.get('session_id', f'session_{user_id}_{datetime.now().timestamp()}')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Indian healthcare-focused chat response based on keywords
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['headache', 'head pain']):
            response = "I understand you're experiencing a headache. In India, headaches can be caused by various factors including heat, pollution, stress, or infections. Can you tell me more about the pain? Is it sharp, dull, or throbbing? How long have you had it?"
            suggested_questions = [
                "How long have you had this headache?",
                "On a scale of 1-10, how would you rate the pain?",
                "Have you been exposed to extreme heat recently?",
                "Are you experiencing any fever along with the headache?"
            ]
        elif any(word in message_lower for word in ['fever', 'temperature']):
            response = "A fever in India can indicate various conditions including dengue, malaria, typhoid, or common infections. What's your current temperature? Are you experiencing any other symptoms like chills, sweating, or body pain?"
            suggested_questions = [
                "What's your current temperature?",
                "How long have you had the fever?",
                "Are you experiencing chills and sweating?",
                "Do you have any body pain or joint pain?",
                "Have you been bitten by mosquitoes recently?"
            ]
        elif any(word in message_lower for word in ['rash', 'skin', 'itching']):
            response = "Skin issues in India can be caused by heat, humidity, allergies, or infections. Can you describe the rash? Is it red, raised, or does it itch? When did you first notice it? Have you been exposed to any new products or foods?"
            suggested_questions = [
                "Can you describe the appearance of the rash?",
                "Is the affected area itchy or painful?",
                "When did you first notice the skin changes?",
                "Have you used any new skincare products recently?",
                "Are you experiencing this during hot weather?"
            ]
        elif any(word in message_lower for word in ['dengue', 'malaria', 'typhoid']):
            response = "These are serious conditions that are common in India. If you suspect any of these, please seek immediate medical attention. Call 108 for emergency services or visit the nearest hospital. These conditions require proper medical diagnosis and treatment."
            suggested_questions = [
                "Do you have a high fever?",
                "Are you experiencing severe body pain?",
                "Have you been bitten by mosquitoes?",
                "Do you have any bleeding from nose or gums?",
                "Are you experiencing severe abdominal pain?"
            ]
        elif any(word in message_lower for word in ['heat', 'summer', 'hot weather']):
            response = "Heat-related illnesses are common in India, especially during summer months. Are you experiencing dizziness, nausea, or excessive sweating? It's important to stay hydrated and avoid direct sun exposure during peak hours."
            suggested_questions = [
                "Are you feeling dizzy or nauseous?",
                "Have you been drinking enough water?",
                "Are you experiencing excessive sweating?",
                "Have you been in direct sunlight for long periods?",
                "Do you have a headache along with these symptoms?"
            ]
        else:
            response = "I'm here to help with your health concerns. In India, it's important to consider factors like climate, local diseases, and environmental conditions. Can you describe your symptoms in more detail? The more specific you are, the better I can assist you."
            suggested_questions = [
                "Can you describe your symptoms in more detail?",
                "How long have you been experiencing these symptoms?",
                "Are there any other symptoms you're concerned about?",
                "Have you been exposed to any environmental factors recently?",
                "Are you taking any medications currently?"
            ]
        
        # Save chat messages to database
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO chat_messages (user_id, session_id, message, response, message_type)
                VALUES (%s, %s, %s, %s, 'user')
            """, (user_id, session_id, message, ''))
            cursor.execute("""
                INSERT INTO chat_messages (user_id, session_id, message, response, message_type)
                VALUES (%s, %s, %s, %s, 'assistant')
            """, (user_id, session_id, '', response))
            connection.commit()
            cursor.close()
            connection.close()
        
        return jsonify({
            'user_id': user_id,
            'response': response,
            'suggested_questions': suggested_questions,
            'confidence_level': 'medium',
            'requires_professional_consultation': False,
            'session_id': session_id,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in chat: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/image/analyze', methods=['POST'])
def analyze_image_endpoint():
    """Simple image analysis endpoint"""
    try:
        # For now, return a simple response since we're focusing on getting the basic platform working
        return jsonify({
            'user_id': 'anonymous',
            'analysis_result': {
                'condition_type': 'skin_condition',
                'possible_conditions': [{
                    'condition_name': 'General Skin Condition',
                    'probability': 0.6,
                    'description': 'Image analysis feature is being developed',
                    'severity': 'low'
                }],
                'detected_features': [],
                'severity_assessment': 'low',
                'confidence_score': 0.6,
                'image_quality': 'good'
            },
            'recommendations': [
                'Consult a healthcare professional for proper evaluation',
                'Keep the affected area clean and dry',
                'Monitor for any changes'
            ],
            'first_aid_advice': {
                'immediate_actions': [
                    'Keep the area clean and dry',
                    'Monitor for changes'
                ],
                'do_not_do': [
                    'Do not scratch or pick at the area'
                ],
                'when_to_seek_help': [
                    'If the condition worsens',
                    'If you develop signs of infection'
                ],
                'emergency_signs': [
                    'Signs of severe infection',
                    'Difficulty breathing'
                ]
            },
            'follow_up_questions': [
                'How long have you had this condition?',
                'Have you experienced any pain or itching?'
            ],
            'timestamp': datetime.now().isoformat(),
            'disclaimer': 'This image analysis is for educational purposes only.'
        })
        
    except Exception as e:
        logger.error(f"Error analyzing image: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/nutrition/consult', methods=['POST'])
def nutrition_consultation():
    """Nutrition consultation endpoint"""
    try:
        data = request.get_json()
        
        user_id = data.get('user_id', 'anonymous')
        query = data.get('query', '')
        user_context = data.get('user_context', {})
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        if not nutrition_classifier:
            return jsonify({'error': 'Nutrition service not available'}), 503
        
        # Get nutrition recommendation
        response = nutrition_classifier.generate_nutrition_response(query, user_context)
        
        # Save to database
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO nutrition_consultations (user_id, query, category, recommendations, meal_plan, confidence_score)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (user_id, query, response['prediction']['category'], 
                  json.dumps(response['prediction']['recommendations']),
                  json.dumps(response['prediction']['meal_plan']),
                  response['prediction']['confidence']))
            connection.commit()
            cursor.close()
            connection.close()
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error in nutrition consultation: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/physio/consult', methods=['POST'])
def physio_consultation():
    """Physiotherapy consultation endpoint"""
    try:
        data = request.get_json()
        
        user_id = data.get('user_id', 'anonymous')
        query = data.get('query', '')
        user_context = data.get('user_context', {})
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        if not physio_classifier:
            return jsonify({'error': 'Physiotherapy service not available'}), 503
        
        # Get physiotherapy recommendation
        response = physio_classifier.generate_physio_response(query, user_context)
        
        # Save to database
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO physio_consultations (user_id, query, category, exercises, recommendations, precautions, confidence_score)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (user_id, query, response['prediction']['category'],
                  json.dumps(response['prediction']['exercises']),
                  json.dumps(response['prediction']['recommendations']),
                  json.dumps(response['prediction']['precautions']),
                  response['prediction']['confidence']))
            connection.commit()
            cursor.close()
            connection.close()
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error in physiotherapy consultation: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/blood-bank/request', methods=['POST'])
def blood_bank_request():
    """Blood bank request endpoint"""
    try:
        data = request.get_json()
        
        user_id = data.get('user_id', 'anonymous')
        blood_type = data.get('blood_type', '')
        request_type = data.get('request_type', 'general')
        urgency_level = data.get('urgency_level', 'medium')
        city = data.get('city', 'Delhi')
        state = data.get('state', 'Delhi')
        contact_number = data.get('contact_number', '')
        additional_info = data.get('additional_info', '')
        
        if not blood_type:
            return jsonify({'error': 'Blood type is required'}), 400
        
        if not blood_bank_system:
            return jsonify({'error': 'Blood bank service not available'}), 503
        
        # Check blood availability
        availability = blood_bank_system.check_blood_availability(blood_type, city)
        
        # Find compatible donors
        donors = blood_bank_system.find_compatible_donors(blood_type, city)
        
        # Save blood request to database (optional - continue if database fails)
        try:
            connection = get_db_connection()
            if connection:
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO blood_requests (user_id, blood_type, request_type, urgency_level, city, state, contact_number, additional_info, status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'pending')
                """, (user_id, blood_type, request_type, urgency_level, city, state, contact_number, additional_info))
                connection.commit()
                cursor.close()
                connection.close()
                logger.info("Blood request saved to database")
        except Exception as db_error:
            logger.warning(f"Database save failed (continuing): {db_error}")
            # Continue without database - the blood bank functionality should still work
        
        response = {
            'blood_type': blood_type,
            'city': city,
            'availability': availability,
            'compatible_donors': donors[:10],  # Top 10 donors
            'total_donors_found': len(donors),
            'emergency_contacts': {
                'national_blood_bank': '+91-1800-180-1234',
                'red_cross_india': '+91-1800-180-1234',
                'emergency_services': '108'
            },
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error in blood bank request: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({'error': f'Blood bank request failed: {str(e)}'}), 500

@app.route('/api/blood-bank/donor-register', methods=['POST'])
def register_blood_donor():
    """Register blood donor endpoint"""
    try:
        data = request.get_json()
        
        user_id = data.get('user_id', 'anonymous')
        name = data.get('name', '')
        age = data.get('age')
        gender = data.get('gender', '')
        blood_type = data.get('blood_type', '')
        city = data.get('city', '')
        state = data.get('state', '')
        contact_number = data.get('contact_number', '')
        email = data.get('email', '')
        medical_conditions = data.get('medical_conditions', [])
        
        if not all([name, age, gender, blood_type, city, state, contact_number]):
            return jsonify({'error': 'All required fields must be provided'}), 400
        
        # Save donor to database
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO blood_donors (user_id, name, age, gender, blood_type, city, state, contact_number, email, medical_conditions)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                name = VALUES(name),
                age = VALUES(age),
                gender = VALUES(gender),
                blood_type = VALUES(blood_type),
                city = VALUES(city),
                state = VALUES(state),
                contact_number = VALUES(contact_number),
                email = VALUES(email),
                medical_conditions = VALUES(medical_conditions)
            """, (user_id, name, age, gender, blood_type, city, state, contact_number, email, json.dumps(medical_conditions)))
            connection.commit()
            cursor.close()
            connection.close()
        
        return jsonify({
            'status': 'success',
            'message': 'Donor registered successfully',
            'donor_id': user_id
        })
        
    except Exception as e:
        logger.error(f"Error registering donor: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/blood-bank/hospitals', methods=['GET'])
def get_nearby_hospitals():
    """Get nearby hospitals endpoint"""
    try:
        lat = float(request.args.get('lat', 28.7041))  # Default to Delhi
        lon = float(request.args.get('lon', 77.1025))
        radius = float(request.args.get('radius', 50))  # Default 50km radius
        
        if not blood_bank_system:
            return jsonify({'error': 'Blood bank service not available'}), 503
        
        hospitals = blood_bank_system.find_nearby_hospitals(lat, lon, radius)
        
        return jsonify({
            'hospitals': hospitals,
            'total_found': len(hospitals),
            'search_radius_km': radius,
            'coordinates': {'lat': lat, 'lon': lon}
        })
        
    except Exception as e:
        logger.error(f"Error getting hospitals: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/services/chat', methods=['POST'])
def service_chat():
    """Multi-service chat endpoint"""
    try:
        data = request.get_json()
        
        user_id = data.get('user_id', 'anonymous')
        message = data.get('message', '')
        service_type = data.get('service_type', 'general')
        session_id = data.get('session_id', f'session_{user_id}_{datetime.now().timestamp()}')
        user_context = data.get('user_context', {})
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        response = None
        
        if service_type == 'nutrition' and nutrition_classifier:
            response = nutrition_classifier.generate_nutrition_response(message, user_context)
            response_text = f"Nutrition Advice: {response['prediction']['description']}\n\nRecommendations:\n"
            for rec in response['prediction']['recommendations']:
                response_text += f"• {rec}\n"
            
        elif service_type == 'physio' and physio_classifier:
            response = physio_classifier.generate_physio_response(message, user_context)
            response_text = f"Physiotherapy Advice: {response['prediction']['description']}\n\nExercises:\n"
            for exercise in response['prediction']['exercises']:
                response_text += f"• {exercise}\n"
            
        elif service_type == 'blood_bank' and blood_bank_system:
            response = blood_bank_system.generate_blood_bank_response(message, user_context)
            response_text = f"Blood Bank Service: {response['request_type']}\n"
            if 'blood_availability' in response:
                response_text += f"Blood availability: {response['blood_availability']['total_units_available']} units\n"
            
        else:
            # Fallback to general chat
            response_text = "I'm here to help with your health concerns. Please specify if you need nutrition advice, physiotherapy guidance, or blood bank services."
        
        # Save chat messages to database
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO chat_messages (user_id, session_id, message, response, message_type, service_type)
                VALUES (%s, %s, %s, %s, 'user', %s)
            """, (user_id, session_id, message, '', service_type))
            cursor.execute("""
                INSERT INTO chat_messages (user_id, session_id, message, response, message_type, service_type)
                VALUES (%s, %s, %s, %s, 'assistant', %s)
            """, (user_id, session_id, '', response_text, service_type))
            connection.commit()
            cursor.close()
            connection.close()
        
        return jsonify({
            'user_id': user_id,
            'response': response_text,
            'service_type': service_type,
            'session_id': session_id,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in service chat: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/hospital/recommend', methods=['POST'])
def recommend_hospitals():
    """Recommend hospitals based on medical issue using ML"""
    try:
        data = request.get_json()
        
        medical_issue = data.get('medical_issue', '')
        user_city = data.get('city', 'Delhi')
        urgency_level = data.get('urgency_level', 'medium')
        max_hospitals = data.get('max_hospitals', 10)
        
        if not medical_issue:
            return jsonify({'error': 'Medical issue is required'}), 400
        
        if not hospital_recommender:
            return jsonify({'error': 'Hospital recommendation service not available'}), 503
        
        # Get hospital recommendations using ML
        recommendations = hospital_recommender.recommend_hospitals(
            medical_issue=medical_issue,
            user_city=user_city,
            urgency_level=urgency_level,
            max_hospitals=max_hospitals
        )
        
        # Get doctor recommendations for the top hospitals
        for hospital in recommendations[:3]:  # Top 3 hospitals
            doctors = hospital_recommender.get_doctor_recommendations(
                specialty=hospital.get('specialty_match', 'cardiology'),
                hospital_id=hospital['id']
            )
            hospital['recommended_doctors'] = doctors[:3]  # Top 3 doctors
        
        return jsonify({
            'success': True,
            'medical_issue': medical_issue,
            'predicted_specialty': recommendations[0].get('specialty_match', 'general') if recommendations else 'general',
            'recommendations': recommendations,
            'total_hospitals': len(recommendations)
        })
        
    except Exception as e:
        logger.error(f"Error in hospital recommendation: {str(e)}")
        return jsonify({'error': f'Hospital recommendation failed: {str(e)}'}), 500

@app.route('/api/hospital/doctors', methods=['GET'])
def get_hospital_doctors():
    """Get doctors for a specific hospital and specialty"""
    try:
        hospital_id = request.args.get('hospital_id')
        specialty = request.args.get('specialty', 'cardiology')
        
        if not hospital_id:
            return jsonify({'error': 'Hospital ID is required'}), 400
        
        if not hospital_recommender:
            return jsonify({'error': 'Hospital recommendation service not available'}), 503
        
        doctors = hospital_recommender.get_doctor_recommendations(
            specialty=specialty,
            hospital_id=hospital_id
        )
        
        return jsonify({
            'success': True,
            'hospital_id': hospital_id,
            'specialty': specialty,
            'doctors': doctors
        })
        
    except Exception as e:
        logger.error(f"Error getting hospital doctors: {str(e)}")
        return jsonify({'error': f'Failed to get doctors: {str(e)}'}), 500

if __name__ == '__main__':
    # Initialize database
    if init_database():
        print("✅ Database initialized successfully")
    else:
        print("❌ Database initialization failed")
    
    # Initialize ML models
    initialize_ml_models()
    
    print("🚀 Starting Health AI Platform Backend...")
    print("📍 Backend will be available at: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    print("🔬 Available services:")
    print("   • General Health Chat")
    print("   • Nutrition Consultation")
    print("   • Physiotherapy Guidance")
    print("   • Blood Bank Services")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
