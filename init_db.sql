-- Hệ thống Y tế Microservices - Thiết lập Database và Dữ liệu Mẫu
-- Chạy script này để tạo databases và thêm dữ liệu mẫu

-- ===========================================
-- 1. TẠO CÁC DATABASE
-- ===========================================

CREATE DATABASE IF NOT EXISTS user_service_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS patient_service_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS doctor_service_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS nurse_service_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS appointment_service_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS health_record_service_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS medication_service_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS laboratory_service_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS pharmacy_service_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS invoice_service_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS payment_service_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS notification_service_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS insurance_service_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS chatbot_service_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- ===========================================
-- 2. DỮ LIỆU DỊCH VỤ NGƯỜI DÙNG
-- ===========================================

USE user_service_db;

-- Dữ liệu người dùng mẫu
INSERT INTO user_service_app_user (username, email, first_name, last_name, password, phone, role, is_verified, is_active, is_staff, is_superuser, date_joined, created_at, updated_at) VALUES
('admin', 'admin@benhvien.vn', 'Quản trị', 'Hệ thống', 'pbkdf2_sha256$600000$random$hashedpassword', '0901234567', 'admin', 1, 1, 1, 1, NOW(), NOW(), NOW()),
('bs_nguyen', 'bs.nguyen@benhvien.vn', 'Nguyễn Văn', 'Minh', 'pbkdf2_sha256$600000$random$hashedpassword', '0901234568', 'doctor', 1, 1, 0, 0, NOW(), NOW(), NOW()),
('bs_tran', 'bs.tran@benhvien.vn', 'Trần Thị', 'Hoa', 'pbkdf2_sha256$600000$random$hashedpassword', '0901234569', 'doctor', 1, 1, 0, 0, NOW(), NOW(), NOW()),
('bs_le', 'bs.le@benhvien.vn', 'Lê Minh', 'Tuấn', 'pbkdf2_sha256$600000$random$hashedpassword', '0901234570', 'doctor', 1, 1, 0, 0, NOW(), NOW(), NOW()),
('yd_pham', 'yd.pham@benhvien.vn', 'Phạm Thị', 'Lan', 'pbkdf2_sha256$600000$random$hashedpassword', '0901234571', 'nurse', 1, 1, 0, 0, NOW(), NOW(), NOW()),
('yd_hoang', 'yd.hoang@benhvien.vn', 'Hoàng Thị', 'Mai', 'pbkdf2_sha256$600000$random$hashedpassword', '0901234572', 'nurse', 1, 1, 0, 0, NOW(), NOW(), NOW()),
('bn_duc', 'bn.duc@email.com', 'Nguyễn Văn', 'Đức', 'pbkdf2_sha256$600000$random$hashedpassword', '0987654321', 'patient', 1, 1, 0, 0, NOW(), NOW(), NOW()),
('bn_linh', 'bn.linh@email.com', 'Trần Thị', 'Linh', 'pbkdf2_sha256$600000$random$hashedpassword', '0987654322', 'patient', 1, 1, 0, 0, NOW(), NOW(), NOW()),
('bn_nam', 'bn.nam@email.com', 'Lê Văn', 'Nam', 'pbkdf2_sha256$600000$random$hashedpassword', '0987654323', 'patient', 1, 1, 0, 0, NOW(), NOW(), NOW()),
('dt_vu', 'dt.vu@benhvien.vn', 'Vũ Minh', 'Hải', 'pbkdf2_sha256$600000$random$hashedpassword', '0901234573', 'pharmacist', 1, 1, 0, 0, NOW(), NOW(), NOW()),
('xn_ly', 'xn.ly@benhvien.vn', 'Lý Thị', 'Thu', 'pbkdf2_sha256$600000$random$hashedpassword', '0901234574', 'lab_tech', 1, 1, 0, 0, NOW(), NOW(), NOW());

-- ===========================================
-- 3. DỮ LIỆU DỊCH VỤ BỆNH NHÂN
-- ===========================================

USE patient_service_db;

INSERT INTO patient_service_app_patient (user_id, first_name, last_name, date_of_birth, gender, blood_type, address, emergency_contact_name, emergency_contact_phone, insurance_number, allergies, created_at, updated_at) VALUES
(7, 'Nguyễn Văn', 'Đức', '1985-06-15', 'M', 'O+', '123 Đường Lê Lợi, Quận 1, TP.HCM', 'Nguyễn Thị Hương', '0987654324', 'BH001', 'Dị ứng Penicillin, Đậu phộng', NOW(), NOW()),
(8, 'Trần Thị', 'Linh', '1990-03-22', 'F', 'A+', '456 Đường Nguyễn Huệ, Quận 1, TP.HCM', 'Trần Văn Bình', '0987654325', 'BH002', 'Dị ứng tôm cua', NOW(), NOW()),
(9, 'Lê Văn', 'Nam', '1978-12-08', 'M', 'B+', '789 Đường Trần Hưng Đạo, Quận 5, TP.HCM', 'Lê Thị Hồng', '0987654326', 'BH003', 'Chưa phát hiện dị ứng', NOW(), NOW());

-- ===========================================
-- 4. DỮ LIỆU DỊCH VỤ BÁC SĨ
-- ===========================================

USE doctor_service_db;

INSERT INTO doctor_service_app_doctor (user_id, first_name, last_name, specialization, license_number, qualification, experience_years, consultation_fee, is_available, created_at) VALUES
(2, 'Nguyễn Văn', 'Minh', 'Tim mạch', 'BS001', 'Tiến sĩ Y khoa, Chuyên khoa Tim mạch - Bệnh viện Chợ Rẫy', 15, 500000.00, 1, NOW()),
(3, 'Trần Thị', 'Hoa', 'Nhi khoa', 'BS002', 'Thạc sĩ Y khoa, Chuyên khoa Nhi - Bệnh viện Nhi Đồng 1', 12, 400000.00, 1, NOW()),
(4, 'Lê Minh', 'Tuấn', 'Chấn thương chỉnh hình', 'BS003', 'Tiến sĩ Y khoa, Chuyên khoa Chấn thương chỉnh hình - Bệnh viện Việt Đức', 18, 600000.00, 1, NOW());

INSERT INTO doctor_service_app_doctoravailability (doctor_id, day_of_week, start_time, end_time, is_available) VALUES
-- BS. Nguyễn Văn Minh (Tim mạch) - Thứ 2 đến Thứ 6
(1, 0, '08:00:00', '17:00:00', 1), -- Thứ 2
(1, 1, '08:00:00', '17:00:00', 1), -- Thứ 3
(1, 2, '08:00:00', '17:00:00', 1), -- Thứ 4
(1, 3, '08:00:00', '17:00:00', 1), -- Thứ 5
(1, 4, '08:00:00', '17:00:00', 1), -- Thứ 6

-- BS. Trần Thị Hoa (Nhi khoa) - Thứ 2 đến Thứ 7
(2, 0, '07:30:00', '16:00:00', 1), -- Thứ 2
(2, 1, '07:30:00', '16:00:00', 1), -- Thứ 3
(2, 2, '07:30:00', '16:00:00', 1), -- Thứ 4
(2, 3, '07:30:00', '16:00:00', 1), -- Thứ 5
(2, 4, '07:30:00', '16:00:00', 1), -- Thứ 6
(2, 5, '08:00:00', '12:00:00', 1), -- Thứ 7

-- BS. Lê Minh Tuấn (Chấn thương chỉnh hình) - Thứ 3 đến Chủ nhật
(3, 1, '09:00:00', '18:00:00', 1), -- Thứ 3
(3, 2, '09:00:00', '18:00:00', 1), -- Thứ 4
(3, 3, '09:00:00', '18:00:00', 1), -- Thứ 5
(3, 4, '09:00:00', '18:00:00', 1), -- Thứ 6
(3, 5, '08:00:00', '16:00:00', 1), -- Thứ 7
(3, 6, '08:00:00', '15:00:00', 1); -- Chủ nhật

-- ===========================================
-- 5. DỮ LIỆU DỊCH VỤ Y TÁ
-- ===========================================

USE nurse_service_db;

INSERT INTO nurse_service_app_nurse (user_id, first_name, last_name, license_number, specialization, experience_years, shift, department, is_available, created_at) VALUES
(5, 'Phạm Thị', 'Lan', 'YT001', 'Điều dưỡng Hồi sức cấp cứu', 8, 'day', 'Khoa Hồi sức tích cực', 1, NOW()),
(6, 'Hoàng Thị', 'Mai', 'YT002', 'Điều dưỡng Nhi khoa', 6, 'night', 'Khoa Nhi', 1, NOW());

INSERT INTO nurse_service_app_nursepatientassignment (nurse_id, patient_id, assigned_date, shift_date, is_active, notes) VALUES
(1, 1, NOW(), CURDATE(), 1, 'Phân công chăm sóc chính'),
(2, 2, NOW(), CURDATE(), 1, 'Phân công chăm sóc nhi khoa');

INSERT INTO nurse_service_app_careactivity (nurse_id, patient_id, activity_type, description, performed_at, notes) VALUES
(1, 1, 'vital_signs', 'Huyết áp: 120/80 mmHg, Mạch: 72 lần/phút, Nhiệt độ: 37°C', NOW(), 'Các chỉ số sinh hiệu bình thường'),
(1, 1, 'medication', 'Đã cho uống thuốc buổi sáng theo đơn', NOW(), 'Bệnh nhân dung nạp tốt'),
(2, 2, 'vital_signs', 'Huyết áp: 110/70 mmHg, Mạch: 85 lần/phút, Nhiệt độ: 37.3°C', NOW(), 'Nhiệt độ hơi cao'),
(2, 2, 'patient_education', 'Hướng dẫn bệnh nhân cách sử dụng thuốc xịt', NOW(), 'Bệnh nhân đã hiểu rõ cách sử dụng');

-- ===========================================
-- 6. DỮ LIỆU DỊCH VỤ LỊCH HẸN
-- ===========================================

USE appointment_service_db;

INSERT INTO appointment_service_app_appointment (patient_id, doctor_id, appointment_date, appointment_time, duration_minutes, status, reason, notes, created_at, updated_at) VALUES
(1, 1, '2025-05-26', '10:00:00', 30, 'scheduled', 'Khám tim mạch định kỳ', 'Theo dõi tăng huyết áp', NOW(), NOW()),
(1, 1, '2025-05-28', '14:30:00', 30, 'confirmed', 'Tái khám đau ngực', 'Bệnh nhân than đau ngực nhẹ', NOW(), NOW()),
(2, 2, '2025-05-27', '09:00:00', 45, 'scheduled', 'Khám sức khỏe định kỳ cho trẻ em', 'Khám sức khỏe hàng năm', NOW(), NOW()),
(3, 3, '2025-05-29', '15:00:00', 60, 'scheduled', 'Tư vấn đau đầu gối', 'Bệnh nhân than đau đầu gối sau khi chạy bộ', NOW(), NOW()),
(1, 2, '2025-05-25', '11:00:00', 30, 'completed', 'Tiêm vaccine', 'Đã tiêm vaccine cúm hàng năm', NOW(), NOW());

-- ===========================================
-- 7. DỮ LIỆU DỊCH VỤ HỒ SƠ SỨC KHỎE
-- ===========================================

USE health_record_service_db;

INSERT INTO health_record_service_app_healthrecord (patient_id, doctor_id, visit_date, chief_complaint, history_present_illness, physical_examination, diagnosis, treatment_plan, notes, created_at, updated_at) VALUES
(1, 1, '2025-05-20 10:00:00', 'Đau ngực', 'Bệnh nhân than đau ngực nhẹ xuất hiện từng cơn trong tuần qua. Đau không lan ra, giảm khi nghỉ ngơi.', 'HA: 125/82 mmHg, Mạch: 75 lần/phút, Thở: 16 lần/phút, Nhiệt độ: 37°C. Tim đều, không tiếng thổi. Phổi trong.', 'Đau ngực không điển hình, có thể do cơ xương', 'Tiếp tục thuốc hiện tại. Tái khám sau 2 tuần. Làm test gắng sức nếu triệu chứng tiếp diễn.', 'Đã tư vấn thay đổi lối sống', NOW(), NOW()),
(2, 2, '2025-05-21 09:30:00', 'Sốt và ho', 'Mẹ cho biết trẻ sốt tới 38.3°C và ho khan trong 3 ngày. Trẻ ăn uống bình thường.', 'Nhiệt độ: 38.1°C, Mạch: 95 lần/phút, Thở: 22 lần/phút. Tai mũi họng: màng nhĩ trong, họng hơi đỏ. Phổi: có rale rời rạc.', 'Nhiễm khuẩn đường hô hấp trên', 'Điều trị hỗ trợ với nhiều nước. Paracetamol hạ sốt. Tái khám nếu nặng hơn.', 'Đã hướng dẫn mẹ các dấu hiệu cần đến viện ngay', NOW(), NOW());

INSERT INTO health_record_service_app_vitalsigns (health_record_id, temperature, blood_pressure_systolic, blood_pressure_diastolic, heart_rate, respiratory_rate, weight, height, recorded_at) VALUES
(1, 37.0, 125, 82, 75, 16, 70.5, 170.0, NOW()),
(2, 38.1, 98, 62, 95, 22, 18.2, 105.0, NOW());

INSERT INTO health_record_service_app_allergy (patient_id, allergen, reaction, severity, created_at) VALUES
(1, 'Penicillin', 'Phát ban và ngứa', 'moderate', NOW()),
(1, 'Đậu phộng', 'Sưng và khó thở', 'severe', NOW()),
(2, 'Tôm cua', 'Mày đay và buồn nôn', 'mild', NOW());

-- ===========================================
-- 8. DỮ LIỆU DỊCH VỤ THUỐC
-- ===========================================

USE medication_service_db;

INSERT INTO medication_service_app_medication (name, generic_name, manufacturer, dosage_form, strength, description, side_effects, contraindications, created_at) VALUES
('Lisinopril', 'Lisinopril', 'Công ty Dược phẩm ABC', 'Viên nén', '10mg', 'Thuốc ức chế ACE điều trị tăng huyết áp', 'Ho khan, chóng mặt, tăng kali máu', 'Có thai, phù mạch', NOW()),
('Amoxicillin', 'Amoxicillin', 'Công ty Kháng sinh XYZ', 'Viên nang', '500mg', 'Kháng sinh nhóm penicillin', 'Tiêu chảy, buồn nôn, phát ban', 'Dị ứng penicillin', NOW()),
('Ibuprofen', 'Ibuprofen', 'Công ty Giảm đau DEF', 'Viên nén', '400mg', 'Thuốc chống viêm giảm đau', 'Đau dạ dày, tăng nguy cơ chảy máu', 'Chảy máu tiêu hóa, suy thận nặng', NOW()),
('Metformin', 'Metformin HCl', 'Công ty Đái tháo đường GHI', 'Viên nén', '500mg', 'Thuốc đái tháo đường hàng đầu', 'Rối loạn tiêu hóa, toan máu lactic (hiếm)', 'Suy thận nặng, toan chuyển hóa', NOW()),
('Ventolin', 'Albuterol Sulfate', 'Công ty Hô hấp JKL', 'Bình xịt', '90mcg/xịt', 'Thuốc giãn phế quản điều trị hen suyễn', 'Run tay, hồi hộp, lo lắng', 'Dị ứng với albuterol', NOW());

INSERT INTO medication_service_app_prescription (patient_id, doctor_id, prescription_date, status, notes, created_at) VALUES
(1, 1, NOW(), 'active', 'Tiếp tục điều trị tăng huyết áp', NOW()),
(2, 2, NOW(), 'completed', 'Đã hoàn thành đợt điều trị', NOW()),
(3, 3, NOW(), 'active', 'Giảm đau cho chấn thương đầu gối', NOW());

INSERT INTO medication_service_app_prescriptionitem (prescription_id, medication_id, dosage, frequency, duration, quantity, instructions) VALUES
(1, 1, '10mg', 'Ngày 1 lần', '30 ngày', 30, 'Uống với thức ăn. Theo dõi huyết áp thường xuyên.'),
(2, 2, '500mg', 'Ngày 3 lần', '7 ngày', 21, 'Uống với thức ăn. Uống đủ liều theo đơn.'),
(3, 3, '400mg', 'Khi cần', '14 ngày', 28, 'Uống với thức ăn. Không quá 3 viên/ngày.');

-- ===========================================
-- 9. DỮ LIỆU DỊCH VỤ XÉT NGHIỆM
-- ===========================================

USE laboratory_service_db;

INSERT INTO laboratory_service_app_labtest (name, code, description, sample_type, reference_range, cost, created_at) VALUES
('Công thức máu toàn phần', 'CTMTP', 'Đếm toàn bộ tế bào máu bao gồm BC, HC, Tiểu cầu', 'Máu', 'BC: 4.0-11.0 K/uL, HC: 4.2-5.4 M/uL, Tiểu cầu: 150-400 K/uL', 120000, NOW()),
('Sinh hóa cơ bản', 'SHCB', 'Glucose, điện giải, chức năng thận', 'Máu', 'Glucose: 3.9-5.6 mmol/L, Natri: 136-145 mEq/L, Creatinin: 53-106 umol/L', 150000, NOW()),
('Mỡ máu', 'MM', 'Cholesterol, triglyceride, HDL, LDL', 'Máu', 'Cholesterol toàn phần: <5.2 mmol/L, LDL: <2.6 mmol/L, HDL: >1.0 mmol/L', 180000, NOW()),
('Tổng phân tích nước tiểu', 'TPTNT', 'Phân tích hoàn chỉnh nước tiểu', 'Nước tiểu', 'Protein: Âm tính, Glucose: Âm tính, BC: 0-5/tr', 80000, NOW()),
('HbA1c', 'A1C', 'Hemoglobin A1c theo dõi đái tháo đường', 'Máu', '<5.7% (bình thường), 5.7-6.4% (tiền đái tháo đường), ≥6.5% (đái tháo đường)', 200000, NOW());

INSERT INTO laboratory_service_app_laborder (patient_id, doctor_id, lab_test_id, order_date, status, priority, clinical_notes) VALUES
(1, 1, 1, NOW(), 'completed', 'routine', 'Tầm soát hàng năm'),
(1, 1, 3, NOW(), 'completed', 'routine', 'Đánh giá nguy cơ tim mạch'),
(2, 2, 4, NOW(), 'processing', 'urgent', 'Nghi ngờ nhiễm khuẩn tiết niệu'),
(3, 3, 2, NOW(), 'ordered', 'routine', 'Kiểm tra trước phẫu thuật');

INSERT INTO laboratory_service_app_labresult (lab_order_id, technician_id, result_value, unit, reference_range, abnormal_flag, comments, result_date, verified_by, verified_at) VALUES
(1, 11, 'BC: 6.5, HC: 4.8, Tiểu cầu: 250', 'K/uL, M/uL, K/uL', 'BC: 4.0-11.0, HC: 4.2-5.4, Tiểu cầu: 150-400', '', 'Công thức máu bình thường', NOW(), 2, NOW()),
(2, 11, 'Tổng: 4.8, LDL: 2.5, HDL: 1.2, Triglyceride: 3.1', 'mmol/L', 'Tổng: <5.2, LDL: <2.6, HDL: >1.0, Triglyceride: <3.9', '', 'Mỡ máu trong giới hạn bình thường', NOW(), 2, NOW());

-- ===========================================
-- 10. DỮ LIỆU DỊCH VỤ NHÀ THUỐC
-- ===========================================

USE pharmacy_service_db;

INSERT INTO pharmacy_service_app_pharmacy (name, address, phone, email, license_number, created_at) VALUES
('Nhà thuốc Bệnh viện Trung tâm', '100 Đường Y tế, Phòng 101', '0901-NT-001', 'truongtam@nhathuoc.vn', 'NT001', NOW()),
('Nhà thuốc Bệnh viện Chi nhánh Tây', '500 Đường Tây, Tòa B', '0901-NT-002', 'chinhanhtay@nhathuoc.vn', 'NT002', NOW());

INSERT INTO pharmacy_service_app_inventoryitem (pharmacy_id, medication_id, batch_number, expiry_date, quantity_in_stock, cost_price, selling_price, reorder_level, created_at, updated_at) VALUES
(1, 1, 'LIS2025001', '2026-12-31', 500, 15000, 25000, 50, NOW(), NOW()),
(1, 2, 'AMX2025001', '2025-08-15', 200, 20000, 45000, 25, NOW(), NOW()),
(1, 3, 'IBU2025001', '2027-03-20', 300, 8000, 18000, 30, NOW(), NOW()),
(2, 1, 'LIS2025002', '2026-11-30', 250, 15000, 25000, 25, NOW(), NOW()),
(2, 4, 'MET2025001', '2026-09-15', 400, 12000, 22000, 40, NOW(), NOW());

INSERT INTO pharmacy_service_app_dispensingrecord (prescription_id, pharmacist_id, inventory_item_id, quantity_dispensed, dispensing_date, patient_counseled, notes) VALUES
(1, 10, 1, 30, NOW(), 1, 'Đã tư vấn bệnh nhân về theo dõi huyết áp'),
(2, 10, 2, 21, NOW(), 1, 'Đã nhắc nhở bệnh nhân uống đủ liều'),
(3, 10, 3, 28, NOW(), 1, 'Đã tư vấn về liều dùng và cách uống với thức ăn');

-- ===========================================
-- 11. DỮ LIỆU DỊCH VỤ HÓA ĐƠN
-- ===========================================

USE invoice_service_db;

INSERT INTO invoice_service_app_invoice (patient_id, invoice_number, issue_date, due_date, total_amount, paid_amount, status, notes, created_at, updated_at) VALUES
(1, 'HD-2025-001', NOW(), DATE_ADD(CURDATE(), INTERVAL 30 DAY), 680000.00, 0.00, 'sent', 'Khám tim mạch và xét nghiệm', NOW(), NOW()),
(2, 'HD-2025-002', NOW(), DATE_ADD(CURDATE(), INTERVAL 30 DAY), 525000.00, 525000.00, 'paid', 'Khám nhi khoa và thuốc', NOW(), NOW()),
(3, 'HD-2025-003', NOW(), DATE_ADD(CURDATE(), INTERVAL 30 DAY), 750000.00, 200000.00, 'partial', 'Khám chấn thương và xét nghiệm', NOW(), NOW());

INSERT INTO invoice_service_app_invoiceitem (invoice_id, description, quantity, unit_price, total_price, service_date) VALUES
(1, 'Khám Tim mạch - BS. Nguyễn Văn Minh', 1, 500000.00, 500000.00, CURDATE()),
(1, 'Xét nghiệm Mỡ máu', 1, 180000.00, 180000.00, CURDATE()),
(2, 'Khám Nhi khoa - BS. Trần Thị Hoa', 1, 400000.00, 400000.00, CURDATE()),
(2, 'Thuốc Amoxicillin', 1, 125000.00, 125000.00, CURDATE()),
(3, 'Khám Chấn thương chỉnh hình - BS. Lê Minh Tuấn', 1, 600000.00, 600000.00, CURDATE()),
(3, 'Sinh hóa cơ bản', 1, 150000.00, 150000.00, CURDATE());

-- ===========================================
-- 12. DỮ LIỆU DỊCH VỤ THANH TOÁN
-- ===========================================

USE payment_service_db;

INSERT INTO payment_service_app_paymentmethod (name, is_active, created_at) VALUES
('Thẻ tín dụng', 1, NOW()),
('Thẻ ghi nợ', 1, NOW()),
('Tiền mặt', 1, NOW()),
('Bảo hiểm y tế', 1, NOW()),
('Chuyển khoản ngân hàng', 1, NOW());

INSERT INTO payment_service_app_payment (invoice_id, payment_method_id, amount, status, transaction_id, gateway_response, payment_date, processed_by) VALUES
(2, 1, 525000.00, 'completed', 'GD-2025-001', 'Thanh toán thành công qua thẻ Visa kết thúc 1234', NOW(), 1),
(3, 1, 200000.00, 'completed', 'GD-2025-002', 'Thanh toán một phần qua thẻ MasterCard kết thúc 5678', NOW(), 1);

-- ===========================================
-- 13. DỮ LIỆU DỊCH VỤ THÔNG BÁO
-- ===========================================

USE notification_service_db;

INSERT INTO notification_service_app_notificationtemplate (name, subject_template, body_template, notification_type, created_at) VALUES
('Nhắc lịch hẹn', 'Nhắc nhở lịch hẹn - {appointment_date}', 'Kính chào {patient_name}, đây là lời nhắc về lịch hẹn với {doctor_name} vào ngày {appointment_date} lúc {appointment_time}.', 'email', NOW()),
('Tạo hóa đơn', 'Hóa đơn mới #{invoice_number}', 'Hóa đơn mới #{invoice_number} với số tiền {amount} VND đã được tạo cho lần khám gần đây của bạn.', 'email', NOW()),
('Xác nhận thanh toán', 'Đã nhận thanh toán', 'Cảm ơn bạn! Chúng tôi đã nhận được khoản thanh toán {amount} VND cho hóa đơn #{invoice_number}.', 'email', NOW()),
('Kết quả xét nghiệm', 'Kết quả xét nghiệm có sẵn', 'Kết quả xét nghiệm của bạn đã có. Vui lòng đăng nhập vào cổng thông tin bệnh nhân để xem.', 'email', NOW());

INSERT INTO notification_service_app_notification (user_id, notification_type, subject, message, status, sent_at, created_at) VALUES
(7, 'email', 'Nhắc lịch hẹn - 26/05/2025', 'Kính chào anh Nguyễn Văn Đức, đây là lời nhắc về lịch hẹn với BS. Nguyễn Văn Minh vào ngày 26/05/2025 lúc 10:00.', 'sent', NOW(), NOW()),
(8, 'email', 'Hóa đơn mới #HD-2025-002', 'Hóa đơn mới #HD-2025-002 với số tiền 525.000 VND đã được tạo cho lần khám gần đây của bạn.', 'delivered', NOW(), NOW()),
(8, 'email', 'Đã nhận thanh toán', 'Cảm ơn bạn! Chúng tôi đã nhận được khoản thanh toán 525.000 VND cho hóa đơn #HD-2025-002.', 'delivered', NOW(), NOW()),
(7, 'in_app', 'Kết quả xét nghiệm có sẵn', 'Kết quả xét nghiệm của bạn đã có. Vui lòng đăng nhập vào cổng thông tin bệnh nhân để xem.', 'read', NOW(), NOW());

-- ===========================================
-- 14. DỮ LIỆU DỊCH VỤ BẢO HIỂM
-- ===========================================

USE insurance_service_db;

INSERT INTO insurance_service_app_insuranceprovider (name, code, contact_email, contact_phone, address, is_active, created_at) VALUES
('Bảo hiểm xã hội Việt Nam', 'BHXH', 'hotro@baohiemxahoi.gov.vn', '1900-1234', '144 Xuân Thủy, Cầu Giấy, Hà Nội', 1, NOW()),
('Bảo hiểm Bảo Việt', 'BV', 'cskh@baoviet.com.vn', '1900-5588', '8 Lê Thái Tổ, Hoàn Kiếm, Hà Nội', 1, NOW()),
('Bảo hiểm Prudential', 'PRU', 'info@prudential.com.vn', '1800-1779', '193A Nam Kỳ Khởi Nghĩa, Quận 3, TP.HCM', 1, NOW());

INSERT INTO insurance_service_app_insurancepolicy (patient_id, provider_id, policy_number, policy_holder_name, coverage_amount, deductible, copayment, start_date, end_date, is_active, created_at) VALUES
(1, 1, 'BHXH-DN4101234567', 'Nguyễn Văn Đức', 50000000.00, 0.00, 200000.00, '2024-01-01', '2025-12-31', 1, NOW()),
(2, 2, 'BV-HC2025001', 'Trần Thị Linh', 100000000.00, 1000000.00, 300000.00, '2024-06-01', '2025-05-31', 1, NOW()),
(3, 3, 'PRU-HL2024999', 'Lê Văn Nam', 200000000.00, 2000000.00, 500000.00, '2024-03-15', '2025-03-14', 1, NOW());

INSERT INTO insurance_service_app_insuranceclaim (policy_id, invoice_id, claim_number, claim_amount, approved_amount, status, submission_date, processed_date, notes) VALUES
(1, 1, 'YC-2025-001', 680000.00, 480000.00, 'approved', NOW(), NOW(), 'Đã duyệt 80% chi phí khám và xét nghiệm'),
(2, 2, 'YC-2025-002', 525000.00, 525000.00, 'paid', NOW(), NOW(), 'Đã thanh toán toàn bộ chi phí'),
(3, 3, 'YC-2025-003', 750000.00, NULL, 'under_review', NOW(), NULL, 'Đang xem xét hồ sơ yêu cầu bồi thường');

-- ===========================================
-- 15. DỮ LIỆU DỊCH VỤ CHATBOT
-- ===========================================

USE chatbot_service_db;

INSERT INTO chatbot_service_app_faq (question, answer, category, is_active, created_at) VALUES
('Làm thế nào để đặt lịch hẹn?', 'Bạn có thể đặt lịch hẹn bằng cách gọi điện thoại đến số hotline hoặc sử dụng ứng dụng di động của chúng tôi.', 'appointment', 1, NOW()),
('Giờ làm việc của bệnh viện?', 'Bệnh viện làm việc từ 7:00 - 18:00 các ngày trong tuần và 8:00 - 16:00 vào cuối tuần.', 'general', 1, NOW()),
('Tôi có thể thanh toán bằng thẻ không?', 'Có, chúng tôi chấp nhận thanh toán bằng thẻ tín dụng, thẻ ghi nợ và chuyển khoản ngân hàng.', 'payment', 1, NOW()),
('Kết quả xét nghiệm có sẵn khi nào?', 'Kết quả xét nghiệm thường có trong vòng 24-48 giờ. Bạn sẽ nhận được thông báo khi kết quả đã sẵn sàng.', 'laboratory', 1, NOW()),
('Tôi quên mang thẻ bảo hiểm thì sao?', 'Bạn vẫn có thể khám và thanh toán trước. Sau đó có thể nộp hồ sơ bảo hiểm để được hoàn lại tiền.', 'insurance', 1, NOW());

INSERT INTO chatbot_service_app_chatsession (user_id, session_id, start_time, end_time, is_active, session_type) VALUES
(7, 'session-001-duc', NOW(), NULL, 1, 'general'),
(8, 'session-002-linh', NOW(), NULL, 1, 'appointment'),
(9, 'session-003-nam', DATE_SUB(NOW(), INTERVAL 1 HOUR), DATE_SUB(NOW(), INTERVAL 30 MINUTE), 0, 'general');

INSERT INTO chatbot_service_app_chatmessage (session_id, sender, message, timestamp, intent, confidence_score) VALUES
(1, 'user', 'Xin chào, tôi muốn đặt lịch hẹn', NOW(), '', NULL),
(1, 'bot', 'Xin chào! Tôi có thể giúp bạn đặt lịch hẹn. Vui lòng cung cấp ngày và giờ bạn mong muốn.', NOW(), 'appointment_booking', 0.95),
(2, 'user', 'Bệnh viện làm việc mấy giờ?', NOW(), '', NULL),
(2, 'bot', 'Bệnh viện làm việc từ 7:00 - 18:00 các ngày trong tuần và 8:00 - 16:00 vào cuối tuần.', NOW(), 'working_hours', 0.98),
(3, 'user', 'Cảm ơn', DATE_SUB(NOW(), INTERVAL 30 MINUTE), '', NULL),
(3, 'bot', 'Rất vui được hỗ trợ bạn! Chúc bạn một ngày tốt lành.', DATE_SUB(NOW(), INTERVAL 30 MINUTE), 'goodbye', 0.92);


-- ===========================================
-- 17. THỐNG KÊ DỮ LIỆU ĐÃ TẠO
-- ===========================================

-- Hiển thị tóm tắt dữ liệu đã tạo
SELECT 'Tóm tắt dữ liệu đã tạo:' as thong_tin;

USE user_service_db;
SELECT 'Người dùng:' as loai_du_lieu, COUNT(*) as so_luong FROM user_service_app_user;

USE patient_service_db;
SELECT 'Bệnh nhân:' as loai_du_lieu, COUNT(*) as so_luong FROM patient_service_app_patient;

USE doctor_service_db;
SELECT 'Bác sĩ:' as loai_du_lieu, COUNT(*) as so_luong FROM doctor_service_app_doctor;

USE nurse_service_db;
SELECT 'Y tá:' as loai_du_lieu, COUNT(*) as so_luong FROM nurse_service_app_nurse;

USE appointment_service_db;
SELECT 'Lịch hẹn:' as loai_du_lieu, COUNT(*) as so_luong FROM appointment_service_app_appointment;

USE medication_service_db;
SELECT 'Đơn thuốc:' as loai_du_lieu, COUNT(*) as so_luong FROM medication_service_app_prescription;

USE laboratory_service_db;
SELECT 'Xét nghiệm:' as loai_du_lieu, COUNT(*) as so_luong FROM laboratory_service_app_laborder;

USE invoice_service_db;
SELECT 'Hóa đơn:' as loai_du_lieu, COUNT(*) as so_luong FROM invoice_service_app_invoice;

USE insurance_service_db;
SELECT 'Bảo hiểm:' as loai_du_lieu, COUNT(*) as so_luong FROM insurance_service_app_insurancepolicy;

-- ===========================================
-- KẾT THÚC SCRIPT
-- ===========================================

SELECT 'Hoàn thành việc tạo database và dữ liệu mẫu cho Hệ thống Y tế Microservices!' as ket_qua;
SELECT 'Tổng cộng đã tạo 14 databases với dữ liệu mẫu đầy đủ.' as thong_tin_them;