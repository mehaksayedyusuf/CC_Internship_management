import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Color Palette (Refined Light Professional Academic Palette)
COLOR_BG = RGBColor(248, 250, 252)          # #F8FAFC
COLOR_PRIMARY = RGBColor(15, 23, 42)        # #0F172A
COLOR_SECONDARY = RGBColor(71, 85, 105)     # #475569
COLOR_MUTED = RGBColor(100, 116, 139)       # #64748B
COLOR_BLUE = RGBColor(37, 99, 235)          # #2563EB
COLOR_BLUE_BG = RGBColor(239, 246, 255)     # #EFF6FF
COLOR_BLUE_BORDER = RGBColor(191, 219, 254) # #BFDBFE
COLOR_CARD_BG = RGBColor(255, 255, 255)     # #FFFFFF
COLOR_BORDER = RGBColor(226, 232, 240)      # #E2E8F0
COLOR_SUCCESS = RGBColor(22, 163, 74)       # #16A34A
COLOR_ROW_ALT = RGBColor(248, 250, 252)     # #F8FAFC

def apply_background(slide):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = COLOR_BG

def add_header(slide, title_text, category_text="CLOUD COMPUTING LABORATORY"):
    # Category tag
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.7), Inches(0.35))
    tf_cat = cat_box.text_frame
    tf_cat.word_wrap = True
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.name = "Arial"
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = COLOR_BLUE

    # Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.6))
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
# SLIDE 1: TITLE — INTERNSHIP MANAGEMENT SYSTEM
# ==============================================================================
s1 = prs.slides.add_slide(blank_layout)
apply_background(s1)

# Main Title Container
t_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(3.4))
t_card.fill.solid()
t_card.fill.fore_color.rgb = COLOR_CARD_BG
t_card.line.color.rgb = COLOR_BORDER
t_card.line.width = Pt(1.5)

tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.1), Inches(10.9), Inches(2.8))
tf1 = tb1.text_frame
tf1.word_wrap = True

p1 = tf1.paragraphs[0]
p1.text = "INTERNSHIP MANAGEMENT SYSTEM"
p1.font.name = "Arial"
p1.font.size = Pt(26)
p1.font.bold = True
p1.font.color.rgb = COLOR_PRIMARY
p1.space_after = Pt(8)

p2 = tf1.add_paragraph()
p2.text = "Build, Deploy & Analyze a Containerized Microservice Application Under Varying Workloads"
p2.font.name = "Arial"
p2.font.size = Pt(16)
p2.font.bold = True
p2.font.color.rgb = COLOR_BLUE
p2.space_after = Pt(14)

p3 = tf1.add_paragraph()
p3.text = "Cloud Computing Laboratory"
p3.font.name = "Arial"
p3.font.size = Pt(13)
p3.font.bold = True
p3.font.color.rgb = COLOR_SECONDARY
p3.space_after = Pt(4)

p4 = tf1.add_paragraph()
p4.text = "FastAPI  |  Docker Compose  |  Locust  |  Resource Profiling"
p4.font.name = "Arial"
p4.font.size = Pt(13)
p4.font.color.rgb = COLOR_MUTED

# Team Members Card
card_team = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.5), Inches(11.733), Inches(2.2))
card_team.fill.solid()
card_team.fill.fore_color.rgb = COLOR_CARD_BG
card_team.line.color.rgb = COLOR_BORDER
card_team.line.width = Pt(1.5)

tb_team = s1.shapes.add_textbox(Inches(1.2), Inches(4.7), Inches(10.9), Inches(0.4))
tf_team = tb_team.text_frame
p_team_title = tf_team.paragraphs[0]
p_team_title.text = "PROJECT TEAM MEMBERS"
p_team_title.font.name = "Arial"
p_team_title.font.size = Pt(11)
p_team_title.font.bold = True
p_team_title.font.color.rgb = COLOR_BLUE

members = [
    ("Vageesh Mathad", "01FE24BCI008"),
    ("Mehak Sayed Yusuf", "01FE24BCI012"),
    ("Joel Biju", "01FE24BCI021"),
    ("Akshay Bhat", "01FE24BCI024")
]

for i, (name, usn) in enumerate(members):
    left = Inches(1.2 + i * 2.7)
    m_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(5.15), Inches(2.5), Inches(1.25))
    m_box.fill.solid()
    m_box.fill.fore_color.rgb = COLOR_BLUE_BG
    m_box.line.color.rgb = COLOR_BLUE_BORDER
    
    tf_m = m_box.text_frame
    tf_m.word_wrap = True
    pm1 = tf_m.paragraphs[0]
    pm1.text = name
    pm1.font.name = "Arial"
    pm1.font.size = Pt(13)
    pm1.font.bold = True
    pm1.font.color.rgb = COLOR_PRIMARY
    pm1.alignment = PP_ALIGN.CENTER
    
    pm2 = tf_m.add_paragraph()
    pm2.text = f"USN: {usn}"
    pm2.font.name = "Arial"
    pm2.font.size = Pt(11)
    pm2.font.color.rgb = COLOR_BLUE
    pm2.alignment = PP_ALIGN.CENTER

# ==============================================================================
# SLIDE 2: AIM & OBJECTIVES
# ==============================================================================
s2 = prs.slides.add_slide(blank_layout)
apply_background(s2)
add_header(s2, "Aim & Objectives")

# Aim Card
aim_card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.733), Inches(1.5))
aim_card.fill.solid()
aim_card.fill.fore_color.rgb = COLOR_CARD_BG
aim_card.line.color.rgb = COLOR_BORDER

tb_aim = s2.shapes.add_textbox(Inches(1.1), Inches(1.65), Inches(11.1), Inches(1.2))
tf_aim = tb_aim.text_frame
tf_aim.word_wrap = True
p = tf_aim.paragraphs[0]
p.text = "Aim"
p.font.name = "Arial"
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = COLOR_BLUE
p.space_after = Pt(4)

p_aim_desc = tf_aim.add_paragraph()
p_aim_desc.text = "To develop, containerize and deploy an Internship Management System using independent microservices, establish inter-service communication, and evaluate performance under varying workloads."
p_aim_desc.font.name = "Arial"
p_aim_desc.font.size = Pt(13.5)
p_aim_desc.font.color.rgb = COLOR_PRIMARY

# Objectives Card
obj_card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.25), Inches(11.733), Inches(3.65))
obj_card.fill.solid()
obj_card.fill.fore_color.rgb = COLOR_CARD_BG
obj_card.line.color.rgb = COLOR_BORDER

tb_obj = s2.shapes.add_textbox(Inches(1.1), Inches(3.45), Inches(11.1), Inches(3.2))
tf_obj = tb_obj.text_frame
tf_obj.word_wrap = True
p = tf_obj.paragraphs[0]
p.text = "Objectives"
p.font.name = "Arial"
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = COLOR_BLUE
p.space_after = Pt(10)

objectives = [
    "Develop three independent core microservices.",
    "Implement REST APIs for student, internship and application management.",
    "Containerize the services using Docker.",
    "Establish inter-service communication through Docker Compose networking.",
    "Test the Application Service with 1, 2, 4, 8 and 16 concurrent users.",
    "Measure response time, throughput, failed requests, CPU and memory usage."
]

for obj in objectives:
    p_o = tf_obj.add_paragraph()
    p_o.text = f"•  {obj}"
    p_o.font.name = "Arial"
    p_o.font.size = Pt(13)
    p_o.font.color.rgb = COLOR_PRIMARY
    p_o.space_after = Pt(6)

# ==============================================================================
# SLIDE 3: CORE MICROSERVICES
# ==============================================================================
s3 = prs.slides.add_slide(blank_layout)
apply_background(s3)
add_header(s3, "Core Microservices")

services_data = [
    ("Student Service", "Port: 8002\nDatabase: students.db", [
        "Student profiles",
        "Student CRUD operations",
        "Student information validation"
    ]),
    ("Internship Service", "Port: 8003\nDatabase: internships.db", [
        "Internship postings",
        "Internship details",
        "Search/filter operations"
    ]),
    ("Application Service", "Port: 8004\nDatabase: applications.db", [
        "Internship applications",
        "Application status",
        "Inter-service validation"
    ])
]

for i, (title, meta, manages) in enumerate(services_data):
    left = Inches(0.8 + i * 4.0)
    card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(1.5), Inches(3.733), Inches(4.3))
    card.fill.solid()
    card.fill.fore_color.rgb = COLOR_CARD_BG
    card.line.color.rgb = COLOR_BORDER
    
    tb = s3.shapes.add_textbox(left + Inches(0.25), Inches(1.75), Inches(3.2), Inches(3.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = "Arial"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(4)
    
    p_meta = tf.add_paragraph()
    p_meta.text = meta
    p_meta.font.name = "Arial"
    p_meta.font.size = Pt(12)
    p_meta.font.color.rgb = COLOR_BLUE
    p_meta.space_after = Pt(12)
    
    p_m_label = tf.add_paragraph()
    p_m_label.text = "Manages:"
    p_m_label.font.name = "Arial"
    p_m_label.font.size = Pt(13)
    p_m_label.font.bold = True
    p_m_label.font.color.rgb = COLOR_SECONDARY
    p_m_label.space_after = Pt(4)
    
    for m in manages:
        pm = tf.add_paragraph()
        pm.text = f"• {m}"
        pm.font.name = "Arial"
        pm.font.size = Pt(12)
        pm.font.color.rgb = COLOR_PRIMARY
        pm.space_after = Pt(4)

# Supporting Service Banner at Bottom
supp_card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.05), Inches(11.733), Inches(0.85))
supp_card.fill.solid()
supp_card.fill.fore_color.rgb = COLOR_BLUE_BG
supp_card.line.color.rgb = COLOR_BLUE_BORDER

tb_supp = s3.shapes.add_textbox(Inches(1.1), Inches(6.2), Inches(11.1), Inches(0.6))
tf_supp = tb_supp.text_frame
p_supp = tf_supp.paragraphs[0]
p_supp.text = "Supporting Service: Authentication Service — Port 8001 (auth.db | User registration & Bcrypt login)"
p_supp.font.name = "Arial"
p_supp.font.size = Pt(13)
p_supp.font.bold = True
p_supp.font.color.rgb = COLOR_BLUE

# ==============================================================================
# SLIDE 4: SYSTEM ARCHITECTURE
# ==============================================================================
s4 = prs.slides.add_slide(blank_layout)
apply_background(s4)
add_header(s4, "System Architecture")

# Diagram Box
diag_card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.733), Inches(4.3))
diag_card.fill.solid()
diag_card.fill.fore_color.rgb = COLOR_CARD_BG
diag_card.line.color.rgb = COLOR_BORDER

# Inner visual elements for architecture
tb_diag = s4.shapes.add_textbox(Inches(1.2), Inches(1.7), Inches(10.9), Inches(3.8))
tf_diag = tb_diag.text_frame
tf_diag.word_wrap = True

diag_text = """                          CLIENT (Web Dashboard / Locust)
                                         |
                                    REST Requests
                                         |
          ┌──────────────────────────────┴──────────────────────────────┐
          │                     Docker Compose Network                  │
          │                                                             │
          │                   Application Service (:8000)               │
          │                            /      \\                         │
          │                           /        \\                        │
          │                          ↓          ↓                       │
          │                    Student        Internship                │
          │                    Service        Service                   │
          │                    (:8000)        (:8000)                   │
          │                                                             │
          │                 Authentication Service (:8000)              │
          └─────────────────────────────────────────────────────────────┘"""

p = tf_diag.paragraphs[0]
p.text = diag_text
p.font.name = "Courier New"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = COLOR_PRIMARY

# Architecture Info Below
info_card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.0), Inches(11.733), Inches(0.95))
info_card.fill.solid()
info_card.fill.fore_color.rgb = COLOR_BLUE_BG
info_card.line.color.rgb = COLOR_BLUE_BORDER

tb_info = s4.shapes.add_textbox(Inches(1.1), Inches(6.1), Inches(11.1), Inches(0.75))
tf_info = tb_info.text_frame
tf_info.word_wrap = True

p_h = tf_info.paragraphs[0]
p_h.text = "Host Ports: Auth: 8001 | Student: 8002 | Internship: 8003 | Application: 8004  (Internal container port: 8000)"
p_h.font.name = "Arial"
p_h.font.size = Pt(12.5)
p_h.font.bold = True
p_h.font.color.rgb = COLOR_PRIMARY
p_h.space_after = Pt(2)

p_imp = tf_info.add_paragraph()
p_imp.text = "Important: All services communicate through the Docker Compose network via internal service names."
p_imp.font.name = "Arial"
p_imp.font.size = Pt(12)
p_imp.font.color.rgb = COLOR_BLUE

# ==============================================================================
# SLIDE 5: REST API DESIGN
# ==============================================================================
s5 = prs.slides.add_slide(blank_layout)
apply_background(s5)
add_header(s5, "REST API Design")

# Table shape for 15 rows (1 header + 14 data), 4 columns
rows, cols = 15, 4
left = Inches(0.8)
top = Inches(1.5)
width = Inches(11.733)
height = Inches(5.4)

table_shape = s5.shapes.add_table(rows, cols, left, top, width, height)
table = table_shape.table

table.columns[0].width = Inches(2.3) # Service
table.columns[1].width = Inches(1.8) # Method
table.columns[2].width = Inches(3.8) # Endpoint
table.columns[3].width = Inches(3.833) # Purpose

headers = ["Service", "Method", "Endpoint", "Purpose"]
for j, h in enumerate(headers):
    cell = table.cell(0, j)
    cell.fill.solid()
    cell.fill.fore_color.rgb = COLOR_BLUE
    p = cell.text_frame.paragraphs[0]
    p.text = h
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.alignment = PP_ALIGN.LEFT

api_rows = [
    ("Student", "POST", "/students", "Create student"),
    ("Student", "GET", "/students", "List students"),
    ("Student", "GET", "/students/{id}", "Get student"),
    ("Student", "PUT", "/students/{id}", "Update student"),
    ("Student", "DELETE", "/students/{id}", "Delete student"),
    ("Internship", "POST", "/internships", "Create internship"),
    ("Internship", "GET", "/internships", "Search/list"),
    ("Internship", "GET", "/internships/{id}", "Get internship"),
    ("Internship", "PUT", "/internships/{id}", "Update internship"),
    ("Internship", "DELETE", "/internships/{id}", "Delete internship"),
    ("Application", "POST", "/applications", "Submit application"),
    ("Application", "GET", "/applications", "List applications"),
    ("Application", "PATCH", "/applications/{id}/status", "Update status"),
    ("Application", "DELETE", "/applications/{id}", "Withdraw")
]

for i, row in enumerate(api_rows):
    for j, val in enumerate(row):
        cell = table.cell(i + 1, j)
        cell.fill.solid()
        if i % 2 == 0:
            cell.fill.fore_color.rgb = COLOR_CARD_BG
        else:
            cell.fill.fore_color.rgb = COLOR_ROW_ALT
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.name = "Arial"
        p.font.size = Pt(10.5)
        if j == 1:
            p.font.bold = True
            if val in ("POST", "PUT", "PATCH"):
                p.font.color.rgb = COLOR_BLUE
            elif val == "DELETE":
                p.font.color.rgb = RGBColor(220, 38, 38)
            else:
                p.font.color.rgb = COLOR_SUCCESS
        else:
            p.font.color.rgb = COLOR_PRIMARY
        p.alignment = PP_ALIGN.LEFT

# ==============================================================================
# SLIDE 6: DOCKER CONTAINERIZATION & DEPLOYMENT
# ==============================================================================
s6 = prs.slides.add_slide(blank_layout)
apply_background(s6)
add_header(s6, "Docker Containerization & Deployment")

# Left Column: Containerization
c_left = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(4.3))
c_left.fill.solid()
c_left.fill.fore_color.rgb = COLOR_CARD_BG
c_left.line.color.rgb = COLOR_BORDER

tb_cl = s6.shapes.add_textbox(Inches(1.1), Inches(1.75), Inches(5.0), Inches(3.8))
tf_cl = tb_cl.text_frame
tf_cl.word_wrap = True
p = tf_cl.paragraphs[0]
p.text = "Containerization"
p.font.name = "Arial"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = COLOR_BLUE
p.space_after = Pt(12)

c_points = [
    "Individual Dockerfile for each service",
    "Python 3.12-slim base image",
    "FastAPI + Uvicorn",
    "Uvicorn listens on container port 8000",
    "Independent service dependencies"
]
for pt in c_points:
    p = tf_cl.add_paragraph()
    p.text = f"•  {pt}"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(8)

# Right Column: Docker Compose
c_right = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(4.3))
c_right.fill.solid()
c_right.fill.fore_color.rgb = COLOR_CARD_BG
c_right.line.color.rgb = COLOR_BORDER

tb_cr = s6.shapes.add_textbox(Inches(7.1), Inches(1.75), Inches(5.1), Inches(3.8))
tf_cr = tb_cr.text_frame
tf_cr.word_wrap = True
p = tf_cr.paragraphs[0]
p.text = "Docker Compose"
p.font.name = "Arial"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = COLOR_BLUE
p.space_after = Pt(8)

dc_flow = """   docker compose up --build -d
                ↓
          Docker Compose
                ↓
     ┌──────────┼──────────┐
     ↓          ↓          ↓
   Student   Internship  Application
   :8000       :8000       :8000"""

p_flow = tf_cr.add_paragraph()
p_flow.text = dc_flow
p_flow.font.name = "Courier New"
p_flow.font.size = Pt(11)
p_flow.font.bold = True
p_flow.font.color.rgb = COLOR_PRIMARY

# Bottom Persistence Card
p_bottom = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.0), Inches(11.733), Inches(0.95))
p_bottom.fill.solid()
p_bottom.fill.fore_color.rgb = COLOR_BLUE_BG
p_bottom.line.color.rgb = COLOR_BLUE_BORDER

tb_pb = s6.shapes.add_textbox(Inches(1.1), Inches(6.15), Inches(11.1), Inches(0.7))
tf_pb = tb_pb.text_frame
p = tf_pb.paragraphs[0]
p.text = "Persistence: student_data  |  internship_data  |  application_data"
p.font.name = "Arial"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = COLOR_PRIMARY
p.space_after = Pt(2)

p_sub = tf_pb.add_paragraph()
p_sub.text = "Docker named volumes guarantee SQLite data persists safely across container teardowns and restarts."
p_sub.font.name = "Arial"
p_sub.font.size = Pt(11.5)
p_sub.font.color.rgb = COLOR_SECONDARY

# ==============================================================================
# SLIDE 7: INTER-SERVICE COMMUNICATION
# ==============================================================================
s7 = prs.slides.add_slide(blank_layout)
apply_background(s7)
add_header(s7, "Inter-Service Communication")

# Left Column: Flow Diagram
comm_l = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(6.6), Inches(5.4))
comm_l.fill.solid()
comm_l.fill.fore_color.rgb = COLOR_CARD_BG
comm_l.line.color.rgb = COLOR_BORDER

tb_comml = s7.shapes.add_textbox(Inches(1.1), Inches(1.75), Inches(6.0), Inches(4.9))
tf_comml = tb_comml.text_frame
tf_comml.word_wrap = True

p = tf_comml.paragraphs[0]
p.text = "Synchronous Validation Protocol"
p.font.name = "Arial"
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = COLOR_BLUE
p.space_after = Pt(8)

flow_text = """POST /applications
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
                (HTTP 200 OK)"""

p_diag = tf_comml.add_paragraph()
p_diag.text = flow_text
p_diag.font.name = "Courier New"
p_diag.font.size = Pt(11)
p_diag.font.bold = True
p_diag.font.color.rgb = COLOR_PRIMARY

# Right Column: DNS & Failure Handling
comm_r = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.7), Inches(1.5), Inches(4.8), Inches(5.4))
comm_r.fill.solid()
comm_r.fill.fore_color.rgb = COLOR_CARD_BG
comm_r.line.color.rgb = COLOR_BORDER

tb_commr = s7.shapes.add_textbox(Inches(7.95), Inches(1.75), Inches(4.3), Inches(4.9))
tf_commr = tb_commr.text_frame
tf_commr.word_wrap = True

p = tf_commr.paragraphs[0]
p.text = "Why student:8000 & internship:8000?"
p.font.name = "Arial"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_PRIMARY
p.space_after = Pt(4)

p_dns = tf_commr.add_paragraph()
p_dns.text = "Docker Compose provides internal DNS, so services communicate using service names instead of container IP addresses."
p_dns.font.name = "Arial"
p_dns.font.size = Pt(12)
p_dns.font.color.rgb = COLOR_SECONDARY
p_dns.space_after = Pt(14)

p_fail = tf_commr.add_paragraph()
p_fail.text = "Failure Handling Flow:"
p_fail.font.name = "Arial"
p_fail.font.size = Pt(14)
p_fail.font.bold = True
p_fail.font.color.rgb = RGBColor(220, 38, 38)
p_fail.space_after = Pt(6)

fail_diag = """Invalid Student
      ↓
Student Service → 404
      ↓
Application NOT created"""

p_fail_d = tf_commr.add_paragraph()
p_fail_d.text = fail_diag
p_fail_d.font.name = "Courier New"
p_fail_d.font.size = Pt(11)
p_fail_d.font.bold = True
p_fail_d.font.color.rgb = COLOR_PRIMARY
p_fail_d.space_after = Pt(10)

p_stat = tf_commr.add_paragraph()
p_stat.text = "• Successful application creation returns HTTP 200 OK."
p_stat.font.name = "Arial"
p_stat.font.size = Pt(12)
p_stat.font.bold = True
p_stat.font.color.rgb = COLOR_SUCCESS

# ==============================================================================
# SLIDE 8: WORKLOAD TESTING METHODOLOGY
# ==============================================================================
s8 = prs.slides.add_slide(blank_layout)
apply_background(s8)
add_header(s8, "Workload Testing Methodology")

# Top Card: Target Info
m_top = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.733), Inches(1.2))
m_top.fill.solid()
m_top.fill.fore_color.rgb = COLOR_CARD_BG
m_top.line.color.rgb = COLOR_BORDER

tb_mt = s8.shapes.add_textbox(Inches(1.1), Inches(1.65), Inches(11.1), Inches(0.9))
tf_mt = tb_mt.text_frame
tf_mt.word_wrap = True
p = tf_mt.paragraphs[0]
p.text = "Tool: Locust   |   Target: Application Service   |   Host: localhost:8004"
p.font.name = "Arial"
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = COLOR_BLUE
p.space_after = Pt(2)

p_ds = tf_mt.add_paragraph()
p_ds.text = "Docker stats was used to monitor container resource utilization during workload testing."
p_ds.font.name = "Arial"
p_ds.font.size = Pt(12.5)
p_ds.font.color.rgb = COLOR_PRIMARY

# Workloads Grid
w_grid_card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.9), Inches(11.733), Inches(1.8))
w_grid_card.fill.solid()
w_grid_card.fill.fore_color.rgb = COLOR_CARD_BG
w_grid_card.line.color.rgb = COLOR_BORDER

tb_wg = s8.shapes.add_textbox(Inches(1.1), Inches(3.05), Inches(11.1), Inches(0.4))
tf_wg = tb_wg.text_frame
p = tf_wg.paragraphs[0]
p.text = "WORKLOAD LEVELS"
p.font.name = "Arial"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = COLOR_BLUE

workloads_data = [
    ("W1", "1 user"),
    ("W2", "2 users"),
    ("W3", "4 users"),
    ("W4", "8 users"),
    ("W5", "16 users")
]

for i, (w_code, w_users) in enumerate(workloads_data):
    left = Inches(1.1 + i * 2.25)
    box = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(3.45), Inches(2.0), Inches(1.05))
    box.fill.solid()
    box.fill.fore_color.rgb = COLOR_BLUE_BG
    box.line.color.rgb = COLOR_BLUE_BORDER
    tf_b = box.text_frame
    p1 = tf_b.paragraphs[0]
    p1.text = w_code
    p1.font.name = "Arial"
    p1.font.size = Pt(16)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_BLUE
    p1.alignment = PP_ALIGN.CENTER
    
    p2 = tf_b.add_paragraph()
    p2.text = w_users
    p2.font.name = "Arial"
    p2.font.size = Pt(12)
    p2.font.color.rgb = COLOR_PRIMARY
    p2.alignment = PP_ALIGN.CENTER

# Metrics Card Bottom
m_bottom = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.9), Inches(11.733), Inches(2.0))
m_bottom.fill.solid()
m_bottom.fill.fore_color.rgb = COLOR_CARD_BG
m_bottom.line.color.rgb = COLOR_BORDER

tb_mb = s8.shapes.add_textbox(Inches(1.1), Inches(5.1), Inches(11.1), Inches(1.6))
tf_mb = tb_mb.text_frame
tf_mb.word_wrap = True
p = tf_mb.paragraphs[0]
p.text = "Metrics Recorded"
p.font.name = "Arial"
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = COLOR_PRIMARY
p.space_after = Pt(8)

metrics_list = [
    "Average Response Time",
    "Throughput (RPS)",
    "Failed Requests",
    "CPU Utilization",
    "Memory Usage"
]
for m in metrics_list:
    p_m = tf_mb.add_paragraph()
    p_m.text = f"•  {m}"
    p_m.font.name = "Arial"
    p_m.font.size = Pt(12.5)
    p_m.font.color.rgb = COLOR_SECONDARY
    p_m.space_after = Pt(3)

# ==============================================================================
# SLIDE 9: PERFORMANCE RESULTS
# ==============================================================================
s9 = prs.slides.add_slide(blank_layout)
apply_background(s9)
add_header(s9, "Performance Results")

# Table for Performance Results
rows, cols = 6, 5
left = Inches(0.8)
top = Inches(1.6)
width = Inches(11.733)
height = Inches(4.2)

t_shape9 = s9.shapes.add_table(rows, cols, left, top, width, height)
t9 = t_shape9.table

t9.columns[0].width = Inches(1.8) # Workload
t9.columns[1].width = Inches(2.0) # Users
t9.columns[2].width = Inches(2.8) # Avg Response Time
t9.columns[3].width = Inches(2.8) # Throughput
t9.columns[4].width = Inches(2.333) # Failures

h9 = ["Workload", "Users", "Avg Response Time", "Throughput", "Failures"]
for j, h in enumerate(h9):
    cell = t9.cell(0, j)
    cell.fill.solid()
    cell.fill.fore_color.rgb = COLOR_BLUE
    p = cell.text_frame.paragraphs[0]
    p.text = h
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.alignment = PP_ALIGN.CENTER

res_data = [
    ["W1", "1", "10.28 ms", "3.2 RPS", "0"],
    ["W2", "2", "—", "—", "—"],
    ["W3", "4", "—", "—", "—"],
    ["W4", "8", "—", "—", "—"],
    ["W5", "16", "—", "—", "—"]
]

for i, row in enumerate(res_data):
    for j, val in enumerate(row):
        cell = t9.cell(i + 1, j)
        cell.fill.solid()
        if i == 0:
            cell.fill.fore_color.rgb = COLOR_BLUE_BG
        elif i % 2 == 0:
            cell.fill.fore_color.rgb = COLOR_CARD_BG
        else:
            cell.fill.fore_color.rgb = COLOR_ROW_ALT
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.name = "Arial"
        p.font.size = Pt(13)
        if i == 0:
            p.font.bold = True
            p.font.color.rgb = COLOR_PRIMARY
        else:
            p.font.color.rgb = COLOR_MUTED
        p.alignment = PP_ALIGN.CENTER

note_box = s9.shapes.add_textbox(Inches(0.8), Inches(6.0), Inches(11.733), Inches(0.6))
tf_nb = note_box.text_frame
p = tf_nb.paragraphs[0]
p.text = "* W1 represents actual measured baseline values. Remaining workload rows are populated as evaluations proceed."
p.font.name = "Arial"
p.font.size = Pt(12)
p.font.color.rgb = COLOR_MUTED

# ==============================================================================
# SLIDE 10: RESOURCE UTILIZATION
# ==============================================================================
s10 = prs.slides.add_slide(blank_layout)
apply_background(s10)
add_header(s10, "Resource Utilization")

rows, cols = 5, 3
left = Inches(0.8)
top = Inches(1.6)
width = Inches(11.733)
height = Inches(3.8)

t_shape10 = s10.shapes.add_table(rows, cols, left, top, width, height)
t10 = t_shape10.table

t10.columns[0].width = Inches(4.5) # Service
t10.columns[1].width = Inches(3.6) # CPU
t10.columns[2].width = Inches(3.633) # Memory

h10 = ["Service", "CPU", "Memory"]
for j, h in enumerate(h10):
    cell = t10.cell(0, j)
    cell.fill.solid()
    cell.fill.fore_color.rgb = COLOR_BLUE
    p = cell.text_frame.paragraphs[0]
    p.text = h
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.alignment = PP_ALIGN.CENTER

res_util_data = [
    ["Authentication", "0.26%", "53.77 MiB"],
    ["Student", "0.31%", "55.21 MiB"],
    ["Internship", "0.28%", "54.64 MiB"],
    ["Application", "0.32%", "59.06 MiB"]
]

for i, row in enumerate(res_util_data):
    for j, val in enumerate(row):
        cell = t10.cell(i + 1, j)
        cell.fill.solid()
        if i % 2 == 0:
            cell.fill.fore_color.rgb = COLOR_CARD_BG
        else:
            cell.fill.fore_color.rgb = COLOR_ROW_ALT
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.name = "Arial"
        p.font.size = Pt(13)
        p.font.color.rgb = COLOR_PRIMARY
        p.alignment = PP_ALIGN.CENTER

note_box10 = s10.shapes.add_textbox(Inches(0.8), Inches(5.8), Inches(11.733), Inches(0.8))
tf_nb10 = note_box10.text_frame
p = tf_nb10.paragraphs[0]
p.text = "* Measured via docker stats under baseline workload W1 (1 concurrent user). Remaining workload tests W2–W5 follow the same profiling methodology."
p.font.name = "Arial"
p.font.size = Pt(12)
p.font.color.rgb = COLOR_MUTED

# ==============================================================================
# SLIDE 11: PERFORMANCE ANALYSIS (GRAPHS)
# ==============================================================================
s11 = prs.slides.add_slide(blank_layout)
apply_background(s11)
add_header(s11, "Performance Analysis")

# 4 Graph cards
graphs = [
    ("Graph 1: Concurrent Users vs Average Response Time", "plots/1_response_time.png", Inches(0.8), Inches(1.5)),
    ("Graph 2: Concurrent Users vs Throughput", "plots/2_throughput.png", Inches(6.8), Inches(1.5)),
    ("Graph 3: Concurrent Users vs CPU Utilization", "plots/3_cpu_utilization.png", Inches(0.8), Inches(3.9)),
    ("Graph 4: Concurrent Users vs Memory Usage", "plots/4_memory_utilization.png", Inches(6.8), Inches(3.9))
]

for g_title, img_path, left, top in graphs:
    card = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.7), Inches(2.25))
    card.fill.solid()
    card.fill.fore_color.rgb = COLOR_CARD_BG
    card.line.color.rgb = COLOR_BORDER
    
    tb = s11.shapes.add_textbox(left + Inches(0.2), top + Inches(0.1), Inches(5.3), Inches(0.35))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = g_title
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    
    if os.path.exists(img_path):
        s11.shapes.add_picture(img_path, left + Inches(0.2), top + Inches(0.45), Inches(5.3), Inches(1.7))

# Observed Behaviour Note Below
obs_card = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.3), Inches(11.733), Inches(0.8))
obs_card.fill.solid()
obs_card.fill.fore_color.rgb = COLOR_BLUE_BG
obs_card.line.color.rgb = COLOR_BLUE_BORDER

tb_obs = s11.shapes.add_textbox(Inches(1.1), Inches(6.4), Inches(11.1), Inches(0.6))
tf_obs = tb_obs.text_frame
p = tf_obs.paragraphs[0]
p.text = "Observed Behaviour: Response time, throughput and resource utilization were compared across increasing concurrent workloads."
p.font.name = "Arial"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = COLOR_BLUE

# ==============================================================================
# SLIDE 12: CONCLUSION & DEMONSTRATION
# ==============================================================================
s12 = prs.slides.add_slide(blank_layout)
apply_background(s12)
add_header(s12, "Conclusion & Demonstration")

# Left Column: Project Demonstrates
c_demo_l = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4))
c_demo_l.fill.solid()
c_demo_l.fill.fore_color.rgb = COLOR_CARD_BG
c_demo_l.line.color.rgb = COLOR_BORDER

tb_dl = s12.shapes.add_textbox(Inches(1.1), Inches(1.75), Inches(5.0), Inches(4.9))
tf_dl = tb_dl.text_frame
tf_dl.word_wrap = True
p = tf_dl.paragraphs[0]
p.text = "Project Demonstrates"
p.font.name = "Arial"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = COLOR_BLUE
p.space_after = Pt(12)

demo_points = [
    "Independent microservices",
    "RESTful APIs",
    "Docker containerization",
    "Docker Compose orchestration",
    "Docker-network service discovery",
    "Inter-service validation",
    "Locust workload testing",
    "CPU and memory monitoring"
]
for pt in demo_points:
    p = tf_dl.add_paragraph()
    p.text = f"✔  {pt}"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(6)

# Right Column: Live Demo Flow
c_demo_r = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4))
c_demo_r.fill.solid()
c_demo_r.fill.fore_color.rgb = COLOR_CARD_BG
c_demo_r.line.color.rgb = COLOR_BORDER

tb_dr = s12.shapes.add_textbox(Inches(7.1), Inches(1.75), Inches(5.1), Inches(4.9))
tf_dr = tb_dr.text_frame
tf_dr.word_wrap = True
p = tf_dr.paragraphs[0]
p.text = "Live Demo Flow"
p.font.name = "Arial"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = COLOR_BLUE
p.space_after = Pt(8)

demo_flow = """   Docker Compose
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
   Show Results"""

p_df = tf_dr.add_paragraph()
p_df.text = demo_flow
p_df.font.name = "Courier New"
p_df.font.size = Pt(11)
p_df.font.bold = True
p_df.font.color.rgb = COLOR_PRIMARY

# Save presentation
primary_file = "Internship_Management_Microservices.pptx"
fallback_file = "Internship_Management_Presentation.pptx"

try:
    prs.save(primary_file)
    print(f"Presentation successfully created: {primary_file}")
except PermissionError:
    print(f"Notice: '{primary_file}' is currently open in PowerPoint. Saving to '{fallback_file}' instead...")
    prs.save(fallback_file)
    print(f"Presentation successfully created: {fallback_file}")

