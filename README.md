# Internship Management System

A **microservices-based Internship Management System** built using **FastAPI, SQLite, Docker, and Docker Compose**.

The project is divided into four independent microservices. Each service has its own dedicated codebase, Docker image, and isolated SQLite database.

---

## Services Overview

| Service | Port | Database | Responsibilities |
| :--- | :---: | :---: | :--- |
| **Authentication Service** | `8001` | `auth.db` | User registration & authentication with Bcrypt password hashing |
| **Student Service** | `8002` | `students.db` | Student profile management (`name`, `email`, `department`, `year`) |
| **Internship Service** | `8003` | `internships.db` | Internship postings and keyword search (`title`, `company`, `location`) |
| **Application Service** | `8004` | `applications.db` | Application submissions, status tracking, and inter-service validation |

Each service runs independently in its own Docker container and persists data using Docker Named Volumes.

---

## Architecture

```
               Client / Locust Load Tester / Browser
                                 │
     ┌───────────────────┬───────┴───────────┬───────────────────┐
     ▼ :8001             ▼ :8002             ▼ :8003             ▼ :8004
┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ Authentication│   │   Student    │   │  Internship  │   │ Application  │
│   Service    │   │   Service    │   │   Service    │   │   Service    │
│  (FastAPI)   │   │  (FastAPI)   │   │  (FastAPI)   │   │  (FastAPI)   │
└──────┬───────┘   └──────┬───────┘   └──────┬───────┘   └──────┬───────┘
       │                  │                  │                  │
       │                  │  HTTP (Docker)   │  HTTP (Docker)   │
       │                  │◄─────────────────┼──────────────────┘
       ▼                  ▼                  ▼                  ▼
  [auth.db]         [students.db]     [internships.db]   [applications.db]
(auth_data vol)    (student_data vol) (internship_data)  (application_data)
```

---

## Project Structure

```text
CC_Internship_management/
├── authentication-service/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── student-service/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── internship-service/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── application-service/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── plots/
│   ├── 1_response_time.png
│   ├── 2_throughput.png
│   ├── 3_cpu_utilization.png
│   └── 4_memory_utilization.png
├── authentication_locustfile.py
├── student_locustfile.py
├── internship_locustfile.py
├── application_locustfile.py
├── generate_plots.py
├── docker-compose.yml
├── .gitignore
├── .env
└── README.md
```

---

## Technologies Used

* **Language & Framework:** Python 3.12+, FastAPI, Pydantic, SQLAlchemy, Requests
* **Database & Persistence:** SQLite, Docker Named Volumes
* **Containerization & Orchestration:** Docker, Docker Compose
* **Benchmarking & Load Testing:** Locust, Docker Stats
* **Plotting & Visualization:** Matplotlib, Pandas

---

## Prerequisites

Ensure the following tools are installed on your host system:
* Git
* Docker Desktop (started and running)
* Python 3.10+ (for running Locust and plot scripts locally)

Verify installations:
```bash
git --version
docker --version
docker compose version
python --version
```

---

## Checkpoint 1: Design and Develop Microservices

Each service is an independent FastAPI application with dedicated endpoints and isolated SQLite persistence.

### Interactive Swagger API Documentation
When services are running, visit:
* **Authentication Service:** [http://localhost:8001/docs](http://localhost:8001/docs)
* **Student Service:** [http://localhost:8002/docs](http://localhost:8002/docs)
* **Internship Service:** [http://localhost:8003/docs](http://localhost:8003/docs)
* **Application Service:** [http://localhost:8004/docs](http://localhost:8004/docs)

### Core Endpoints & Payloads

#### 1. Register User (`POST http://localhost:8001/register`)
```json
{
  "name": "Asha",
  "email": "asha@example.com",
  "password": "Password123"
}
```

#### 2. User Login (`POST http://localhost:8001/login`)
```json
{
  "email": "asha@example.com",
  "password": "Password123"
}
```

#### 3. Register Student (`POST http://localhost:8002/students`)
```json
{
  "name": "Asha",
  "email": "asha@example.com",
  "department": "CSE",
  "year": 3
}
```

#### 4. Post Internship (`POST http://localhost:8003/internships`)
```json
{
  "title": "Cloud Engineer Intern",
  "company": "Tech Solutions",
  "location": "Remote",
  "description": "FastAPI, Docker, Microservices"
}
```

#### 5. Submit Application (`POST http://localhost:8004/applications`)
```json
{
  "student_id": 1,
  "internship_id": 1
}
```

#### 6. Update Application Status (`PATCH http://localhost:8004/applications/1/status`)
```json
{
  "status": "accepted"
}
```
*(Valid status options: `pending`, `accepted`, `rejected`)*

---

## Checkpoint 2: Containerize and Deploy via Docker Compose

Each microservice contains its own `Dockerfile`. Docker Compose builds all images and runs the entire stack in one command.

### 1. Build & Start All Services
```bash
docker compose up --build -d
```

### 2. Verify Running Containers
```bash
docker ps
```
You should see 4 active containers: `auth-service`, `student-service`, `internship-service`, and `application-service`.

### 3. (Optional) Tag & Push to Docker Hub
If required by your college submission:
```bash
docker login
docker tag auth-service <your_username>/auth-service:latest
docker push <your_username>/auth-service:latest
```

---

## Checkpoint 3: Inter-Service Communication

Inter-service communication is achieved over Docker's internal bridge network.

```
 Client Request (POST /applications)
        │
        ▼
┌──────────────┐      Internal HTTP       ┌──────────────┐
│ Application  ├─────────────────────────►│   Student    │
│   Service    │  http://student:8000/    │   Service    │
│  (Port 8004) │                          └──────────────┘
│              │      Internal HTTP       ┌──────────────┐
│              ├─────────────────────────►│  Internship  │
│              │ http://internship:8000/  │   Service    │
└──────────────┘                          └──────────────┘
```

* **Service Discovery:** Services reach each other by container service name (`student:8000` and `internship:8000`) rather than brittle IP addresses.
* **Validation Flow:** Before creating an application in `applications.db`, `application-service` verifies:
  1. Does `student_id` exist in Student Service? If not, returns `404 Not Found`.
  2. Does `internship_id` exist in Internship Service? If not, returns `404 Not Found`.
  3. If both exist and no prior duplicate exists, application is recorded with status `pending`.

---

## Checkpoint 4: Load Testing & Performance Monitoring

Workload benchmarking is performed using **Locust** across 5 concurrency levels:
* **W1:** 1 user
* **W2:** 2 users
* **W3:** 4 users
* **W4:** 8 users
* **W5:** 16 users

### Running Locust
In a terminal, run the test for the desired service:

```bash
# Student Service
locust -f student_locustfile.py --host http://localhost:8002

# Internship Service
locust -f internship_locustfile.py --host http://localhost:8003

# Application Service
locust -f application_locustfile.py --host http://localhost:8004

# Authentication Service
locust -f authentication_locustfile.py --host http://localhost:8001
```

Open [http://localhost:8089](http://localhost:8089) in your browser. Configure the number of users and spawn rate, then start the test.

### Real-Time Resource Monitoring
In a separate terminal, monitor container CPU and RAM:
```bash
docker stats
```

### Observation Tables

#### Student Service
| Workload | Concurrent Users | Avg Response Time (ms) | Throughput (RPS) | Failures | CPU (%) | Memory (MB) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **W1** | 1 | 10.53 | 3.1 | 0 | 1.00% | 55.2 MB |
| **W2** | 2 | 10.45 | 5.8 | 0 | 2.60% | 55.5 MB |
| **W3** | 4 | 10.27 | 12.4 | 0 | 5.14% | 55.1 MB |
| **W4** | 8 | 10.19 | 25.6 | 0 | 3.93% | 55.1 MB |
| **W5** | 16 | 10.40 | 50.6 | 0 | 3.93% | 55.1 MB |

#### Internship Service
| Workload | Concurrent Users | Avg Response Time (ms) | Throughput (RPS) | Failures | CPU (%) | Memory (MB) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **W1** | 1 | 9.25 | 3.1 | 0 | 1.70% | 53.9 MB |
| **W2** | 2 | 8.96 | 6.4 | 0 | 2.55% | 54.3 MB |
| **W3** | 4 | 9.40 | 13.6 | 0 | 5.54% | 54.5 MB |
| **W4** | 8 | 11.23 | 26.4 | 0 | 10.87% | 55.5 MB |
| **W5** | 16 | 11.74 | 50.8 | 0 | 19.20% | 56.1 MB |

#### Application Service
| Workload | Concurrent Users | Avg Response Time (ms) | Throughput (RPS) | Failures | CPU (%) | Memory (MB) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **W1** | 1 | 7.98 | 3.0 | 0 | 2.10% | 53.2 MB |
| **W2** | 2 | 8.95 | 6.9 | 0 | 2.98% | 53.9 MB |
| **W3** | 4 | 9.15 | 11.6 | 0 | 4.94% | 55.0 MB |
| **W4** | 8 | 9.41 | 25.7 | 0 | 11.11% | 55.0 MB |
| **W5** | 16 | 10.51 | 50.4 | 0 | 16.31% | 54.2 MB |

---

## Checkpoint 5: Plotting, Data Persistence & Insights

### Generate Benchmark Graphs
To generate or refresh graphs from the observation data:
```bash
python generate_plots.py
```
Output graphs are placed in the `plots/` folder:
1. `1_response_time.png` (Concurrency vs Average Response Time)
2. `2_throughput.png` (Concurrency vs Throughput)
3. `3_cpu_utilization.png` (Concurrency vs CPU Utilization)
4. `4_memory_utilization.png` (Concurrency vs Memory Utilization)

### Data Persistence via Named Volumes
Databases survive container restarts because they are mounted to Docker named volumes:
* `auth_data` -> `/data/auth.db`
* `student_data` -> `/data/students.db`
* `internship_data` -> `/data/internships.db`
* `application_data` -> `/data/applications.db`

### Useful Docker Commands
```bash
# View aggregated container logs
docker compose logs -f

# View logs for a single service
docker compose logs application

# Stop containers without losing database data
docker compose down

# Stop and delete databases (fresh start)
docker compose down -v
```

---

## Step-by-Step Guide to Push to GitHub

1. Initialize git and stage all files:
   ```bash
   git init
   git add .
   git commit -m "Complete microservices internship management system"
   ```
2. Create a new repository on GitHub (e.g. `CC-Internship-Management`).
3. Link your remote repository and push:
   ```bash
   git branch -M main
   git remote add origin https://github.com/<your-username>/<your-repo-name>.git
   git push -u origin main
   ```
