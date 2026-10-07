# Cloud Computing Laboratory Evaluation Presentation
## Build, Deploy & Analyze a Containerized Microservice Application Under Varying Workloads

**Presentation Files:**
- **Updated Presentation (12 Slides):** [Internship_Management_Presentation.pptx](file:///a:/CC_Internship_management/Internship_Management_Presentation.pptx)
- **Primary Presentation:** [Internship_Management_Microservices.pptx](file:///a:/CC_Internship_management/Internship_Management_Microservices.pptx)

**Domain:** Internship Management System  
**Team Members:**
- **Vageesh Mathad** (USN: `01FE24BCI008`)
- **Mehak Sayed Yusuf** (USN: `01FE24BCI012`)
- **Joel Biju** (USN: `01FE24BCI021`)
- **Akshay Bhat** (USN: `01FE24BCI024`)

---

### Slide 1: Title
* **Title:** INTERNSHIP MANAGEMENT SYSTEM
* **Subtitle:** Build, Deploy & Analyze a Containerized Microservice Application Under Varying Workloads
* **Laboratory:** Cloud Computing Laboratory
* **Tech Stack:** FastAPI | Docker Compose | Locust | Resource Profiling
* **Team Members:**
  1. Vageesh Mathad (`01FE24BCI008`)
  2. Mehak Sayed Yusuf (`01FE24BCI012`)
  3. Joel Biju (`01FE24BCI021`)
  4. Akshay Bhat (`01FE24BCI024`)
* **Speaker:** Vageesh Mathad

---

### Slide 2: Aim & Objectives
* **Aim:**
  To develop, containerize and deploy an Internship Management System using independent microservices, establish inter-service communication, and evaluate performance under varying workloads.
* **Objectives:**
  - Develop three independent core microservices.
  - Implement REST APIs for student, internship and application management.
  - Containerize the services using Docker.
  - Establish inter-service communication through Docker Compose networking.
  - Test the Application Service with 1, 2, 4, 8 and 16 concurrent users.
  - Measure response time, throughput, failed requests, CPU and memory usage.
* **Speaker:** Vageesh Mathad

---

### Slide 3: Core Microservices
* **Student Service:**
  * Port: `8002` | Database: `students.db`
  * Manages: Student profiles, Student CRUD operations, Student information validation
* **Internship Service:**
  * Port: `8003` | Database: `internships.db`
  * Manages: Internship postings, Internship details, Search/filter operations
* **Application Service:**
  * Port: `8004` | Database: `applications.db`
  * Manages: Internship applications, Application status, Inter-service validation
* **Supporting Service:**
  * Authentication Service — Port `8001` (`auth.db` | User registration & Bcrypt login)
* **Speaker:** Mehak Sayed Yusuf

---

### Slide 4: System Architecture
* **Architecture Diagram:**
```text
                          CLIENT (Web Dashboard / Locust)
                                         |
                                    REST Requests
                                         |
          ┌──────────────────────────────┴──────────────────────────────┐
          │                     Docker Compose Network                  │
          │                                                             │
          │                   Application Service (:8000)               │
          │                            /      \                         │
          │                           /        \                        │
          │                          ↓          ↓                       │
          │                    Student        Internship                │
          │                    Service        Service                   │
          │                    (:8000)        (:8000)                   │
          │                                                             │
          │                 Authentication Service (:8000)              │
          └─────────────────────────────────────────────────────────────┘
```
* **Host Ports:**
  * Auth: `8001` | Student: `8002` | Internship: `8003` | Application: `8004`
  * Internal container port: `8000`
* **Key Architecture Rule:** All services communicate through the Docker Compose network via internal service names.
* **Speaker:** Mehak Sayed Yusuf

---

### Slide 5: REST API Design

| Service | Method | Endpoint | Purpose |
| :--- | :--- | :--- | :--- |
| **Student** | `POST` | `/students` | Create student |
| **Student** | `GET` | `/students` | List students |
| **Student** | `GET` | `/students/{id}` | Get student |
| **Student** | `PUT` | `/students/{id}` | Update student |
| **Student** | `DELETE` | `/students/{id}` | Delete student |
| **Internship** | `POST` | `/internships` | Create internship |
| **Internship** | `GET` | `/internships` | Search/list |
| **Internship** | `GET` | `/internships/{id}` | Get internship |
| **Internship** | `PUT` | `/internships/{id}` | Update internship |
| **Internship** | `DELETE` | `/internships/{id}` | Delete internship |
| **Application** | `POST` | `/applications` | Submit application |
| **Application** | `GET` | `/applications` | List applications |
| **Application** | `PATCH` | `/applications/{id}/status` | Update status |
| **Application** | `DELETE` | `/applications/{id}` | Withdraw |

* **Speaker:** Mehak Sayed Yusuf

---

### Slide 6: Docker Containerization & Deployment
* **Containerization (Left Column):**
  - Individual Dockerfile for each service
  - `python:3.12-slim` base image
  - FastAPI + Uvicorn ASGI runtime
  - Uvicorn listens on container port `8000`
  - Independent service dependencies
* **Docker Compose (Right Column):**
```text
   docker compose up --build -d
                ↓
          Docker Compose
                ↓
     ┌──────────┼──────────┐
     ↓          ↓          ↓
   Student   Internship  Application
   :8000       :8000       :8000
```
* **Persistence (Bottom Card):**
  - `student_data` | `internship_data` | `application_data`
  - Docker named volumes guarantee SQLite data persists safely across container teardowns and restarts.
* **Speaker:** Joel Biju

---

### Slide 7: Inter-Service Communication
* **Synchronous Validation Protocol:**
```text
POST /applications
        |
        ↓
Application Service
        |
        ├──→ GET http://student:8000/students/{id}
        |             ↓
        |       Student Service
        |
        └──→ GET http://internship:8000/internships/{id}
                      ↓
                Internship Service
                      |
                      ↓
              Application Created
                (HTTP 200 OK)
```
* **Why `student:8000` and `internship:8000`?**
  Docker Compose provides internal DNS, so services communicate using service names instead of container IP addresses.
* **Failure Handling:**
```text
Invalid Student
      ↓
Student Service → 404
      ↓
Application NOT created
```
* **Status Code:** Successful application creation returns **HTTP 200 OK**.
* **Speaker:** Joel Biju

---

### Slide 8: Workload Testing Methodology
* **Configuration:**
  - Tool: **Locust**
  - Target: **Application Service**
  - Host: `localhost:8004`
  - Resource Monitor: `docker stats` was used to monitor container resource utilization during workload testing.
* **Workloads Progression:**
  - **W1:** 1 user
  - **W2:** 2 users
  - **W3:** 4 users
  - **W4:** 8 users
  - **W5:** 16 users
* **Metrics Recorded:**
  - Average Response Time
  - Throughput (RPS)
  - Failed Requests
  - CPU Utilization
  - Memory Usage
* **Speaker:** Joel Biju

---

### Slide 9: Performance Results

| Workload | Users | Avg Response Time | Throughput | Failures |
| :---: | :---: | :---: | :---: | :---: |
| **W1** | **1** | **10.28 ms** | **3.2 RPS** | **0** |
| **W2** | 2 | — | — | — |
| **W3** | 4 | — | — | — |
| **W4** | 8 | — | — | — |
| **W5** | 16 | — | — | — |

* **Note:** W1 represents actual measured baseline values. Remaining workload rows are populated as evaluations proceed.
* **Speaker:** Akshay Bhat

---

### Slide 10: Resource Utilization

| Service | CPU | Memory |
| :--- | :---: | :---: |
| **Authentication** | 0.26% | 53.77 MiB |
| **Student** | 0.31% | 55.21 MiB |
| **Internship** | 0.28% | 54.64 MiB |
| **Application** | 0.32% | 59.06 MiB |

* **Note:** Measured via `docker stats` under baseline workload W1 (1 concurrent user). Remaining workload tests W2–W5 follow the same profiling methodology.
* **Speaker:** Akshay Bhat

---

### Slide 11: Performance Analysis
* **4 Benchmark Visual Graphs:**
  1. Graph 1: Concurrent Users vs Average Response Time
  2. Graph 2: Concurrent Users vs Throughput
  3. Graph 3: Concurrent Users vs CPU Utilization
  4. Graph 4: Concurrent Users vs Memory Usage
* **Observed Behaviour:**
  Response time, throughput and resource utilization were compared across increasing concurrent workloads.
* **Speaker:** Akshay Bhat

---

### Slide 12: Conclusion & Demonstration
* **Project Demonstrates:**
  - Independent microservices
  - RESTful APIs
  - Docker containerization
  - Docker Compose orchestration
  - Docker-network service discovery
  - Inter-service validation
  - Locust workload testing
  - CPU and memory monitoring
* **Live Demo Flow:**
```text
   Docker Compose
         ↓
   Verify Containers
         ↓
   Verify Docker Network
         ↓
   Create Student
         ↓
   Create Internship
         ↓
   Submit Application
         ↓
   Show Inter-Service Validation
         ↓
   Run Locust
         ↓
   Show Results
```
* **Speaker:** Akshay Bhat
