from locust import HttpUser, task, between
import json
import uuid

class UserAPIUser(HttpUser):
    wait_time = between(1, 5)
    host = "http://127.0.0.1:8000"

    def on_start(self):
        """Run once per user when they start."""
        self.user_id = None
        self.create_user()

    @task(2)
    def list_profiles(self):
        self.client.get("/api/v1/task/users/")

    @task(2)
    def create_user(self):
        """Simulate POST /api/users/ to create a user and profile."""
        unique_id = str(uuid.uuid4())[:8]  # Use UUID for unique username
        payload = {
            "username": f"user_{unique_id}",
            "email": f"user_{unique_id}@example.com",
            "first_name": "Test",
            "last_name": "User",
            "profile": {
                "website": "https://example.com",
                "bio": "This is a sufficiently long bio with more than 50 characters for load testing."
            }
        }
        response = self.client.post("/api/v1/task/users/", json=payload, name="create_user")
        
        if response.status_code == 201:
            self.user_id = response.json().get("id")
        elif response.status_code == 400:
            print(f"Create failed: {response.status_code}, {response.text}")
        else:
            print(f"Unexpected response: {response.status_code}, {response.text}")

    @task(1)
    def update_user(self):
        """Simulate PATCH /api/users/<id>/ to update a user and profile."""
        if self.user_id is None:
            return  # Skip if no user was created
        
        payload = {
            "email": f"updated_{self.user_id}@example.com",
            "profile": {
                "website": "https://updated.com",
                "bio": "This is an updated bio with more than 50 characters for load testing purposes."
            }
        }
        response = self.client.patch(f"/api/v1/task/users/{self.user_id}/", json=payload, name="update_user")
        
        if response.status_code != 200:
            print(f"Update failed: {response.status_code}, {response.text}")

    @task(1)
    def create_invalid_user(self):
        """Simulate POST /api/users/ with invalid data to test validation."""
        payload = {
            "username": f"user_{str(uuid.uuid4())[:8]}",
            "profile": {
                "website": "invalid-url",
                "bio": "Short"
            }
        }
        response = self.client.post("/api/v1/task/users/", json=payload, name="create_invalid_user")
        if response.status_code != 400:
            print(f"Expected 400, got: {response.status_code}, {response.text}")