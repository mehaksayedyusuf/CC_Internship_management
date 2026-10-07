import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Color Palette
COLOR_BG = RGBColor(247, 249, 252)       # #F7F9FC
COLOR_PRIMARY = RGBColor(17, 24, 39)     # #111827
COLOR_SECONDARY = RGBColor(100, 116, 139)# #64748B
COLOR_BLUE = RGBColor(37, 99, 235)       # #2563EB
COLOR_CARD_BG = RGBColor(255, 255, 255)  # #FFFFFF
COLOR_BORDER = RGBColor(226, 232, 240)   # #E2E8F0
COLOR_SUCCESS = RGBColor(22, 163, 74)    # #16A34A

def apply_background(slide):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = COLOR_BG

def add_header(slide, title_text, category_text="CLOUD COMPUTING LAB EVALUATION"):
    # Category tag
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.4))
    tf_cat = cat_box.text_frame
    tf_cat.word_wrap = True
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.name = "Arial"
    p_cat.font.size = Pt(11)
    p_cat.font.bold = True
    p_cat.font.color.rgb = COLOR_BLUE

    # Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.85), Inches(11.7), Inches(0.8))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.name = "Arial"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY

blank_layout = prs.slide_layouts[6]

# ==============================================================================
# SLIDE 1: Title & Team Details
# ==============================================================================
s1 = prs.slides.add_slide(blank_layout)
apply_background(s1)

# Main Title Card
card1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(3.2))
card1.fill.solid()
card1.fill.fore_color.rgb = COLOR_CARD_BG
card1.line.color.rgb = COLOR_BORDER
card1.line.width = Pt(1.5)

tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.1), Inches(10.9), Inches(2.6))
tf1 = tb1.text_frame
tf1.word_wrap = True

p = tf1.paragraphs[0]
p.text = "CLOUD COMPUTING LABORATORY (EXPERIMENT EVALUATION)"
p.font.name = "Arial"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = COLOR_BLUE
p.space_after = Pt(10)

p2 = tf1.add_paragraph()
p2.text = "Build, Deploy & Analyze a Containerized Microservice Application Under Varying Workloads"
p2.font.name = "Arial"
p2.font.size = Pt(24)
p2.font.bold = True
p2.font.color.rgb = COLOR_PRIMARY
p2.space_after = Pt(8)

p3 = tf1.add_paragraph()
p3.text = "Domain: Internship Management System | FastAPI • Docker Compose • Locust • Resource Profiling"
p3.font.name = "Arial"
p3.font.size = Pt(14)
p3.font.color.rgb = COLOR_SECONDARY

# Team Members Card
card_team = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.3), Inches(11.733), Inches(2.4))
card_team.fill.solid()
card_team.fill.fore_color.rgb = COLOR_CARD_BG
card_team.line.color.rgb = COLOR_BORDER
card_team.line.width = Pt(1.5)

tb_team = s1.shapes.add_textbox(Inches(1.2), Inches(4.5), Inches(10.9), Inches(2.0))
tf_team = tb_team.text_frame
p_team_title = tf_team.paragraphs[0]
p_team_title.text = "PROJECT TEAM MEMBERS"
p_team_title.font.name = "Arial"
p_team_title.font.size = Pt(12)
p_team_title.font.bold = True
p_team_title.font.color.rgb = COLOR_BLUE
p_team_title.space_after = Pt(12)

# 4 team members in grid
members = [
    ("Vageesh Mathad", "01FE24BCI008"),
    ("Mehak Sayed Yusuf", "01FE24BCI012"),
    ("Joel Biju", "01FE24BCI021"),
    ("Akshay Bhat", "01FE24BCI024")
]

for i, (name, usn) in enumerate(members):
    left = Inches(1.2 + i * 2.7)
    m_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(5.0), Inches(2.5), Inches(1.3))
    m_box.fill.solid()
    m_box.fill.fore_color.rgb = RGBColor(239, 246, 255)
    m_box.line.color.rgb = RGBColor(191, 219, 254)
    
    tf_m = m_box.text_frame
    tf_m.word_wrap = True
    pm1 = tf_m.paragraphs[0]
    pm1.text = name
    pm1.font.name = "Arial"
    pm1.font.size = Pt(14)
    pm1.font.bold = True
    pm1.font.color.rgb = COLOR_PRIMARY
    pm1.alignment = PP_ALIGN.CENTER
    
    pm2 = tf_m.add_paragraph()
    pm2.text = f"USN: {usn}"
    pm2.font.name = "Arial"
    pm2.font.size = Pt(12)
    pm2.font.color.rgb = COLOR_BLUE
    pm2.alignment = PP_ALIGN.CENTER

# ==============================================================================
# SLIDE 2: Objectives & Architecture Overview
# ==============================================================================
s2 = prs.slides.add_slide(blank_layout)
apply_background(s2)
add_header(s2, "Aim, Domain & Experiment Objectives", "CHECKPOINT 1 — OVERVIEW")

# Left Column: Objectives Card
left_card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
left_card.fill.solid()
left_card.fill.fore_color.rgb = COLOR_CARD_BG
left_card.line.color.rgb = COLOR_BORDER

tb_l = s2.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.0), Inches(4.5))
tf_l = tb_l.text_frame
tf_l.word_wrap = True

p = tf_l.paragraphs[0]
p.text = "Experiment Aim & Domain"
p.font.name = "Arial"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = COLOR_PRIMARY
p.space_after = Pt(12)

points_l = [
    ("Domain:", "Internship Management System for academic placements."),
    ("Core Goal:", "Develop exactly 3 independent microservices, containerize with Docker, establish inter-service communication, generate varying workloads, and profile performance."),
    ("Microservice Principle:", "Loose coupling, high cohesion, independent database per service, and stateless REST endpoints."),
    ("Evaluator Requirement:", "Fulfill all 5 mandatory checkpoints with real measured metrics.")
]
for title, desc in points_l:
    p = tf_l.add_paragraph()
    p.text = f"• {title} "
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_BLUE
    
    run = p.add_run()
    run.text = desc
    run.font.bold = False
    run.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(8)

# Right Column: 3 Services Overview Card
right_card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
right_card.fill.solid()
right_card.fill.fore_color.rgb = COLOR_CARD_BG
right_card.line.color.rgb = COLOR_BORDER

tb_r = s2.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.1), Inches(4.5))
tf_r = tb_r.text_frame
tf_r.word_wrap = True

p = tf_r.paragraphs[0]
p.text = "Three Independent Microservices"
p.font.name = "Arial"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = COLOR_PRIMARY
p.space_after = Pt(12)

services_info = [
    ("1. Student Service (:8002)", "students.db", "Maintains student profiles (name, email, department, year). Validates academic eligibility."),
    ("2. Internship Service (:8003)", "internships.db", "Stores internship job postings, requirements, stipends, and keyword search filters."),
    ("3. Application Service (:8004)", "applications.db", "Orchestrates application workflow, coordinates inter-service validation, and tracks review status.")
]
for s_title, db_name, s_desc in services_info:
    p = tf_r.add_paragraph()
    p.text = s_title
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = COLOR_PRIMARY
    
    p_sub = tf_r.add_paragraph()
    p_sub.text = f"Database: {db_name} | {s_desc}"
    p_sub.font.size = Pt(12)
    p_sub.font.color.rgb = COLOR_SECONDARY
    p_sub.space_after = Pt(10)

# ==============================================================================
# SLIDE 3: Architecture & REST API Design (Checkpoint 1)
# ==============================================================================
s3 = prs.slides.add_slide(blank_layout)
apply_background(s3)
add_header(s3, "Architecture & REST API Implementation", "CHECKPOINT 1 — DETAILED DESIGN")

# Architectural Flow Card
arch_card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(11.733), Inches(1.8))
arch_card.fill.solid()
arch_card.fill.fore_color.rgb = COLOR_CARD_BG
arch_card.line.color.rgb = COLOR_BORDER

tb_arch = s3.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(11.1), Inches(1.5))
tf_arch = tb_arch.text_frame
tf_arch.word_wrap = True
p = tf_arch.paragraphs[0]
p.text = "MINIMUM ARCHITECTURE: Client → Service 1 → Service 2 / Service 3"
p.font.name = "Arial"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = COLOR_BLUE
p.space_after = Pt(4)

p_flow = tf_arch.add_paragraph()
p_flow.text = "Client (Web Dashboard / Locust / cURL)  ──►  Application Service (Port 8004)\n                                                                     ├──► Student Service (Port 8002) [Validates Student ID]\n                                                                     └──► Internship Service (Port 8003) [Validates Internship ID]"
p_flow.font.name = "Courier New"
p_flow.font.size = Pt(11)
p_flow.font.color.rgb = COLOR_PRIMARY

# 3 API Endpoint Cards
apis = [
    ("Student Service (:8002)", [
        "POST /students (Create)",
        "GET /students (List all)",
        "GET /students/{id} (Fetch details)",
        "PUT /students/{id} (Update)",
        "DELETE /students/{id} (Remove)"
    ]),
    ("Internship Service (:8003)", [
        "POST /internships (Create posting)",
        "GET /internships (Search & filter)",
        "GET /internships/{id} (Fetch details)",
        "PUT /internships/{id} (Update details)",
        "DELETE /internships/{id} (Delete)"
    ]),
    ("Application Service (:8004)", [
        "POST /applications (Submit application)",
        "GET /applications (List applications)",
        "PATCH /applications/{id}/status (Accept/Reject)",
        "DELETE /applications/{id} (Withdraw)",
        "Inter-Service Validation on Submit"
    ])
]

for i, (title, endpoints) in enumerate(apis):
    left = Inches(0.8 + i * 4.0)
    card_api = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(3.8), Inches(3.733), Inches(3.0))
    card_api.fill.solid()
    card_api.fill.fore_color.rgb = COLOR_CARD_BG
    card_api.line.color.rgb = COLOR_BORDER
    
    tb_api = s3.shapes.add_textbox(left + Inches(0.2), Inches(4.0), Inches(3.3), Inches(2.6))
    tf_api = tb_api.text_frame
    tf_api.word_wrap = True
    p = tf_api.paragraphs[0]
    p.text = title
    p.font.name = "Arial"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(8)
    
    for ep in endpoints:
        p_ep = tf_api.add_paragraph()
        p_ep.text = f"• {ep}"
        p_ep.font.size = Pt(11)
        p_ep.font.color.rgb = COLOR_SECONDARY
        p_ep.space_after = Pt(4)

# ==============================================================================
# SLIDE 4: Containerization & Docker Compose Deployment (Checkpoint 2)
# ==============================================================================
s4 = prs.slides.add_slide(blank_layout)
apply_background(s4)
add_header(s4, "Docker Containerization & Multi-Container Deployment", "CHECKPOINT 2 — DOCKER DEPLOYMENT")

# Left Column: Dockerfile specs
d_card_l = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
d_card_l.fill.solid()
d_card_l.fill.fore_color.rgb = COLOR_CARD_BG
d_card_l.line.color.rgb = COLOR_BORDER

tb_dl = s4.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.0), Inches(4.5))
tf_dl = tb_dl.text_frame
tf_dl.word_wrap = True
p = tf_dl.paragraphs[0]
p.text = "Microservice Containerization"
p.font.name = "Arial"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = COLOR_PRIMARY
p.space_after = Pt(12)

d_points = [
    ("Base Image:", "python:3.12-slim (minimal footprint ~280MB)."),
    ("Isolated Dependencies:", "Each service packages its own requirements.txt (FastAPI, uvicorn, sqlalchemy, requests)."),
    ("Execution:", "Uvicorn ASGI server bound to 0.0.0.0:8000 inside each container."),
    ("Build Process:", "Three distinct images: student-service:latest, internship-service:latest, application-service:latest."),
    ("Port Isolation:", "Internal port 8000 mapped to host ports 8002, 8003, 8004.")
]
for k, v in d_points:
    p = tf_dl.add_paragraph()
    p.text = f"• {k} "
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_BLUE
    run = p.add_run()
    run.text = v
    run.font.bold = False
    run.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(6)

# Right Column: Docker Compose Specs
d_card_r = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
d_card_r.fill.solid()
d_card_r.fill.fore_color.rgb = COLOR_CARD_BG
d_card_r.line.color.rgb = COLOR_BORDER

tb_dr = s4.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.1), Inches(4.5))
tf_dr = tb_dr.text_frame
tf_dr.word_wrap = True
p = tf_dr.paragraphs[0]
p.text = "Docker Compose Orchestration"
p.font.name = "Arial"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = COLOR_PRIMARY
p.space_after = Pt(12)

dc_points = [
    ("Single Command Deploy:", "docker compose up --build -d starts all microservices + Nginx frontend."),
    ("Named Volumes Persistence:", "student_data, internship_data, application_data preserve SQLite data across container teardowns."),
    ("Service Dependency:", "application depends_on student and internship to ensure correct startup order."),
    ("Automatic Network:", "Creates default bridge network enabling container DNS resolution."),
    ("Zero Downtime Scaling:", "Services run as isolated processes without port conflicts.")
]
for k, v in dc_points:
    p = tf_dr.add_paragraph()
    p.text = f"• {k} "
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_BLUE
    run = p.add_run()
    run.text = v
    run.font.bold = False
    run.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(6)

# ==============================================================================
# SLIDE 5: Inter-Service Communication Flow (Checkpoint 3)
# ==============================================================================
s5 = prs.slides.add_slide(blank_layout)
apply_background(s5)
add_header(s5, "Establishing & Demonstrating Inter-Service Communication", "CHECKPOINT 3 — SERVICE-TO-SERVICE")

# Main Communication Details
c_card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(11.733), Inches(5.0))
c_card.fill.solid()
c_card.fill.fore_color.rgb = COLOR_CARD_BG
c_card.line.color.rgb = COLOR_BORDER

tb_c = s5.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(11.1), Inches(4.5))
tf_c = tb_c.text_frame
tf_c.word_wrap = True

p = tf_c.paragraphs[0]
p.text = "How Microservices Communicate (Docker Network Service Discovery)"
p.font.name = "Arial"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = COLOR_PRIMARY
p.space_after = Pt(8)

p_dns = tf_c.add_paragraph()
p_dns.text = "Instead of hardcoded host IP addresses, Application Service utilizes Docker's built-in DNS to reach target services by service name:\n• Student URL: http://student:8000/students/{id}\n• Internship URL: http://internship:8000/internships/{id}"
p_dns.font.size = Pt(13)
p_dns.font.color.rgb = COLOR_SECONDARY
p_dns.space_after = Pt(14)

p_flow_title = tf_c.add_paragraph()
p_flow_title.text = "Validation & End-to-End Request Demonstration Flow:"
p_flow_title.font.name = "Arial"
p_flow_title.font.size = Pt(15)
p_flow_title.font.bold = True
p_flow_title.font.color.rgb = COLOR_PRIMARY
p_flow_title.space_after = Pt(6)

steps = [
    ("Step 1: Application Submission", "Client issues POST /applications with student_id and internship_id."),
    ("Step 2: Student Existence Check", "Application Service sends HTTP GET to http://student:8000/students/{student_id}."),
    ("Step 3: Internship Existence Check", "Application Service sends HTTP GET to http://internship:8000/internships/{internship_id}."),
    ("Step 4: Error Handling & Failure Case", "If student does NOT exist, Student Service responds 404. Application Service immediately returns HTTP 404: 'Student 99999 not found' without saving orphan data."),
    ("Step 5: Successful State Transition", "If both entities exist, Application Service records the row in applications.db and returns HTTP 201 Created.")
]
for title, desc in steps:
    p = tf_c.add_paragraph()
    p.text = f"• {title}: "
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_BLUE
    run = p.add_run()
    run.text = desc
    run.font.bold = False
    run.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(4)

# ==============================================================================
# SLIDE 6: Workload Generation & Observation Table (Checkpoint 4)
# ==============================================================================
s6 = prs.slides.add_slide(blank_layout)
apply_background(s6)
add_header(s6, "Varying Workload Testing & Observation Table (W1 - W5)", "CHECKPOINT 4 — LOAD TESTING")

# Explanation note
tb_w = s6.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.733), Inches(0.6))
tf_w = tb_w.text_frame
p = tf_w.paragraphs[0]
p.text = "Load Testing Tool: Locust | Metrics Monitored: Response Time, Throughput (RPS), Failures, CPU %, Memory (MB)"
p.font.size = Pt(13)
p.font.color.rgb = COLOR_SECONDARY

# Table shape
rows, cols = 6, 7
left = Inches(0.8)
top = Inches(2.2)
width = Inches(11.733)
height = Inches(4.6)

table_shape = s6.shapes.add_table(rows, cols, left, top, width, height)
table = table_shape.table

# Column widths
table.columns[0].width = Inches(1.3) # Workload
table.columns[1].width = Inches(1.8) # Users
table.columns[2].width = Inches(2.2) # Resp Time
table.columns[3].width = Inches(1.8) # Throughput
table.columns[4].width = Inches(1.3) # Failures
table.columns[5].width = Inches(1.6) # CPU
table.columns[6].width = Inches(1.733) # Memory

headers = ["Workload", "Concurrency", "Avg Response Time", "Throughput (RPS)", "Failures", "CPU Utilization", "Memory Usage"]
for j, h in enumerate(headers):
    cell = table.cell(0, j)
    cell.fill.solid()
    cell.fill.fore_color.rgb = COLOR_BLUE
    p = cell.text_frame.paragraphs[0]
    p.text = h
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.alignment = PP_ALIGN.CENTER

table_data = [
    ["W1", "1 User", "8.0 – 10.5 ms", "3.1 RPS", "0", "1.0 – 2.1 %", "53 – 55 MB"],
    ["W2", "2 Users", "9.0 – 10.5 ms", "5.8 – 6.9 RPS", "0", "2.5 – 3.0 %", "54 – 55 MB"],
    ["W3", "4 Users", "9.1 – 10.3 ms", "11.6 – 13.6 RPS", "0", "4.9 – 5.5 %", "54 – 55 MB"],
    ["W4", "8 Users", "9.4 – 11.2 ms", "25.6 – 26.4 RPS", "0", "3.9 – 11.1 %", "55.0 MB"],
    ["W5", "16 Users", "10.4 – 11.7 ms", "50.4 – 50.8 RPS", "0", "3.9 – 19.2 %", "54 – 56 MB"]
]

for i, row in enumerate(table_data):
    for j, val in enumerate(row):
        cell = table.cell(i + 1, j)
        cell.fill.solid()
        if i % 2 == 0:
            cell.fill.fore_color.rgb = RGBColor(255, 255, 255)
        else:
            cell.fill.fore_color.rgb = RGBColor(241, 245, 249)
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.name = "Arial"
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_PRIMARY
        p.alignment = PP_ALIGN.CENTER

# ==============================================================================
# SLIDE 7: Performance Graphs & Results Analysis (Checkpoint 5)
# ==============================================================================
s7 = prs.slides.add_slide(blank_layout)
apply_background(s7)
add_header(s7, "Benchmark Graphs & Performance Analysis", "CHECKPOINT 5 — VISUAL RESULTS")

# Insert 4 generated plot images in 2x2 grid
plot_files = [
    ("plots/1_response_time.png", Inches(0.8), Inches(1.7), Inches(5.6), Inches(2.5)),
    ("plots/2_throughput.png", Inches(6.8), Inches(1.7), Inches(5.6), Inches(2.5)),
    ("plots/3_cpu_utilization.png", Inches(0.8), Inches(4.5), Inches(5.6), Inches(2.5)),
    ("plots/4_memory_utilization.png", Inches(6.8), Inches(4.5), Inches(5.6), Inches(2.5))
]

for p_path, left, top, width, height in plot_files:
    if os.path.exists(p_path):
        s7.shapes.add_picture(p_path, left, top, width, height)

# ==============================================================================
# SLIDE 8: Insights, Conclusions & Viva Deliverables
# ==============================================================================
s8 = prs.slides.add_slide(blank_layout)
apply_background(s8)
add_header(s8, "Key Insights, Viva Conclusions & Final Deliverables", "EXPERIMENT SUMMARY")

# Left Column: Insights
card_i = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
card_i.fill.solid()
card_i.fill.fore_color.rgb = COLOR_CARD_BG
card_i.line.color.rgb = COLOR_BORDER

tb_i = s8.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.0), Inches(4.5))
tf_i = tb_i.text_frame
tf_i.word_wrap = True
p = tf_i.paragraphs[0]
p.text = "Workload & Resource Analysis"
p.font.name = "Arial"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = COLOR_PRIMARY
p.space_after = Pt(12)

insights = [
    ("Throughput Scaling:", "Linear scaling from 3.1 RPS (1 user) to 50.8 RPS (16 users). No bottleneck reached."),
    ("Response Time Stability:", "Latency remained tightly bound between 8.0ms and 11.7ms. Zero request failures recorded."),
    ("Resource Utilization:", "Internship and Application services consume slightly more CPU (~19% and ~16%) due to filtering and inter-service HTTP calls."),
    ("Memory Footprint:", "Memory remained constant around 54–56 MB across all containers thanks to Python connection pooling and lightweight footprint.")
]
for k, v in insights:
    p = tf_i.add_paragraph()
    p.text = f"• {k} "
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_BLUE
    run = p.add_run()
    run.text = v
    run.font.bold = False
    run.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(6)

# Right Column: Deliverables
card_del = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
card_del.fill.solid()
card_del.fill.fore_color.rgb = COLOR_CARD_BG
card_del.line.color.rgb = COLOR_BORDER

tb_del = s8.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.1), Inches(4.5))
tf_del = tb_del.text_frame
tf_del.word_wrap = True
p = tf_del.paragraphs[0]
p.text = "Student Deliverables Checklist"
p.font.name = "Arial"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = COLOR_PRIMARY
p.space_after = Pt(12)

deliverables = [
    ("3 Microservice Codebases:", "student, internship, application with independent models."),
    ("Dockerfiles & Compose:", "Individual Dockerfiles and working docker-compose.yml."),
    ("Active Containers:", "All containers deployed and verified on ports 8000–8004."),
    ("Inter-Service Demo:", "Verified end-to-end communication and 404 validation."),
    ("Observation Table & Graphs:", "Complete W1–W5 benchmark data and 4 generated plots."),
    ("Live Dashboard:", "Simple, professional UI for evaluator demonstration.")
]
for k, v in deliverables:
    p = tf_del.add_paragraph()
    p.text = f"✔ {k} "
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_SUCCESS
    run = p.add_run()
    run.text = v
    run.font.bold = False
    run.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(6)

output_filename = "Internship_Management_Microservices.pptx"
prs.save(output_filename)
print(f"PowerPoint successfully created: {output_filename}")
