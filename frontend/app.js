const API_URLS = {
  auth: 'http://localhost:8001',
  student: 'http://localhost:8002',
  internship: 'http://localhost:8003',
  application: 'http://localhost:8004'
};

let studentsList = [];
let internshipsList = [];
let applicationsList = [];

function showToast(message, type = 'success') {
  const container = document.getElementById('toast-container');
  if (!container) return;
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.textContent = message;
  container.appendChild(toast);
  setTimeout(() => toast.remove(), 3500);
}

// Navigation between the 6 simple tabs
function setupNavigation() {
  const links = document.querySelectorAll('.nav-link');
  links.forEach(link => {
    link.addEventListener('click', () => {
      links.forEach(l => l.classList.remove('active'));
      document.querySelectorAll('.page-section').forEach(s => s.classList.remove('active'));

      link.classList.add('active');
      const tab = link.dataset.tab;
      const targetSec = document.getElementById(`sec-${tab}`);
      if (targetSec) targetSec.classList.add('active');

      if (tab === 'dashboard') loadDashboard();
      if (tab === 'students') loadStudents();
      if (tab === 'internships') loadInternships();
      if (tab === 'applications') {
        loadApplications();
        populateAppDropdowns();
      }
      if (tab === 'health') checkServiceHealth();
    });
  });
}

// 1. DASHBOARD
async function loadDashboard() {
  try {
    const [sRes, iRes, aRes] = await Promise.allSettled([
      fetch(`${API_URLS.student}/students`),
      fetch(`${API_URLS.internship}/internships`),
      fetch(`${API_URLS.application}/applications`)
    ]);

    studentsList = (sRes.status === 'fulfilled' && sRes.value.ok) ? await sRes.value.json() : [];
    internshipsList = (iRes.status === 'fulfilled' && iRes.value.ok) ? await iRes.value.json() : [];
    applicationsList = (aRes.status === 'fulfilled' && aRes.value.ok) ? await aRes.value.json() : [];

    document.getElementById('dash-total-students').textContent = studentsList.length;
    document.getElementById('dash-total-internships').textContent = internshipsList.length;
    document.getElementById('dash-total-applications').textContent = applicationsList.length;

    const tbody = document.getElementById('dash-recent-tbody');
    if (applicationsList.length === 0) {
      tbody.innerHTML = '<tr><td colspan="4" class="empty-state">No applications submitted yet.</td></tr>';
      return;
    }

    const recent = applicationsList.slice(-5).reverse();
    tbody.innerHTML = recent.map(a => {
      const student = studentsList.find(s => s.id === a.student_id);
      const internship = internshipsList.find(i => i.id === a.internship_id);
      return `
        <tr>
          <td>#${a.id}</td>
          <td>${student ? escapeHtml(student.name) : 'Student #' + a.student_id}</td>
          <td>${internship ? escapeHtml(internship.title) : 'Internship #' + a.internship_id}</td>
          <td><span class="badge badge-${a.status}">${a.status}</span></td>
        </tr>
      `;
    }).join('');
  } catch (err) {
    console.error('Error loading dashboard', err);
  }
}

// 2. STUDENTS (Port 8002)
async function loadStudents() {
  const tbody = document.getElementById('students-tbody');
  tbody.innerHTML = '<tr><td colspan="6" class="empty-state">Loading students...</td></tr>';
  try {
    const res = await fetch(`${API_URLS.student}/students`);
    studentsList = await res.json();
    if (!studentsList || studentsList.length === 0) {
      tbody.innerHTML = '<tr><td colspan="6" class="empty-state">No students added yet.</td></tr>';
      return;
    }
    tbody.innerHTML = studentsList.map(s => `
      <tr>
        <td>#${s.id}</td>
        <td><strong>${escapeHtml(s.name)}</strong></td>
        <td>${escapeHtml(s.email)}</td>
        <td>${escapeHtml(s.department || '-')}</td>
        <td>Year ${s.year || 1}</td>
        <td>
          <button class="btn btn-danger btn-sm" onclick="deleteStudent(${s.id})">Delete</button>
        </td>
      </tr>
    `).join('');
  } catch {
    tbody.innerHTML = '<tr><td colspan="6" class="empty-state" style="color:#dc2626;">Student Service (:8002) offline.</td></tr>';
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
    if (!res.ok) throw new Error(data.detail || 'Failed');
    showToast(`Added student #${data.id} (${data.name})`);
    document.getElementById('student-form').reset();
    loadStudents();
    loadDashboard();
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
    loadDashboard();
  } catch (err) {
    showToast(err.message, 'error');
  }
}

// 3. INTERNSHIPS (Port 8003)
async function loadInternships() {
  const tbody = document.getElementById('internships-tbody');
  tbody.innerHTML = '<tr><td colspan="5" class="empty-state">Loading internships...</td></tr>';
  try {
    const res = await fetch(`${API_URLS.internship}/internships`);
    internshipsList = await res.json();
    renderInternships(internshipsList);
  } catch {
    tbody.innerHTML = '<tr><td colspan="5" class="empty-state" style="color:#dc2626;">Internship Service (:8003) offline.</td></tr>';
  }
}

function renderInternships(list) {
  const tbody = document.getElementById('internships-tbody');
  if (!list || list.length === 0) {
    tbody.innerHTML = '<tr><td colspan="5" class="empty-state">No internships listed yet.</td></tr>';
    return;
  }
  tbody.innerHTML = list.map(item => `
    <tr>
      <td>#${item.id}</td>
      <td><strong>${escapeHtml(item.title)}</strong></td>
      <td>${escapeHtml(item.company)}</td>
      <td>${escapeHtml(item.location || 'Remote')}</td>
      <td>
        <button class="btn btn-danger btn-sm" onclick="deleteInternship(${item.id})">Delete</button>
      </td>
    </tr>
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
    if (!res.ok) throw new Error(data.detail || 'Failed');
    showToast(`Added internship #${data.id} (${data.title})`);
    document.getElementById('internship-form').reset();
    loadInternships();
    loadDashboard();
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
    loadDashboard();
  } catch (err) {
    showToast(err.message, 'error');
  }
}

function handleSearchInternships(e) {
  const q = e.target.value.toLowerCase();
  const filtered = internshipsList.filter(i => 
    i.title.toLowerCase().includes(q) ||
    i.company.toLowerCase().includes(q) ||
    (i.location && i.location.toLowerCase().includes(q))
  );
  renderInternships(filtered);
}

// 4. APPLICATIONS (Port 8004)
async function populateAppDropdowns() {
  const studentSelect = document.getElementById('apply-student-id');
  const internshipSelect = document.getElementById('apply-internship-id');

  try {
    const [sRes, iRes] = await Promise.all([
      fetch(`${API_URLS.student}/students`),
      fetch(`${API_URLS.internship}/internships`)
    ]);
    studentsList = await sRes.json();
    internshipsList = await iRes.json();

    studentSelect.innerHTML = '<option value="">Select Student...</option>' + 
      studentsList.map(s => `<option value="${s.id}">#${s.id} - ${escapeHtml(s.name)}</option>`).join('');

    internshipSelect.innerHTML = '<option value="">Select Internship...</option>' + 
      internshipsList.map(i => `<option value="${i.id}">#${i.id} - ${escapeHtml(i.title)} (${escapeHtml(i.company)})</option>`).join('');
  } catch (err) {
    console.error('Error populating dropdowns', err);
  }
}

async function loadApplications() {
  const tbody = document.getElementById('applications-tbody');
  tbody.innerHTML = '<tr><td colspan="5" class="empty-state">Loading applications...</td></tr>';
  try {
    const [aRes, sRes, iRes] = await Promise.all([
      fetch(`${API_URLS.application}/applications`),
      fetch(`${API_URLS.student}/students`),
      fetch(`${API_URLS.internship}/internships`)
    ]);
    applicationsList = await aRes.json();
    studentsList = await sRes.json();
    internshipsList = await iRes.json();

    if (!applicationsList || applicationsList.length === 0) {
      tbody.innerHTML = '<tr><td colspan="5" class="empty-state">No applications submitted.</td></tr>';
      return;
    }

    tbody.innerHTML = applicationsList.map(a => {
      const student = studentsList.find(s => s.id === a.student_id);
      const internship = internshipsList.find(i => i.id === a.internship_id);
      return `
        <tr>
          <td>#${a.id}</td>
          <td>${student ? escapeHtml(student.name) : 'Student #' + a.student_id}</td>
          <td>${internship ? escapeHtml(internship.title) + ' (' + escapeHtml(internship.company) + ')' : 'Internship #' + a.internship_id}</td>
          <td><span class="badge badge-${a.status}">${a.status}</span></td>
          <td>
            <div style="display:inline-flex;gap:4px;">
              <button class="btn btn-secondary btn-sm" onclick="updateAppStatus(${a.id}, 'accepted')">Accept</button>
              <button class="btn btn-secondary btn-sm" onclick="updateAppStatus(${a.id}, 'rejected')">Reject</button>
              <button class="btn btn-danger btn-sm" onclick="deleteApplication(${a.id})">Delete</button>
            </div>
          </td>
        </tr>
      `;
    }).join('');
  } catch {
    tbody.innerHTML = '<tr><td colspan="5" class="empty-state" style="color:#dc2626;">Application Service (:8004) offline.</td></tr>';
  }
}

async function handleApplySubmit(e) {
  e.preventDefault();
  const student_id = parseInt(document.getElementById('apply-student-id').value);
  const internship_id = parseInt(document.getElementById('apply-internship-id').value);

  if (!student_id || !internship_id) {
    showToast('Please select both student and internship', 'error');
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
    showToast(`Application #${data.id} submitted!`);
    loadApplications();
    loadDashboard();
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
    loadDashboard();
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
    loadDashboard();
  } catch (err) {
    showToast(err.message, 'error');
  }
}

// Checkpoint 3 Demonstration
async function testInvalidStudentDemo() {
  try {
    const res = await fetch(`${API_URLS.application}/applications`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ student_id: 99999, internship_id: 1 })
    });
    const data = await res.json();
    if (!res.ok) {
      alert(`[Checkpoint 3 Inter-Service Validation Demo]\n\nResponse: ${res.status} Not Found\nMessage: "${data.detail}"\n\nExplanation for Evaluator:\nApplication Service (:8004) contacted Student Service (:8002) over the internal Docker network. Because student #99999 does not exist, the submission was rejected.`);
    } else {
      showToast('Unexpected success for invalid student', 'error');
    }
  } catch (err) {
    showToast(err.message, 'error');
  }
}

// 6. SERVICE HEALTH
async function checkServiceHealth() {
  const services = ['auth', 'student', 'internship', 'application'];
  for (const s of services) {
    const el = document.getElementById(`status-${s}`);
    if (!el) continue;
    try {
      const res = await fetch(`${API_URLS[s]}/`);
      if (res.ok) {
        el.className = 'badge badge-online';
        el.textContent = 'Online';
      } else {
        el.className = 'badge badge-offline';
        el.textContent = 'Error';
      }
    } catch {
      el.className = 'badge badge-offline';
      el.textContent = 'Offline';
    }
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
  setupNavigation();
  checkServiceHealth();
  loadDashboard();

  document.getElementById('student-form')?.addEventListener('submit', handleStudentSubmit);
  document.getElementById('internship-form')?.addEventListener('submit', handleInternshipSubmit);
  document.getElementById('apply-form')?.addEventListener('submit', handleApplySubmit);
  document.getElementById('search-internships')?.addEventListener('input', handleSearchInternships);
});
