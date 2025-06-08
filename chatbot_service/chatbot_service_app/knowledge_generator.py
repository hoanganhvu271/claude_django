from sentence_transformers import SentenceTransformer
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class MedicalKnowledgeGenerator:
    """Generate medical knowledge base using NLP models"""
    
    def __init__(self):
        self.encoder = SentenceTransformer('keepitreal/vietnamese-sbert')
        
        # Knowledge templates for different medical contexts
        self.knowledge_templates = {
            'disease_description': [
                "{disease} là một bệnh {category} với các triệu chứng chính: {symptoms}. {description}",
                "Bệnh {disease} thuộc nhóm {category}, thường biểu hiện qua {symptoms}. {treatment_info}",
                "{disease} - {description}. Các dấu hiệu cần chú ý: {symptoms}."
            ],
            'symptom_analysis': [
                "Triệu chứng {symptom} có thể là dấu hiệu của các bệnh: {diseases}. {medical_advice}",
                "Khi xuất hiện {symptom}, cần lưu ý khả năng mắc {diseases}. {care_instructions}",
                "{symptom} thường gặp trong {diseases}. {when_to_see_doctor}"
            ],
            'treatment_guidance': [
                "Điều trị {disease}: {recommendations}. {severity_note}",
                "Đối với {disease}, khuyến nghị: {treatment_steps}. {follow_up}",
                "Cách xử lý {disease}: {immediate_care}. {long_term_management}"
            ],
            'emergency_protocols': [
                "Khi có dấu hiệu {emergency_symptoms}, cần {emergency_action}. {urgency_note}",
                "Tình huống khẩn cấp: {emergency_symptoms} - {immediate_steps}. {contact_info}",
                "{emergency_symptoms} là dấu hiệu nguy hiểm. {emergency_response}."
            ]
        }
        
        # Medical advice templates
        self.advice_templates = {
            'mild': [
                "Theo dõi triệu chứng và nghỉ ngơi đầy đủ",
                "Uống nhiều nước và duy trì chế độ ăn nhẹ",
                "Nếu triệu chứng kéo dài quá 3 ngày, nên tham khảo bác sĩ"
            ],
            'moderate': [
                "Nên đặt lịch khám với bác sĩ trong 1-2 ngày",
                "Theo dõi sát sao và ghi lại diễn biến triệu chứng",
                "Tránh các hoạt động nặng và nghỉ ngơi nhiều"
            ],
            'severe': [
                "Cần khám bác sĩ ngay trong ngày",
                "Không tự ý dùng thuốc mà chưa có chỉ định",
                "Chuẩn bị đến bệnh viện nếu triệu chứng nặng lên"
            ],
            'emergency': [
                "GỌI 115 NGAY LẬP TỨC",
                "Đến phòng cấp cứu gần nhất",
                "Không trì hoãn việc tìm kiếm chăm sóc y tế"
            ]
        }
    
    def generate_disease_knowledge(self, disease_data: Dict) -> List[Dict]:
        """Generate comprehensive knowledge for a disease"""
        knowledge_items = []
        
        disease_name = disease_data['name']
        category = disease_data.get('category', 'general')
        description = disease_data.get('description', '')
        symptoms = disease_data.get('symptoms', [])
        recommendations = disease_data.get('recommendations', '')
        severity = disease_data.get('severity_level', 'medium')
        
        # Generate different types of knowledge
        knowledge_types = [
            ('disease_description', {
                'disease': disease_name,
                'category': category,
                'symptoms': ', '.join(symptoms[:5]),
                'description': description,
                'treatment_info': recommendations
            }),
            ('symptom_analysis', {
                'symptom': symptoms[0] if symptoms else 'các triệu chứng',
                'diseases': disease_name,
                'medical_advice': random.choice(self.advice_templates.get(severity, self.advice_templates['moderate'])),
                'care_instructions': recommendations,
                'when_to_see_doctor': self._get_doctor_advice(severity)
            }),
            ('treatment_guidance', {
                'disease': disease_name,
                'recommendations': recommendations,
                'treatment_steps': recommendations,
                'immediate_care': recommendations,
                'severity_note': self._get_severity_note(severity),
                'follow_up': "Theo dõi diễn biến và tái khám theo hẹn",
                'long_term_management': "Tuân thủ điều trị và thay đổi lối sống"
            })
        ]
        
        # Add emergency knowledge for severe cases
        if severity in ['severe', 'emergency']:
            emergency_symptoms = ', '.join(symptoms[:3])
            knowledge_types.append(('emergency_protocols', {
                'emergency_symptoms': emergency_symptoms,
                'emergency_action': 'tìm kiếm chăm sóc y tế khẩn cấp',
                'immediate_steps': 'Gọi 115 hoặc đến cấp cứu ngay',
                'emergency_response': 'Đây là tình huống cấp cứu',
                'urgency_note': 'Không được trì hoãn',
                'contact_info': 'Hotline cấp cứu: 115'
            }))
        
        # Generate knowledge items
        for knowledge_type, template_vars in knowledge_types:
            try:
                templates = self.knowledge_templates[knowledge_type]
                for template in templates[:2]:  # Use 2 templates per type
                    content = template.format(**template_vars)
                    
                    # Generate embedding
                    embedding = self.encoder.encode(content)
                    
                    knowledge_items.append({
                        'content': content,
                        'topic': f"{knowledge_type}_{disease_name}",
                        'embedding': embedding,
                        'confidence': self._calculate_confidence(knowledge_type, severity),
                        'source_type': 'generated',
                        'knowledge_type': knowledge_type
                    })
                    
            except KeyError as e:
                logger.warning(f"Missing template variable {e} for {knowledge_type}")
                continue
            except Exception as e:
                logger.error(f"Error generating knowledge: {e}")
                continue
        
        return knowledge_items
    
    def _get_doctor_advice(self, severity: str) -> str:
        """Get appropriate doctor consultation advice"""
        advice_map = {
            'mild': 'Nên tham khảo bác sĩ nếu triệu chứng không cải thiện sau 3-5 ngày',
            'moderate': 'Khuyên nên đặt lịch khám với bác sĩ trong 1-2 ngày tới',
            'severe': 'Cần khám bác sĩ ngay trong ngày hôm nay',
            'emergency': 'Cần chăm sóc y tế khẩn cấp ngay lập tức'
        }
        return advice_map.get(severity, advice_map['moderate'])
    
    def _get_severity_note(self, severity: str) -> str:
        """Get severity-appropriate note"""
        notes = {
            'mild': 'Thường tự khỏi với chăm sóc tại nhà',
            'moderate': 'Cần theo dõi sát và có thể cần điều trị y tế',
            'severe': 'Yêu cầu chăm sóc y tế chuyên nghiệp',
            'emergency': 'Tình trạng khẩn cấp cần cấp cứu ngay'
        }
        return notes.get(severity, notes['moderate'])
    
    def _calculate_confidence(self, knowledge_type: str, severity: str) -> float:
        """Calculate confidence score for generated knowledge"""
        base_confidence = {
            'disease_description': 0.9,
            'symptom_analysis': 0.8,
            'treatment_guidance': 0.85,
            'emergency_protocols': 0.95
        }
        
        severity_modifier = {
            'mild': 0.0,
            'moderate': 0.05,
            'severe': 0.1,
            'emergency': 0.15
        }
        
        return min(1.0, base_confidence.get(knowledge_type, 0.8) + severity_modifier.get(severity, 0.0))

