import copy

from fastapi.testclient import TestClient

from src import app as app_module

client = TestClient(app_module.app)
INITIAL_ACTIVITIES = copy.deepcopy(app_module.activities)


def setup_function():
    app_module.activities = copy.deepcopy(INITIAL_ACTIVITIES)


def test_unregister_participant_removes_email():
    response = client.delete("/activities/Chess Club/participants/michael@mergington.edu")

    assert response.status_code == 200
    assert response.json()["message"] == "Unregistered michael@mergington.edu from Chess Club"

    activities = client.get("/activities").json()
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]


def test_unregister_participant_returns_404_for_missing_participant():
    response = client.delete("/activities/Chess Club/participants/not-found@example.com")

    assert response.status_code == 404
