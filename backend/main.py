from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Import our custom modules
from services.ml_symptom_checker import MLSymptomCheckerService
from services.ml_image_analyzer import MLImageAnalysisService
from models.schemas import (
    SymptomRequest, 
    SymptomResponse, 
    ImageAnalysisRequest, 
    ImageAnalysisResponse,
    ChatMessage,
    ChatResponse
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Health AI Platform",
    description="Multi-modal AI platform for preliminary health assessment",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ML services
symptom_checker = MLSymptomCheckerService()
image_analyzer = MLImageAnalysisService()

@app.get("/")
async def root():
    return {
        "message": "Health AI Platform API",
        "version": "1.0.0",
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "services": {
        "symptom_checker": "operational",
        "image_analyzer": "operational"
    }}

@app.post("/api/symptoms/analyze", response_model=SymptomResponse)
async def analyze_symptoms(request: SymptomRequest):
    """
    Analyze symptoms through conversational AI
    """
    try:
        # Validate input
        if not request.symptoms or len(request.symptoms) == 0:
            raise HTTPException(status_code=400, detail="At least one symptom must be provided")
        
        if not request.user_id:
            raise HTTPException(status_code=400, detail="User ID is required")
        
        logger.info(f"Analyzing symptoms for user: {request.user_id}")
        response = await symptom_checker.analyze_symptoms(request)
        return response
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing symptoms: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error analyzing symptoms: {str(e)}")

@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_bot(message: ChatMessage):
    """
    Chat with the health AI bot for symptom discussion
    """
    try:
        # Validate input
        if not message.message or not message.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        if not message.user_id:
            raise HTTPException(status_code=400, detail="User ID is required")
        
        logger.info(f"Processing chat message from user: {message.user_id}")
        response = await symptom_checker.process_chat_message(message)
        return response
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing chat message: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

@app.post("/api/image/analyze", response_model=ImageAnalysisResponse)
async def analyze_image(
    file: UploadFile = File(...),
    user_id: str = Form(...),
    description: Optional[str] = Form(None)
):
    """
    Analyze uploaded image for wound/skin condition assessment
    """
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Validate file size (5MB limit)
        max_size = int(os.getenv("MAX_IMAGE_SIZE", 5242880))
        content = await file.read()
        if len(content) > max_size:
            raise HTTPException(status_code=400, detail="Image file too large")
        
        logger.info(f"Analyzing image for user: {user_id}")
        
        # Create analysis request
        analysis_request = ImageAnalysisRequest(
            user_id=user_id,
            description=description,
            image_data=content,
            filename=file.filename or "uploaded_image"
        )
        
        response = await image_analyzer.analyze_image(analysis_request)
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error analyzing image: {str(e)}")

@app.get("/api/disclaimers")
async def get_disclaimers():
    """
    Get medical disclaimers and terms of use
    """
    return {
        "medical_disclaimer": """
        IMPORTANT MEDICAL DISCLAIMER:
        
        This AI platform is for educational and informational purposes only. It is NOT a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of qualified health professionals with any questions about medical conditions.
        
        The AI analysis provided should not be used to:
        - Make definitive medical diagnoses
        - Replace professional medical consultation
        - Treat, cure, or prevent any disease or condition
        
        If you have a medical emergency, call emergency services immediately.
        
        The accuracy of AI-generated health assessments cannot be guaranteed and should always be verified by qualified healthcare professionals.
        """,
        "data_privacy": """
        DATA PRIVACY NOTICE:
        
        Your uploaded images and health information are processed securely and are not stored permanently. However, please avoid sharing highly sensitive personal health information.
        
        Images are processed locally when possible and transmitted securely. We do not share your personal health data with third parties without your explicit consent.
        """,
        "terms_of_use": """
        TERMS OF USE:
        
        By using this platform, you agree that:
        - You understand this is for educational purposes only
        - You will not rely solely on AI analysis for medical decisions
        - You will consult healthcare professionals for actual medical concerns
        - You understand the limitations of AI health assessment technology
        """
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "False").lower() == "true"
    )
