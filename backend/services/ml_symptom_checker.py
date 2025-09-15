"""
ML-based Symptom Checker Service
Replaces OpenAI-based symptom analysis with trained ML models
"""
import sys
import os
import logging
from typing import List, Dict, Any
from datetime import datetime

# Add the ml_models directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'ml_models'))

from symptom_classifier import SymptomClassifier
from models.schemas import (
    SymptomRequest, 
    SymptomResponse, 
    PossibleCondition, 
    FirstAidAdvice,
    ChatMessage,
    ChatResponse,
    SeverityLevel
)

logger = logging.getLogger(__name__)

class MLSymptomCheckerService:
    def __init__(self):
        self.classifier = SymptomClassifier()
        self.classifier.load_model()
        
        # First aid advice database
        self.first_aid_database = {
            'common_cold': {
                'immediate_actions': [
                    'Get plenty of rest',
                    'Stay hydrated by drinking water, tea, or clear broths',
                    'Use a humidifier or take steamy showers to ease congestion',
                    'Gargle with warm salt water for sore throat'
                ],
                'do_not_do': [
                    'Do not take antibiotics unless prescribed by a doctor',
                    'Avoid smoking and secondhand smoke',
                    'Do not share utensils or cups with others'
                ],
                'when_to_seek_help': [
                    'If symptoms persist for more than 10 days',
                    'If you develop a high fever (over 101.3°F)',
                    'If you have difficulty breathing or chest pain'
                ],
                'emergency_signs': [
                    'Severe difficulty breathing',
                    'Chest pain',
                    'Confusion or disorientation',
                    'Persistent high fever'
                ]
            },
            'flu': {
                'immediate_actions': [
                    'Get plenty of rest',
                    'Stay hydrated with water, electrolyte drinks, or clear broths',
                    'Take over-the-counter pain relievers for fever and body aches',
                    'Use a humidifier to ease breathing'
                ],
                'do_not_do': [
                    'Do not take aspirin if you are under 19 years old',
                    'Avoid close contact with others to prevent spread',
                    'Do not return to work or school until fever-free for 24 hours'
                ],
                'when_to_seek_help': [
                    'If symptoms worsen or persist beyond 7-10 days',
                    'If you develop difficulty breathing',
                    'If you have a high fever that does not respond to medication'
                ],
                'emergency_signs': [
                    'Severe difficulty breathing or shortness of breath',
                    'Chest pain or pressure',
                    'Sudden dizziness or confusion',
                    'Severe or persistent vomiting'
                ]
            },
            'headache': {
                'immediate_actions': [
                    'Rest in a quiet, dark room',
                    'Apply a cold or warm compress to your head or neck',
                    'Stay hydrated by drinking water',
                    'Try gentle neck and shoulder stretches'
                ],
                'do_not_do': [
                    'Do not take more than the recommended dose of pain medication',
                    'Avoid bright lights and loud noises',
                    'Do not skip meals'
                ],
                'when_to_seek_help': [
                    'If headache is severe and sudden (thunderclap headache)',
                    'If headache is accompanied by fever, stiff neck, or rash',
                    'If headache worsens with coughing, sneezing, or bending over'
                ],
                'emergency_signs': [
                    'Sudden, severe headache (worst headache of your life)',
                    'Headache with fever, stiff neck, and confusion',
                    'Headache after head injury',
                    'Headache with vision changes or difficulty speaking'
                ]
            },
            'food_poisoning': {
                'immediate_actions': [
                    'Stay hydrated with clear fluids (water, broth, electrolyte drinks)',
                    'Rest and avoid solid foods until vomiting stops',
                    'Gradually reintroduce bland foods (bananas, rice, applesauce, toast)',
                    'Wash hands frequently to prevent spread'
                ],
                'do_not_do': [
                    'Do not eat solid foods while vomiting',
                    'Avoid dairy products, caffeine, and alcohol',
                    'Do not take anti-diarrheal medication without consulting a doctor'
                ],
                'when_to_seek_help': [
                    'If symptoms persist for more than 2-3 days',
                    'If you cannot keep fluids down',
                    'If you have signs of dehydration (dry mouth, dizziness, no urination)'
                ],
                'emergency_signs': [
                    'Severe dehydration (no urination for 8+ hours)',
                    'Blood in vomit or stool',
                    'High fever (over 101.5°F)',
                    'Severe abdominal pain'
                ]
            },
            'rash': {
                'immediate_actions': [
                    'Keep the affected area clean and dry',
                    'Apply cool, wet compresses to reduce itching',
                    'Use fragrance-free moisturizers',
                    'Avoid scratching the affected area'
                ],
                'do_not_do': [
                    'Do not use harsh soaps or hot water',
                    'Avoid known allergens or irritants',
                    'Do not apply strong topical medications without medical advice'
                ],
                'when_to_seek_help': [
                    'If rash spreads rapidly or covers a large area',
                    'If rash is accompanied by fever or other symptoms',
                    'If rash does not improve with basic care'
                ],
                'emergency_signs': [
                    'Rash with difficulty breathing or swallowing',
                    'Rash with fever and joint pain',
                    'Rash that looks like bruises or bleeding under the skin',
                    'Rash with signs of infection (pus, warmth, red streaks)'
                ]
            }
        }
        
        # Default first aid advice for unknown conditions
        self.default_first_aid = {
            'immediate_actions': [
                'Monitor your symptoms closely',
                'Get plenty of rest',
                'Stay hydrated',
                'Keep a record of your symptoms'
            ],
            'do_not_do': [
                'Do not ignore persistent or worsening symptoms',
                'Do not self-medicate without medical advice',
                'Do not delay seeking medical help if concerned'
            ],
            'when_to_seek_help': [
                'If symptoms worsen or persist',
                'If you develop new symptoms',
                'If you are concerned about your health'
            ],
            'emergency_signs': [
                'Severe pain',
                'Difficulty breathing',
                'Chest pain',
                'Signs of severe allergic reaction'
            ]
        }

    async def analyze_symptoms(self, request: SymptomRequest) -> SymptomResponse:
        """
        Analyze symptoms using ML model
        """
        try:
            logger.info(f"Analyzing symptoms for user: {request.user_id}")
            
            # Use ML model to predict conditions
            prediction = self.classifier.predict_condition(
                request.symptoms, 
                request.additional_info or ""
            )
            
            # Convert ML prediction to response format
            possible_conditions = []
            for condition_data in prediction['possible_conditions']:
                possible_conditions.append(PossibleCondition(
                    condition_name=condition_data['condition_name'],
                    probability=condition_data['probability'],
                    description=condition_data['description'],
                    symptoms_match=request.symptoms,
                    severity=SeverityLevel(condition_data['severity'])
                ))
            
            # Get first aid advice for the primary condition
            primary_condition = prediction['primary_condition']
            first_aid_advice = self._get_first_aid_advice(primary_condition)
            
            # Generate follow-up questions
            follow_up_questions = self._generate_follow_up_questions(request, primary_condition)
            
            return SymptomResponse(
                user_id=request.user_id,
                possible_conditions=possible_conditions,
                first_aid_advice=first_aid_advice,
                confidence_score=prediction['confidence_score'],
                follow_up_questions=follow_up_questions,
                disclaimer=self._get_medical_disclaimer()
            )
            
        except Exception as e:
            logger.error(f"Error in ML symptom analysis: {str(e)}")
            return self._create_error_response(request.user_id, str(e))

    async def process_chat_message(self, message: ChatMessage) -> ChatResponse:
        """
        Process conversational messages using ML-based responses
        """
        try:
            logger.info(f"Processing chat message from user: {message.user_id}")
            
            # Extract symptoms from the message
            symptoms = self._extract_symptoms_from_message(message.message)
            
            # Get ML prediction
            prediction = self.classifier.predict_condition(symptoms)
            
            # Generate conversational response
            response = self._generate_conversational_response(
                message.message, 
                prediction, 
                message.conversation_history
            )
            
            # Generate follow-up questions
            suggested_questions = self._generate_chat_follow_up_questions(
                message.message, 
                prediction
            )
            
            # Determine if professional consultation is needed
            requires_consultation = self._requires_professional_consultation(prediction)
            
            return ChatResponse(
                user_id=message.user_id,
                response=response,
                suggested_questions=suggested_questions,
                confidence_level=self._get_confidence_level(prediction['confidence_score']),
                requires_professional_consultation=requires_consultation,
                session_id=message.session_id or f"ml_session_{message.user_id}_{datetime.now().timestamp()}"
            )
            
        except Exception as e:
            logger.error(f"Error in ML chat processing: {str(e)}")
            return self._create_error_chat_response(message.user_id, str(e))

    def _extract_symptoms_from_message(self, message: str) -> List[str]:
        """Extract symptoms from chat message"""
        # Simple keyword extraction - in production, this would be more sophisticated
        symptom_keywords = [
            'headache', 'fever', 'cough', 'sore throat', 'nausea', 'vomiting',
            'diarrhea', 'fatigue', 'dizziness', 'chest pain', 'shortness of breath',
            'rash', 'itching', 'swelling', 'pain', 'ache', 'tired', 'sick'
        ]
        
        detected_symptoms = []
        message_lower = message.lower()
        
        for symptom in symptom_keywords:
            if symptom in message_lower:
                detected_symptoms.append(symptom)
        
        return detected_symptoms if detected_symptoms else ['general health concern']

    def _generate_conversational_response(self, message: str, prediction: Dict, history: List) -> str:
        """Generate conversational response based on ML prediction"""
        primary_condition = prediction.get('primary_condition', {})
        condition_name = primary_condition.get('condition_name', 'Unknown condition')
        confidence = prediction.get('confidence_score', 0.5)
        
        if confidence > 0.7:
            response = f"Based on your symptoms, it sounds like you might be experiencing {condition_name.lower()}. "
        elif confidence > 0.4:
            response = f"Your symptoms could be related to {condition_name.lower()}, though I'd need more information to be certain. "
        else:
            response = "I understand you're not feeling well. "
        
        response += "Let me ask you a few questions to better understand your situation. "
        
        return response

    def _generate_chat_follow_up_questions(self, message: str, prediction: Dict) -> List[str]:
        """Generate follow-up questions for chat"""
        questions = [
            "How long have you been experiencing these symptoms?",
            "On a scale of 1-10, how would you rate the severity?",
            "Are you experiencing any other symptoms I should know about?"
        ]
        
        # Add condition-specific questions
        primary_condition = prediction.get('primary_condition', {})
        condition_name = primary_condition.get('condition_name', '').lower()
        
        if 'headache' in condition_name:
            questions.append("Where exactly do you feel the pain?")
        elif 'rash' in condition_name or 'skin' in condition_name:
            questions.append("Is the affected area itchy or painful?")
        elif 'stomach' in condition_name or 'nausea' in condition_name:
            questions.append("Have you eaten anything unusual recently?")
        
        return questions[:3]  # Return top 3 questions

    def _generate_follow_up_questions(self, request: SymptomRequest, primary_condition: Dict) -> List[str]:
        """Generate follow-up questions for detailed analysis"""
        questions = [
            "How long have you been experiencing these symptoms?",
            "Have you tried any treatments or medications?",
            "Are there any factors that make your symptoms better or worse?"
        ]
        
        # Add condition-specific questions
        if primary_condition:
            condition_name = primary_condition.get('condition_name', '').lower()
            if 'fever' in condition_name:
                questions.append("What is your current temperature?")
            elif 'pain' in condition_name:
                questions.append("On a scale of 1-10, how would you rate the pain?")
        
        return questions

    def _get_first_aid_advice(self, primary_condition: Dict) -> FirstAidAdvice:
        """Get first aid advice for the primary condition"""
        if not primary_condition:
            return FirstAidAdvice(**self.default_first_aid)
        
        condition_name = primary_condition.get('condition_name', '').lower().replace(' ', '_')
        
        # Find matching advice in database
        advice_data = None
        for key, advice in self.first_aid_database.items():
            if key in condition_name or condition_name in key:
                advice_data = advice
                break
        
        if not advice_data:
            advice_data = self.default_first_aid
        
        return FirstAidAdvice(
            immediate_actions=advice_data['immediate_actions'],
            do_not_do=advice_data['do_not_do'],
            when_to_seek_help=advice_data['when_to_seek_help'],
            emergency_signs=advice_data['emergency_signs']
        )

    def _requires_professional_consultation(self, prediction: Dict) -> bool:
        """Determine if professional consultation is needed"""
        primary_condition = prediction.get('primary_condition', {})
        severity = primary_condition.get('severity', 'low')
        confidence = prediction.get('confidence_score', 0.5)
        
        # Require consultation for high severity or low confidence
        return severity in ['high', 'critical'] or confidence < 0.4

    def _get_confidence_level(self, confidence_score: float) -> str:
        """Convert confidence score to level"""
        if confidence_score > 0.7:
            return 'high'
        elif confidence_score > 0.4:
            return 'medium'
        else:
            return 'low'

    def _create_error_response(self, user_id: str, error_msg: str) -> SymptomResponse:
        """Create error response for symptom analysis"""
        return SymptomResponse(
            user_id=user_id,
            possible_conditions=[],
            first_aid_advice=FirstAidAdvice(**self.default_first_aid),
            confidence_score=0.0,
            follow_up_questions=["Please describe your symptoms again"],
            disclaimer=self._get_medical_disclaimer()
        )

    def _create_error_chat_response(self, user_id: str, error_msg: str) -> ChatResponse:
        """Create error response for chat"""
        return ChatResponse(
            user_id=user_id,
            response="I apologize, but I'm having trouble processing your message right now. Please try again or consult with a healthcare professional for your health concerns.",
            suggested_questions=["Could you rephrase your question?", "Would you like to start over?"],
            confidence_level="low",
            requires_professional_consultation=True,
            session_id=f"error_session_{user_id}"
        )

    def _get_medical_disclaimer(self) -> str:
        """Get standard medical disclaimer"""
        return """
        IMPORTANT: This ML-based assessment is for educational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of qualified health professionals with any questions about medical conditions. If you have a medical emergency, call emergency services immediately.
        """
