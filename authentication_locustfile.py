from locust import HttpUser, task, between
import random
import string

class AuthenticationServiceUser(HttpUser):
    wait_time = between(0.1, 0.5)

    def on_start(self):
        """Register a test user once so login tests succeed."""
        self.email = f"user_{''.join(random.choices(string.ascii_lowercase, k=6))}@example.com"
        self.password = "secret123"
        self.client.post("/register", json={
            "name": "Benchmark User",
            "email": self.email,
            "password": self.password,
            "role": "student"
        })

    @task(3)
    def test_login(self):
        """Benchmark POST /login (Bcrypt hashing + JWT issuance)"""
        self.client.post("/login", json={
            "email": self.email,
            "password": self.password
        })

    @task(1)
    def test_health_check(self):
        """Benchmark GET /health"""
        self.client.get("/health")