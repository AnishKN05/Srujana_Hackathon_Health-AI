import openai
import json
import logging
from typing import List, Dict, Any
from datetime import datetime
import os
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

class SymptomCheckerService:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.client = openai.OpenAI()
        self.system_prompt = self._get_system_prompt()
        
    def _get_system_prompt(self) -> str:
        return """
        You are an AI health assessment assistant designed to help users understand their symptoms and provide preliminary guidance. 

        CRITICAL GUIDELINES:
        1. You are NOT a doctor and cannot provide medical diagnoses
        2. Always recommend consulting healthcare professionals for serious concerns
        3. Focus on educational information and first aid guidance
        4. Be empathetic but maintain professional boundaries
        5. If symptoms suggest emergency conditions, strongly recommend immediate medical attention
        6. Ask specific, targeted questions to gather more information
        7. Consider common conditions first, then rare ones
        8. Always provide confidence scores based on available information

        RESPONSE FORMAT:
        Provide structured responses that include:
        - Possible conditions with probability scores (0-1) based on symptom patterns
        - Immediate first aid advice tailored to the specific symptoms
        - Clear guidance on when to seek professional help
        - Educational information about symptoms and conditions
        - Specific follow-up questions to gather more diagnostic information

        SEVERITY ASSESSMENT:
        - LOW: Minor symptoms that can be managed with basic care (colds, minor cuts, mild headaches)
        - MODERATE: Symptoms that warrant monitoring and possible medical consultation (persistent fever, moderate pain, unusual rashes)
        - HIGH: Symptoms that require prompt medical attention (severe pain, difficulty breathing, signs of infection)
        - CRITICAL: Emergency symptoms requiring immediate medical care (chest pain, severe allergic reactions, loss of consciousness)

        DIAGNOSTIC APPROACH:
        - Consider the most common conditions first
        - Look for symptom patterns and combinations
        - Consider age, gender, and medical history when provided
        - Provide realistic probability assessments
        - Always err on the side of caution for serious symptoms

        Always include appropriate medical disclaimers and emphasize that this is for educational purposes only.
        """

    async def analyze_symptoms(self, request: SymptomRequest) -> SymptomResponse:
        """
        Analyze symptoms and provide preliminary assessment
        """
        try:
            # Create detailed prompt for symptom analysis
            user_prompt = self._create_analysis_prompt(request)
            
            # Get response from OpenAI
            response = await self._get_ai_response(user_prompt)
            
            # Parse and structure the response
            structured_response = self._parse_analysis_response(response, request.user_id)
            
            return structured_response
            
        except Exception as e:
            logger.error(f"Error in symptom analysis: {str(e)}")
            return self._create_error_response(request.user_id, str(e))

    async def process_chat_message(self, message: ChatMessage) -> ChatResponse:
        """
        Process conversational messages for symptom discussion
        """
        try:
            # Create chat prompt with conversation history
            chat_prompt = self._create_chat_prompt(message)
            
            # Get AI response
            response = await self._get_ai_response(chat_prompt, is_chat=True)
            
            # Structure the chat response
            chat_response = self._parse_chat_response(response, message)
            
            return chat_response
            
        except Exception as e:
            logger.error(f"Error in chat processing: {str(e)}")
            return self._create_error_chat_response(message.user_id, str(e))

    def _create_analysis_prompt(self, request: SymptomRequest) -> str:
        """
        Create detailed prompt for symptom analysis
        """
        prompt = f"""
        You are a medical AI assistant analyzing symptoms. Provide a comprehensive health assessment based on the following information:

        PATIENT INFORMATION:
        - Primary Symptoms: {', '.join(request.symptoms) if request.symptoms else 'Not specified'}
        - Duration: {request.duration or 'Not specified'}
        - Perceived Severity: {request.severity or 'Not specified'}
        - Age: {request.age or 'Not specified'}
        - Gender: {request.gender or 'Not specified'}
        - Medical History: {', '.join(request.medical_history) if request.medical_history else 'None provided'}
        - Additional Context: {request.additional_info or 'None'}

        ANALYSIS INSTRUCTIONS:
        1. Consider the most common conditions that match these symptoms
        2. Look for symptom patterns and combinations
        3. Consider age-appropriate conditions
        4. Factor in medical history if provided
        5. Provide realistic probability assessments (0.1-0.9 range)
        6. Prioritize safety - err on the side of caution

        COMMON CONDITIONS TO CONSIDER:
        - Upper respiratory infections (colds, flu, sinusitis)
        - Gastrointestinal issues (food poisoning, gastroenteritis, indigestion)
        - Skin conditions (rashes, allergic reactions, infections)
        - Musculoskeletal issues (strains, sprains, arthritis)
        - Headaches and migraines
        - Anxiety and stress-related symptoms
        - Seasonal allergies
        - Minor injuries and wounds

        Provide your assessment in this EXACT JSON format:
        {{
            "possible_conditions": [
                {{
                    "condition_name": "Specific condition name (e.g., 'Viral Upper Respiratory Infection')",
                    "probability": 0.75,
                    "description": "Brief explanation of the condition and why it matches the symptoms",
                    "symptoms_match": ["specific symptoms that match this condition"],
                    "severity": "low|moderate|high|critical"
                }}
            ],
            "first_aid_advice": {{
                "immediate_actions": ["specific, actionable steps for immediate care"],
                "do_not_do": ["specific things to avoid doing"],
                "when_to_seek_help": ["specific situations that require medical attention"],
                "emergency_signs": ["specific warning signs that require immediate emergency care"]
            }},
            "confidence_score": 0.8,
            "follow_up_questions": ["specific questions to gather more diagnostic information"]
        }}

        IMPORTANT: 
        - Provide 2-4 most likely conditions
        - Use realistic probability scores (0.3-0.8 for most conditions)
        - Make advice specific to the symptoms described
        - Include age-appropriate considerations
        - Always prioritize patient safety
        """
        return prompt

    def _create_chat_prompt(self, message: ChatMessage) -> str:
        """
        Create prompt for conversational chat
        """
        conversation_context = ""
        if message.conversation_history:
            conversation_context = "\n".join([
                f"{'User' if msg.get('role') == 'user' else 'Assistant'}: {msg.get('content', '')}"
                for msg in message.conversation_history[-10:]  # Last 10 messages for context
            ])

        prompt = f"""
        You are a helpful health AI assistant having a conversation with someone about their health concerns. Be empathetic, professional, and educational.

        CONVERSATION HISTORY:
        {conversation_context}

        CURRENT USER MESSAGE:
        {message.message}

        RESPONSE GUIDELINES:
        1. Be empathetic and understanding
        2. Ask specific, targeted questions to gather more information
        3. Provide educational information about symptoms and conditions
        4. Offer practical first aid or self-care advice when appropriate
        5. Clearly indicate when professional medical consultation is needed
        6. Maintain appropriate boundaries - you're not a doctor
        7. Be conversational and natural, not robotic

        QUESTION TYPES TO ASK:
        - Duration: "How long have you been experiencing this?"
        - Severity: "On a scale of 1-10, how would you rate the pain/discomfort?"
        - Location: "Where exactly do you feel this?"
        - Triggers: "What makes it better or worse?"
        - Associated symptoms: "Are you experiencing any other symptoms?"
        - Medical history: "Do you have any relevant medical conditions?"

        Respond naturally and helpfully. Structure your response as JSON:
        {{
            "response": "Your natural, conversational response to the user",
            "suggested_questions": ["2-3 specific follow-up questions to ask"],
            "confidence_level": "high|medium|low",
            "requires_professional_consultation": true/false
        }}

        IMPORTANT: Be conversational and human-like, not clinical or robotic.
        """
        return prompt

    async def _get_ai_response(self, prompt: str, is_chat: bool = False) -> str:
        """
        Get response from OpenAI API
        """
        try:
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ]
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                max_tokens=2000,
                temperature=0.3,  # Lower temperature for more consistent medical advice
                response_format={"type": "json_object"} if not is_chat else None
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error getting AI response: {str(e)}")
            raise e

    def _parse_analysis_response(self, response: str, user_id: str) -> SymptomResponse:
        """
        Parse AI response into structured SymptomResponse
        """
        try:
            # Parse JSON response
            parsed = json.loads(response)
            
            # Create PossibleCondition objects
            possible_conditions = [
                PossibleCondition(
                    condition_name=condition["condition_name"],
                    probability=condition["probability"],
                    description=condition["description"],
                    symptoms_match=condition["symptoms_match"],
                    severity=SeverityLevel(condition["severity"])
                )
                for condition in parsed["possible_conditions"]
            ]
            
            # Create FirstAidAdvice object
            first_aid = FirstAidAdvice(
                immediate_actions=parsed["first_aid_advice"]["immediate_actions"],
                do_not_do=parsed["first_aid_advice"]["do_not_do"],
                when_to_seek_help=parsed["first_aid_advice"]["when_to_seek_help"],
                emergency_signs=parsed["first_aid_advice"]["emergency_signs"]
            )
            
            return SymptomResponse(
                user_id=user_id,
                possible_conditions=possible_conditions,
                first_aid_advice=first_aid,
                confidence_score=parsed["confidence_score"],
                follow_up_questions=parsed["follow_up_questions"],
                disclaimer=self._get_medical_disclaimer()
            )
            
        except Exception as e:
            logger.error(f"Error parsing analysis response: {str(e)}")
            return self._create_error_response(user_id, f"Error parsing AI response: {str(e)}")

    def _parse_chat_response(self, response: str, message: ChatMessage) -> ChatResponse:
        """
        Parse AI chat response into structured ChatResponse
        """
        try:
            # Try to parse as JSON first
            try:
                parsed = json.loads(response)
                response_text = parsed["response"]
                suggested_questions = parsed["suggested_questions"]
                confidence_level = parsed["confidence_level"]
                requires_consultation = parsed["requires_professional_consultation"]
            except:
                # Fallback if not JSON formatted
                response_text = response
                suggested_questions = ["Could you describe your symptoms in more detail?", "How long have you been experiencing this?"]
                confidence_level = "medium"
                requires_consultation = True
            
            return ChatResponse(
                user_id=message.user_id,
                response=response_text,
                suggested_questions=suggested_questions,
                confidence_level=confidence_level,
                requires_professional_consultation=requires_consultation,
                session_id=message.session_id or f"session_{message.user_id}_{datetime.now().timestamp()}"
            )
            
        except Exception as e:
            logger.error(f"Error parsing chat response: {str(e)}")
            return self._create_error_chat_response(message.user_id, str(e))

    def _create_error_response(self, user_id: str, error_msg: str) -> SymptomResponse:
        """
        Create error response for symptom analysis
        """
        return SymptomResponse(
            user_id=user_id,
            possible_conditions=[],
            first_aid_advice=FirstAidAdvice(
                immediate_actions=["Consult with a healthcare professional"],
                do_not_do=["Do not ignore persistent symptoms"],
                when_to_seek_help=["If symptoms persist or worsen"],
                emergency_signs=["Severe pain, difficulty breathing, chest pain"]
            ),
            confidence_score=0.0,
            follow_up_questions=["Please describe your symptoms again"],
            disclaimer=self._get_medical_disclaimer()
        )

    def _create_error_chat_response(self, user_id: str, error_msg: str) -> ChatResponse:
        """
        Create error response for chat
        """
        return ChatResponse(
            user_id=user_id,
            response="I apologize, but I'm having trouble processing your message right now. Please try again or consult with a healthcare professional for your health concerns.",
            suggested_questions=["Could you rephrase your question?", "Would you like to start over?"],
            confidence_level="low",
            requires_professional_consultation=True,
            session_id=f"error_session_{user_id}"
        )

    def _get_medical_disclaimer(self) -> str:
        """
        Get standard medical disclaimer
        """
        return """
        IMPORTANT: This AI assessment is for educational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of qualified health professionals with any questions about medical conditions. If you have a medical emergency, call emergency services immediately.
        """
