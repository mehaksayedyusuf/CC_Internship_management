from locust import HttpUser, task, between

class ApplicationServiceUser(HttpUser):
    # Wait between 0.1 and 0.5 seconds between tasks to simulate continuous requests
    wait_time = between(0.1, 0.5)

    @task(3)
    def test_list_applications(self):
        # Benchmark GET /applications endpoint
        self.client.get("/applications")

    @task(1)
    def test_health_check(self):
        # Benchmark GET / endpoint
        self.client.get("/")