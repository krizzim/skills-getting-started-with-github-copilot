"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    # sports‑related
    "Soccer Team": {
        "description": "Practice and compete in inter‑school soccer matches",
        "schedule": "Mondays and Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 18,
        "participants": ["alex@mergington.edu", "lea@mergington.edu"]
    },
    "Swimming Club": {
        "description": "Improve swimming technique and endurance",
        "schedule": "Wednesdays, 5:00 PM - 6:30 PM",
        "max_participants": 25,
        "participants": ["maria@mergington.edu", "kevin@mergington.edu"]
    },
    # artistic
    "Drama Club": {
        "description": "Rehearse and perform plays and skits",
        "schedule": "Tuesdays, 3:00 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["lily@mergington.edu", "omar@mergington.edu"]
    },
    "Art Workshop": {
        "description": "Explore painting, sculpture, and other visual arts",
        "schedule": "Fridays, 1:00 PM - 3:00 PM",
        "max_participants": 15,
        "participants": ["zoe@mergington.edu", "carlos@mergington.edu"]
    },
    # intellectual
    "Math Olympiad": {
        "description": "Prepare for math competitions and problem solving",
        "schedule": "Thursdays, 4:30 PM - 6:00 PM",
        "max_participants": 10,
        "participants": ["nina@mergington.edu", "ryan@mergington.edu"]
    },
    "Science Fair": {
        "description": "Develop projects and experiments for the annual fair",
        "schedule": "Wednesdays, 2:00 PM - 4:00 PM",
        "max_participants": 12,
        "participants": ["sara@mergington.edu", "jon@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Check if student is already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/participants")
def remove_participant(activity_name: str, email: str):
    """Unregister a student from an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    activity = activities[activity_name]
    if email not in activity["participants"]:
        raise HTTPException(status_code=404, detail="Student not signed up for this activity")

    activity["participants"].remove(email)
    return {"message": f"Removed {email} from {activity_name}"}
