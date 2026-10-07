from locust import HttpUser, between, task


class InternshipServiceUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task(3)
    def test_list_internships(self):
        self.client.get("/internships")

    @task(1)
    def test_health_check(self):
        self.client.get("/")