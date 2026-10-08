from locust import HttpUser, between, task

class InternshipServiceUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task(3)
    def test_list_internships(self):
        self.client.get("/internships")

    @task(2)
    def test_search_and_filter(self):
        self.client.get("/internships?status=open&search=Cloud")

    @task(1)
    def test_health_check(self):
        self.client.get("/health")