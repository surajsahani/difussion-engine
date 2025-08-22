#!/usr/bin/env python3
"""
FastAPI REST API for Prompt Guessing Game
Provides endpoints for CLI and web frontends
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uvicorn
import os
import json
import uuid
from datetime import datetime
import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image
from ai_prompt_game.comparison import ImageComparison

# Import our game logic
from ai_prompt_game.image_generator import ImageGenerator

# FastAPI app
app = FastAPI(
    title="Prompt Guessing Game API",
    description="AI-powered reverse prompt engineering game API",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # ReDoc
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class GameSession(BaseModel):
    session_id: str
    target_image_path: str
    model_type: str
    created_at: str
    attempts: int = 0
    best_score: float = 0.0
    best_prompt: str = ""

class PromptRequest(BaseModel):
    session_id: str
    prompt: str
    num_inference_steps: int = 20
    guidance_scale: float = 7.5

class AttemptResult(BaseModel):
    attempt_number: int
    prompt: str
    score: float
    detailed_scores: Dict[str, float]
    feedback: str
    is_best: bool
    generated_image_path: str
    comparison_image_path: str
    timestamp: str

class GameProgress(BaseModel):
    session_id: str
    attempts: int
    best_score: float
    best_prompt: str
    recent_scores: List[float]
    is_victory: bool

class ErrorResponse(BaseModel):
    error: str
    message: str

# In-memory storage (use Redis/database in production)
game_sessions: Dict[str, Dict] = {}
image_generators: Dict[str, ImageGenerator] = {}

# Helper functions
def encode_image_to_base64(image_path: str) -> str:
    """Convert image to base64 string"""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception:
        return ""

def decode_base64_to_image(base64_string: str, output_path: str) -> bool:
    """Convert base64 string to image file"""
    try:
        image_data = base64.b64decode(base64_string)
        image = Image.open(BytesIO(image_data))
        image.save(output_path)
        return True
    except Exception:
        return False

def calculate_similarity(generated_image, target_image):
    """Calculate similarity between images (simplified version)"""
    if generated_image.shape != target_image.shape:
        generated_image = cv2.resize(generated_image, (target_image.shape[1], target_image.shape[0]))
    
    # Convert to grayscale
    gen_gray = cv2.cvtColor(generated_image, cv2.COLOR_BGR2GRAY)
    target_gray = cv2.cvtColor(target_image, cv2.COLOR_BGR2GRAY)
    
    # Structural similarity
    mse = np.mean((gen_gray.astype(float) - target_gray.astype(float)) ** 2)
    structural_sim = max(0, 1 - (mse / (255 * 255)))
    
    # Color histogram
    gen_hist = cv2.calcHist([generated_image], [0, 1, 2], None, [50, 50, 50], [0, 256, 0, 256, 0, 256])
    target_hist = cv2.calcHist([target_image], [0, 1, 2], None, [50, 50, 50], [0, 256, 0, 256, 0, 256])
    hist_sim = max(0, cv2.compareHist(gen_hist, target_hist, cv2.HISTCMP_CORREL))
    
    # Combined score
    combined = (structural_sim * 0.6 + hist_sim * 0.4)
    
    return {
        'combined': max(0, min(1, combined)),
        'structural': max(0, structural_sim),
        'histogram': max(0, hist_sim),
        'edges': structural_sim,  # Simplified
        'colors': hist_sim  # Simplified
    }

# API Endpoints

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Prompt Guessing Game API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/game/create", response_model=GameSession)
async def create_game_session(
    model_type: str = Form(default="pollinations"),
    target_image: UploadFile = File(...)
):
    """
    Create a new game session with target image
    
    - **model_type**: AI model to use (pollinations, huggingface, replicate)
    - **target_image**: Target image file to match
    """
    try:
        # Generate session ID
        session_id = str(uuid.uuid4())
        
        # Create session directory
        session_dir = f"api_sessions/{session_id}"
        os.makedirs(session_dir, exist_ok=True)
        
        # Save target image
        target_path = f"{session_dir}/target.jpg"
        with open(target_path, "wb") as f:
            content = await target_image.read()
            f.write(content)
        
        # Initialize image generator
        try:
            generator = ImageGenerator(model_type=model_type)
            image_generators[session_id] = generator
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to initialize {model_type}: {str(e)}")
        
        # Create session
        session = {
            "session_id": session_id,
            "target_image_path": target_path,
            "model_type": model_type,
            "created_at": datetime.now().isoformat(),
            "attempts": 0,
            "best_score": 0.0,
            "best_prompt": "",
            "attempt_history": []
        }
        
        game_sessions[session_id] = session
        
        return GameSession(**session)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create session: {str(e)}")

@app.get("/game/{session_id}/target")
async def get_target_image(session_id: str):
    """Get the target image for a session"""
    if session_id not in game_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = game_sessions[session_id]
    target_path = session["target_image_path"]
    
    if not os.path.exists(target_path):
        raise HTTPException(status_code=404, detail="Target image not found")
    
    return FileResponse(target_path, media_type="image/jpeg")

@app.get("/game/{session_id}/target/base64")
async def get_target_image_base64(session_id: str):
    """Get the target image as base64 string"""
    if session_id not in game_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = game_sessions[session_id]
    target_path = session["target_image_path"]
    
    if not os.path.exists(target_path):
        raise HTTPException(status_code=404, detail="Target image not found")
    
    base64_image = encode_image_to_base64(target_path)
    return {"image_base64": base64_image, "format": "jpeg"}

@app.post("/game/comparison")
async def get_comparison(
    generated_img: UploadFile = File(...),
    target_img: UploadFile = File(...)
):
    gen_bytes = await generated_img.read()
    tar_bytes = await target_img.read()
    # Convert bytes -> numpy arrays with cv2
    gen_arr = np.frombuffer(gen_bytes, np.uint8)
    tar_arr = np.frombuffer(tar_bytes, np.uint8)
    gen_img = cv2.imdecode(gen_arr, cv2.IMREAD_COLOR)
    tar_img = cv2.imdecode(tar_arr, cv2.IMREAD_COLOR)
    comp = ImageComparison()
    result = comp.compare(generated_image=gen_img, target_image=tar_img)
    # --- :key: Fix: Convert any numpy values in dict to JSON-safe types ---
    def to_serializable(val):
        if isinstance(val, (np.floating, np.integer)):
            return val.item()
        if isinstance(val, np.ndarray):
            return val.tolist()
        return val
    safe_result = {k: to_serializable(v) for k, v in result.items()}
    return {"result": safe_result}

@app.post("/game/attempt", response_model=AttemptResult)
async def make_attempt(request: PromptRequest):
    """
    Make a prompt attempt and generate image
    
    - **session_id**: Game session ID
    - **prompt**: Text prompt to generate image
    - **num_inference_steps**: Number of inference steps (default: 20)
    - **guidance_scale**: Guidance scale (default: 7.5)
    """
    if request.session_id not in game_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if request.session_id not in image_generators:
        raise HTTPException(status_code=404, detail="Image generator not found")
    
    try:
        session = game_sessions[request.session_id]
        generator = image_generators[request.session_id]
        
        # Increment attempt counter
        session["attempts"] += 1
        attempt_number = session["attempts"]
        
        # Generate image
        generated_image = generator.generate_image(
            request.prompt,
            request.num_inference_steps,
            request.guidance_scale
        )
        
        if generated_image is None:
            raise HTTPException(status_code=500, detail="Failed to generate image")
        
        # Save generated image
        session_dir = f"api_sessions/{request.session_id}"
        gen_path = f"{session_dir}/attempt_{attempt_number:03d}_generated.jpg"
        cv2.imwrite(gen_path, generated_image)
        
        # Load target image and calculate similarity
        target_image = cv2.imread(session["target_image_path"])
        scores = calculate_similarity(generated_image, target_image)
        combined_score = scores['combined']
        
        # Update best score
        is_best = False
        if combined_score > session["best_score"]:
            session["best_score"] = combined_score
            session["best_prompt"] = request.prompt
            is_best = True
        
        # Generate feedback
        if combined_score >= 0.85:
            feedback = "🎉 Excellent! Very close match!"
        elif combined_score >= 0.70:
            feedback = "👍 Good work! Getting closer."
        elif combined_score >= 0.50:
            feedback = "🤔 Fair attempt. Keep refining."
        else:
            feedback = "💪 Keep trying! Analyze the target more carefully."
        
        # Create comparison image (simplified - just save paths)
        comparison_path = f"{session_dir}/attempt_{attempt_number:03d}_comparison.jpg"
        
        # Save attempt data
        attempt_data = {
            "attempt": attempt_number,
            "prompt": request.prompt,
            "score": combined_score,
            "detailed_scores": scores,
            "generated_image_path": gen_path,
            "comparison_image_path": comparison_path,
            "is_best": is_best,
            "feedback": feedback,
            "timestamp": datetime.now().isoformat()
        }
        
        session["attempt_history"].append(attempt_data)
        
        return AttemptResult(**attempt_data)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process attempt: {str(e)}")

@app.get("/game/{session_id}/progress", response_model=GameProgress)
async def get_game_progress(session_id: str):
    """Get current game progress and statistics"""
    if session_id not in game_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = game_sessions[session_id]
    
    # Get recent scores
    recent_scores = []
    if session["attempt_history"]:
        recent_attempts = session["attempt_history"][-5:]  # Last 5 attempts
        recent_scores = [attempt["score"] for attempt in recent_attempts]
    
    # Check victory condition
    is_victory = session["best_score"] >= 0.80
    
    return GameProgress(
        session_id=session_id,
        attempts=session["attempts"],
        best_score=session["best_score"],
        best_prompt=session["best_prompt"],
        recent_scores=recent_scores,
        is_victory=is_victory
    )

@app.get("/game/{session_id}/attempts")
async def get_attempt_history(session_id: str):
    """Get full attempt history for a session"""
    if session_id not in game_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = game_sessions[session_id]
    return {"attempts": session["attempt_history"]}

@app.get("/game/{session_id}/attempt/{attempt_number}/image")
async def get_generated_image(session_id: str, attempt_number: int):
    """Get generated image from specific attempt"""
    if session_id not in game_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = game_sessions[session_id]
    
    if attempt_number > len(session["attempt_history"]) or attempt_number < 1:
        raise HTTPException(status_code=404, detail="Attempt not found")
    
    attempt = session["attempt_history"][attempt_number - 1]
    image_path = attempt["generated_image_path"]
    
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Generated image not found")
    
    return FileResponse(image_path, media_type="image/jpeg")

@app.get("/game/{session_id}/attempt/{attempt_number}/image/base64")
async def get_generated_image_base64(session_id: str, attempt_number: int):
    """Get generated image as base64 string"""
    if session_id not in game_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = game_sessions[session_id]
    
    if attempt_number > len(session["attempt_history"]) or attempt_number < 1:
        raise HTTPException(status_code=404, detail="Attempt not found")
    
    attempt = session["attempt_history"][attempt_number - 1]
    image_path = attempt["generated_image_path"]
    
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Generated image not found")
    
    base64_image = encode_image_to_base64(image_path)
    return {"image_base64": base64_image, "format": "jpeg"}

@app.delete("/game/{session_id}")
async def delete_session(session_id: str):
    """Delete a game session and cleanup files"""
    if session_id not in game_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    try:
        # Cleanup files
        session_dir = f"api_sessions/{session_id}"
        if os.path.exists(session_dir):
            import shutil
            shutil.rmtree(session_dir)
        
        # Remove from memory
        del game_sessions[session_id]
        if session_id in image_generators:
            del image_generators[session_id]
        
        return {"message": "Session deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete session: {str(e)}")

@app.get("/game/sessions")
async def list_sessions():
    """List all active game sessions"""
    sessions = []
    for session_id, session_data in game_sessions.items():
        sessions.append({
            "session_id": session_id,
            "model_type": session_data["model_type"],
            "created_at": session_data["created_at"],
            "attempts": session_data["attempts"],
            "best_score": session_data["best_score"]
        })
    
    return {"sessions": sessions}

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "Not Found", "message": "The requested resource was not found"}
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error", "message": "An internal error occurred"}
    )

if __name__ == "__main__":
    # Create necessary directories
    os.makedirs("api_sessions", exist_ok=True)
    
    # Run the server
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )