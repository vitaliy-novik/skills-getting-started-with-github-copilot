import copy

from fastapi.testclient import TestClient

from src import app as app_module

client = TestClient(app_module.app)
INITIAL_ACTIVITIES = copy.deepcopy(app_module.activities)


def setup_function():
    app_module.activities = copy.deepcopy(INITIAL_ACTIVITIES)


def test_unregister_participant_removes_email():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"

    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]


def test_unregister_participant_returns_404_for_missing_participant():
    # Arrange
    activity_name = "Chess Club"
    email = "not-found@example.com"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    # Assert
    assert response.status_code == 404
