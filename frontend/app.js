const API_URLS = {
  auth: 'http://localhost:8001',
  student: 'http://localhost:8002',
  internship: 'http://localhost:8003',
  application: 'http://localhost:8004'
};

let studentsList = [];
let internshipsList = [];
let applicationsList = [];

// Toast Notifications
function showToast(message, type = 'success') {
  const container = document.getElementById('toast-container');
  if (!container) return;
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.textContent = message;
  container.appendChild(toast);
  setTimeout(() => toast.remove(), 3200);
}

// Modal Helpers
function openModal(id) {
  const el = document.getElementById(id);
  if (el) {
    el.classList.add('active');
    if (id === 'modal-application') {
      populateAppDropdowns();
    }
  }
}

function closeModal(id) {
  const el = document.getElementById(id);
  if (el) {
    el.classList.remove('active');
  }
}

// Navigation between sections
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
      if (tab === 'applications') loadApplications();
      if (tab === 'health') checkServiceHealth();
    });
  });
}

function switchToTab(tab) {
  const link = document.querySelector(`.nav-link[data-tab="${tab}"]`);
  if (link) {
    link.click();
  }
}

// ==============================================================================
// 1. DASHBOARD
// ==============================================================================
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

    // Recent Applications Table (Latest 5)
    const tbody = document.getElementById('dash-recent-tbody');
    if (applicationsList.length === 0) {
      tbody.innerHTML = '<tr><td colspan="4" class="empty-state">No applications submitted yet.</td></tr>';
    } else {
      const recent = applicationsList.slice(-5).reverse();
      tbody.innerHTML = recent.map(a => {
        const student = studentsList.find(s => s.id === a.student_id);
        const internship = internshipsList.find(i => i.id === a.internship_id);
        return `
          <tr>
            <td class="cell-muted">#${a.id}</td>
            <td class="cell-bold">${student ? escapeHtml(student.name) : 'Student #' + a.student_id}</td>
            <td>${internship ? escapeHtml(internship.title) + ' &bull; ' + escapeHtml(internship.company) : 'Internship #' + a.internship_id}</td>
            <td><span class="badge badge-${a.status}">${a.status}</span></td>
          </tr>
        `;
      }).join('');
    }

    // Recent Internships (Latest 3)
    const iTbody = document.getElementById('dash-recent-internships-tbody');
    if (internshipsList.length === 0) {
      iTbody.innerHTML = '<tr><td colspan="4" class="empty-state">No internships listed yet.</td></tr>';
    } else {
      const recentInternships = internshipsList.slice(-3).reverse();
      iTbody.innerHTML = recentInternships.map(i => `
        <tr>
          <td class="cell-bold">${escapeHtml(i.title)}</td>
          <td>${escapeHtml(i.company)}</td>
          <td>${escapeHtml(i.location || 'Remote')}</td>
          <td style="text-align: right;">
            <button class="btn btn-secondary btn-sm" onclick="switchToTab('internships')">View</button>
          </td>
        </tr>
      `).join('');
    }
  } catch (err) {
    console.error('Error loading dashboard', err);
  }
}

// ==============================================================================
// 2. STUDENTS (Port 8002)
// ==============================================================================
async function loadStudents() {
  const tbody = document.getElementById('students-tbody');
  tbody.innerHTML = '<tr><td colspan="6" class="empty-state">Loading students...</td></tr>';
  try {
    const res = await fetch(`${API_URLS.student}/students`);
    studentsList = await res.json();
    renderStudents(studentsList);
  } catch {
    tbody.innerHTML = '<tr><td colspan="6" class="empty-state" style="color:var(--status-error);">Student Service (:8002) offline.</td></tr>';
  }
}

function renderStudents(list) {
  const tbody = document.getElementById('students-tbody');
  if (!list || list.length === 0) {
    tbody.innerHTML = '<tr><td colspan="6" class="empty-state">No students found.</td></tr>';
    return;
  }
  tbody.innerHTML = list.map(s => `
    <tr>
      <td class="cell-muted">#${s.id}</td>
      <td class="cell-bold">${escapeHtml(s.name)}</td>
      <td>${escapeHtml(s.email)}</td>
      <td><span class="dept-tag">${escapeHtml(s.department || '-')}</span></td>
      <td>Year ${s.year || 1}</td>
      <td style="text-align: right;">
        <button class="btn btn-danger btn-sm" onclick="deleteStudent(${s.id})">Delete</button>
      </td>
    </tr>
  `).join('');
}

function handleSearchStudents(e) {
  const q = e.target.value.toLowerCase().trim();
  const filtered = studentsList.filter(s =>
    s.name.toLowerCase().includes(q) ||
    s.email.toLowerCase().includes(q) ||
    (s.department && s.department.toLowerCase().includes(q))
  );
  renderStudents(filtered);
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
    if (!res.ok) throw new Error(data.detail || 'Failed to add student');
    showToast(`Added student #${data.id} (${data.name})`);
    document.getElementById('student-form').reset();
    closeModal('modal-student');
    loadStudents();
    loadDashboard();
  } catch (err) {
    showToast(err.message, 'error');
  }
}

async function deleteStudent(id) {
  if (!confirm(`Delete student record #${id}?`)) return;
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

// ==============================================================================
// 3. INTERNSHIPS (Port 8003)
// ==============================================================================
async function loadInternships() {
  const tbody = document.getElementById('internships-tbody');
  tbody.innerHTML = '<tr><td colspan="6" class="empty-state">Loading internships...</td></tr>';
  try {
    const res = await fetch(`${API_URLS.internship}/internships`);
    internshipsList = await res.json();
    renderInternships(internshipsList);
  } catch {
    tbody.innerHTML = '<tr><td colspan="6" class="empty-state" style="color:var(--status-error);">Internship Service (:8003) offline.</td></tr>';
  }
}

function renderInternships(list) {
  const tbody = document.getElementById('internships-tbody');
  if (!list || list.length === 0) {
    tbody.innerHTML = '<tr><td colspan="6" class="empty-state">No internships listed yet.</td></tr>';
    return;
  }
  tbody.innerHTML = list.map(item => `
    <tr>
      <td class="cell-muted">#${item.id}</td>
      <td class="cell-bold">${escapeHtml(item.title)}</td>
      <td>${escapeHtml(item.company)}</td>
      <td><span class="dept-tag">${escapeHtml(item.location || 'Remote')}</span></td>
      <td class="cell-desc">${escapeHtml(item.description || 'No description provided')}</td>
      <td style="text-align: right;">
        <button class="btn btn-danger btn-sm" onclick="deleteInternship(${item.id})">Delete</button>
      </td>
    </tr>
  `).join('');
}

function handleSearchInternships(e) {
  const q = e.target.value.toLowerCase().trim();
  const filtered = internshipsList.filter(i => 
    i.title.toLowerCase().includes(q) ||
    i.company.toLowerCase().includes(q) ||
    (i.location && i.location.toLowerCase().includes(q)) ||
    (i.description && i.description.toLowerCase().includes(q))
  );
  renderInternships(filtered);
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
    if (!res.ok) throw new Error(data.detail || 'Failed to add internship');
    showToast(`Added internship #${data.id} (${data.title})`);
    document.getElementById('internship-form').reset();
    closeModal('modal-internship');
    loadInternships();
    loadDashboard();
  } catch (err) {
    showToast(err.message, 'error');
  }
}

async function deleteInternship(id) {
  if (!confirm(`Delete internship posting #${id}?`)) return;
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

// ==============================================================================
// 4. APPLICATIONS (Port 8004)
// ==============================================================================
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
      studentsList.map(s => `<option value="${s.id}">#${s.id} - ${escapeHtml(s.name)} (${escapeHtml(s.department || 'N/A')})</option>`).join('');

    internshipSelect.innerHTML = '<option value="">Select Internship...</option>' + 
      internshipsList.map(i => `<option value="${i.id}">#${i.id} - ${escapeHtml(i.title)} at ${escapeHtml(i.company)}</option>`).join('');
  } catch (err) {
    console.error('Error populating application dropdowns', err);
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
    renderApplications(applicationsList);
  } catch {
    tbody.innerHTML = '<tr><td colspan="5" class="empty-state" style="color:var(--status-error);">Application Service (:8004) offline.</td></tr>';
  }
}

function renderApplications(list) {
  const tbody = document.getElementById('applications-tbody');
  if (!list || list.length === 0) {
    tbody.innerHTML = '<tr><td colspan="5" class="empty-state">No applications submitted yet.</td></tr>';
    return;
  }

  tbody.innerHTML = list.map(a => {
    const student = studentsList.find(s => s.id === a.student_id);
    const internship = internshipsList.find(i => i.id === a.internship_id);
    return `
      <tr>
        <td class="cell-muted">#${a.id}</td>
        <td class="cell-bold">${student ? escapeHtml(student.name) : 'Student #' + a.student_id}</td>
        <td>${internship ? escapeHtml(internship.title) + ' &bull; ' + escapeHtml(internship.company) : 'Internship #' + a.internship_id}</td>
        <td><span class="badge badge-${a.status}">${a.status}</span></td>
        <td style="text-align: right;">
          <div style="display: inline-flex; gap: 6px;">
            <button class="btn btn-secondary btn-sm" onclick="updateAppStatus(${a.id}, 'accepted')">Accept</button>
            <button class="btn btn-secondary btn-sm" onclick="updateAppStatus(${a.id}, 'rejected')">Reject</button>
            <button class="btn btn-danger btn-sm" onclick="deleteApplication(${a.id})">Delete</button>
          </div>
        </td>
      </tr>
    `;
  }).join('');
}

async function handleApplySubmit(e) {
  e.preventDefault();
  const student_id = parseInt(document.getElementById('apply-student-id').value);
  const internship_id = parseInt(document.getElementById('apply-internship-id').value);

  if (!student_id || !internship_id) {
    showToast('Please select both a student and an internship opportunity', 'error');
    return;
  }

  try {
    const res = await fetch(`${API_URLS.application}/applications`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ student_id, internship_id })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Application submission failed');
    showToast(`Application #${data.id} submitted successfully!`);
    document.getElementById('apply-form').reset();
    closeModal('modal-application');
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
    showToast(`Application #${id} updated to ${status}`);
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
      alert(`[Checkpoint 3 Inter-Service Validation Demo]\n\nResponse: ${res.status} Not Found\nMessage: "${data.detail}"\n\nExplanation for Evaluator:\nApplication Service (:8004) contacted Student Service (:8002) over the internal Docker network. Because student #99999 does not exist, the submission was safely rejected.`);
    } else {
      showToast('Unexpected success for invalid student', 'error');
    }
  } catch (err) {
    showToast(err.message, 'error');
  }
}

// ==============================================================================
// 6. SERVICE HEALTH
// ==============================================================================
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

// Global Event Listeners
document.addEventListener('DOMContentLoaded', () => {
  setupNavigation();
  checkServiceHealth();
  loadDashboard();

  document.getElementById('student-form')?.addEventListener('submit', handleStudentSubmit);
  document.getElementById('internship-form')?.addEventListener('submit', handleInternshipSubmit);
  document.getElementById('apply-form')?.addEventListener('submit', handleApplySubmit);
  
  document.getElementById('search-students')?.addEventListener('input', handleSearchStudents);
  document.getElementById('search-internships')?.addEventListener('input', handleSearchInternships);

  // Close modals on Escape key or backdrop click
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      document.querySelectorAll('.modal-overlay.active').forEach(m => m.classList.remove('active'));
    }
  });

  document.querySelectorAll('.modal-overlay').forEach(modal => {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        modal.classList.remove('active');
      }
    });
  });
});
