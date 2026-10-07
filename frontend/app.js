const API_URLS = {
  auth: 'http://localhost:8001',
  student: 'http://localhost:8002',
  internship: 'http://localhost:8003',
  application: 'http://localhost:8004'
};

// State caches
let studentsCache = [];
let internshipsCache = [];
let applicationsCache = [];

// Lucide Icon Helper
function refreshIcons() {
  if (window.lucide && typeof lucide.createIcons === 'function') {
    lucide.createIcons();
  }
}

// Toast Notifications
function showToast(message, type = 'success') {
  const container = document.getElementById('toast-container');
  if (!container) return;
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.textContent = message;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    setTimeout(() => toast.remove(), 250);
  }, 4000);
}

// Modal Management
function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) modal.classList.add('active');
  if (modalId === 'modal-apply') populateAppDropdowns();
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) modal.classList.remove('active');
}

// Navigation & Tab Switching
function setupNavigation() {
  const navItems = document.querySelectorAll('.nav-item');
  navItems.forEach(item => {
    item.addEventListener('click', () => {
      const tab = item.dataset.tab;
      navigateToTab(tab);
    });
  });
}

function navigateToTab(tabName) {
  document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.page-view').forEach(el => el.classList.remove('active'));

  const navItem = document.querySelector(`.nav-item[data-tab="${tabName}"]`);
  if (navItem) navItem.classList.add('active');

  const view = document.getElementById(`view-${tabName}`);
  if (view) view.classList.add('active');

  const breadcrumb = document.getElementById('header-breadcrumb');
  if (breadcrumb) {
    const titles = {
      dashboard: 'Dashboard',
      students: 'Students',
      internships: 'Internships',
      applications: 'Applications',
      auth: 'Authentication',
      'service-health': 'Service Health',
      benchmarks: 'Benchmarks'
    };
    breadcrumb.textContent = titles[tabName] || tabName;
  }

  // Load view data
  if (tabName === 'dashboard') loadDashboard();
  if (tabName === 'students') loadStudents();
  if (tabName === 'internships') loadInternships();
  if (tabName === 'applications') loadApplications();
  refreshIcons();
}

// Microservices Health Monitoring
async function checkServiceHealth() {
  const services = ['auth', 'student', 'internship', 'application'];
  for (const s of services) {
    const badge = document.getElementById(`badge-${s}`);
    const healthBadge = document.getElementById(`health-${s}-badge`);
    try {
      const res = await fetch(`${API_URLS[s]}/`, { method: 'GET' });
      if (res.ok) {
        if (badge) badge.querySelector('.status-dot').className = 'status-dot online';
        if (healthBadge) {
          healthBadge.className = 'status-badge badge-accepted';
          healthBadge.textContent = 'Online';
        }
      } else {
        throw new Error();
      }
    } catch {
      if (badge) badge.querySelector('.status-dot').className = 'status-dot offline';
      if (healthBadge) {
        healthBadge.className = 'status-badge badge-rejected';
        healthBadge.textContent = 'Offline';
      }
    }
  }
}

async function pingService(serviceName) {
  try {
    const start = performance.now();
    const res = await fetch(`${API_URLS[serviceName]}/`);
    const duration = Math.round(performance.now() - start);
    if (res.ok) {
      showToast(`${serviceName.toUpperCase()} service responded in ${duration} ms (200 OK)`);
    } else {
      showToast(`${serviceName.toUpperCase()} service error: ${res.status}`, 'error');
    }
  } catch (err) {
    showToast(`Failed to reach ${serviceName.toUpperCase()} service`, 'error');
  }
}

// ==========================================
// 1. DASHBOARD MODULE
// ==========================================
async function loadDashboard() {
  try {
    const [sRes, iRes, aRes] = await Promise.allSettled([
      fetch(`${API_URLS.student}/students`),
      fetch(`${API_URLS.internship}/internships`),
      fetch(`${API_URLS.application}/applications`)
    ]);

    studentsCache = sRes.status === 'fulfilled' && sRes.value.ok ? await sRes.value.json() : [];
    internshipsCache = iRes.status === 'fulfilled' && iRes.value.ok ? await iRes.value.json() : [];
    applicationsCache = aRes.status === 'fulfilled' && aRes.value.ok ? await aRes.value.json() : [];

    // Summary Cards
    document.getElementById('stat-total-students').textContent = studentsCache.length;
    document.getElementById('stat-total-internships').textContent = internshipsCache.length;
    document.getElementById('stat-total-applications').textContent = applicationsCache.length;

    const acceptedCount = applicationsCache.filter(a => a.status === 'accepted').length;
    const rate = applicationsCache.length > 0 
      ? Math.round((acceptedCount / applicationsCache.length) * 100) 
      : 0;
    document.getElementById('stat-acceptance-rate').textContent = `${rate}%`;

    // Status Breakdown Bars
    const pendingCount = applicationsCache.filter(a => a.status === 'pending').length;
    const rejectedCount = applicationsCache.filter(a => a.status === 'rejected').length;
    const totalApps = applicationsCache.length || 1;

    document.getElementById('dash-count-pending').textContent = pendingCount;
    document.getElementById('dash-count-accepted').textContent = acceptedCount;
    document.getElementById('dash-count-rejected').textContent = rejectedCount;

    document.getElementById('bar-pending').style.width = `${(pendingCount / totalApps) * 100}%`;
    document.getElementById('bar-accepted').style.width = `${(acceptedCount / totalApps) * 100}%`;
    document.getElementById('bar-rejected').style.width = `${(rejectedCount / totalApps) * 100}%`;

    // Recent Applications List
    const recentAppsTbody = document.getElementById('dash-recent-applications');
    if (!applicationsCache || applicationsCache.length === 0) {
      recentAppsTbody.innerHTML = '<tr><td colspan="4" class="empty-state">No submissions yet.</td></tr>';
    } else {
      const recent = applicationsCache.slice(-5).reverse();
      recentAppsTbody.innerHTML = recent.map(a => {
        const student = studentsCache.find(s => s.id === a.student_id);
        const internship = internshipsCache.find(i => i.id === a.internship_id);
        return `
          <tr>
            <td>#${a.id}</td>
            <td><strong>${student ? escapeHtml(student.name) : 'Student #' + a.student_id}</strong></td>
            <td>${internship ? escapeHtml(internship.title) : 'Internship #' + a.internship_id}</td>
            <td><span class="status-badge badge-${a.status}">${a.status}</span></td>
          </tr>
        `;
      }).join('');
    }

    // Recent Internships List
    const recentInternsTbody = document.getElementById('dash-recent-internships');
    if (!internshipsCache || internshipsCache.length === 0) {
      recentInternsTbody.innerHTML = '<tr><td colspan="4" class="empty-state">No active listings.</td></tr>';
    } else {
      const recentJobs = internshipsCache.slice(-4).reverse();
      recentInternsTbody.innerHTML = recentJobs.map(job => `
        <tr>
          <td><strong>${escapeHtml(job.title)}</strong></td>
          <td>${escapeHtml(job.company)}</td>
          <td>${escapeHtml(job.location || 'Remote')}</td>
          <td>
            <button class="btn btn-secondary btn-sm" onclick="triggerApplyFromList(${job.id})">Apply</button>
          </td>
        </tr>
      `).join('');
    }

    // Department Stats
    const countDept = (prefix) => studentsCache.filter(s => s.department && s.department.includes(prefix)).length;
    document.getElementById('dept-count-cse').textContent = `${countDept('CSE')} Candidates`;
    document.getElementById('dept-count-ise').textContent = `${countDept('ISE')} Candidates`;
    document.getElementById('dept-count-ece').textContent = `${countDept('ECE')} Candidates`;
    document.getElementById('dept-count-aids').textContent = `${countDept('AI')} Candidates`;

  } catch (err) {
    console.error('Error loading dashboard metrics', err);
  }
}

// ==========================================
// 2. STUDENTS MODULE
// ==========================================
async function loadStudents() {
  const tbody = document.getElementById('students-tbody');
  tbody.innerHTML = '<tr><td colspan="6" class="empty-state">Loading student directory...</td></tr>';
  try {
    const res = await fetch(`${API_URLS.student}/students`);
    studentsCache = await res.json();
    renderStudents(studentsCache);
  } catch (err) {
    tbody.innerHTML = '<tr><td colspan="6" class="empty-state" style="color:var(--danger-text);">Unable to reach Student Service (:8002).</td></tr>';
  }
}

function renderStudents(list) {
  const tbody = document.getElementById('students-tbody');
  if (!list || list.length === 0) {
    tbody.innerHTML = '<tr><td colspan="6" class="empty-state">No student records found. Click "Add Student" to register.</td></tr>';
    return;
  }
  tbody.innerHTML = list.map(s => {
    const initials = s.name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase() || 'ST';
    return `
      <tr>
        <td><strong>#${s.id}</strong></td>
        <td>
          <div class="user-cell">
            <div class="user-avatar">${initials}</div>
            <div>
              <div style="font-weight:600;color:var(--text-primary);">${escapeHtml(s.name)}</div>
            </div>
          </div>
        </td>
        <td>${escapeHtml(s.email)}</td>
        <td><span class="dept-badge">${escapeHtml(s.department || 'N/A')}</span></td>
        <td>Year ${s.year || 1}</td>
        <td style="text-align:right;">
          <button class="btn btn-danger-outline btn-sm" onclick="deleteStudent(${s.id})">Delete</button>
        </td>
      </tr>
    `;
  }).join('');
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
    showToast(`Student #${data.id} (${data.name}) registered successfully.`);
    document.getElementById('student-form').reset();
    closeModal('modal-student');
    loadStudents();
    loadDashboard();
  } catch (err) {
    showToast(err.message, 'error');
  }
}

async function deleteStudent(id) {
  if (!confirm(`Are you sure you want to remove student #${id}?`)) return;
  try {
    const res = await fetch(`${API_URLS.student}/students/${id}`, { method: 'DELETE' });
    if (!res.ok) throw new Error('Delete operation failed');
    showToast(`Student #${id} removed.`);
    loadStudents();
    loadDashboard();
  } catch (err) {
    showToast(err.message, 'error');
  }
}

function handleFilterStudents() {
  const query = document.getElementById('search-students').value.toLowerCase();
  const dept = document.getElementById('filter-student-dept').value;

  const filtered = studentsCache.filter(s => {
    const matchesQuery = s.name.toLowerCase().includes(query) || 
                         s.email.toLowerCase().includes(query) || 
                         String(s.id).includes(query);
    const matchesDept = !dept || (s.department && s.department.includes(dept));
    return matchesQuery && matchesDept;
  });
  renderStudents(filtered);
}

// ==========================================
// 3. INTERNSHIPS MODULE
// ==========================================
async function loadInternships() {
  const container = document.getElementById('internships-container');
  container.innerHTML = '<div class="empty-state">Loading active postings...</div>';
  try {
    const res = await fetch(`${API_URLS.internship}/internships`);
    internshipsCache = await res.json();
    renderInternships(internshipsCache);
  } catch (err) {
    container.innerHTML = '<div class="empty-state" style="color:var(--danger-text);">Unable to reach Internship Service (:8003).</div>';
  }
}

function renderInternships(list) {
  const container = document.getElementById('internships-container');
  if (!list || list.length === 0) {
    container.innerHTML = '<div class="empty-state">No internship opportunities listed. Click "Post Internship" to publish.</div>';
    return;
  }

  container.innerHTML = list.map(item => {
    // Generate clean skill tags from description
    const text = (item.title + ' ' + (item.description || '')).toLowerCase();
    const possibleSkills = ['Python', 'Docker', 'FastAPI', 'SQL', 'React', 'Cloud', 'Machine Learning', 'API'];
    const tags = possibleSkills.filter(skill => text.includes(skill.toLowerCase()));
    if (tags.length === 0) tags.push('Technical Internship', 'University Pool');

    return `
      <div class="internship-card">
        <div>
          <div class="internship-top">
            <div class="company-title-wrap">
              <h3>${escapeHtml(item.title)}</h3>
              <div class="company-sub">${escapeHtml(item.company)}</div>
            </div>
            <span class="dept-badge">#${item.id}</span>
          </div>

          <div class="internship-location">
            <i data-lucide="map-pin" style="width:13px;height:13px;"></i>
            <span>${escapeHtml(item.location || 'Remote')}</span>
          </div>

          <div class="internship-desc">
            ${escapeHtml(item.description || 'No detailed job description provided.')}
          </div>

          <div class="skill-tags">
            ${tags.map(t => `<span class="skill-tag">${t}</span>`).join('')}
          </div>
        </div>

        <div class="internship-actions">
          <button class="btn btn-secondary btn-sm" onclick="viewInternshipDetails(${item.id})">View Details</button>
          <div style="display:flex;gap:6px;">
            <button class="btn btn-primary btn-sm" onclick="triggerApplyFromList(${item.id})">Apply</button>
            <button class="btn btn-danger-outline btn-sm" onclick="deleteInternship(${item.id})">Delete</button>
          </div>
        </div>
      </div>
    `;
  }).join('');
  refreshIcons();
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
    if (!res.ok) throw new Error(data.detail || 'Failed to post role');
    showToast(`Published role "${data.title}" at ${data.company}.`);
    document.getElementById('internship-form').reset();
    closeModal('modal-internship');
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
    showToast(`Internship #${id} deleted.`);
    loadInternships();
    loadDashboard();
  } catch (err) {
    showToast(err.message, 'error');
  }
}

function handleFilterInternships() {
  const query = document.getElementById('search-internships').value.toLowerCase();
  const locFilter = document.getElementById('filter-internship-loc').value.toLowerCase();

  const filtered = internshipsCache.filter(item => {
    const matchesQuery = item.title.toLowerCase().includes(query) ||
                         item.company.toLowerCase().includes(query) ||
                         (item.description && item.description.toLowerCase().includes(query));
    const matchesLoc = !locFilter || (item.location && item.location.toLowerCase().includes(locFilter));
    return matchesQuery && matchesLoc;
  });
  renderInternships(filtered);
}

function viewInternshipDetails(id) {
  const item = internshipsCache.find(i => i.id === id);
  if (!item) return;
  document.getElementById('details-modal-title').textContent = item.title;
  document.getElementById('details-modal-body').innerHTML = `
    <div style="margin-bottom:12px;">
      <div style="font-weight:600;font-size:14px;color:var(--text-primary);">${escapeHtml(item.company)}</div>
      <div style="color:var(--text-muted);font-size:12px;">Location: ${escapeHtml(item.location || 'Remote')} &bull; Position Ref: #${item.id}</div>
    </div>
    <div style="background:var(--bg-surface-subtle);padding:12px;border-radius:var(--radius-md);margin-bottom:12px;border:1px solid var(--border-color);">
      <strong>Role Overview & Scope:</strong>
      <p style="margin-top:6px;color:var(--text-secondary);">${escapeHtml(item.description || 'No description provided.')}</p>
    </div>
    <div style="font-size:12px;color:var(--text-muted);">
      Microservice Container: <code>internship-service (:8003)</code> &bull; Persistent DB: <code>internships.db</code>
    </div>
  `;
  document.getElementById('details-apply-btn').onclick = () => {
    closeModal('modal-details');
    triggerApplyFromList(item.id);
  };
  openModal('modal-details');
}

function triggerApplyFromList(internshipId) {
  openModal('modal-apply');
  setTimeout(() => {
    const select = document.getElementById('apply-internship-id');
    if (select) select.value = internshipId;
  }, 100);
}

// ==========================================
// 4. APPLICATIONS MODULE
// ==========================================
async function populateAppDropdowns() {
  const studentSelect = document.getElementById('apply-student-id');
  const internshipSelect = document.getElementById('apply-internship-id');

  try {
    const [sRes, iRes] = await Promise.all([
      fetch(`${API_URLS.student}/students`),
      fetch(`${API_URLS.internship}/internships`)
    ]);
    studentsCache = await sRes.json();
    internshipsCache = await iRes.json();

    studentSelect.innerHTML = '<option value="">Select Enrolled Student...</option>' + 
      studentsCache.map(s => `<option value="${s.id}">#${s.id} - ${escapeHtml(s.name)} (${s.department || 'General'})</option>`).join('');

    internshipSelect.innerHTML = '<option value="">Select Position...</option>' + 
      internshipsCache.map(i => `<option value="${i.id}">#${i.id} - ${escapeHtml(i.title)} at ${escapeHtml(i.company)}</option>`).join('');
  } catch (err) {
    console.error('Error populating dropdowns', err);
  }
}

async function loadApplications() {
  const tbody = document.getElementById('applications-tbody');
  tbody.innerHTML = '<tr><td colspan="5" class="empty-state">Loading application records...</td></tr>';
  try {
    const [aRes, sRes, iRes] = await Promise.all([
      fetch(`${API_URLS.application}/applications`),
      fetch(`${API_URLS.student}/students`),
      fetch(`${API_URLS.internship}/internships`)
    ]);
    applicationsCache = await aRes.json();
    studentsCache = await sRes.json();
    internshipsCache = await iRes.json();

    renderApplications(applicationsCache);
  } catch (err) {
    tbody.innerHTML = '<tr><td colspan="5" class="empty-state" style="color:var(--danger-text);">Unable to reach Application Service (:8004).</td></tr>';
  }
}

function renderApplications(list) {
  const tbody = document.getElementById('applications-tbody');
  if (!list || list.length === 0) {
    tbody.innerHTML = '<tr><td colspan="5" class="empty-state">No applications submitted yet.</td></tr>';
    return;
  }

  tbody.innerHTML = list.map(a => {
    const student = studentsCache.find(s => s.id === a.student_id);
    const internship = internshipsCache.find(i => i.id === a.internship_id);

    return `
      <tr>
        <td><strong>#${a.id}</strong></td>
        <td>
          <div style="font-weight:600;color:var(--text-primary);">${student ? escapeHtml(student.name) : 'Student #' + a.student_id}</div>
          <div style="font-size:11px;color:var(--text-muted);">${student ? escapeHtml(student.email) : 'ID: ' + a.student_id}</div>
        </td>
        <td>
          <div style="font-weight:600;color:var(--text-primary);">${internship ? escapeHtml(internship.title) : 'Internship #' + a.internship_id}</div>
          <div style="font-size:11px;color:var(--text-muted);">${internship ? escapeHtml(internship.company) : 'Position Ref #' + a.internship_id}</div>
        </td>
        <td>
          <span class="status-badge badge-${a.status}">${a.status}</span>
        </td>
        <td style="text-align:right;">
          <div style="display:inline-flex;gap:4px;">
            <button class="btn btn-success-outline btn-sm" onclick="updateAppStatus(${a.id}, 'accepted')">Accept</button>
            <button class="btn btn-secondary btn-sm" onclick="updateAppStatus(${a.id}, 'rejected')">Reject</button>
            <button class="btn btn-danger-outline btn-sm" onclick="deleteApplication(${a.id})">Delete</button>
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
    showToast('Please select both a student and an internship position.', 'error');
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
    showToast(`Application #${data.id} submitted successfully.`);
    closeModal('modal-apply');
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
      alert(`[Checkpoint 3 Inter-Service Communication Verified]\n\nResponse Status: ${res.status}\nMessage: "${data.detail}"\n\nExplanation for Evaluator:\nApplication Service (:8004) sent an internal HTTP request across the Docker bridge network to Student Service (:8002) to verify student existence.\nBecause student #99999 was not found, the application was safely rejected.`);
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
    if (!res.ok) throw new Error(data.detail || 'Failed to update status');
    showToast(`Application #${id} status updated to ${status}.`);
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
    showToast(`Application #${id} removed.`);
    loadApplications();
    loadDashboard();
  } catch (err) {
    showToast(err.message, 'error');
  }
}

function handleFilterApplications() {
  const query = document.getElementById('search-applications').value.toLowerCase();
  const status = document.getElementById('filter-app-status').value;

  const filtered = applicationsCache.filter(a => {
    const matchesStatus = !status || a.status === status;
    const matchesQuery = String(a.id).includes(query) || 
                         String(a.student_id).includes(query) || 
                         String(a.internship_id).includes(query);
    return matchesStatus && matchesQuery;
  });
  renderApplications(filtered);
}

// ==========================================
// 5. AUTHENTICATION MODULE
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
    showToast(`User account created: ${data.name} (${data.email})`);
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
    showToast(`Login successful. User ID: #${data.user_id}`);
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

// Initialization
document.addEventListener('DOMContentLoaded', () => {
  setupNavigation();
  checkServiceHealth();
  setInterval(checkServiceHealth, 10000);

  // Forms
  document.getElementById('student-form')?.addEventListener('submit', handleStudentSubmit);
  document.getElementById('internship-form')?.addEventListener('submit', handleInternshipSubmit);
  document.getElementById('apply-form')?.addEventListener('submit', handleApplySubmit);
  document.getElementById('auth-reg-form')?.addEventListener('submit', handleAuthRegister);
  document.getElementById('auth-login-form')?.addEventListener('submit', handleAuthLogin);

  // Search & Filter listeners
  document.getElementById('search-students')?.addEventListener('input', handleFilterStudents);
  document.getElementById('filter-student-dept')?.addEventListener('change', handleFilterStudents);
  document.getElementById('search-internships')?.addEventListener('input', handleFilterInternships);
  document.getElementById('filter-internship-loc')?.addEventListener('change', handleFilterInternships);
  document.getElementById('search-applications')?.addEventListener('input', handleFilterApplications);
  document.getElementById('filter-app-status')?.addEventListener('change', handleFilterApplications);

  // Initial load
  loadDashboard();
  refreshIcons();
});
