from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from airtable_client import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
