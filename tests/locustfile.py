from locust import HttpUser, task, between
import random

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)
    token = None

    def on_start(self):
        """Login to get token"""
        email = f"test_{random.randint(1, 100000)}@example.com"
        password = "password"
        
        # Try to register first
        self.client.post("/users/", json={"email": email, "password": password})
        
        # Login
        response = self.client.post("/token", data={"username": email, "password": password})
        if response.status_code == 200:
            self.token = response.json()["access_token"]

    @task(3)
    def view_universities(self):
        self.client.get("/universities/")

    @task(1)
    def chat_with_ai(self):
        if self.token:
            headers = {"Authorization": f"Bearer {self.token}"}
            self.client.post("/chat", json={"question": "考研分数线"}, headers=headers)

    @task(2)
    def view_home(self):
        self.client.get("/")
