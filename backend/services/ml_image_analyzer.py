"""
ML-based Image Analysis Service
Replaces OpenAI-based image analysis with trained ML models
"""
import sys
import os
import logging
import time
from typing import List, Dict, Any
from datetime import datetime
import numpy as np
import cv2
from PIL import Image
import io

# Add the ml_models directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'ml_models'))

from image_classifier import SkinConditionClassifier
from models.schemas import (
    ImageAnalysisRequest,
    ImageAnalysisResponse,
    ImageAnalysisResult,
    DetectedFeature,
    PossibleCondition,
    FirstAidAdvice,
    ConditionType,
    SeverityLevel
)

logger = logging.getLogger(__name__)

class MLImageAnalysisService:
    def __init__(self):
        self.classifier = SkinConditionClassifier()
        self.classifier.load_model()
        
        # First aid advice database for skin conditions
        self.skin_condition_advice = {
            'acne': {
                'immediate_actions': [
                    'Gently wash the affected area with mild soap and water',
                    'Apply over-the-counter acne treatment containing benzoyl peroxide or salicylic acid',
                    'Avoid picking or squeezing pimples',
                    'Use non-comedogenic moisturizers'
                ],
                'do_not_do': [
                    'Do not scrub the skin harshly',
                    'Avoid using multiple acne treatments at once',
                    'Do not pick or pop pimples'
                ],
                'when_to_seek_help': [
                    'If acne is severe or painful',
                    'If over-the-counter treatments are not working',
                    'If acne is causing scarring'
                ],
                'emergency_signs': [
                    'Signs of severe infection (increasing redness, warmth, pus)',
                    'Severe allergic reaction to acne treatment'
                ]
            },
            'eczema': {
                'immediate_actions': [
                    'Keep the skin moisturized with fragrance-free creams',
                    'Use gentle, fragrance-free cleansers',
                    'Apply cool, wet compresses to reduce itching',
                    'Avoid known triggers'
                ],
                'do_not_do': [
                    'Do not scratch the affected area',
                    'Avoid harsh soaps and hot water',
                    'Do not use products with fragrances or alcohol'
                ],
                'when_to_seek_help': [
                    'If eczema is severe or widespread',
                    'If the skin becomes infected',
                    'If over-the-counter treatments are not effective'
                ],
                'emergency_signs': [
                    'Signs of skin infection (increasing redness, warmth, pus)',
                    'Severe allergic reaction'
                ]
            },
            'wound': {
                'immediate_actions': [
                    'Clean the wound gently with mild soap and water',
                    'Apply pressure to stop any bleeding',
                    'Cover with a clean, dry bandage',
                    'Keep the wound clean and dry'
                ],
                'do_not_do': [
                    'Do not use hydrogen peroxide or alcohol on the wound',
                    'Avoid picking at scabs',
                    'Do not apply butter or other home remedies'
                ],
                'when_to_seek_help': [
                    'If the wound is deep or won\'t stop bleeding',
                    'If signs of infection develop',
                    'If the wound is from a bite or puncture'
                ],
                'emergency_signs': [
                    'Heavy bleeding that won\'t stop',
                    'Signs of infection (redness, warmth, pus, red streaks)',
                    'Foreign object embedded in the wound'
                ]
            },
            'burn': {
                'immediate_actions': [
                    'Cool the burn with cool (not cold) running water for 10-15 minutes',
                    'Remove jewelry or tight clothing before swelling occurs',
                    'Cover with a clean, dry cloth or bandage',
                    'Take over-the-counter pain relievers if needed'
                ],
                'do_not_do': [
                    'Do not use ice, butter, or other home remedies',
                    'Do not break blisters',
                    'Do not apply adhesive bandages to large burns'
                ],
                'when_to_seek_help': [
                    'If the burn is larger than 3 inches',
                    'If the burn is on the face, hands, feet, or genitals',
                    'If signs of infection develop'
                ],
                'emergency_signs': [
                    'Third-degree burns (white, charred, or leathery skin)',
                    'Burns covering a large area of the body',
                    'Burns with signs of shock (pale, clammy skin, rapid breathing)'
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
                    'Rash that looks like bruises or bleeding under the skin'
                ]
            }
        }
        
        # Default advice for unknown conditions
        self.default_advice = {
            'immediate_actions': [
                'Keep the affected area clean and dry',
                'Monitor for changes in appearance',
                'Avoid scratching or picking at the area',
                'Apply gentle, fragrance-free moisturizer if the skin is dry'
            ],
            'do_not_do': [
                'Do not use harsh chemicals or strong medications',
                'Avoid scratching or picking at the affected area',
                'Do not ignore persistent or worsening symptoms'
            ],
            'when_to_seek_help': [
                'If the condition worsens or spreads',
                'If you develop signs of infection',
                'If you are concerned about the appearance'
            ],
            'emergency_signs': [
                'Signs of severe infection (increasing redness, warmth, pus)',
                'Difficulty breathing or swallowing',
                'Severe allergic reaction'
            ]
        }

    async def analyze_image(self, request: ImageAnalysisRequest) -> ImageAnalysisResponse:
        """
        Analyze image using ML model
        """
        start_time = time.time()
        
        try:
            logger.info(f"Analyzing image for user: {request.user_id}")
            
            # Load and preprocess image
            image = self._load_image_from_bytes(request.image_data)
            
            # Assess image quality
            quality_assessment = self._assess_image_quality(image)
            
            # Use ML model to predict skin condition
            prediction = self.classifier.predict_condition(image)
            
            # Detect visual features using computer vision
            detected_features = self.classifier.detect_features(image)
            
            # Convert ML prediction to analysis result
            analysis_result = self._convert_prediction_to_result(
                prediction, 
                detected_features, 
                quality_assessment
            )
            
            # Generate recommendations and first aid advice
            recommendations = self._generate_recommendations(analysis_result)
            first_aid_advice = self._generate_first_aid_advice(analysis_result)
            
            processing_time = time.time() - start_time
            
            return ImageAnalysisResponse(
                user_id=request.user_id,
                analysis_result=analysis_result,
                recommendations=recommendations,
                first_aid_advice=first_aid_advice,
                follow_up_questions=self._generate_follow_up_questions(analysis_result),
                disclaimer=self._get_medical_disclaimer(),
                processing_time=processing_time
            )
            
        except Exception as e:
            logger.error(f"Error in ML image analysis: {str(e)}")
            return self._create_error_response(request.user_id, str(e))

    def _load_image_from_bytes(self, image_data: bytes) -> np.ndarray:
        """Load image from bytes and convert to OpenCV format"""
        try:
            # Convert bytes to PIL Image
            pil_image = Image.open(io.BytesIO(image_data))
            
            # Convert to RGB if necessary
            if pil_image.mode != 'RGB':
                pil_image = pil_image.convert('RGB')
            
            # Convert to OpenCV format (BGR)
            opencv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            
            return opencv_image
            
        except Exception as e:
            logger.error(f"Error loading image: {str(e)}")
            raise e

    def _assess_image_quality(self, image: np.ndarray) -> str:
        """Assess the quality of the image for medical analysis"""
        try:
            # Convert to grayscale for analysis
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Calculate sharpness using Laplacian variance
            sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            # Calculate brightness
            brightness = np.mean(gray)
            
            # Calculate contrast
            contrast = gray.std()
            
            # Determine quality based on metrics
            if sharpness > 100 and 50 < brightness < 200 and contrast > 30:
                return "excellent"
            elif sharpness > 50 and 30 < brightness < 220 and contrast > 20:
                return "good"
            elif sharpness > 20 and 20 < brightness < 240 and contrast > 15:
                return "fair"
            else:
                return "poor"
                
        except Exception as e:
            logger.error(f"Error assessing image quality: {str(e)}")
            return "unknown"

    def _convert_prediction_to_result(self, prediction: Dict, detected_features: List, quality: str) -> ImageAnalysisResult:
        """Convert ML prediction to ImageAnalysisResult"""
        try:
            # Create possible conditions from ML prediction
            possible_conditions = []
            for condition_data in prediction['possible_conditions']:
                possible_conditions.append(PossibleCondition(
                    condition_name=condition_data['condition_name'],
                    probability=condition_data['probability'],
                    description=condition_data['description'],
                    symptoms_match=[],  # No symptoms for image analysis
                    severity=SeverityLevel(condition_data['severity'])
                ))
            
            # Determine condition type
            primary_condition = prediction.get('primary_condition', {})
            condition_name = primary_condition.get('condition_name', '').lower()
            
            if 'wound' in condition_name or 'cut' in condition_name or 'burn' in condition_name:
                condition_type = ConditionType.WOUND
            elif 'rash' in condition_name or 'eczema' in condition_name or 'psoriasis' in condition_name:
                condition_type = ConditionType.RASH
            elif 'infection' in condition_name:
                condition_type = ConditionType.INFECTION
            elif 'allergic' in condition_name or 'hives' in condition_name:
                condition_type = ConditionType.ALLERGIC_REACTION
            else:
                condition_type = ConditionType.SKIN_CONDITION
            
            # Determine severity
            severity = SeverityLevel(primary_condition.get('severity', 'moderate'))
            
            # Convert detected features
            detected_features_objects = []
            for feature in detected_features:
                detected_features_objects.append(DetectedFeature(
                    feature_type=feature['feature_type'],
                    confidence=feature['confidence'],
                    location=feature.get('location'),
                    description=feature['description']
                ))
            
            return ImageAnalysisResult(
                condition_type=condition_type,
                possible_conditions=possible_conditions,
                detected_features=detected_features_objects,
                severity_assessment=severity,
                confidence_score=prediction['confidence_score'],
                image_quality=quality
            )
            
        except Exception as e:
            logger.error(f"Error converting prediction to result: {str(e)}")
            return self._get_fallback_result()

    def _generate_recommendations(self, analysis: ImageAnalysisResult) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        if analysis.severity_assessment == SeverityLevel.CRITICAL:
            recommendations.extend([
                "Seek immediate emergency medical attention",
                "Do not delay treatment",
                "Go to the nearest emergency room"
            ])
        elif analysis.severity_assessment == SeverityLevel.HIGH:
            recommendations.extend([
                "Consult a healthcare provider promptly",
                "Schedule an appointment within 24-48 hours",
                "Monitor for worsening symptoms"
            ])
        elif analysis.severity_assessment == SeverityLevel.MODERATE:
            recommendations.extend([
                "Consider consulting a healthcare provider",
                "Monitor the condition for changes",
                "Keep the area clean and dry"
            ])
        else:
            recommendations.extend([
                "Monitor the condition",
                "Practice good hygiene",
                "Consult a healthcare provider if symptoms persist"
            ])
        
        # Add specific recommendations based on detected features
        for feature in analysis.detected_features:
            if feature.feature_type == "redness" and feature.confidence > 0.7:
                recommendations.append("Apply cold compress to reduce inflammation")
            elif feature.feature_type == "swelling" and feature.confidence > 0.7:
                recommendations.append("Elevate the affected area if possible")
        
        return recommendations

    def _generate_first_aid_advice(self, analysis: ImageAnalysisResult) -> FirstAidAdvice:
        """Generate first aid advice based on analysis"""
        primary_condition = analysis.possible_conditions[0] if analysis.possible_conditions else None
        
        if not primary_condition:
            return FirstAidAdvice(**self.default_advice)
        
        condition_name = primary_condition.condition_name.lower()
        
        # Find matching advice in database
        advice_data = None
        for key, advice in self.skin_condition_advice.items():
            if key in condition_name or condition_name in key:
                advice_data = advice
                break
        
        if not advice_data:
            advice_data = self.default_advice
        
        # Customize based on severity
        immediate_actions = advice_data['immediate_actions'].copy()
        emergency_signs = advice_data['emergency_signs'].copy()
        
        if analysis.severity_assessment in [SeverityLevel.HIGH, SeverityLevel.CRITICAL]:
            immediate_actions.insert(0, "Seek immediate medical attention")
            emergency_signs.extend(["Difficulty breathing", "Chest pain", "Severe allergic reaction"])
        
        return FirstAidAdvice(
            immediate_actions=immediate_actions,
            do_not_do=advice_data['do_not_do'],
            when_to_seek_help=advice_data['when_to_seek_help'],
            emergency_signs=emergency_signs
        )

    def _generate_follow_up_questions(self, analysis: ImageAnalysisResult) -> List[str]:
        """Generate follow-up questions"""
        questions = [
            "How long have you had this condition?",
            "Have you experienced any pain or itching?",
            "Have you tried any treatments so far?"
        ]
        
        # Add condition-specific questions
        if analysis.condition_type == ConditionType.WOUND:
            questions.append("How did the wound occur?")
        elif analysis.condition_type == ConditionType.RASH:
            questions.extend([
                "Have you been exposed to any new substances?",
                "Do you have any known allergies?"
            ])
        elif analysis.condition_type == ConditionType.INFECTION:
            questions.append("Have you noticed any pus or discharge?")
        
        return questions

    def _get_fallback_result(self) -> ImageAnalysisResult:
        """Fallback result when analysis fails"""
        return ImageAnalysisResult(
            condition_type=ConditionType.OTHER,
            possible_conditions=[],
            detected_features=[],
            severity_assessment=SeverityLevel.MODERATE,
            confidence_score=0.1,
            image_quality="unknown"
        )

    def _create_error_response(self, user_id: str, error_msg: str) -> ImageAnalysisResponse:
        """Create error response"""
        return ImageAnalysisResponse(
            user_id=user_id,
            analysis_result=self._get_fallback_result(),
            recommendations=["Please consult a healthcare professional"],
            first_aid_advice=FirstAidAdvice(**self.default_advice),
            follow_up_questions=["Please describe your symptoms"],
            disclaimer=self._get_medical_disclaimer(),
            processing_time=0.0
        )

    def _get_medical_disclaimer(self) -> str:
        """Get medical disclaimer"""
        return """
        IMPORTANT: This ML-based image analysis is for educational purposes only and is not a substitute for professional medical diagnosis. Image quality and lighting conditions can significantly affect analysis accuracy. Always consult qualified healthcare professionals for proper medical evaluation and treatment.
        """
