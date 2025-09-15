import cv2
import numpy as np
import torch
import torchvision.transforms as transforms
from PIL import Image, ImageEnhance
import logging
import io
import os
import time
from typing import List, Dict, Any, Tuple
import base64
import json
import openai

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

class ImageAnalysisService:
    def __init__(self):
        self.client = openai.OpenAI()
        self.setup_models()
        
    def setup_models(self):
        """
        Initialize computer vision models and preprocessing pipeline
        """
        try:
            # Set up image preprocessing
            self.preprocess = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
            ])
            
            # Initialize OpenCV for feature detection
            self.feature_detector = cv2.SimpleBlobDetector_create()
            
            logger.info("Image analysis models initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing models: {str(e)}")
            raise e

    async def analyze_image(self, request: ImageAnalysisRequest) -> ImageAnalysisResponse:
        """
        Main image analysis function
        """
        start_time = time.time()
        
        try:
            # Load and preprocess image
            image = self._load_image_from_bytes(request.image_data)
            
            # Assess image quality
            quality_assessment = self._assess_image_quality(image)
            
            # Extract visual features
            detected_features = self._extract_visual_features(image)
            
            # Use GPT-4 Vision for detailed analysis
            vision_analysis = await self._analyze_with_gpt4_vision(request.image_data, request.description)
            
            # Combine analyses
            analysis_result = self._combine_analyses(detected_features, vision_analysis, quality_assessment)
            
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
            logger.error(f"Error in image analysis: {str(e)}")
            return self._create_error_response(request.user_id, str(e))

    def _load_image_from_bytes(self, image_data: bytes) -> np.ndarray:
        """
        Load image from bytes and convert to OpenCV format
        """
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
        """
        Assess the quality of the image for medical analysis
        """
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

    def _extract_visual_features(self, image: np.ndarray) -> List[DetectedFeature]:
        """
        Extract visual features from the image using computer vision
        """
        features = []
        
        try:
            # Convert to different color spaces for analysis
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Detect redness
            redness_features = self._detect_redness(image, hsv)
            features.extend(redness_features)
            
            # Detect swelling/raised areas
            swelling_features = self._detect_swelling(gray)
            features.extend(swelling_features)
            
            # Detect irregular shapes or lesions
            lesion_features = self._detect_lesions(gray)
            features.extend(lesion_features)
            
            # Detect color variations
            color_features = self._detect_color_variations(lab)
            features.extend(color_features)
            
            # Detect texture abnormalities
            texture_features = self._detect_texture_abnormalities(gray)
            features.extend(texture_features)
            
        except Exception as e:
            logger.error(f"Error extracting visual features: {str(e)}")
            
        return features

    def _detect_redness(self, image: np.ndarray, hsv: np.ndarray) -> List[DetectedFeature]:
        """
        Detect areas of redness in the image
        """
        features = []
        
        try:
            # Define range for red colors in HSV
            lower_red1 = np.array([0, 50, 50])
            upper_red1 = np.array([10, 255, 255])
            lower_red2 = np.array([170, 50, 50])
            upper_red2 = np.array([180, 255, 255])
            
            # Create masks for red areas
            mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
            mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
            red_mask = mask1 + mask2
            
            # Find contours
            contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 100:  # Filter small areas
                    # Calculate confidence based on area and intensity
                    confidence = min(area / 10000, 1.0)
                    
                    # Get bounding box
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    features.append(DetectedFeature(
                        feature_type="redness",
                        confidence=confidence,
                        location={"x": int(x), "y": int(y), "width": int(w), "height": int(h)},
                        description=f"Red area detected with {confidence:.2f} confidence"
                    ))
                    
        except Exception as e:
            logger.error(f"Error detecting redness: {str(e)}")
            
        return features

    def _detect_swelling(self, gray: np.ndarray) -> List[DetectedFeature]:
        """
        Detect potential swelling or raised areas
        """
        features = []
        
        try:
            # Use edge detection to find raised areas
            edges = cv2.Canny(gray, 50, 150)
            
            # Find contours
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 200:
                    # Calculate roundness (closer to 1 means more circular)
                    perimeter = cv2.arcLength(contour, True)
                    if perimeter > 0:
                        roundness = 4 * np.pi * area / (perimeter * perimeter)
                        
                        # Swelling tends to be more circular
                        if roundness > 0.3:
                            confidence = min(roundness * area / 5000, 1.0)
                            
                            x, y, w, h = cv2.boundingRect(contour)
                            
                            features.append(DetectedFeature(
                                feature_type="swelling",
                                confidence=confidence,
                                location={"x": int(x), "y": int(y), "width": int(w), "height": int(h)},
                                description=f"Potential swelling detected with {confidence:.2f} confidence"
                            ))
                            
        except Exception as e:
            logger.error(f"Error detecting swelling: {str(e)}")
            
        return features

    def _detect_lesions(self, gray: np.ndarray) -> List[DetectedFeature]:
        """
        Detect lesions or irregular shapes
        """
        features = []
        
        try:
            # Apply threshold to segment potential lesions
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Find contours
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if 50 < area < 10000:  # Filter by size
                    # Calculate irregularity
                    hull = cv2.convexHull(contour)
                    hull_area = cv2.contourArea(hull)
                    
                    if hull_area > 0:
                        solidity = area / hull_area
                        
                        # Lower solidity indicates more irregular shape
                        if solidity < 0.8:
                            confidence = (1 - solidity) * min(area / 1000, 1.0)
                            
                            x, y, w, h = cv2.boundingRect(contour)
                            
                            features.append(DetectedFeature(
                                feature_type="lesion",
                                confidence=confidence,
                                location={"x": int(x), "y": int(y), "width": int(w), "height": int(h)},
                                description=f"Irregular lesion detected with {confidence:.2f} confidence"
                            ))
                            
        except Exception as e:
            logger.error(f"Error detecting lesions: {str(e)}")
            
        return features

    def _detect_color_variations(self, lab: np.ndarray) -> List[DetectedFeature]:
        """
        Detect unusual color variations
        """
        features = []
        
        try:
            # Calculate standard deviation of color channels
            l_std = np.std(lab[:, :, 0])
            a_std = np.std(lab[:, :, 1])
            b_std = np.std(lab[:, :, 2])
            
            # High standard deviation indicates color variation
            total_variation = l_std + a_std + b_std
            
            if total_variation > 50:  # Threshold for significant variation
                confidence = min(total_variation / 100, 1.0)
                
                features.append(DetectedFeature(
                    feature_type="color_variation",
                    confidence=confidence,
                    location=None,
                    description=f"Significant color variation detected with {confidence:.2f} confidence"
                ))
                
        except Exception as e:
            logger.error(f"Error detecting color variations: {str(e)}")
            
        return features

    def _detect_texture_abnormalities(self, gray: np.ndarray) -> List[DetectedFeature]:
        """
        Detect texture abnormalities
        """
        features = []
        
        try:
            # Calculate texture using Local Binary Pattern approximation
            kernel = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
            texture_response = cv2.filter2D(gray, cv2.CV_64F, kernel)
            texture_variance = np.var(texture_response)
            
            if texture_variance > 1000:  # Threshold for abnormal texture
                confidence = min(texture_variance / 5000, 1.0)
                
                features.append(DetectedFeature(
                    feature_type="texture_abnormality",
                    confidence=confidence,
                    location=None,
                    description=f"Abnormal texture pattern detected with {confidence:.2f} confidence"
                ))
                
        except Exception as e:
            logger.error(f"Error detecting texture abnormalities: {str(e)}")
            
        return features

    async def _analyze_with_gpt4_vision(self, image_data: bytes, description: str = None) -> Dict[str, Any]:
        """
        Use GPT-4 Vision for detailed image analysis
        """
        try:
            # Encode image to base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            # Create prompt
            prompt = f"""
            You are a medical AI analyzing a skin/wound image. Provide a detailed assessment based on visual features.

            User description: {description or 'No description provided'}

            ANALYSIS INSTRUCTIONS:
            1. Examine the image carefully for visual features
            2. Consider common skin conditions and wounds
            3. Look for signs of infection, inflammation, or healing
            4. Assess size, color, texture, and shape
            5. Consider the location and pattern if visible
            6. Provide realistic probability assessments

            COMMON CONDITIONS TO CONSIDER:
            - Minor cuts, scrapes, and abrasions
            - Insect bites and stings
            - Allergic reactions and contact dermatitis
            - Acne and skin blemishes
            - Minor burns and sunburns
            - Bruises and contusions
            - Rashes (viral, bacterial, allergic)
            - Skin infections (impetigo, cellulitis)
            - Eczema and dermatitis
            - Fungal infections (ringworm, athlete's foot)

            Provide your analysis in this EXACT JSON format:
            {{
                "condition_type": "wound|rash|skin_condition|infection|allergic_reaction|other",
                "possible_conditions": [
                    {{
                        "condition_name": "Specific condition name (e.g., 'Minor Abrasion with Mild Inflammation')",
                        "probability": 0.75,
                        "description": "Detailed explanation of what you see and why it matches this condition",
                        "symptoms_match": ["specific visual features that match this condition"],
                        "severity": "low|moderate|high|critical"
                    }}
                ],
                "severity_assessment": "low|moderate|high|critical",
                "confidence_score": 0.8,
                "visual_observations": ["specific visual findings like 'redness', 'swelling', 'irregular edges'"],
                "recommendations": ["specific recommendations based on the visual assessment"]
            }}

            IMPORTANT:
            - Be specific about what you observe in the image
            - Consider the most common conditions first
            - Use realistic probability scores (0.3-0.8 for most conditions)
            - If the image is unclear, mention this in your assessment
            - Always prioritize patient safety in recommendations
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}",
                                    "detail": "high"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1500,
                response_format={"type": "json_object"}
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            logger.error(f"Error in GPT-4 Vision analysis: {str(e)}")
            return self._get_fallback_analysis()

    def _combine_analyses(self, detected_features: List[DetectedFeature], vision_analysis: Dict[str, Any], quality: str) -> ImageAnalysisResult:
        """
        Combine computer vision and AI analyses
        """
        try:
            # Create possible conditions from vision analysis
            possible_conditions = []
            for condition in vision_analysis.get("possible_conditions", []):
                possible_conditions.append(PossibleCondition(
                    condition_name=condition["condition_name"],
                    probability=condition["probability"],
                    description=condition["description"],
                    symptoms_match=condition.get("symptoms_match", []),
                    severity=SeverityLevel(condition["severity"])
                ))
            
            # Determine condition type
            condition_type = ConditionType(vision_analysis.get("condition_type", "other"))
            
            # Determine severity
            severity = SeverityLevel(vision_analysis.get("severity_assessment", "moderate"))
            
            # Calculate overall confidence
            vision_confidence = vision_analysis.get("confidence_score", 0.5)
            cv_confidence = len(detected_features) / 10  # Simple heuristic
            overall_confidence = (vision_confidence + cv_confidence) / 2
            
            return ImageAnalysisResult(
                condition_type=condition_type,
                possible_conditions=possible_conditions,
                detected_features=detected_features,
                severity_assessment=severity,
                confidence_score=min(overall_confidence, 1.0),
                image_quality=quality
            )
            
        except Exception as e:
            logger.error(f"Error combining analyses: {str(e)}")
            return self._get_fallback_result()

    def _generate_recommendations(self, analysis: ImageAnalysisResult) -> List[str]:
        """
        Generate recommendations based on analysis
        """
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
        """
        Generate first aid advice based on analysis
        """
        immediate_actions = ["Clean hands before touching the area", "Gently clean the affected area with mild soap and water"]
        do_not_do = ["Do not pick or scratch the area", "Avoid applying unsterile materials"]
        when_to_seek_help = ["If symptoms worsen", "If you develop fever"]
        emergency_signs = ["Severe pain", "Rapid spreading", "Signs of infection"]
        
        # Customize based on severity
        if analysis.severity_assessment in [SeverityLevel.HIGH, SeverityLevel.CRITICAL]:
            immediate_actions.insert(0, "Seek immediate medical attention")
            emergency_signs.extend(["Difficulty breathing", "Chest pain", "Severe allergic reaction"])
        
        return FirstAidAdvice(
            immediate_actions=immediate_actions,
            do_not_do=do_not_do,
            when_to_seek_help=when_to_seek_help,
            emergency_signs=emergency_signs
        )

    def _generate_follow_up_questions(self, analysis: ImageAnalysisResult) -> List[str]:
        """
        Generate follow-up questions
        """
        questions = [
            "How long have you had this condition?",
            "Have you experienced any pain or itching?",
            "Have you tried any treatments so far?"
        ]
        
        # Add condition-specific questions
        if analysis.condition_type == ConditionType.WOUND:
            questions.append("How did the wound occur?")
        elif analysis.condition_type == ConditionType.RASH:
            questions.extend(["Have you been exposed to any new substances?", "Do you have any known allergies?"])
        
        return questions

    def _get_fallback_analysis(self) -> Dict[str, Any]:
        """
        Fallback analysis when GPT-4 Vision fails
        """
        return {
            "condition_type": "other",
            "possible_conditions": [{
                "condition_name": "Unknown condition",
                "probability": 0.3,
                "description": "Unable to determine specific condition from image",
                "symptoms_match": [],
                "severity": "moderate"
            }],
            "severity_assessment": "moderate",
            "confidence_score": 0.3,
            "visual_observations": ["Image analysis incomplete"],
            "recommendations": ["Consult healthcare professional for proper evaluation"]
        }

    def _get_fallback_result(self) -> ImageAnalysisResult:
        """
        Fallback result when analysis fails
        """
        return ImageAnalysisResult(
            condition_type=ConditionType.OTHER,
            possible_conditions=[],
            detected_features=[],
            severity_assessment=SeverityLevel.MODERATE,
            confidence_score=0.1,
            image_quality="unknown"
        )

    def _create_error_response(self, user_id: str, error_msg: str) -> ImageAnalysisResponse:
        """
        Create error response
        """
        return ImageAnalysisResponse(
            user_id=user_id,
            analysis_result=self._get_fallback_result(),
            recommendations=["Please consult a healthcare professional"],
            first_aid_advice=FirstAidAdvice(
                immediate_actions=["Consult healthcare professional"],
                do_not_do=["Do not ignore symptoms"],
                when_to_seek_help=["As soon as possible"],
                emergency_signs=["Any concerning symptoms"]
            ),
            follow_up_questions=["Please describe your symptoms"],
            disclaimer=self._get_medical_disclaimer(),
            processing_time=0.0
        )

    def _get_medical_disclaimer(self) -> str:
        """
        Get medical disclaimer
        """
        return """
        IMPORTANT: This AI image analysis is for educational purposes only and is not a substitute for professional medical diagnosis. Image quality and lighting conditions can significantly affect analysis accuracy. Always consult qualified healthcare professionals for proper medical evaluation and treatment.
        """
