from locust import HttpUser, between, task

class DjangoUser(HttpUser):
    wait_time = between(1, 2)  # Wait between 1 and 2 seconds between requests

    def on_start(self):
        # Perform a GET request to retrieve the CSRF token
        response = self.client.get("http://localhost/secureapp/login/")
        # Extract CSRF token from cookies
        csrf_token = response.cookies['csrftoken']
        self.csrf_token = csrf_token

    @task(1)
    def login(self):
        headers = {'X-CSRFToken': self.csrf_token}
        data = {"username": "Bekzat", "password": "beka2004abc"}
        self.client.post("http://localhost/secureapp/login/", data=data, headers=headers)
        
    @task(2)
    def view_home(self):
        self.client.get("http://localhost/")

    @task(3)
    def access_protected(self):
        self.client.get("http://localhost/protected", headers={"Authorization": "Bearer YOUR_JWT_TOKEN"})

    # You can add more tasks as needed for other routes or API endpoints


class LoadTestUser(HttpUser):
    wait_time = between(1, 3)  # Wait between requests

    def on_start(self):
        """This runs at the start of each simulated user's session to log in."""
        self.client.post("/api/token/", json={
            "username": "admin",  # Use a valid test admin username
            "password": "password123"  # Use a valid test admin password
        })

    @task(2)
    def view_profile(self):
        """Simulates a request to the profile view."""
        self.client.get("/secureapp/profiles/")

    @task(1)
    def access_sensitive_data(self):
        """Simulates a request to the sensitive data view."""
        self.client.get("/secureapp/sensitive-data/1/")  # Adjust ID as needed

    @task(1)
    def update_sensitive_data(self):
        """Simulates an update request to the sensitive data view."""
        self.client.put("/secureapp/sensitive-data/1/", json={
            "ssn": "123-45-6789",
            "credit_card_number": "4111111111111111"
        })


class DatasetUploadUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def upload_dataset(self):
        with open("sample.csv", "rb") as file:
            self.client.post("/dataset_processor/upload/", files={"file": file})

    @task
    def check_status(self):
        self.client.get("/dataset_processor/status/<dataset_id>/")  # Replace with a valid dataset ID