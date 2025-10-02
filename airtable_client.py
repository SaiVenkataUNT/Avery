import os
import requests
from dotenv import load_dotenv

load_dotenv()

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")
HEADERS = {"Authorization": f"Bearer {AIRTABLE_API_KEY}"}


def get_user_progress(email):
    url = f"https://api.airtable.com/v0/{BASE_ID}/Incubator signup data"
    params = {"filterByFormula": f"{{Email}}='{email}'"}
    response = requests.get(url, headers=HEADERS, params=params)
    records = response.json().get("records", [])
    if not records:
        return {}
    fields = records[0]["fields"]
    return {
        "name": fields.get("Name"),
        "email": fields.get("Email"),
        "stage": fields.get("Major Focuss"),
        "currentModule": fields.get("ModuleID_ForigneKey (from Internal Lessons)"),
        "completedCourses": fields.get("CoursesThatareCompleted", []),
        "totalPoints": fields.get("User_TotalPoints", 0),
    }


def get_mentors_by_topic(topic):
    url = f"https://api.airtable.com/v0/{BASE_ID}/Mentors Table"
    params = {"filterByFormula": f"SEARCH(LOWER('{topic}'), LOWER({{Tags}}))"}
    response = requests.get(url, headers=HEADERS, params=params)
    return [record["fields"] for record in response.json().get("records", [])]


def get_next_milestone(stage):
    url = f"https://api.airtable.com/v0/{BASE_ID}/Roadmap Table"
    params = {"filterByFormula": f"{{Stage}}='{stage}'"}
    response = requests.get(url, headers=HEADERS, params=params)
    records = response.json().get("records", [])
    return records[0]["fields"] if records else {}


def get_lessons_feedback(email):
    url = f"https://api.airtable.com/v0/{BASE_ID}/LessonsFeedback"
    params = {"filterByFormula": f"{{Email (from Name_ForeignKey)}}='{email}'"}
    response = requests.get(url, headers=HEADERS, params=params)
    return [record["fields"] for record in response.json().get("records", [])]


def get_conversation_summary(email):
    url = f"https://api.airtable.com/v0/{BASE_ID}/User Profile Data"
    params = {"filterByFormula": f"{{Email}}='{email}'"}
    response = requests.get(url, headers=HEADERS, params=params)
    records = response.json().get("records", [])
    if not records:
        return {}
    fields = records[0]["fields"]
    return {
        "name": fields.get("Name"),
        "email": fields.get("Email"),
        "totalStarted": fields.get("Total conversations started", 0),
        "totalReceived": fields.get("Total conversations received", 0),
        "total": fields.get("Total conversation", 0)
    }


def get_all_courses():
    url = f"https://api.airtable.com/v0/{BASE_ID}/All Courses"
    response = requests.get(url, headers=HEADERS)
    return [record["fields"] for record in response.json().get("records", [])]


def get_modules_by_course(course_name):
    url = f"https://api.airtable.com/v0/{BASE_ID}/Module Table"
    params = {
        "filterByFormula": f"{{CourseName (from AllCourses_foreignkey) 2}}='{course_name}'"}
    response = requests.get(url, headers=HEADERS, params=params)
    return [record["fields"] for record in response.json().get("records", [])]


def get_internal_lessons_by_module(module_id):
    url = f"https://api.airtable.com/v0/{BASE_ID}/Internal Lessons"
    params = {"filterByFormula": f"{{ModuleID_ForigneKey}}='{module_id}'"}
    response = requests.get(url, headers=HEADERS, params=params)
    return [record["fields"] for record in response.json().get("records", [])]


def get_lesson_link(lesson_name):
    url = f"https://api.airtable.com/v0/{BASE_ID}/Lesson URL's"
    params = {"filterByFormula": f"{{LessonName_LinkName}}='{lesson_name}'"}
    response = requests.get(url, headers=HEADERS, params=params)
    records = response.json().get("records", [])
    return records[0]["fields"] if records else {}


def get_quiz_scores(email):
    url = f"https://api.airtable.com/v0/{BASE_ID}/Table 22"
    params = {"filterByFormula": f"{{Name/Email}}='{email}'"}
    response = requests.get(url, headers=HEADERS, params=params)
    records = response.json().get("records", [])
    return records[0]["fields"] if records else {}


def get_weekly_feedback():
    url = f"https://api.airtable.com/v0/{BASE_ID}/Weekly Response Forms"
    response = requests.get(url, headers=HEADERS)
    return [record["fields"] for record in response.json().get("records", [])]


def get_pitch_submissions():
    url = f"https://api.airtable.com/v0/{BASE_ID}/Pitch for ya life file Uploads"
    response = requests.get(url, headers=HEADERS)
    return [record["fields"] for record in response.json().get("records", [])]


def get_student_feedback(email):
    url = f"https://api.airtable.com/v0/{BASE_ID}/Student to mentor feedback"
    params = {"filterByFormula": f"{{Your Email ID}}='{email}'"}
    response = requests.get(url, headers=HEADERS, params=params)
    return [record["fields"] for record in response.json().get("records", [])]


def get_mentor_feedback(email):
    url = f"https://api.airtable.com/v0/{BASE_ID}/Mentor to student feedback table"
    params = {"filterByFormula": f"{{Mentor Email ID}}='{email}'"}
    response = requests.get(url, headers=HEADERS, params=params)
    return [record["fields"] for record in response.json().get("records", [])]
