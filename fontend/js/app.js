// API Gateway URL
const API_BASE_URL = 'http://localhost:8000/api/v1';

// Global variables
let currentUser = null;
let authToken = null;
let allAppointments = [];
let allDoctors = [];

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
            
            // Save to localStorage
            localStorage.setItem('authToken', authToken);
            localStorage.setItem('currentUser', JSON.stringify(currentUser));
            
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

// Auto-refresh appointments every 30 seconds when on appointments panel
setInterval(() => {
    if (document.getElementById('appointments').classList.contains('active') && authToken) {
        loadAppointments(false);
    }
}, 30000);