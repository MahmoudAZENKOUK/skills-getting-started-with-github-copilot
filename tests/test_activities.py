import copy
import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


# Snapshot of initial activities to restore between tests
INITIAL_ACTIVITIES = copy.deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities():
    activities.clear()
    activities.update(copy.deepcopy(INITIAL_ACTIVITIES))
    yield


def test_get_activities():
    client = TestClient(app)
    r = client.get("/activities")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_success():
    client = TestClient(app)
    email = "new.student@school.test"
    activity_name = "Chess Club"
    r = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert r.status_code == 200
    assert email in activities[activity_name]["participants"]


def test_signup_already_registered():
    client = TestClient(app)
    email = "michael@mergington.edu"  # already in initial participants
    activity_name = "Chess Club"
    r = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert r.status_code == 400


def test_unregister_success():
    client = TestClient(app)
    email = "michael@mergington.edu"
    activity_name = "Chess Club"
    r = client.delete(f"/activities/{activity_name}/signup", params={"email": email})
    assert r.status_code == 200
    assert email not in activities[activity_name]["participants"]


def test_unregister_not_registered():
    client = TestClient(app)
    email = "not.registered@school.test"
    activity_name = "Chess Club"
    r = client.delete(f"/activities/{activity_name}/signup", params={"email": email})
    assert r.status_code == 400
