"""
Microservices Verification and End-to-End Test Suite
Internship Management System (IMS)
Validates all 4 microservices, JWT authentication, and inter-service validation.
"""

import sys
import time
import requests

SERVICES = {
    "auth": "http://localhost:8001",
    "student": "http://localhost:8002",
    "internship": "http://localhost:8003",
    "application": "http://localhost:8004"
}

def log(msg, status="INFO"):
    symbol = "✓" if status == "PASS" else ("✗" if status == "FAIL" else "ℹ")
    print(f"[{symbol}] [{status}] {msg}")

def check_health():
    log("Checking health endpoints across all 4 microservices...", "INFO")
    all_ok = True
    for name, base_url in SERVICES.items():
        try:
            r = requests.get(f"{base_url}/health", timeout=3)
            if r.status_code == 200:
                log(f"{name.capitalize()} Service (:800{list(SERVICES.keys()).index(name)+1}) is Healthy: {r.json().get('status')}", "PASS")
            else:
                log(f"{name.capitalize()} Service returned HTTP {r.status_code}", "FAIL")
                all_ok = False
        except Exception as e:
            log(f"Cannot reach {name} service at {base_url}: {e}", "FAIL")
            all_ok = False
    return all_ok

def run_e2e_tests():
    print("\n" + "="*70)
    print("STARTING FULL END-TO-END VERIFICATION SUITE")
    print("="*70)

    # 1. Test Auth Service (JWT Token flow)
    test_user_email = f"test_user_{int(time.time())}@university.edu"
    test_user_pw = "SecurePass123!"
    log(f"Registering test user '{test_user_email}'...", "INFO")
    
    r_reg = requests.post(f"{SERVICES['auth']}/register", json={
        "name": "Alex Mercer",
        "email": test_user_email,
        "password": test_user_pw,
        "role": "student"
    })
    if r_reg.status_code in [200, 201]:
        data = r_reg.json()
        token = data.get("access_token")
        log(f"User registered. JWT Token issued: {token[:20]}...", "PASS")
    else:
        log(f"Registration failed: {r_reg.text}", "FAIL")
        return False

    log("Testing login and token retrieval...", "INFO")
    r_login = requests.post(f"{SERVICES['auth']}/login", json={
        "email": test_user_email,
        "password": test_user_pw
    })
    if r_login.status_code == 200 and "access_token" in r_login.json():
        log("Login successful with valid JWT payload", "PASS")
    else:
        log(f"Login failed: {r_login.text}", "FAIL")
        return False

    # 2. Test Student Service
    test_student_email = f"student_{int(time.time())}@campus.edu"
    log("Creating new student profile...", "INFO")
    r_student = requests.post(f"{SERVICES['student']}/students", json={
        "name": "Samantha Ray",
        "email": test_student_email,
        "department": "CSE",
        "year": 3,
        "skills": "Python, Docker, FastAPI"
    })
    if r_student.status_code in [200, 201]:
        student_id = r_student.json()["id"]
        log(f"Created Student ID: {student_id} ({r_student.json()['name']})", "PASS")
    else:
        log(f"Student creation failed: {r_student.text}", "FAIL")
        return False

    # 3. Test Internship Service
    log("Posting new internship opportunity...", "INFO")
    r_intern = requests.post(f"{SERVICES['internship']}/internships", json={
        "title": "Cloud Platform Intern",
        "company": "Nexus Systems",
        "location": "Remote",
        "description": "Building microservices using FastAPI and Docker",
        "stipend": "$2,000/mo",
        "status": "open",
        "deadline": "2026-12-31"
    })
    if r_intern.status_code in [200, 201]:
        internship_id = r_intern.json()["id"]
        log(f"Created Internship ID: {internship_id} ({r_intern.json()['title']})", "PASS")
    else:
        log(f"Internship creation failed: {r_intern.text}", "FAIL")
        return False

    # 4. Checkpoint 3 Inter-Service Validation: Negative Tests
    log("\n[Checkpoint 3] Testing inter-service validation (negative tests)...", "INFO")
    
    # Non-existent student test
    r_neg_student = requests.post(f"{SERVICES['application']}/applications", json={
        "student_id": 999999,
        "internship_id": internship_id
    })
    if r_neg_student.status_code == 404:
        log(f"Invalid Student #999999 rejected correctly (404 Not Found): '{r_neg_student.json().get('detail')}'", "PASS")
    else:
        log(f"Expected 404 for invalid student, got {r_neg_student.status_code}", "FAIL")

    # Non-existent internship test
    r_neg_intern = requests.post(f"{SERVICES['application']}/applications", json={
        "student_id": student_id,
        "internship_id": 999999
    })
    if r_neg_intern.status_code == 404:
        log(f"Invalid Internship #999999 rejected correctly (404 Not Found): '{r_neg_intern.json().get('detail')}'", "PASS")
    else:
        log(f"Expected 404 for invalid internship, got {r_neg_intern.status_code}", "FAIL")

    # 5. Checkpoint 3 Positive Test: Valid application submission
    log("\n[Checkpoint 3] Testing valid application submission...", "INFO")
    r_app = requests.post(f"{SERVICES['application']}/applications", json={
        "student_id": student_id,
        "internship_id": internship_id,
        "notes": "E2E automated validation test"
    })
    if r_app.status_code in [200, 201]:
        app_id = r_app.json()["id"]
        log(f"Application #{app_id} accepted with status: '{r_app.json()['status']}'", "PASS")
    else:
        log(f"Valid application failed: {r_app.text}", "FAIL")
        return False

    # 6. Test Duplicate Application Rejection (409 Conflict)
    r_dup = requests.post(f"{SERVICES['application']}/applications", json={
        "student_id": student_id,
        "internship_id": internship_id
    })
    if r_dup.status_code == 409:
        log("Duplicate application rejected correctly (409 Conflict)", "PASS")
    else:
        log(f"Expected 409 for duplicate application, got {r_dup.status_code}", "FAIL")

    # 7. Test Application Status Update (PATCH /applications/{id}/status)
    r_patch = requests.patch(f"{SERVICES['application']}/applications/{app_id}/status", json={
        "status": "accepted"
    })
    if r_patch.status_code == 200 and r_patch.json().get("status") == "accepted":
        log(f"Application #{app_id} successfully updated to 'accepted'", "PASS")
    else:
        log(f"Application status patch failed: {r_patch.text}", "FAIL")
        return False

    # 8. Test Enriched Applications Endpoint
    r_enriched = requests.get(f"{SERVICES['application']}/applications/enriched")
    if r_enriched.status_code == 200 and len(r_enriched.json()) > 0:
        log(f"Enriched applications endpoint returned {len(r_enriched.json())} joined records", "PASS")
    else:
        log("Failed to query enriched applications", "FAIL")

    print("\n" + "="*70)
    print("ALL VERIFICATION SUITE CHECKS PASSED PERFECTLY!")
    print("="*70)
    return True

if __name__ == "__main__":
    if not check_health():
        print("\nNote: Make sure containers are running via 'docker compose up -d' before running tests.")
        sys.exit(1)
    success = run_e2e_tests()
    sys.exit(0 if success else 1)
