# main.py
import os
import uuid
import logging
import requests
from typing import Optional
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# import your existing Airtable helpers
from airtable_client import *

load_dotenv()  # only for local development; Render will use env vars

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for production: set to your domain only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static UI at /chat-ui (serves static/index.html)
app.mount("/chat-ui", StaticFiles(directory="static", html=True), name="chat_ui")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# Optional: put your assistant/system prompt in env to make it editable
AVERY_SYSTEM_PROMPT = os.getenv(
    "AVERY_SYSTEM_PROMPT",
    "You are Avery, an assistant for EOT Labs. Be concise, helpful, and use organization data when provided."
)

# -----------------------
# Existing Airtable endpoints (your original endpoints)
# keep these as-is — copied from your uploaded main.py
# -----------------------
@app.get("/user-progress")
async def user_progress(email: str):
    try:
        return get_user_progress(email)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/mentors")
async def mentors(topic: str):
    try:
        return get_mentors_by_topic(topic)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/next-milestone")
async def next_milestone(stage: str):
    try:
        return get_next_milestone(stage)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/lessons-feedback")
async def lessons_feedback(email: str):
    try:
        return get_lessons_feedback(email)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/conversation-summary")
async def conversation_summary(email: str):
    try:
        return get_conversation_summary(email)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/all-courses")
async def all_courses():
    try:
        return get_all_courses()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/modules-by-course")
async def modules_by_course(course_name: str):
    try:
        return get_modules_by_course(course_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/internal-lessons")
async def internal_lessons(module_id: str):
    try:
        return get_internal_lessons_by_module(module_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/lesson-links")
async def lesson_links(lesson_name: str):
    try:
        return get_lesson_link(lesson_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/quiz-scores")
async def quiz_scores(email: str):
    try:
        return get_quiz_scores(email)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/weekly-feedback")
async def weekly_feedback():
    try:
        return get_weekly_feedback()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/pitch-submissions")
async def pitch_submissions():
    try:
        return get_pitch_submissions()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/student-feedback")
async def student_feedback(email: str):
    try:
        return get_student_feedback(email)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/mentor-feedback")
async def mentor_feedback(email: str):
    try:
        return get_mentor_feedback(email)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------
# Chat: OpenAI integration
# -----------------------
class ChatRequest(BaseModel):
    message: str
    email: Optional[str] = None  # optional: to fetch Airtable context
    session_id: Optional[str] = None  # optional: client session id


# lightweight in-memory session store (simple; ephemeral)
SESSIONS = {}  # session_id -> list of {"role": "...", "content": "..."}

MAX_HISTORY_MESSAGES = 20  # keep last N messages to limit token usage


def add_to_session(session_id: str, role: str, content: str):
    history = SESSIONS.setdefault(session_id, [])
    history.append({"role": role, "content": content})
    if len(history) > MAX_HISTORY_MESSAGES:
        del history[0: len(history) - MAX_HISTORY_MESSAGES]


@app.post("/chat")
async def chat(req: ChatRequest):
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY not configured on the server.")

    # session id: use provided or create one
    session_id = req.session_id or str(uuid.uuid4())

    # prepare message history
    # start with system instruction
    messages = [{"role": "system", "content": AVERY_SYSTEM_PROMPT}]

    # optionally enrich with Airtable user context
    if req.email:
        try:
            user_data = get_user_progress(req.email)
            if user_data:
                context_text = (
                    f"User data: name={user_data.get('name')}, "
                    f"stage={user_data.get('stage')}, "
                    f"currentModule={user_data.get('currentModule')}, "
                    f"totalPoints={user_data.get('totalPoints', 0)}."
                )
                messages.append({"role": "system", "content": context_text})
        except Exception as e:
            logger.warning("Airtable context fetch failed: %s", e)

    # append session history (if any)
    if session_id in SESSIONS:
        messages.extend(SESSIONS[session_id])

    # append current user message
    messages.append({"role": "user", "content": req.message})

    # save user message to session
    add_to_session(session_id, "user", req.message)

    # Call OpenAI Chat Completions
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o",  # change if you want gpt-4.1 or gpt-3.5-turbo
        "messages": messages,
        "max_tokens": 600,
        "temperature": 0.2
    }

    try:
        resp = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=30)
    except Exception as e:
        logger.exception("OpenAI request failed")
        raise HTTPException(status_code=500, detail=str(e))

    if not resp.ok:
        # bubble up the OpenAI error but without secret info
        logger.error("OpenAI API error: %s %s", resp.status_code, resp.text)
        raise HTTPException(status_code=resp.status_code, detail="OpenAI API error: " + resp.text)

    data = resp.json()
    reply = ""
    try:
        reply = data.get("choices", [])[0].get("message", {}).get("content", "")
    except Exception:
        logger.exception("Failed to parse OpenAI response")

    # store assistant reply in session
    if reply:
        add_to_session(session_id, "assistant", reply)

    return {"reply": reply, "session_id": session_id}
