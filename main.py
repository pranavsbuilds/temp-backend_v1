import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
import uuid
import time
import json
import asyncio
import requests
from typing import List, Dict, Any

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from vosk import Model, KaldiRecognizer

from config import PORT, HOST, QUIZ_API_KEY, VOSK_MODEL_PATH, CHEAT_PENALTY, TOTAL_QUESTIONS, MOCK_QUESTIONS
from ml_models import calculate_similarity, predict_performance_cluster

app = FastAPI(
    title="Smart Interview Taker Backend",
    description="FastAPI backend exposing STT transcription, SBERT scoring, and KMeans results clustering.",
    version="1.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session store (database-free)
SESSIONS: Dict[str, Dict[str, Any]] = {}

# Initialize Vosk Model
vosk_model = None
try:
    if os.path.exists(VOSK_MODEL_PATH):
        print(f"Loading Vosk model from: {os.path.abspath(VOSK_MODEL_PATH)}")
        vosk_model = Model(VOSK_MODEL_PATH)
        print("Vosk model loaded successfully.")
    else:
        print(f"WARNING: Vosk model directory not found at '{VOSK_MODEL_PATH}'.")
        print("WebSocket STT will run in simulation fallback mode.")
except Exception as e:
    print(f"WARNING: Failed to load Vosk model: {e}")
    print("WebSocket STT will run in simulation fallback mode.")

# --- Pydantic Models ---

class StartSessionRequest(BaseModel):
    uid: str
    job: str
    level: str
    api_key: str = ""

class LegacyStartSessionRequest(BaseModel):
    Field: str
    Difficulty: str
    API_KEY: str = ""

class ScorePayload(BaseModel):
    answer: str
    explanation: str

# --- Helper Functions ---

def fetch_quiz_questions(category: str, difficulty: str, api_key: str) -> List[Dict[str, Any]]:
    """
    Fetches questions from QuizAPI. Returns raw API list or empty list if failed.
    """
    url = "https://quizapi.io/api/v1/questions"
    
    # Map frontend job selection to QuizAPI parameters
    params = {
        "difficulty": difficulty,
        "limit": 20
    }
    if category == "python":
        params["tags"] = "python"
    elif category == "frontend":
        params["tags"] = "react,css,typescript"
    else:
        params["category"] = category

    headers = {
        "X-Api-Key": api_key,
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(url, params=params, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            # Handle list directly or nested under 'data'/'questions' key
            if isinstance(data, dict):
                data = data.get('data', []) or data.get('questions', []) or [data]
            if isinstance(data, list):
                return data
    except Exception as e:
        print(f"Error fetching from QuizAPI: {e}")
    return []

def title_fetch_helper(query_phrase: str) -> List[str]:
    """
    Queries Wikipedia API for article titles relevant to query_phrase.
    """
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query_phrase,
        "format": "json",
        "origin": "*"
    }
    headers = {
        "User-Agent": "SmartInterviewerBot/1.0 (contact@example.com)"
    }
    try:
        response = requests.get(url, params=params, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            search_results = data.get("query", {}).get("search", [])
            return [result.get("title") for result in search_results if result.get("title")]
    except Exception as e:
        print(f"Error fetching titles from Wikipedia: {e}")
    return []

def handle_session_start(uid: str, job: str, level: str, api_key: str) -> Dict[str, Any]:
    """
    Shared handler to initialize the session parameters, fetch/fill questions,
    and save session state in-memory.
    """
    sid = f"session-{uuid.uuid4()}"
    
    # Normalize inputs
    normalized_job = job.strip().lower()
    normalized_level = level.strip().lower()
    
    # Validate level
    if normalized_level not in ["easy", "medium", "hard"]:
        normalized_level = "easy"
        
    api_key_to_use = api_key or QUIZ_API_KEY
    questions_data = []
    
    # Try QuizAPI
    if api_key_to_use:
        questions_data = fetch_quiz_questions(normalized_job, normalized_level, api_key_to_use)
        
    questions = []
    explanations = []
    
    # Extract QuizAPI questions
    for item in questions_data:
        q_text = item.get('question') or item.get('text')
        q_exp = item.get('explanation') or item.get('description') or "No explanation available."
        if q_text:
            questions.append({
                "qid": len(questions) + 1,
                "text": q_text,
                "order": len(questions) + 1
            })
            explanations.append(q_exp)
            if len(questions) >= TOTAL_QUESTIONS:
                break
                
    # Fallback to local mock question bank if API returned insufficient questions
    if len(questions) < TOTAL_QUESTIONS:
        fallback_list = MOCK_QUESTIONS.get(normalized_job, {}).get(normalized_level, [])
        if not fallback_list:
            # Absolute fallback
            fallback_list = MOCK_QUESTIONS.get("programming", {}).get("easy", [])
            
        for item in fallback_list:
            if len(questions) >= TOTAL_QUESTIONS:
                break
            # Avoid duplicating questions already fetched
            if not any(q["text"] == item["text"] for q in questions):
                questions.append({
                    "qid": len(questions) + 1,
                    "text": item["text"],
                    "order": len(questions) + 1
                })
                explanations.append(item["explanation"])
                
    # Store session details in memory
    SESSIONS[sid] = {
        "sid": sid,
        "uid": uid,
        "job": normalized_job,
        "level": normalized_level,
        "questions": questions,
        "explanations": explanations,
        "responses": [],
        "cheating_count": 0,
        "violations": [],
        "start_time": time.time()
    }
    
    return {
        "sid": sid,
        "status": "created",
        "questions": [q["text"] for q in questions],
        "explanation": explanations
    }

# --- API Routes ---

@app.get("/hello")
def hello():
    """Health check route."""
    return {"hi": "hello"}

@app.post("/api/sessions/start")
def start_session_modern(payload: StartSessionRequest):
    """
    Frontend endpoint for starting a session.
    """
    return handle_session_start(
        uid=payload.uid,
        job=payload.job,
        level=payload.level,
        api_key=payload.api_key
    )

@app.post("/start_interview")
def start_session_legacy(payload: LegacyStartSessionRequest):
    """
    Original backend endpoint for starting a session.
    """
    return handle_session_start(
        uid="legacy-user",
        job=payload.Field,
        level=payload.Difficulty,
        api_key=payload.API_KEY
    )

@app.post("/api/interview/{sid}/flag")
@app.post("/api/interview/{sid}/flag/")
def flag_session(sid: str):
    """
    Increments cheating occurrences count for a session.
    """
    session = SESSIONS.get(sid)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
        
    session["cheating_count"] += 1
    session["violations"].append("Cheating Flagged")
    return {"flagged": True, "cheating_count": session["cheating_count"]}

@app.post("/score")
def legacy_score(payload: ScorePayload):
    """
    Original backend scoring route for comparing text answers.
    """
    sim_score = calculate_similarity(payload.answer, payload.explanation)
    return {"similarity": [sim_score]}

@app.post("/title_fetch")
def legacy_title_fetch(payload: dict):
    """
    Original backend route for retrieving matching Wikipedia articles.
    """
    query = payload.get("query_phrase", "")
    titles = title_fetch_helper(query)
    return {"titles": titles}

@app.get("/api/interview/{sid}/results")
def get_results(sid: str):
    """
    Aggregates session results, calculates final score, runs KMeans performance group prediction,
    and fetches learning resources.
    """
    session = SESSIONS.get(sid)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
        
    responses = session["responses"]
    similarities = [r["similarity_score"] for r in responses]
    cheating_count = session["cheating_count"]
    
    # Calculate average similarity (0-1 scale)
    avg_similarity = sum(similarities) / len(similarities) if similarities else 0.0
    
    # Calculate final score (0-10 scale)
    # Deduct cheat penalty: CHEAT_PENALTY * 10 (which is 2.0 per cheat)
    raw_score = avg_similarity * 10.0
    penalty = cheating_count * CHEAT_PENALTY * 10.0
    final_score = max(0.0, min(10.0, round(raw_score - penalty + 1e-9, 1)))
    
    # Predict performance cluster (KMeans)
    primary_anomaly = "None"
    if session["violations"]:
        primary_anomaly = session["violations"][0]
        
    cluster_label = predict_performance_cluster(
        anomaly=primary_anomaly,
        level=session["level"],
        avg_similarity=avg_similarity
    )
    
    # Pre-resolve Wikipedia links for low similarity scores
    questions_results = []
    for r in responses:
        q_res = {
            "qid": r["qid"],
            "question_text": r["question_text"],
            "user_transcript": r["user_transcript"],
            "ideal_answer": r["ideal_answer"],
            "similarity_score": r["similarity_score"]
        }
        
        # If score is below threshold, fetch resources
        if r["similarity_score"] < 0.6:
            wiki_titles = title_fetch_helper(r["question_text"])
            if wiki_titles:
                best_title = wiki_titles[0]
                url_title = best_title.replace(" ", "_")
                q_res["wikipedia_link"] = {
                    "title": best_title,
                    "url": f"https://en.wikipedia.org/wiki/{url_title}",
                    "snippet": f"Wikipedia article about {best_title}"
                }
        questions_results.append(q_res)
        
    return {
        "sid": sid,
        "final_score": final_score,
        "cluster_label": cluster_label,
        "cheating_count": cheating_count,
        "questions": questions_results
    }

# --- WebSocket STT Stream Endpoints ---

async def handle_websocket_stt(websocket: WebSocket, sid: str):
    """
    Handles streaming binary mono 16kHz PCM audio over WebSocket,
    transcribing with Vosk, and evaluating similarity.
    """
    session = SESSIONS.get(sid)
    
    # Initialize Vosk recognizer if model is available
    rec = None
    if vosk_model:
        rec = KaldiRecognizer(vosk_model, 16000)
        
    sentence = []
    
    try:
        while True:
            # Wait for PCM audio chunks with a 5-second silence timeout
            try:
                data = await asyncio.wait_for(websocket.receive_bytes(), timeout=5.0)
                if rec and data:
                    if rec.AcceptWaveform(data):
                        result = json.loads(rec.Result())
                        text = result.get('text', '')
                        if text:
                            print(f"[STT User Spoke]: {text}")
                            sentence.append(text)
                else:
                    # Simulation mode sleep
                    await asyncio.sleep(0.1)
            except asyncio.TimeoutError:
                print(f"[WebSocket] 5s silence timeout reached for session {sid}.")
                break
    except WebSocketDisconnect:
        print(f"[WebSocket] Client disconnected session {sid}.")
    except Exception as e:
        print(f"[WebSocket] Error: {e}")
        
    # Process final transcription result
    final_text = ""
    if rec:
        final_result = json.loads(rec.FinalResult())
        text = final_result.get('text', '')
        if text:
            sentence.append(text)
        final_text = " ".join(sentence).strip()
    else:
        # Fallback simulation transcript for local development/testing without Vosk model
        final_text = "This is a simulated transcript because the Vosk speech model was not loaded."
        
    if not final_text:
        final_text = "No speech detected."
        
    score = 0.0
    if session:
        # Synchronize question response using the count of recorded responses
        current_idx = len(session["responses"])
        if current_idx < len(session["questions"]):
            ideal_explanation = session["explanations"][current_idx]
            score = calculate_similarity(final_text, ideal_explanation)
            
            # Save response details
            response_entry = {
                "qid": current_idx + 1,
                "question_text": session["questions"][current_idx]["text"],
                "user_transcript": final_text,
                "ideal_answer": ideal_explanation,
                "similarity_score": score,
                "attempt": 1
            }
            session["responses"].append(response_entry)
            
    # Send combined response to satisfy all expected models
    response_payload = {
        "transcript": final_text,
        "score": score,
        "text": [final_text]  # Week 3 legacy compatibility
    }
    
    try:
        await websocket.send_json(response_payload)
        await websocket.close()
    except Exception as e:
        print(f"Error closing WebSocket: {e}")

@app.websocket("/api/interview/{sid}/stream")
async def websocket_interview_stream(websocket: WebSocket, sid: str):
    """
    WebSocket endpoint expected by the modern frontend.
    """
    await websocket.accept()
    await handle_websocket_stt(websocket, sid)

@app.websocket("/STT")
async def websocket_stt_legacy(websocket: WebSocket):
    """
    WebSocket endpoint expected by the legacy backend specifications.
    Retrieves or creates a default session if sid is not supplied.
    """
    await websocket.accept()
    
    # Try to find an active session ID, or create a default mock one
    sid = websocket.query_params.get("sid")
    if not sid:
        if SESSIONS:
            sid = list(SESSIONS.keys())[-1]
        else:
            # Generate a mock default session
            res = handle_session_start("default-user", "programming", "easy", "")
            sid = res["sid"]
            
    await handle_websocket_stt(websocket, sid)

if __name__ == "__main__":
    import uvicorn
    print(f"Starting Smart Interviewer Backend on http://{HOST}:{PORT}")
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
