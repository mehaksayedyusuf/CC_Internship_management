from locust import HttpUser, task, between

class StudentServiceUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task(3)
    def test_list_students(self):
        self.client.get("/students")

    @task(2)
    def test_filter_department(self):
        self.client.get("/students?department=CSE")

    @task(1)
    def test_health_check(self):
        self.client.get("/health")