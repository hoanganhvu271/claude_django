// API Gateway URL
const API_BASE_URL = 'http://localhost:8000/api/v1';

// Global variables
let currentUser = null;
let authToken = null;
let allAppointments = [];
let allDoctors = [];
let allHealthRecords = [];
let allAllergies = [];
let currentPatientId = null;

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    // Check if user is already logged in
    const token = localStorage.getItem('authToken');
    if (token) {
        authToken = token;
        currentUser = JSON.parse(localStorage.getItem('currentUser') || '{}');
        showLoggedInState();
    }

    // Set minimum date for appointment booking (today)
    const today = new Date().toISOString().split('T')[0];
    const appointmentDate = document.getElementById('appointmentDate');
    if (appointmentDate) {
        appointmentDate.min = today;
    }

    // Load doctors for appointment booking
    loadDoctors();

    // Set up form handlers
    setupFormHandlers();
});

// Show/hide panels
function showPanel(panelName) {
    // Hide all panels
    const panels = document.querySelectorAll('.content-panel');
    panels.forEach(panel => panel.classList.remove('active'));

    // Hide all nav pills active state
    const navPills = document.querySelectorAll('.nav-pill');
    navPills.forEach(pill => pill.classList.remove('active'));

    // Show selected panel
    const targetPanel = document.getElementById(panelName);
    const targetNavPill = document.querySelector(`[onclick="showPanel('${panelName}')"]`);
    
    if (targetPanel) {
        targetPanel.classList.add('active');
    }
    if (targetNavPill) {
        targetNavPill.classList.add('active');
    }

    // Load data based on panel
    if (panelName === 'dashboard') {
        loadDashboard();
    } else if (panelName === 'appointments') {
        loadAppointments();
    } else if (panelName === 'health-records') {
        loadHealthRecords();
    }
}

// Setup form handlers
function setupFormHandlers() {
    // Login form
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }

    // Register form
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
    }

    // Book appointment form
    const bookAppointmentForm = document.getElementById('bookAppointmentForm');
    if (bookAppointmentForm) {
        bookAppointmentForm.addEventListener('submit', handleBookAppointment);
    }
}

// Handle login
async function handleLogin(e) {
    e.preventDefault();
    
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;
    const alertDiv = document.getElementById('loginAlert');

    try {
        showAlert(alertDiv, 'Đang đăng nhập...', 'info');
        
        const response = await fetch(`${API_BASE_URL}/users/login/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (response.ok) {
            authToken = data.token;
            currentUser = data.user;
            currentPatientId = data.user.id;
            
            // Save to localStorage
            localStorage.setItem('authToken', authToken);
            localStorage.setItem('currentUser', JSON.stringify(currentUser));
            
            // Get patient ID if user is a patient
            if (currentUser.role === 'patient') {
                await loadCurrentPatientId();
            }
            
            showAlert(alertDiv, 'Đăng nhập thành công!', 'success');
            
            setTimeout(() => {
                showLoggedInState();
                showPanel('dashboard');
            }, 1000);
        } else {
            showAlert(alertDiv, data.error || 'Đăng nhập thất bại', 'error');
        }
    } catch (error) {
        console.error('Login error:', error);
        showAlert(alertDiv, 'Lỗi kết nối. Vui lòng thử lại.', 'error');
    }
}

// Load current patient ID
async function loadCurrentPatientId() {
    try {
        const response = await fetch(`${API_BASE_URL}/patients/`, {
            headers: {
                'Authorization': `Token ${authToken}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const patients = await response.json();
            const currentPatient = patients.find(p => p.user_id === currentUser.id);
            if (currentPatient) {
                currentPatientId = currentPatient.id;
            }
        }
    } catch (error) {
        console.error('Error loading patient ID:', error);
    }
}

// Handle register
async function handleRegister(e) {
    e.preventDefault();
    
    const formData = {
        username: document.getElementById('username').value,
        email: document.getElementById('email').value,
        password: document.getElementById('password').value,
        password_confirm: document.getElementById('password_confirm').value,
        phone: document.getElementById('phone').value,
        role: document.getElementById('role').value
    };
    
    const alertDiv = document.getElementById('registerAlert');

    // Validate password confirmation
    if (formData.password !== formData.password_confirm) {
        showAlert(alertDiv, 'Mật khẩu xác nhận không khớp', 'error');
        return;
    }

    try {
        showAlert(alertDiv, 'Đang tạo tài khoản...', 'info');
        
        const response = await fetch(`${API_BASE_URL}/users/register/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (response.ok) {
            showAlert(alertDiv, 'Đăng ký thành công! Vui lòng đăng nhập.', 'success');
            
            // Clear form
            document.getElementById('registerForm').reset();
            
            setTimeout(() => {
                showPanel('login');
            }, 2000);
        } else {
            const errorMessage = typeof data === 'object' ? 
                Object.values(data).flat().join(', ') : 
                (data.error || 'Đăng ký thất bại');
            showAlert(alertDiv, errorMessage, 'error');
        }
    } catch (error) {
        console.error('Register error:', error);
        showAlert(alertDiv, 'Lỗi kết nối. Vui lòng thử lại.', 'error');
    }
}

// Show logged in state
function showLoggedInState() {
    // Show dashboard and management tabs
    document.getElementById('dashboardTab').style.display = 'block';
    document.getElementById('appointmentsTab').style.display = 'block';
    document.getElementById('bookTab').style.display = 'block';
    document.getElementById('healthRecordsTab').style.display = 'block';
    
    // Hide login/register tabs
    const loginTab = document.querySelector('[onclick="showPanel(\'login\')"]');
    const registerTab = document.querySelector('[onclick="showPanel(\'register\')"]');
    if (loginTab) loginTab.style.display = 'none';
    if (registerTab) registerTab.style.display = 'none';
}

// Logout
function logout() {
    if (confirm('Bạn có chắc chắn muốn đăng xuất?')) {
        authToken = null;
        currentUser = null;
        currentPatientId = null;
        localStorage.removeItem('authToken');
        localStorage.removeItem('currentUser');
        
        // Show login/register tabs
        const loginTab = document.querySelector('[onclick="showPanel(\'login\')"]');
        const registerTab = document.querySelector('[onclick="showPanel(\'register\')"]');
        if (loginTab) loginTab.style.display = 'block';
        if (registerTab) registerTab.style.display = 'block';
        
        // Hide dashboard tabs
        document.getElementById('dashboardTab').style.display = 'none';
        document.getElementById('appointmentsTab').style.display = 'none';
        document.getElementById('bookTab').style.display = 'none';
        document.getElementById('healthRecordsTab').style.display = 'none';
        
        // Go to login panel
        showPanel('login');
    }
}

// Load dashboard data
async function loadDashboard() {
    if (!currentUser) return;
    
    // Update user info
    const userInfo = document.getElementById('userInfo');
    userInfo.innerHTML = `
        <h3>👋 Chào mừng, ${currentUser.username}!</h3>
        <p><strong>Email:</strong> ${currentUser.email}</p>
        <p><strong>Vai trò:</strong> ${getRoleDisplayName(currentUser.role)}</p>
        <p><strong>Số điện thoại:</strong> ${currentUser.phone || 'Chưa cập nhật'}</p>
    `;
    
    // Load appointment statistics
    await loadAppointmentStats();
}

// Get role display name
function getRoleDisplayName(role) {
    const roleMap = {
        'patient': 'Bệnh nhân',
        'doctor': 'Bác sĩ',
        'nurse': 'Y tá',
        'admin': 'Quản trị viên',
        'pharmacist': 'Dược sĩ',
        'lab_tech': 'Kỹ thuật viên xét nghiệm'
    };
    return roleMap[role] || role;
}

// Load appointment statistics
async function loadAppointmentStats() {
    try {
        await loadAppointments(false); // Load without showing alerts
        
        const today = new Date().toISOString().split('T')[0];
        const todayAppointments = allAppointments.filter(apt => 
            apt.appointment_date === today
        );
        
        const upcomingAppointments = allAppointments.filter(apt => 
            new Date(apt.appointment_date) > new Date() && 
            apt.status !== 'cancelled'
        );
        
        document.getElementById('todayAppointments').textContent = todayAppointments.length;
        document.getElementById('upcomingAppointments').textContent = upcomingAppointments.length;
    } catch (error) {
        console.error('Error loading appointment stats:', error);
    }
}

// Load doctors
async function loadDoctors() {
    try {
        const response = await fetch(`${API_BASE_URL}/doctors/`, {
            headers: {
                'Authorization': authToken ? `Token ${authToken}` : '',
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const doctors = await response.json();
            allDoctors = doctors;
            
            const doctorSelect = document.getElementById('doctorSelect');
            doctorSelect.innerHTML = '<option value="">Chọn bác sĩ</option>';
            
            doctors.forEach(doctor => {
                const option = document.createElement('option');
                option.value = doctor.id;
                option.textContent = `BS. ${doctor.first_name} ${doctor.last_name} - ${doctor.specialization}`;
                option.dataset.fee = doctor.consultation_fee;
                doctorSelect.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error loading doctors:', error);
    }
}

// Handle book appointment
async function handleBookAppointment(e) {
    e.preventDefault();
    
    if (!currentUser) {
        alert('Vui lòng đăng nhập để đặt lịch hẹn');
        return;
    }
    
    const formData = {
        patient_id: currentUser.id,
        doctor_id: parseInt(document.getElementById('doctorSelect').value),
        appointment_date: document.getElementById('appointmentDate').value,
        appointment_time: document.getElementById('appointmentTime').value,
        duration_minutes: parseInt(document.getElementById('duration').value),
        reason: document.getElementById('reason').value,
        notes: document.getElementById('notes').value,
        status: 'scheduled'
    };
    
    const alertDiv = document.getElementById('bookAlert');

    try {
        showAlert(alertDiv, 'Đang đặt lịch hẹn...', 'info');
        
        const response = await fetch(`${API_BASE_URL}/appointments/`, {
            method: 'POST',
            headers: {
                'Authorization': `Token ${authToken}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (response.ok) {
            showAlert(alertDiv, 'Đặt lịch hẹn thành công!', 'success');
            
            // Clear form
            document.getElementById('bookAppointmentForm').reset();
            
            // Reload appointments if on appointments panel
            if (document.getElementById('appointments').classList.contains('active')) {
                loadAppointments();
            }
        } else {
            const errorMessage = typeof data === 'object' ? 
                Object.values(data).flat().join(', ') : 
                (data.error || 'Đặt lịch hẹn thất bại');
            showAlert(alertDiv, errorMessage, 'error');
        }
    } catch (error) {
        console.error('Book appointment error:', error);
        showAlert(alertDiv, 'Lỗi kết nối. Vui lòng thử lại.', 'error');
    }
}

// Load appointments
async function loadAppointments(showAlerts = true) {
    if (!currentUser) return;
    
    const alertDiv = document.getElementById('appointmentsAlert');
    const appointmentsList = document.getElementById('appointmentsList');
    
    if (showAlerts) {
        appointmentsList.innerHTML = `
            <div class="loading">
                <div class="spinner"></div>
                <p>Đang tải danh sách lịch hẹn...</p>
            </div>
        `;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/appointments/`, {
            headers: {
                'Authorization': `Token ${authToken}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const appointments = await response.json();
            allAppointments = appointments;
            displayAppointments(appointments);
            
            if (showAlerts) {
                showAlert(alertDiv, `Đã tải ${appointments.length} lịch hẹn`, 'success');
            }
        } else {
            const data = await response.json();
            if (showAlerts) {
                showAlert(alertDiv, data.error || 'Không thể tải danh sách lịch hẹn', 'error');
            }
            appointmentsList.innerHTML = '<p>Không thể tải danh sách lịch hẹn</p>';
        }
    } catch (error) {
        console.error('Error loading appointments:', error);
        if (showAlerts) {
            showAlert(alertDiv, 'Lỗi kết nối. Vui lòng thử lại.', 'error');
        }
        appointmentsList.innerHTML = '<p>Lỗi kết nối</p>';
    }
}

// Display appointments
function displayAppointments(appointments) {
    const appointmentsList = document.getElementById('appointmentsList');
    
    if (appointments.length === 0) {
        appointmentsList.innerHTML = '<p>Không có lịch hẹn nào.</p>';
        return;
    }
    
    appointmentsList.innerHTML = appointments.map(appointment => {
        const doctor = allDoctors.find(d => d.id === appointment.doctor_id);
        const doctorName = doctor ? 
            `BS. ${doctor.first_name} ${doctor.last_name}` : 
            `Bác sĩ ID: ${appointment.doctor_id}`;
        
        const appointmentDate = new Date(appointment.appointment_date).toLocaleDateString('vi-VN');
        const isUpcoming = new Date(appointment.appointment_date) > new Date();
        
        return `
            <div class="appointment-card">
                <div class="appointment-header">
                    <div class="appointment-date">${appointmentDate} - ${appointment.appointment_time}</div>
                    <div class="status-badge status-${appointment.status}">${getStatusDisplayName(appointment.status)}</div>
                </div>
                <div class="appointment-doctor">${doctorName}</div>
                <div class="appointment-reason">${appointment.reason}</div>
                ${appointment.notes ? `<div class="appointment-notes"><strong>Ghi chú:</strong> ${appointment.notes}</div>` : ''}
                <div class="doctor-info">
                    <strong>Chuyên khoa:</strong> ${doctor ? doctor.specialization : 'Không xác định'}<br>
                    <strong>Thời gian:</strong> ${appointment.duration_minutes} phút
                </div>
                <div class="appointment-actions">
                    ${isUpcoming && appointment.status === 'scheduled' ? 
                        `<button class="btn btn-danger" onclick="cancelAppointment(${appointment.id})">Hủy lịch hẹn</button>` : 
                        ''
                    }
                    <button class="btn btn-secondary" onclick="viewAppointmentDetails(${appointment.id})">Xem chi tiết</button>
                </div>
            </div>
        `;
    }).join('');
}

// Get status display name
function getStatusDisplayName(status) {
    const statusMap = {
        'scheduled': 'Đã lên lịch',
        'confirmed': 'Đã xác nhận',
        'completed': 'Hoàn thành',
        'cancelled': 'Đã hủy',
        'no_show': 'Không đến'
    };
    return statusMap[status] || status;
}

// Filter appointments
function filterAppointments(status) {
    let filteredAppointments = allAppointments;
    
    if (status !== 'all') {
        filteredAppointments = allAppointments.filter(apt => apt.status === status);
    }
    
    displayAppointments(filteredAppointments);
}

// Cancel appointment
async function cancelAppointment(appointmentId) {
    if (!confirm('Bạn có chắc chắn muốn hủy lịch hẹn này?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/appointments/${appointmentId}/`, {
            method: 'PUT',
            headers: {
                'Authorization': `Token ${authToken}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ status: 'cancelled' })
        });

        if (response.ok) {
            showAlert(document.getElementById('appointmentsAlert'), 'Đã hủy lịch hẹn thành công', 'success');
            loadAppointments();
        } else {
            const data = await response.json();
            showAlert(document.getElementById('appointmentsAlert'), data.error || 'Không thể hủy lịch hẹn', 'error');
        }
    } catch (error) {
        console.error('Error cancelling appointment:', error);
        showAlert(document.getElementById('appointmentsAlert'), 'Lỗi kết nối. Vui lòng thử lại.', 'error');
    }
}

// View appointment details
function viewAppointmentDetails(appointmentId) {
    const appointment = allAppointments.find(apt => apt.id === appointmentId);
    if (!appointment) return;
    
    const doctor = allDoctors.find(d => d.id === appointment.doctor_id);
    const doctorName = doctor ? 
        `BS. ${doctor.first_name} ${doctor.last_name}` : 
        `Bác sĩ ID: ${appointment.doctor_id}`;
    
    const appointmentDate = new Date(appointment.appointment_date).toLocaleDateString('vi-VN');
    
    alert(`Chi tiết lịch hẹn:
    
Ngày: ${appointmentDate}
Giờ: ${appointment.appointment_time}
Bác sĩ: ${doctorName}
Chuyên khoa: ${doctor ? doctor.specialization : 'Không xác định'}
Thời gian: ${appointment.duration_minutes} phút
Lý do: ${appointment.reason}
Ghi chú: ${appointment.notes || 'Không có'}
Trạng thái: ${getStatusDisplayName(appointment.status)}
Ngày tạo: ${new Date(appointment.created_at).toLocaleDateString('vi-VN')}`);
}

// Load health records
async function loadHealthRecords(showAlerts = true) {
    if (!currentUser || !currentPatientId) {
        console.warn('Không có người dùng hoặc ID bệnh nhân hiện tại', currentUser, currentPatientId);
        const alertDiv = document.getElementById('healthRecordsAlert');
        showAlert(alertDiv, 'Không thể tải hồ sơ sức khỏe. Vui lòng đăng nhập lại.', 'error');
        return;
    }
    
    const alertDiv = document.getElementById('healthRecordsAlert');
    const healthRecordsList = document.getElementById('healthRecordsList');
    
    if (showAlerts) {
        healthRecordsList.innerHTML = `
            <div class="loading">
                <div class="spinner"></div>
                <p>Đang tải hồ sơ sức khỏe...</p>
            </div>
        `;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/patients/${currentPatientId}/health-records/`, {
            headers: {
                'Authorization': `Token ${authToken}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const healthRecords = await response.json();
            allHealthRecords = healthRecords;
            displayHealthRecords(healthRecords);
            
            if (showAlerts) {
                showAlert(alertDiv, `Đã tải ${healthRecords.length} hồ sơ sức khỏe`, 'success');
            }
        } else {
            const data = await response.json();
            if (showAlerts) {
                showAlert(alertDiv, data.error || 'Không thể tải hồ sơ sức khỏe', 'error');
            }
            healthRecordsList.innerHTML = '<p>Không thể tải hồ sơ sức khỏe</p>';
        }
    } catch (error) {
        console.error('Error loading health records:', error);
        if (showAlerts) {
            showAlert(alertDiv, 'Lỗi kết nối. Vui lòng thử lại.', 'error');
        }
        healthRecordsList.innerHTML = '<p>Lỗi kết nối</p>';
    }
}

// Display health records
function displayHealthRecords(healthRecords) {
    const healthRecordsList = document.getElementById('healthRecordsList');
    
    if (healthRecords.length === 0) {
        healthRecordsList.innerHTML = '<p>Không có hồ sơ sức khỏe nào.</p>';
        return;
    }
    
    healthRecordsList.innerHTML = healthRecords.map(record => {
        const doctor = allDoctors.find(d => d.id === record.doctor_id);
        const doctorName = doctor ? 
            `BS. ${doctor.first_name} ${doctor.last_name}` : 
            `Bác sĩ ID: ${record.doctor_id}`;
        
        const visitDate = new Date(record.visit_date).toLocaleDateString('vi-VN');
        const visitTime = new Date(record.visit_date).toLocaleTimeString('vi-VN', {
            hour: '2-digit',
            minute: '2-digit'
        });
        
        return `
            <div class="health-record-card">
                <div class="health-record-header">
                    <div class="health-record-date">${visitDate} - ${visitTime}</div>
                </div>
                <div class="health-record-doctor">👨‍⚕️ ${doctorName}</div>
                <div class="health-record-complaint">
                    <strong>Lý do khám:</strong> ${record.chief_complaint}
                </div>
                <div class="health-record-diagnosis">
                    <strong>Chẩn đoán:</strong> ${record.diagnosis}
                </div>
                <div class="health-record-actions">
                    <button class="btn btn-info" onclick="viewHealthRecordDetails(${record.id})">Xem chi tiết</button>
                </div>
            </div>
        `;
    }).join('');
}

// View health record details
function viewHealthRecordDetails(recordId) {
    const record = allHealthRecords.find(r => r.id === recordId);
    if (!record) return;
    
    const doctor = allDoctors.find(d => d.id === record.doctor_id);
    const doctorName = doctor ? 
        `BS. ${doctor.first_name} ${doctor.last_name}` : 
        `Bác sĩ ID: ${record.doctor_id}`;
    
    const visitDate = new Date(record.visit_date).toLocaleDateString('vi-VN');
    const visitTime = new Date(record.visit_date).toLocaleTimeString('vi-VN', {
        hour: '2-digit',
        minute: '2-digit'
    });

    // Show modal with detailed information
    const modal = document.getElementById('healthRecordModal');
    const modalBody = document.getElementById('healthRecordModalBody');
    
    modalBody.innerHTML = `
        <div class="detail-section">
            <h4>📅 Thông tin khám</h4>
            <p><strong>Ngày khám:</strong> ${visitDate} lúc ${visitTime}</p>
            <p><strong>Bác sĩ khám:</strong> ${doctorName}</p>
            <p><strong>Chuyên khoa:</strong> ${doctor ? doctor.specialization : 'Không xác định'}</p>
        </div>
        
        <div class="detail-section">
            <h4>🗣️ Triệu chứng</h4>
            <p><strong>Lý do khám:</strong> ${record.chief_complaint}</p>
            <p><strong>Tiền sử bệnh:</strong> ${record.history_present_illness}</p>
        </div>
        
        <div class="detail-section">
            <h4>🔍 Khám lâm sàng</h4>
            <p>${record.physical_examination}</p>
        </div>
        
        <div class="detail-section">
            <h4>⚕️ Chẩn đoán</h4>
            <p>${record.diagnosis}</p>
        </div>
        
        <div class="detail-section">
            <h4>💊 Phương án điều trị</h4>
            <p>${record.treatment_plan}</p>
        </div>
        
        ${record.notes ? `
            <div class="detail-section">
                <h4>📝 Ghi chú thêm</h4>
                <p>${record.notes}</p>
            </div>
        ` : ''}
        
        ${record.vital_signs && record.vital_signs.length > 0 ? `
            <div class="detail-section">
                <h4>📊 Chỉ số sinh hiệu</h4>
                <div class="vital-signs-grid">
                    ${record.vital_signs.map(vs => `
                        ${vs.temperature ? `
                            <div class="vital-sign-item">
                                <div class="vital-sign-value">${vs.temperature}°C</div>
                                <div class="vital-sign-label">Nhiệt độ</div>
                            </div>
                        ` : ''}
                        ${vs.blood_pressure_systolic && vs.blood_pressure_diastolic ? `
                            <div class="vital-sign-item">
                                <div class="vital-sign-value">${vs.blood_pressure_systolic}/${vs.blood_pressure_diastolic}</div>
                                <div class="vital-sign-label">Huyết áp (mmHg)</div>
                            </div>
                        ` : ''}
                        ${vs.heart_rate ? `
                            <div class="vital-sign-item">
                                <div class="vital-sign-value">${vs.heart_rate}</div>
                                <div class="vital-sign-label">Nhịp tim (lần/phút)</div>
                            </div>
                        ` : ''}
                        ${vs.respiratory_rate ? `
                            <div class="vital-sign-item">
                                <div class="vital-sign-value">${vs.respiratory_rate}</div>
                                <div class="vital-sign-label">Nhịp thở (lần/phút)</div>
                            </div>
                        ` : ''}
                        ${vs.weight ? `
                            <div class="vital-sign-item">
                                <div class="vital-sign-value">${vs.weight} kg</div>
                                <div class="vital-sign-label">Cân nặng</div>
                            </div>
                        ` : ''}
                        ${vs.height ? `
                            <div class="vital-sign-item">
                                <div class="vital-sign-value">${vs.height} cm</div>
                                <div class="vital-sign-label">Chiều cao</div>
                            </div>
                        ` : ''}
                    `).join('')}
                </div>
            </div>
        ` : ''}
    `;
    
    modal.style.display = 'block';
}

// Close health record modal
function closeHealthRecordModal() {
    const modal = document.getElementById('healthRecordModal');
    modal.style.display = 'none';
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('healthRecordModal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
}

// Load allergies
async function loadAllergies() {
    if (!currentUser || !currentPatientId) {
        const alertDiv = document.getElementById('healthRecordsAlert');
        showAlert(alertDiv, 'Không thể tải thông tin dị ứng.', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/patients/${currentPatientId}/allergies/`, {
            headers: {
                'Authorization': `Token ${authToken}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const allergies = await response.json();
            allAllergies = allergies;
            displayAllergies(allergies);
            
            // Show allergies section
            document.getElementById('allergiesSection').style.display = 'block';
        } else {
            const data = await response.json();
            showAlert(document.getElementById('healthRecordsAlert'), data.error || 'Không thể tải thông tin dị ứng', 'error');
        }
    } catch (error) {
        console.error('Error loading allergies:', error);
        showAlert(document.getElementById('healthRecordsAlert'), 'Lỗi kết nối khi tải thông tin dị ứng.', 'error');
    }
}

// Display allergies
function displayAllergies(allergies) {
    const allergiesList = document.getElementById('allergiesList');
    
    if (allergies.length === 0) {
        allergiesList.innerHTML = '<p>Không có thông tin dị ứng được ghi nhận.</p>';
        return;
    }
    
    allergiesList.innerHTML = allergies.map(allergy => {
        return `
            <div class="allergy-card">
                <div class="allergy-header">
                    <div class="allergy-name">⚠️ ${allergy.allergen}</div>
                    <div class="severity-badge severity-${allergy.severity}">
                        ${getSeverityDisplayName(allergy.severity)}
                    </div>
                </div>
                <div class="allergy-reaction">
                    <strong>Phản ứng:</strong> ${allergy.reaction}
                </div>
            </div>
        `;
    }).join('');
}

// Get severity display name
function getSeverityDisplayName(severity) {
    const severityMap = {
        'mild': 'Nhẹ',
        'moderate': 'Trung bình',
        'severe': 'Nặng'
    };
    return severityMap[severity] || severity;
}

// Show alert
function showAlert(container, message, type) {
    if (!container) return;
    
    container.innerHTML = `
        <div class="alert alert-${type}">
            ${message}
        </div>
    `;
    
    // Auto hide success alerts after 3 seconds
    if (type === 'success') {
        setTimeout(() => {
            if (container.innerHTML.includes(message)) {
                container.innerHTML = '';
            }
        }, 3000);
    }
}

// Doctor selection change handler
document.addEventListener('DOMContentLoaded', function() {
    const doctorSelect = document.getElementById('doctorSelect');
    if (doctorSelect) {
        doctorSelect.addEventListener('change', function() {
            const selectedOption = this.options[this.selectedIndex];
            if (selectedOption.dataset.fee) {
                const fee = parseFloat(selectedOption.dataset.fee);
                const doctorInfo = document.querySelector('.doctor-info');
                if (doctorInfo) {
                    doctorInfo.remove();
                }
                
                if (fee > 0) {
                    const infoDiv = document.createElement('div');
                    infoDiv.className = 'doctor-info';
                    infoDiv.innerHTML = `<strong>Phí khám:</strong> ${fee.toLocaleString('vi-VN')} VND`;
                    this.parentNode.appendChild(infoDiv);
                }
            }
        });
    }
});

// Auto-refresh data every 30 seconds when on respective panels
setInterval(() => {
    if (authToken) {
        if (document.getElementById('appointments').classList.contains('active')) {
            loadAppointments(false);
        }
        if (document.getElementById('health-records').classList.contains('active')) {
            loadHealthRecords(false);
        }
    }
}, 30000);