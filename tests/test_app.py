import copy

from fastapi.testclient import TestClient

from src import app as app_module


client = TestClient(app_module.app)


def reset_activities():
    app_module.activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
        },
    }


def test_unregister_participant_removes_email_from_activity():
    reset_activities()

    response = client.delete(
        "/activities/Chess Club/signup?email=michael@mergington.edu"
    )

    assert response.status_code == 200
    assert "michael@mergington.edu" not in app_module.activities["Chess Club"]["participants"]
    assert "daniel@mergington.edu" in app_module.activities["Chess Club"]["participants"]


def test_unregister_participant_returns_error_for_unknown_email():
    reset_activities()

    response = client.delete(
        "/activities/Chess Club/signup?email=unknown@mergington.edu"
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up for this activity"
