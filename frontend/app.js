const API_URLS = {
  auth: 'http://localhost:8001',
  student: 'http://localhost:8002',
  internship: 'http://localhost:8003',
  application: 'http://localhost:8004'
};

// Toast notifications
function showToast(message, type = 'success') {
  const container = document.getElementById('toast-container');
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `<span>${type === 'success' ? '✓' : '⚠'}</span> <span>${message}</span>`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

// Health check indicators
async function checkServiceHealth() {
  const services = ['auth', 'student', 'internship', 'application'];
  for (const s of services) {
    const el = document.getElementById(`pill-${s}`);
    try {
      const res = await fetch(`${API_URLS[s]}/`, { method: 'GET' });
      if (res.ok) {
        el.className = 'service-pill online';
        el.querySelector('.status-text').textContent = 'Online';
      } else {
        el.className = 'service-pill offline';
        el.querySelector('.status-text').textContent = 'Error';
      }
    } catch {
      el.className = 'service-pill offline';
      el.querySelector('.status-text').textContent = 'Offline';
    }
  }
}

// Tab Switching
function setupTabs() {
  const tabs = document.querySelectorAll('.tab-btn');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      tab.classList.add('active');
      const target = document.getElementById(`tab-${tab.dataset.tab}`);
      if (target) target.classList.add('active');

      if (tab.dataset.tab === 'students') loadStudents();
      if (tab.dataset.tab === 'internships') loadInternships();
      if (tab.dataset.tab === 'applications') {
        loadApplications();
        populateAppDropdowns();
      }
    });
  });
}

// ==========================================
// 1. STUDENTS MODULE
// ==========================================
async function loadStudents() {
  const tbody = document.getElementById('students-tbody');
  tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;">Loading...</td></tr>';
  try {
    const res = await fetch(`${API_URLS.student}/students`);
    const students = await res.json();
    if (!students || students.length === 0) {
      tbody.innerHTML = '<tr><td colspan="6" class="empty-state">No students registered yet. Add one on the left!</td></tr>';
      return;
    }
    tbody.innerHTML = students.map(s => `
      <tr>
        <td><strong>#${s.id}</strong></td>
        <td>${escapeHtml(s.name)}</td>
        <td>${escapeHtml(s.email)}</td>
        <td><span class="badge" style="background:rgba(99,102,241,0.15);color:#a5b4fc;">${s.department || 'N/A'}</span></td>
        <td>Year ${s.year || 1}</td>
        <td>
          <button class="btn btn-danger" onclick="deleteStudent(${s.id})">Delete</button>
        </td>
      </tr>
    `).join('');
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="6" class="empty-state" style="color:#ef4444;">Failed to connect to Student Service (:8002).</td></tr>`;
  }
}

async function handleStudentSubmit(e) {
  e.preventDefault();
  const name = document.getElementById('student-name').value.trim();
  const email = document.getElementById('student-email').value.trim();
  const department = document.getElementById('student-dept').value;
  const year = parseInt(document.getElementById('student-year').value);

  try {
    const res = await fetch(`${API_URLS.student}/students`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, department, year })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Failed to create student');
    showToast(`Student "${data.name}" registered successfully!`);
    document.getElementById('student-form').reset();
    loadStudents();
  } catch (err) {
    showToast(err.message, 'error');
  }
}

async function deleteStudent(id) {
  if (!confirm(`Delete student #${id}?`)) return;
  try {
    const res = await fetch(`${API_URLS.student}/students/${id}`, { method: 'DELETE' });
    if (!res.ok) throw new Error('Failed to delete student');
    showToast(`Student #${id} deleted.`);
    loadStudents();
  } catch (err) {
    showToast(err.message, 'error');
  }
}

// ==========================================
// 2. INTERNSHIPS MODULE
// ==========================================
let allInternships = [];

async function loadInternships() {
  const container = document.getElementById('internships-container');
  container.innerHTML = '<div class="empty-state">Loading internships...</div>';
  try {
    const res = await fetch(`${API_URLS.internship}/internships`);
    allInternships = await res.json();
    renderInternships(allInternships);
  } catch (err) {
    container.innerHTML = '<div class="empty-state" style="color:#ef4444;">Failed to connect to Internship Service (:8003).</div>';
  }
}

function renderInternships(list) {
  const container = document.getElementById('internships-container');
  if (!list || list.length === 0) {
    container.innerHTML = '<div class="empty-state">No internships found. Create one using the form on the left!</div>';
    return;
  }
  container.innerHTML = list.map(item => `
    <div class="job-card">
      <div>
        <div class="job-header">
          <div>
            <div class="job-title">${escapeHtml(item.title)}</div>
            <div class="job-company">${escapeHtml(item.company)}</div>
          </div>
          <span class="badge" style="background:rgba(255,255,255,0.06);color:#9ca3af;">#${item.id}</span>
        </div>
        <div class="job-location">📍 ${escapeHtml(item.location || 'Remote')}</div>
        <div class="job-desc">${escapeHtml(item.description || 'No description provided.')}</div>
      </div>
      <div style="display:flex;gap:8px;margin-top:12px;">
        <button class="btn btn-accent-outline" style="font-size:0.75rem;padding:6px 12px;" onclick="quickApply(${item.id})">Quick Apply</button>
        <button class="btn btn-danger" onclick="deleteInternship(${item.id})">Delete</button>
      </div>
    </div>
  `).join('');
}

async function handleInternshipSubmit(e) {
  e.preventDefault();
  const title = document.getElementById('internship-title').value.trim();
  const company = document.getElementById('internship-company').value.trim();
  const location = document.getElementById('internship-location').value.trim();
  const description = document.getElementById('internship-desc').value.trim();

  try {
    const res = await fetch(`${API_URLS.internship}/internships`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, company, location, description })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Failed to create internship');
    showToast(`Internship "${data.title}" posted!`);
    document.getElementById('internship-form').reset();
    loadInternships();
  } catch (err) {
    showToast(err.message, 'error');
  }
}

async function deleteInternship(id) {
  if (!confirm(`Delete internship #${id}?`)) return;
  try {
    const res = await fetch(`${API_URLS.internship}/internships/${id}`, { method: 'DELETE' });
    if (!res.ok) throw new Error('Failed to delete internship');
    showToast(`Internship #${id} deleted.`);
    loadInternships();
  } catch (err) {
    showToast(err.message, 'error');
  }
}

function handleSearchInternships(e) {
  const query = e.target.value.toLowerCase();
  const filtered = allInternships.filter(item => 
    item.title.toLowerCase().includes(query) ||
    item.company.toLowerCase().includes(query) ||
    (item.location && item.location.toLowerCase().includes(query))
  );
  renderInternships(filtered);
}

// ==========================================
// 3. APPLICATIONS & INTER-SERVICE MODULE
// ==========================================
async function populateAppDropdowns() {
  const studentSelect = document.getElementById('apply-student-id');
  const internshipSelect = document.getElementById('apply-internship-id');

  try {
    const [sRes, iRes] = await Promise.all([
      fetch(`${API_URLS.student}/students`),
      fetch(`${API_URLS.internship}/internships`)
    ]);
    const students = await sRes.json();
    const internships = await iRes.json();

    studentSelect.innerHTML = '<option value="">Select Registered Student...</option>' + 
      students.map(s => `<option value="${s.id}">#${s.id} - ${escapeHtml(s.name)} (${s.department || 'N/A'})</option>`).join('');

    internshipSelect.innerHTML = '<option value="">Select Internship Position...</option>' + 
      internships.map(i => `<option value="${i.id}">#${i.id} - ${escapeHtml(i.title)} at ${escapeHtml(i.company)}</option>`).join('');
  } catch {
    // Graceful fallback
  }
}

async function loadApplications() {
  const tbody = document.getElementById('applications-tbody');
  tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;">Loading applications...</td></tr>';
  try {
    const res = await fetch(`${API_URLS.application}/applications`);
    const apps = await res.json();
    if (!apps || apps.length === 0) {
      tbody.innerHTML = '<tr><td colspan="5" class="empty-state">No applications submitted yet.</td></tr>';
      return;
    }
    tbody.innerHTML = apps.map(a => `
      <tr>
        <td><strong>#${a.id}</strong></td>
        <td>Student <strong>#${a.student_id}</strong></td>
        <td>Internship <strong>#${a.internship_id}</strong></td>
        <td><span class="badge badge-${a.status}">${a.status}</span></td>
        <td>
          <div style="display:flex;gap:6px;">
            <button class="btn btn-secondary" style="padding:4px 10px;font-size:0.75rem;width:auto;" onclick="updateAppStatus(${a.id}, 'accepted')">Accept</button>
            <button class="btn btn-secondary" style="padding:4px 10px;font-size:0.75rem;width:auto;" onclick="updateAppStatus(${a.id}, 'rejected')">Reject</button>
            <button class="btn btn-danger" onclick="deleteApplication(${a.id})">Delete</button>
          </div>
        </td>
      </tr>
    `).join('');
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="5" class="empty-state" style="color:#ef4444;">Failed to connect to Application Service (:8004).</td></tr>`;
  }
}

async function handleApplySubmit(e) {
  e.preventDefault();
  const student_id = parseInt(document.getElementById('apply-student-id').value);
  const internship_id = parseInt(document.getElementById('apply-internship-id').value);

  if (!student_id || !internship_id) {
    showToast('Please select both a student and an internship.', 'error');
    return;
  }

  try {
    const res = await fetch(`${API_URLS.application}/applications`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ student_id, internship_id })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Application failed');
    showToast(`Application #${data.id} submitted! Status: ${data.status}`);
    loadApplications();
  } catch (err) {
    showToast(err.message, 'error');
  }
}

// Checkpoint 3 Demonstration trigger: Test invalid student rejection
async function testInvalidStudentDemo() {
  showToast('Sending application with invalid Student ID (99999)...', 'info');
  try {
    const res = await fetch(`${API_URLS.application}/applications`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ student_id: 99999, internship_id: 1 })
    });
    const data = await res.json();
    if (!res.ok) {
      alert(`[Checkpoint 3 Success]\nInter-Service Communication Verified!\n\nStatus Code: ${res.status}\nError Response: "${data.detail}"\n\nExplanation: Application Service (:8004) contacted Student Service (:8002) over the internal Docker network. Because student 99999 was not found, the application was rejected.`);
    } else {
      showToast('Unexpected success for invalid student', 'error');
    }
  } catch (err) {
    showToast(`Error: ${err.message}`, 'error');
  }
}

async function updateAppStatus(id, status) {
  try {
    const res = await fetch(`${API_URLS.application}/applications/${id}/status`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Failed to update status');
    showToast(`Application #${id} status changed to ${status}!`);
    loadApplications();
  } catch (err) {
    showToast(err.message, 'error');
  }
}

async function deleteApplication(id) {
  if (!confirm(`Delete application #${id}?`)) return;
  try {
    const res = await fetch(`${API_URLS.application}/applications/${id}`, { method: 'DELETE' });
    if (!res.ok) throw new Error('Failed to delete application');
    showToast(`Application #${id} deleted.`);
    loadApplications();
  } catch (err) {
    showToast(err.message, 'error');
  }
}

function quickApply(internshipId) {
  const appTab = document.querySelector('.tab-btn[data-tab="applications"]');
  if (appTab) appTab.click();
  setTimeout(() => {
    const select = document.getElementById('apply-internship-id');
    if (select) select.value = internshipId;
  }, 300);
}

// ==========================================
// 4. AUTH MODULE
// ==========================================
async function handleAuthRegister(e) {
  e.preventDefault();
  const name = document.getElementById('auth-name').value.trim();
  const email = document.getElementById('auth-email').value.trim();
  const password = document.getElementById('auth-pass').value;

  try {
    const res = await fetch(`${API_URLS.auth}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, password })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Registration failed');
    showToast(`User ${data.name} registered successfully with Bcrypt hash!`);
    document.getElementById('auth-reg-form').reset();
  } catch (err) {
    showToast(err.message, 'error');
  }
}

async function handleAuthLogin(e) {
  e.preventDefault();
  const email = document.getElementById('login-email').value.trim();
  const password = document.getElementById('login-pass').value;

  try {
    const res = await fetch(`${API_URLS.auth}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Login failed');
    showToast(`Login successful! User ID: #${data.user_id}`);
    document.getElementById('auth-login-form').reset();
  } catch (err) {
    showToast(err.message, 'error');
  }
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
  setupTabs();
  checkServiceHealth();
  setInterval(checkServiceHealth, 8000);

  // Forms
  document.getElementById('student-form')?.addEventListener('submit', handleStudentSubmit);
  document.getElementById('internship-form')?.addEventListener('submit', handleInternshipSubmit);
  document.getElementById('apply-form')?.addEventListener('submit', handleApplySubmit);
  document.getElementById('auth-reg-form')?.addEventListener('submit', handleAuthRegister);
  document.getElementById('auth-login-form')?.addEventListener('submit', handleAuthLogin);
  document.getElementById('search-internships')?.addEventListener('input', handleSearchInternships);

  // Initial load
  loadStudents();
});
