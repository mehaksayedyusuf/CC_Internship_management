from locust import HttpUser, task, between

class ApplicationServiceUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task(3)
    def test_list_applications(self):
        self.client.get("/applications")

    @task(2)
    def test_application_stats(self):
        self.client.get("/applications/stats")

    @task(1)
    def test_health_check(self):
        self.client.get("/health")