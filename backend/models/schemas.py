from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from enum import Enum

class SeverityLevel(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"

class ConditionType(str, Enum):
    SKIN_CONDITION = "skin_condition"
    WOUND = "wound"
    RASH = "rash"
    INFECTION = "infection"
    ALLERGIC_REACTION = "allergic_reaction"
    OTHER = "other"

class SymptomRequest(BaseModel):
    user_id: str = Field(..., description="Unique identifier for the user")
    symptoms: List[str] = Field(..., description="List of reported symptoms")
    duration: Optional[str] = Field(None, description="Duration of symptoms")
    severity: Optional[SeverityLevel] = Field(None, description="Perceived severity level")
    additional_info: Optional[str] = Field(None, description="Additional context or information")
    age: Optional[int] = Field(None, ge=0, le=120, description="User's age")
    gender: Optional[str] = Field(None, description="User's gender")
    medical_history: Optional[List[str]] = Field(default_factory=list, description="Relevant medical history")

class PossibleCondition(BaseModel):
    condition_name: str = Field(..., description="Name of the possible condition")
    probability: float = Field(..., ge=0, le=1, description="Probability score (0-1)")
    description: str = Field(..., description="Description of the condition")
    symptoms_match: List[str] = Field(..., description="Symptoms that match this condition")
    severity: SeverityLevel = Field(..., description="Typical severity of this condition")

class FirstAidAdvice(BaseModel):
    immediate_actions: List[str] = Field(..., description="Immediate first aid steps")
    do_not_do: List[str] = Field(..., description="Things to avoid doing")
    when_to_seek_help: List[str] = Field(..., description="When to seek professional medical help")
    emergency_signs: List[str] = Field(..., description="Signs that require immediate emergency care")

class SymptomResponse(BaseModel):
    user_id: str
    possible_conditions: List[PossibleCondition]
    first_aid_advice: FirstAidAdvice
    confidence_score: float = Field(..., ge=0, le=1, description="Overall confidence in the assessment")
    follow_up_questions: List[str] = Field(..., description="Suggested follow-up questions")
    timestamp: datetime = Field(default_factory=datetime.now)
    disclaimer: str = Field(..., description="Medical disclaimer text")

class ChatMessage(BaseModel):
    user_id: str = Field(..., description="Unique identifier for the user")
    message: str = Field(..., description="User's message")
    conversation_history: Optional[List[Dict[str, str]]] = Field(default_factory=list, description="Previous conversation context")
    session_id: Optional[str] = Field(None, description="Session identifier for conversation continuity")

class ChatResponse(BaseModel):
    user_id: str
    response: str = Field(..., description="AI's response message")
    suggested_questions: List[str] = Field(..., description="Suggested follow-up questions")
    confidence_level: str = Field(..., description="Confidence level of the response")
    requires_professional_consultation: bool = Field(..., description="Whether professional consultation is recommended")
    session_id: str = Field(..., description="Session identifier")
    timestamp: datetime = Field(default_factory=datetime.now)

class ImageAnalysisRequest(BaseModel):
    user_id: str = Field(..., description="Unique identifier for the user")
    image_data: bytes = Field(..., description="Image file data")
    filename: str = Field(..., description="Original filename")
    description: Optional[str] = Field(None, description="User's description of the image")
    body_part: Optional[str] = Field(None, description="Body part where the condition is located")

class DetectedFeature(BaseModel):
    feature_type: str = Field(..., description="Type of detected feature (e.g., redness, swelling)")
    confidence: float = Field(..., ge=0, le=1, description="Confidence score for this feature")
    location: Optional[Dict[str, Any]] = Field(None, description="Location coordinates of the feature")
    description: str = Field(..., description="Description of the detected feature")

class ImageAnalysisResult(BaseModel):
    condition_type: ConditionType = Field(..., description="Type of condition detected")
    possible_conditions: List[PossibleCondition] = Field(..., description="Possible conditions based on image analysis")
    detected_features: List[DetectedFeature] = Field(..., description="Features detected in the image")
    severity_assessment: SeverityLevel = Field(..., description="Assessed severity level")
    confidence_score: float = Field(..., ge=0, le=1, description="Overall confidence in the analysis")
    image_quality: str = Field(..., description="Assessment of image quality for analysis")

class ImageAnalysisResponse(BaseModel):
    user_id: str
    analysis_result: ImageAnalysisResult
    recommendations: List[str] = Field(..., description="Recommendations based on analysis")
    first_aid_advice: FirstAidAdvice
    follow_up_questions: List[str] = Field(..., description="Suggested follow-up questions")
    timestamp: datetime = Field(default_factory=datetime.now)
    disclaimer: str = Field(..., description="Medical disclaimer text")
    processing_time: float = Field(..., description="Time taken to process the image in seconds")

class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")
    error_code: str = Field(..., description="Error code")
    timestamp: datetime = Field(default_factory=datetime.now)
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
