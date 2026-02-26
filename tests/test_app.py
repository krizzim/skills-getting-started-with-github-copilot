from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


class TestRoot:
    def test_root_redirects_to_static(self):
        # Arrange
        expected_status = 307
        expected_location_suffix = "/static/index.html"

        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == expected_status
        assert response.headers["location"].endswith(expected_location_suffix)


class TestGetActivities:
    def test_get_activities_returns_dict(self):
        # Arrange
        expected_status = 200

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == expected_status
        assert isinstance(response.json(), dict)
        assert len(response.json()) > 0


class TestSignup:
    def test_signup_adds_participant(self):
        # Arrange
        activity_name = "Chess Club"
        test_email = "new-student@mergington.edu"
        if test_email in activities[activity_name]["participants"]:
            activities[activity_name]["participants"].remove(test_email)

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": test_email}
        )

        # Assert
        assert response.status_code == 200
        assert test_email in activities[activity_name]["participants"]

    def test_signup_duplicate_returns_400(self):
        # Arrange
        activity_name = "Chess Club"
        test_email = "existing-student@mergington.edu"
        activities[activity_name]["participants"].append(test_email)

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": test_email}
        )

        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"].lower()


class TestRemoveParticipant:
    def test_remove_participant_succeeds(self):
        # Arrange
        activity_name = "Chess Club"
        test_email = "remove-me@mergington.edu"
        activities[activity_name]["participants"].append(test_email)

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": test_email}
        )

        # Assert
        assert response.status_code == 200
        assert test_email not in activities[activity_name]["participants"]

    def test_remove_nonexistent_participant_returns_404(self):
        # Arrange
        activity_name = "Chess Club"
        test_email = "never-signed-up@mergington.edu"
        if test_email in activities[activity_name]["participants"]:
            activities[activity_name]["participants"].remove(test_email)

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": test_email}
        )

        # Assert
        assert response.status_code == 404
        assert "not signed up" in response.json()["detail"].lower()
