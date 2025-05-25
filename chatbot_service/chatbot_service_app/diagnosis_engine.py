import re
import json
from typing import List, Dict, Tuple
from django.db.models import Q
from .models import Symptom, Disease, DiseaseSymptom, DiagnosisSession, ReportedSymptom

class DiagnosisEngine:
    """Engine chẩn đoán thông minh dựa trên triệu chứng"""
    
    def __init__(self):
        self.symptom_patterns = self._load_symptom_patterns()
        self.severity_patterns = self._load_severity_patterns()
        self.duration_patterns = self._load_duration_patterns()
        self.urgent_symptoms = self._load_urgent_symptoms()
    
    def _load_symptom_patterns(self) -> Dict[str, List[str]]:
        """Tải các pattern để nhận diện triệu chứng từ text"""
        return {
            'đau_đầu': ['đau đầu', 'nhức đầu', 'đau đầu', 'đầu đau', 'cứng đầu'],
            'sốt': ['sốt', 'nóng người', 'ấm người', 'nhiệt độ cao', 'bị nóng'],
            'ho': ['ho', 'ke', 'ho khan', 'ho có đờm', 'bị ho'],
            'buồn_nôn': ['buồn nôn', 'nôn', 'muốn nôn', 'cảm giác nôn', 'ợt'],
            'chóng_mặt': ['chóng mặt', 'hoa mắt', 'choáng váng', 'mệt lả', 'lảo đảo'],
            'đau_bụng': ['đau bụng', 'đau dạ dày', 'đau ruột', 'quặn bụng', 'bụng đau'],
            'khó_thở': ['khó thở', 'thở khó', 'ngạt thở', 'thở gấp', 'hụt hơi'],
            'đau_ngực': ['đau ngực', 'tức ngực', 'ngực đau', 'đau tim', 'đau lồng ngực'],
            'mệt_mỏi': ['mệt mỏi', 'mệt', 'uể oải', 'kiệt sức', 'không có sức'],
            'tiêu_chảy': ['tiêu chảy', 'đi lỏng', 'đi ngoài nhiều', 'lỏng bụng', 'rối loạn tiêu hóa'],
            'táo_bón': ['táo bón', 'khó đi ngoài', 'bí đại tiện', 'không đi được'],
            'đau_họng': ['đau họng', 'rát họng', 'khàn giọng', 'nuốt đau', 'họng đau'],
            'đau_lưng': ['đau lưng', 'nhức lưng', 'lưng đau', 'đau cột sống'],
            'đau_khớp': ['đau khớp', 'nhức khớp', 'cứng khớp', 'sưng khớp'],
            'phát_ban': ['phát ban', 'nổi mề đay', 'ngứa', 'da đỏ', 'ban đỏ'],
            'mất_ngủ': ['mất ngủ', 'không ngủ được', 'khó ngủ', 'thức khuya'],
            'đau_răng': ['đau răng', 'nhức răng', 'răng đau', 'sâu răng'],
            'chảy_máu_cam': ['chảy máu cam', 'máu cam', 'chảy máu mũi'],
            'đau_tai': ['đau tai', 'tai đau', 'nhức tai', 'ù tai']
        }
    
    def _load_severity_patterns(self) -> Dict[str, List[str]]:
        """Tải các pattern để nhận diện mức độ nghiêm trọng"""
        return {
            'mild': ['nhẹ', 'chút ít', 'hơi', 'ít', 'không nhiều', '1', '2', '3'],
            'moderate': ['vừa', 'trung bình', 'khá', 'tương đối', '4', '5', '6', '7'],
            'severe': ['nặng', 'nhiều', 'dữ dội', 'khủng khiếp', 'không chịu nổi', '8', '9', '10']
        }
    
    def _load_duration_patterns(self) -> Dict[str, List[str]]:
        """Tải các pattern để nhận diện thời gian"""
        return {
            'hours': ['giờ', 'tiếng', 'từ sáng', 'từ chiều', 'từ tối', 'hôm nay'],
            'days': ['ngày', 'hôm qua', 'tuần này', 'mấy ngày'],
            'weeks': ['tuần', 'mấy tuần', 'tuần trước'],
            'months': ['tháng', 'mấy tháng', 'tháng trước', 'lâu rồi']
        }
    
    def _load_urgent_symptoms(self) -> List[str]:
        """Tải danh sách triệu chứng cần cấp cứu"""
        return [
            'đau_ngực_dữ_dội',
            'khó_thở_nặng',
            'bất_tỉnh',
            'đau_đầu_đột_ngột',
            'co_giật',
            'chảy_máu_nhiều',
            'đau_bụng_dữ_dối',
            'sốt_cao'
        ]

    def extract_symptoms_from_text(self, text: str) -> List[Dict]:
        """Trích xuất triệu chứng từ văn bản"""
        text = text.lower()
        extracted_symptoms = []
        
        for symptom_key, patterns in self.symptom_patterns.items():
            for pattern in patterns:
                if pattern in text:
                    # Tìm triệu chứng trong database
                    try:
                        symptom = Symptom.objects.get(
                            Q(name__icontains=symptom_key.replace('_', ' ')) |
                            Q(keywords__icontains=pattern)
                        )
                        
                        # Trích xuất mức độ nghiêm trọng
                        severity = self._extract_severity(text, pattern)
                        
                        # Trích xuất thời gian
                        duration = self._extract_duration(text, pattern)
                        
                        extracted_symptoms.append({
                            'symptom': symptom,
                            'severity': severity,
                            'duration': duration,
                            'context': self._extract_context(text, pattern)
                        })
                        break
                    except Symptom.DoesNotExist:
                        # Tạo triệu chứng mới nếu chưa có
                        symptom = self._create_new_symptom(symptom_key, pattern)
                        if symptom:
                            extracted_symptoms.append({
                                'symptom': symptom,
                                'severity': 'mild',
                                'duration': '',
                                'context': pattern
                            })
        
        return extracted_symptoms
    
    def _extract_severity(self, text: str, symptom_context: str) -> str:
        """Trích xuất mức độ nghiêm trọng từ ngữ cảnh"""
        # Tìm văn bản xung quanh triệu chứng
        symptom_index = text.find(symptom_context)
        context_start = max(0, symptom_index - 50)
        context_end = min(len(text), symptom_index + len(symptom_context) + 50)
        context = text[context_start:context_end]
        
        for severity, patterns in self.severity_patterns.items():
            for pattern in patterns:
                if pattern in context:
                    return severity
        
        return 'mild'  # Default
    
    def _extract_duration(self, text: str, symptom_context: str) -> str:
        """Trích xuất thời gian từ ngữ cảnh"""
        symptom_index = text.find(symptom_context)
        context_start = max(0, symptom_index - 50)
        context_end = min(len(text), symptom_index + len(symptom_context) + 50)
        context = text[context_start:context_end]
        
        for duration, patterns in self.duration_patterns.items():
            for pattern in patterns:
                if pattern in context:
                    return duration
        
        return ''
    
    def _extract_context(self, text: str, symptom_pattern: str) -> str:
        """Trích xuất ngữ cảnh xung quanh triệu chứng"""
        symptom_index = text.find(symptom_pattern)
        context_start = max(0, symptom_index - 30)
        context_end = min(len(text), symptom_index + len(symptom_pattern) + 30)
        return text[context_start:context_end]
    
    def _create_new_symptom(self, symptom_key: str, pattern: str) -> Symptom:
        """Tạo triệu chứng mới nếu chưa có trong database"""
        try:
            symptom_name = symptom_key.replace('_', ' ').title()
            symptom = Symptom.objects.create(
                name=symptom_name,
                description=f"Triệu chứng được tự động tạo từ: {pattern}",
                category="general",
                keywords=pattern
            )
            return symptom
        except:
            return None
    
    def diagnose(self, diagnosis_session: DiagnosisSession) -> Dict:
        """Thực hiện chẩn đoán dựa trên triệu chứng đã báo cáo"""
        reported_symptoms = diagnosis_session.reportedsymptom_set.all()
        
        if not reported_symptoms.exists():
            return {
                'diseases': [],
                'confidence_level': 'low',
                'urgent_care': False,
                'recommendations': []
            }
        
        # Kiểm tra triệu chứng cấp cứu
        urgent_care = self._check_urgent_symptoms(reported_symptoms)
        
        # Tính điểm cho các bệnh có thể
        disease_scores = self._calculate_disease_scores(reported_symptoms)
        
        # Sắp xếp theo điểm số và lấy top diseases
        sorted_diseases = sorted(disease_scores.items(), key=lambda x: x[1], reverse=True)
        top_diseases = sorted_diseases[:5]  # Top 5 bệnh có thể
        
        # Chuyển đổi thành format phản hồi
        diseases_result = []
        for disease, score in top_diseases:
            diseases_result.append({
                'id': disease.id,
                'name': disease.name,
                'description': disease.description,
                'confidence': min(score / 100, 1.0),  # Normalize to 0-1
                'urgency': disease.urgency_level,
                'recommendations': disease.recommendations
            })
        
        # Xác định mức độ tin cậy tổng thể
        confidence_level = self._determine_confidence_level(diseases_result, reported_symptoms)
        
        # Tạo khuyến nghị
        recommendations = self._generate_recommendations(diseases_result, urgent_care, confidence_level)
        
        return {
            'diseases': diseases_result,
            'confidence_level': confidence_level,
            'urgent_care': urgent_care,
            'recommendations': recommendations
        }
    
    def _check_urgent_symptoms(self, reported_symptoms) -> bool:
        """Kiểm tra có triệu chứng cần cấp cứu không"""
        urgent_keywords = [
            'đau ngực dữ dội', 'khó thở nặng', 'đau đầu đột ngột',
            'co giật', 'bất tỉnh', 'chảy máu nhiều', 'sốt cao'
        ]
        
        for symptom in reported_symptoms:
            # Kiểm tra triệu chứng nghiêm trọng
            if symptom.severity == 'severe' and symptom.symptom.is_critical:
                return True
            
            # Kiểm tra từ khóa cấp cứu
            symptom_text = f"{symptom.symptom.name} {symptom.additional_details}".lower()
            for keyword in urgent_keywords:
                if keyword in symptom_text:
                    return True
        
        return False
    
    def _calculate_disease_scores(self, reported_symptoms) -> Dict[Disease, float]:
        """Tính điểm cho các bệnh dựa trên triệu chứng"""
        disease_scores = {}
        
        # Lấy tất cả bệnh có liên quan đến triệu chứng đã báo cáo
        symptom_ids = [rs.symptom.id for rs in reported_symptoms]
        related_diseases = Disease.objects.filter(
            symptoms__id__in=symptom_ids
        ).distinct()
        
        for disease in related_diseases:
            score = 0
            disease_symptoms = DiseaseSymptom.objects.filter(disease=disease)
            total_disease_symptoms = disease_symptoms.count()
            
            # Tính điểm dựa trên triệu chứng khớp
            matched_symptoms = 0
            for reported_symptom in reported_symptoms:
                disease_symptom = disease_symptoms.filter(
                    symptom=reported_symptom.symptom
                ).first()
                
                if disease_symptom:
                    matched_symptoms += 1
                    
                    # Điểm cơ bản
                    base_score = disease_symptom.weight * 10
                    
                    # Bonus cho triệu chứng bắt buộc
                    if disease_symptom.is_required:
                        base_score *= 2
                    
                    # Bonus cho mức độ nghiêm trọng
                    severity_multiplier = {
                        'mild': 1.0,
                        'moderate': 1.3,
                        'severe': 1.7
                    }
                    base_score *= severity_multiplier.get(reported_symptom.severity, 1.0)
                    
                    # Bonus cho tần suất triệu chứng
                    frequency_multiplier = {
                        'rare': 0.7,
                        'common': 1.0,
                        'very_common': 1.3
                    }
                    base_score *= frequency_multiplier.get(disease_symptom.frequency, 1.0)
                    
                    score += base_score
            
            # Penalty nếu thiếu triệu chứng bắt buộc
            required_symptoms = disease_symptoms.filter(is_required=True)
            for req_symptom in required_symptoms:
                if not reported_symptoms.filter(symptom=req_symptom.symptom).exists():
                    score *= 0.3  # Giảm 70% điểm
            
            # Bonus cho tỷ lệ triệu chứng khớp
            if total_disease_symptoms > 0:
                match_ratio = matched_symptoms / total_disease_symptoms
                score *= (0.5 + match_ratio * 0.5)  # 50-100% dựa trên tỷ lệ khớp
            
            if score > 0:
                disease_scores[disease] = score
        
        return disease_scores
    
    def _determine_confidence_level(self, diseases_result: List[Dict], reported_symptoms) -> str:
        """Xác định mức độ tin cậy chung"""
        if not diseases_result:
            return 'low'
        
        top_confidence = diseases_result[0]['confidence']
        symptom_count = len(reported_symptoms)
        
        if top_confidence > 0.8 and symptom_count >= 3:
            return 'high'
        elif top_confidence > 0.6 and symptom_count >= 2:
            return 'medium'
        else:
            return 'low'
    
    def _generate_recommendations(self, diseases_result: List[Dict], urgent_care: bool, confidence_level: str) -> List[str]:
        """Tạo khuyến nghị dựa trên kết quả chẩn đoán"""
        recommendations = []
        
        if urgent_care:
            recommendations.extend([
                'Đến phòng cấp cứu ngay lập tức',
                'Gọi 115 nếu cần thiết',
                'Không trì hoãn việc tìm kiếm chăm sóc y tế'
            ])
        elif confidence_level == 'high':
            recommendations.extend([
                'Đặt lịch khám với bác sĩ chuyên khoa trong 1-2 ngày',
                'Theo dõi triệu chứng và ghi lại thay đổi',
                'Nghỉ ngơi đầy đủ và uống nhiều nước'
            ])
        elif confidence_level == 'medium':
            recommendations.extend([
                'Theo dõi triệu chứng trong 24-48 giờ',
                'Đặt lịch khám nếu triệu chứng không cải thiện',
                'Tránh các hoạt động nặng'
            ])
        else:
            recommendations.extend([
                'Theo dõi triệu chứng và ghi lại chi tiết',
                'Tham khảo ý kiến bác sĩ nếu lo lắng',
                'Duy trì lối sống lành mạnh'
            ])
        
        # Thêm khuyến nghị đặc biệt từ bệnh có khả năng cao nhất
        if diseases_result and diseases_result[0].get('recommendations'):
            recommendations.append(diseases_result[0]['recommendations'])
        
        return recommendations
    
    def get_follow_up_questions(self, diagnosis_session: DiagnosisSession) -> List[str]:
        """Tạo câu hỏi follow-up để thu thập thêm thông tin"""
        reported_symptoms = diagnosis_session.reportedsymptom_set.all()
        questions = []
        
        if not reported_symptoms.exists():
            return [
                "Bạn có thể mô tả cụ thể hơn về triệu chứng bạn đang gặp phải không?",
                "Triệu chứng này bắt đầu từ khi nào?",
                "Mức độ nghiêm trọng từ 1-10 là bao nhiêu?"
            ]
        
        # Câu hỏi dựa trên triệu chứng đã có
        symptom_categories = set(rs.symptom.category for rs in reported_symptoms)
        
        if 'respiratory' in symptom_categories:
            questions.extend([
                "Bạn có khó thở hoặc thở gấp không?",
                "Có ho ra máu không?",
                "Có cảm giác tức ngực không?"
            ])
        
        if 'cardiovascular' in symptom_categories:
            questions.extend([
                "Bạn có cảm giác tim đập nhanh hoặc bất thường không?",
                "Có đau lan ra cánh tay hoặc hàm không?",
                "Có cảm giác choáng váng khi đứng dậy không?"
            ])
        
        if 'neurological' in symptom_categories:
            questions.extend([
                "Bạn có cảm thấy tê bì hoặc yếu ở tay chân không?",
                "Có thay đổi về thị lực hoặc nói năng không?",
                "Có cảm giác buồn nôn kèm theo không?"
            ])
        
        # Câu hỏi về tiền sử
        questions.extend([
            "Bạn có tiền sử bệnh lý gì không?",
            "Đang dùng thuốc gì thường xuyên không?",
            "Có ai trong gia đình bị bệnh tương tự không?"
        ])
        
        return questions[:3]  # Giới hạn 3 câu hỏi mỗi lần