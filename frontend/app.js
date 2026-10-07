const API_URLS = {
  auth: 'http://localhost:8001',
  student: 'http://localhost:8002',
  internship: 'http://localhost:8003',
  application: 'http://localhost:8004'
};

function showToast(message, type = 'success') {
  const container = document.getElementById('toast-container');
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.textContent = `[${type.toUpperCase()}] ${message}`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.remove();
  }, 4000);
}

async function checkServiceHealth() {
  const services = ['auth', 'student', 'internship', 'application'];
  for (const s of services) {
    const el = document.getElementById(`pill-${s}`);
    if (!el) continue;
    try {
      const res = await fetch(`${API_URLS[s]}/`, { method: 'GET' });
      if (res.ok) {
        el.className = 'service-pill online';
        el.querySelector('.status-text').textContent = 'ONLINE';
      } else {
        el.className = 'service-pill offline';
        el.querySelector('.status-text').textContent = 'ERROR';
      }
    } catch {
      el.className = 'service-pill offline';
      el.querySelector('.status-text').textContent = 'OFFLINE';
    }
  }
}

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

// 1. Students
async function loadStudents() {
  const tbody = document.getElementById('students-tbody');
  tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;">Loading...</td></tr>';
  try {
    const res = await fetch(`${API_URLS.student}/students`);
    const students = await res.json();
    if (!students || students.length === 0) {
      tbody.innerHTML = '<tr><td colspan="6" class="empty-state">No student records.</td></tr>';
      return;
    }
    tbody.innerHTML = students.map(s => `
      <tr>
        <td>#${s.id}</td>
        <td>${escapeHtml(s.name)}</td>
        <td>${escapeHtml(s.email)}</td>
        <td>${escapeHtml(s.department || '-')}</td>
        <td>Year ${s.year || 1}</td>
        <td>
          <button class="btn btn-danger" onclick="deleteStudent(${s.id})">Delete</button>
        </td>
      </tr>
    `).join('');
  } catch (err) {
    tbody.innerHTML = '<tr><td colspan="6" class="empty-state">Unable to connect to Student Service (:8002).</td></tr>';
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
    showToast(`Created student #${data.id} (${data.name})`);
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
    if (!res.ok) throw new Error('Delete failed');
    showToast(`Deleted student #${id}`);
    loadStudents();
  } catch (err) {
    showToast(err.message, 'error');
  }
}

// 2. Internships
let allInternships = [];

async function loadInternships() {
  const container = document.getElementById('internships-container');
  container.innerHTML = '<div class="empty-state">Loading internships...</div>';
  try {
    const res = await fetch(`${API_URLS.internship}/internships`);
    allInternships = await res.json();
    renderInternships(allInternships);
  } catch (err) {
    container.innerHTML = '<div class="empty-state">Unable to connect to Internship Service (:8003).</div>';
  }
}

function renderInternships(list) {
  const container = document.getElementById('internships-container');
  if (!list || list.length === 0) {
    container.innerHTML = '<div class="empty-state">No internships found.</div>';
    return;
  }
  container.innerHTML = list.map(item => `
    <div class="job-item">
      <div class="job-title-row">
        <span class="job-title">${escapeHtml(item.title)}</span>
        <span style="font-size:11px;color:var(--text-muted);">#${item.id}</span>
      </div>
      <div class="job-meta">${escapeHtml(item.company)} | ${escapeHtml(item.location || 'Remote')}</div>
      <div class="job-desc">${escapeHtml(item.description || 'No description.')}</div>
      <div style="display:flex;gap:6px;">
        <button class="btn btn-secondary" style="width:auto;" onclick="quickApply(${item.id})">Select for Application</button>
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
    showToast(`Created internship #${data.id} (${data.title})`);
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
    if (!res.ok) throw new Error('Delete failed');
    showToast(`Deleted internship #${id}`);
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

// 3. Applications
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

    studentSelect.innerHTML = '<option value="">Select Student...</option>' + 
      students.map(s => `<option value="${s.id}">#${s.id} - ${escapeHtml(s.name)}</option>`).join('');

    internshipSelect.innerHTML = '<option value="">Select Internship...</option>' + 
      internships.map(i => `<option value="${i.id}">#${i.id} - ${escapeHtml(i.title)} (${escapeHtml(i.company)})</option>`).join('');
  } catch {
    //
  }
}

async function loadApplications() {
  const tbody = document.getElementById('applications-tbody');
  tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;">Loading...</td></tr>';
  try {
    const res = await fetch(`${API_URLS.application}/applications`);
    const apps = await res.json();
    if (!apps || apps.length === 0) {
      tbody.innerHTML = '<tr><td colspan="5" class="empty-state">No applications submitted.</td></tr>';
      return;
    }
    tbody.innerHTML = apps.map(a => `
      <tr>
        <td>#${a.id}</td>
        <td>Student #${a.student_id}</td>
        <td>Internship #${a.internship_id}</td>
        <td><span class="badge badge-${a.status}">${a.status}</span></td>
        <td>
          <div style="display:flex;gap:4px;">
            <button class="btn btn-secondary" style="padding:2px 8px;font-size:11px;width:auto;" onclick="updateAppStatus(${a.id}, 'accepted')">Accept</button>
            <button class="btn btn-secondary" style="padding:2px 8px;font-size:11px;width:auto;" onclick="updateAppStatus(${a.id}, 'rejected')">Reject</button>
            <button class="btn btn-danger" onclick="deleteApplication(${a.id})">Delete</button>
          </div>
        </td>
      </tr>
    `).join('');
  } catch (err) {
    tbody.innerHTML = '<tr><td colspan="5" class="empty-state">Unable to connect to Application Service (:8004).</td></tr>';
  }
}

async function handleApplySubmit(e) {
  e.preventDefault();
  const student_id = parseInt(document.getElementById('apply-student-id').value);
  const internship_id = parseInt(document.getElementById('apply-internship-id').value);

  if (!student_id || !internship_id) {
    showToast('Select both student and internship', 'error');
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
    showToast(`Application #${data.id} recorded (${data.status})`);
    loadApplications();
  } catch (err) {
    showToast(err.message, 'error');
  }
}

async function testInvalidStudentDemo() {
  try {
    const res = await fetch(`${API_URLS.application}/applications`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ student_id: 99999, internship_id: 1 })
    });
    const data = await res.json();
    if (!res.ok) {
      alert(`[Checkpoint 3 Inter-Service Validation Result]\n\nHTTP Status: ${res.status}\nMessage: "${data.detail}"\n\nExplanation: Application Service (:8004) sent a request to Student Service (:8002) to verify student existence. Student #99999 was not found, so the submission was rejected.`);
    } else {
      showToast('Unexpected success for invalid student', 'error');
    }
  } catch (err) {
    showToast(err.message, 'error');
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
    if (!res.ok) throw new Error(data.detail || 'Failed');
    showToast(`Application #${id} status: ${status}`);
    loadApplications();
  } catch (err) {
    showToast(err.message, 'error');
  }
}

async function deleteApplication(id) {
  if (!confirm(`Delete application #${id}?`)) return;
  try {
    const res = await fetch(`${API_URLS.application}/applications/${id}`, { method: 'DELETE' });
    if (!res.ok) throw new Error('Delete failed');
    showToast(`Deleted application #${id}`);
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
  }, 200);
}

// 4. Auth
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
    showToast(`Registered user: ${data.name} (${data.email})`);
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
    showToast(`Authenticated user #${data.user_id}`);
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

document.addEventListener('DOMContentLoaded', () => {
  setupTabs();
  checkServiceHealth();
  setInterval(checkServiceHealth, 8000);

  document.getElementById('student-form')?.addEventListener('submit', handleStudentSubmit);
  document.getElementById('internship-form')?.addEventListener('submit', handleInternshipSubmit);
  document.getElementById('apply-form')?.addEventListener('submit', handleApplySubmit);
  document.getElementById('auth-reg-form')?.addEventListener('submit', handleAuthRegister);
  document.getElementById('auth-login-form')?.addEventListener('submit', handleAuthLogin);
  document.getElementById('search-internships')?.addEventListener('input', handleSearchInternships);

  loadStudents();
});
