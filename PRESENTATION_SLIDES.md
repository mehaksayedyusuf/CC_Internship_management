# Cloud Computing Laboratory Evaluation Presentation
## Build, Deploy and Analyze a Containerized Microservice Application Under Varying Workloads

**Presentation File:** [Internship_Management_Microservices.pptx](file:///a:/CC_Internship_management/Internship_Management_Microservices.pptx)  
**Domain:** Internship Management System  
**Team Members:**
- **Vageesh Mathad** (USN: `01FE24BCI008`)
- **Mehak Sayed Yusuf** (USN: `01FE24BCI012`)
- **Joel Biju** (USN: `01FE24BCI021`)
- **Akshay Bhat** (USN: `01FE24BCI024`)

---

### Slide 1: Title & Team Details
* **Heading:** Cloud Computing Laboratory (Experiment Evaluation)
* **Title:** Build, Deploy & Analyze a Containerized Microservice Application Under Varying Workloads
* **Domain:** Internship Management System | FastAPI • Docker Compose • Locust • Resource Profiling
* **Team Cards:**
  1. **Vageesh Mathad** — `01FE24BCI008`
  2. **Mehak Sayed Yusuf** — `01FE24BCI012`
  3. **Joel Biju** — `01FE24BCI021`
  4. **Akshay Bhat** — `01FE24BCI024`
* **Speaker:** Vageesh Mathad (Introduction of project aim and team)

---

### Slide 2: Experiment Aim, Domain & Objectives (Checkpoint 1 Overview)
* **Aim:** To develop a microservice-based application containing three independent services, containerize and deploy using Docker, establish inter-service communication, generate varying workloads, monitor resource utilization, and analyze application performance.
* **Application Domain:** Internship Management System (managing student profiles, internship listings, and application lifecycle).
* **Three Independent Microservices:**
  1. **Student Service (`:8002`):** Profile CRUD, academic department, study year, and email uniqueness.
  2. **Internship Service (`:8003`):** Posting listings, company details, stipend/location, and search filtering.
  3. **Application Service (`:8004`):** Application submissions, review workflow, and cross-service validation.
* **Speaker:** Vageesh Mathad (Explaining domain choice and architectural decoupling)

---

### Slide 3: Architecture & REST API Implementation (Checkpoint 1)
* **Minimum Architecture Flow:**
  $$\text{Client / Browser} \longrightarrow \text{Application Service (:8004)} \begin{cases} \longrightarrow \text{Student Service (:8002)} \\ \longrightarrow \text{Internship Service (:8003)} \end{cases}$$
* **REST API Endpoints:**
  * **Student Service:** `POST /students`, `GET /students`, `GET /students/{id}`, `PUT /students/{id}`, `DELETE /students/{id}`
  * **Internship Service:** `POST /internships`, `GET /internships`, `GET /internships/{id}`, `PUT /internships/{id}`, `DELETE /internships/{id}`
  * **Application Service:** `POST /applications`, `GET /applications`, `PATCH /applications/{id}/status`, `DELETE /applications/{id}`
* **Interactive Swagger Documentation:** Built-in at `/docs` for every service.
* **Speaker:** Mehak Sayed Yusuf (Explaining endpoints, schemas, and independent execution)

---

### Slide 4: Containerization & Docker Compose Deployment (Checkpoint 2)
* **Microservice Containerization:**
  * Base Image: `python:3.12-slim` for minimal container image footprint (~280 MB).
  * Isolated dependencies per service via individual `Dockerfile` and `requirements.txt`.
  * Production ASGI runtime: Uvicorn bound to `0.0.0.0:8000`.
* **Docker Compose Orchestration (`docker-compose.yml`):**
  * Single command deployment: `docker compose up --build -d`.
  * Named volumes (`student_data`, `internship_data`, `application_data`) ensure persistent SQLite storage across container restarts.
  * Dependency management: `application` declares `depends_on: [student, internship]`.
* **Speaker:** Mehak Sayed Yusuf (Explaining Dockerfiles, volumes, and multi-container orchestration)

---

### Slide 5: Inter-Service Communication Flow (Checkpoint 3)
* **Docker Network Service Discovery:**
  * Communicates over internal Docker bridge network without brittle hardcoded IP addresses.
  * Internal target URLs: `http://student:8000` and `http://internship:8000`.
* **End-to-End Validation Protocol:**
  1. Client sends `POST /applications` with `student_id` and `internship_id`.
  2. Application Service sends internal HTTP GET to Student Service to verify `student_id`.
  3. Application Service sends internal HTTP GET to Internship Service to verify `internship_id`.
  4. **Failure Case:** If student or internship does not exist, an immediate `HTTP 404` is returned, preventing orphan data.
  5. **Success Case:** If both exist, application is committed with status `pending`.
* **Live Demo:** Tested with student ID `99999` returning `404 Not Found`.
* **Speaker:** Joel Biju (Demonstrating inter-service communication and error handling)

---

### Slide 6: Workload Generation & Observation Table (Checkpoint 4)
* **Load Testing Methodology:**
  * Load Testing Tool: **Locust** ([student_locustfile.py](file:///a:/CC_Internship_management/student_locustfile.py), [internship_locustfile.py](file:///a:/CC_Internship_management/internship_locustfile.py), [application_locustfile.py](file:///a:/CC_Internship_management/application_locustfile.py)).
  * Monitoring Tool: `docker stats` tracking container CPU (%) and Memory (MB).
  * 5 Workload Levels: **W1 (1 user), W2 (2 users), W3 (4 users), W4 (8 users), W5 (16 users)**.
* **Observation Table:**

| Workload | Concurrency | Avg Response Time | Throughput (RPS) | Failures | CPU Utilization | Memory Usage |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **W1** | 1 User | 8.0 – 10.5 ms | 3.1 RPS | 0 | 1.0 – 2.1 % | 53 – 55 MB |
| **W2** | 2 Users | 9.0 – 10.5 ms | 5.8 – 6.9 RPS | 0 | 2.5 – 3.0 % | 54 – 55 MB |
| **W3** | 4 Users | 9.1 – 10.3 ms | 11.6 – 13.6 RPS | 0 | 4.9 – 5.5 % | 54 – 55 MB |
| **W4** | 8 Users | 9.4 – 11.2 ms | 25.6 – 26.4 RPS | 0 | 3.9 – 11.1 % | 55.0 MB |
| **W5** | 16 Users | 10.4 – 11.7 ms | 50.4 – 50.8 RPS | 0 | 3.9 – 19.2 % | 54 – 56 MB |

* **Speaker:** Joel Biju (Presenting Locust execution, concurrency levels, and raw measurements)

---

### Slide 7: Benchmark Graphs & Performance Analysis (Checkpoint 5)
* **Four Embedded Matplotlib Plots:**
  1. **Concurrent Requests vs. Average Response Time:** Response time remains essentially flat (~8.0ms to 11.7ms), proving no saturation at 16 users.
  2. **Concurrent Requests vs. Throughput:** Throughput scales directly with concurrency from 3.1 RPS to 50.8 RPS.
  3. **Concurrent Requests vs. CPU Utilization:** CPU increases proportionally with load. Internship Service reached 19.2% and Application Service 16.3% due to keyword filtering and inter-service HTTP requests.
  4. **Concurrent Requests vs. Memory Utilization:** Flat memory line (~54–56 MB per service), demonstrating excellent Python memory management without leaks.
* **Speaker:** Akshay Bhat (Explaining graph trends, performance trade-offs, and service comparison)

---

### Slide 8: Key Insights, Conclusions & Final Deliverables
* **Key Technical Insights:**
  * Microservices ensure zero single-point-of-failure (isolated SQLite databases).
  * Docker internal bridge network and DNS provide high-speed, transparent communication.
  * FastAPI's asynchronous architecture handles increasing concurrent requests with sub-12ms response times.
* **Final Deliverables Checklist:**
  * [x] Source code of all 3 microservices with isolated databases
  * [x] Three Dockerfiles + `docker-compose.yml`
  * [x] Running Docker containers (`frontend-dashboard`, `student`, `internship`, `application`, `auth`)
  * [x] Interactive inter-service communication demonstration
  * [x] Locust workload test scripts & observation table
  * [x] 4 Performance benchmark graphs
  * [x] Live web dashboard at `http://localhost:8000`
* **Speaker:** Akshay Bhat (Concluding presentation and inviting evaluator questions)
