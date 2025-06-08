import random

class MedicalDataLoader:
    """Load and create medical training data"""
    
    @staticmethod
    def get_sample_medical_data():
        """Get comprehensive sample medical data for training"""
        return [
            {
                'disease': 'Cảm lạnh thông thường',
                'category': 'respiratory',
                'severity': 'mild',
                'description': 'Nhiễm virus đường hô hấp trên, thường tự khỏi trong 7-10 ngày',
                'recommendations': 'Nghỉ ngơi, uống nhiều nước, dùng thuốc hạ sốt nếu cần',
                'symptoms': [
                    ('ho', 0.8, 1.2),
                    ('chảy nước mũi', 0.9, 1.5),
                    ('đau họng', 0.7, 1.0),
                    ('sốt', 0.6, 0.8),
                    ('mệt mỏi', 0.7, 0.9),
                    ('đau đầu', 0.5, 0.7)
                ]
            },
            {
                'disease': 'Cúm mùa',
                'category': 'respiratory',
                'severity': 'medium',
                'description': 'Nhiễm virus cúm, triệu chứng nặng hơn cảm lạnh',
                'recommendations': 'Nghỉ ngơi tuyệt đối, thuốc kháng virus nếu trong 48h đầu',
                'symptoms': [
                    ('sốt', 0.95, 2.5),
                    ('ho', 0.8, 2.0),
                    ('đau đầu', 0.85, 2.2),
                    ('mệt mỏi', 0.9, 2.5),
                    ('đau khớp', 0.8, 2.0),
                    ('chóng mặt', 0.6, 1.5)
                ]
            },
            {
                'disease': 'Viêm họng cấp',
                'category': 'respiratory',
                'severity': 'medium',
                'description': 'Viêm nhiễm cấp tính ở cổ họng',
                'recommendations': 'Súc miệng nước muối, thuốc kháng sinh nếu do vi khuẩn',
                'symptoms': [
                    ('đau họng', 0.98, 3.0),
                    ('sốt', 0.8, 2.0),
                    ('đau đầu', 0.6, 1.5),
                    ('mệt mỏi', 0.7, 1.5)
                ]
            },
            {
                'disease': 'Đau nửa đầu',
                'category': 'neurological',
                'severity': 'medium',
                'description': 'Cơn đau đầu dữ dội, thường một bên',
                'recommendations': 'Nghỉ ngơi trong phòng tối, thuốc giảm đau chuyên biệt',
                'symptoms': [
                    ('đau đầu', 0.98, 3.0),
                    ('buồn nôn', 0.85, 2.5),
                    ('chóng mặt', 0.7, 2.0),
                    ('mệt mỏi', 0.8, 1.8)
                ]
            },
            {
                'disease': 'Viêm dạ dày cấp',
                'category': 'gastrointestinal',
                'severity': 'medium',
                'description': 'Viêm cấp tính niêm mạc dạ dày',
                'recommendations': 'Nhịn ăn tạm thời, uống nhiều nước, thuốc kháng acid',
                'symptoms': [
                    ('đau bụng', 0.95, 3.0),
                    ('buồn nôn', 0.9, 2.5),
                    ('mệt mỏi', 0.6, 1.5)
                ]
            },
            {
                'disease': 'Nhồi máu cơ tim',
                'category': 'cardiovascular',
                'severity': 'emergency',
                'description': 'Tắc nghẽn hoàn toàn động mạch cung cấp máu cho tim',
                'recommendations': 'GỌI CẤP CỨU 115 NGAY! Không được trì hoãn',
                'symptoms': [
                    ('đau ngực', 0.95, 3.0),
                    ('khó thở', 0.85, 2.8),
                    ('buồn nôn', 0.7, 2.0),
                    ('chóng mặt', 0.65, 2.0),
                    ('mệt mỏi', 0.8, 2.0)
                ]
            },
            {
                'disease': 'Hen suyễn cấp',
                'category': 'respiratory',
                'severity': 'severe',
                'description': 'Co thắt phế quản gây khó thở',
                'recommendations': 'Thuốc xịt giãn phế quản, đến bệnh viện nếu không đỡ',
                'symptoms': [
                    ('khó thở', 0.95, 3.0),
                    ('ho', 0.8, 2.0),
                    ('đau ngực', 0.6, 1.8),
                    ('mệt mỏi', 0.7, 1.5)
                ]
            },
            {
                'disease': 'Ngộ độc thực phẩm',
                'category': 'gastrointestinal',
                'severity': 'medium',
                'description': 'Nhiễm độc do thực phẩm bẩn hoặc hỏng',
                'recommendations': 'Bù nước điện giải, nhịn ăn tạm thời',
                'symptoms': [
                    ('đau bụng', 0.9, 2.5),
                    ('tiêu chảy', 0.95, 3.0),
                    ('buồn nôn', 0.9, 2.8),
                    ('mệt mỏi', 0.7, 2.0),
                    ('sốt', 0.6, 1.5)
                ]
            },
            {
                'disease': 'Đau đầu căng thẳng',
                'category': 'neurological',
                'severity': 'mild',
                'description': 'Đau đầu do stress, mệt mỏi',
                'recommendations': 'Nghỉ ngơi, massage, giảm stress',
                'symptoms': [
                    ('đau đầu', 0.9, 2.5),
                    ('mệt mỏi', 0.8, 2.0),
                    ('chóng mặt', 0.5, 1.0)
                ]
            },
            {
                'disease': 'Viêm amidan',
                'category': 'respiratory',
                'severity': 'medium',
                'description': 'Viêm nhiễm amidan do vi khuẩn hoặc virus',
                'recommendations': 'Thuốc kháng sinh, súc miệng, uống nước ấm',
                'symptoms': [
                    ('đau họng', 0.95, 3.0),
                    ('sốt', 0.85, 2.5),
                    ('đau đầu', 0.6, 1.5),
                    ('mệt mỏi', 0.7, 1.8)
                ]
            }
        ]
    
    @staticmethod
    def create_medical_data(ml_engine):
        """Create medical data in database"""
        from .models import Disease, Symptom, DiseaseSymptom, KnowledgeBase
        
        medical_data = MedicalDataLoader.get_sample_medical_data()
        
        created_diseases = 0
        created_symptoms = 0
        created_relations = 0
        
        for data in medical_data:
            # Create disease
            disease, created = Disease.objects.get_or_create(
                name=data['disease'],
                defaults={
                    'description': data['description'],
                    'category': data['category'],
                    'severity_level': data['severity'],
                    'recommendations': data['recommendations']
                }
            )
            if created:
                created_diseases += 1
            
            # Create symptoms and relations
            for symptom_name, probability, importance in data['symptoms']:
                symptom, created = Symptom.objects.get_or_create(
                    name=symptom_name,
                    defaults={
                        'description': f'Triệu chứng {symptom_name}',
                        'category': data['category'],
                        'is_critical': importance > 2.5
                    }
                )
                if created:
                    created_symptoms += 1
                
                # Create relation
                relation, created = DiseaseSymptom.objects.get_or_create(
                    disease=disease,
                    symptom=symptom,
                    defaults={
                        'probability': probability,
                        'importance': importance
                    }
                )
                if created:
                    created_relations += 1
        
        # Generate knowledge base
        knowledge_count = 0
        for disease in Disease.objects.all():
            symptoms = [ds.symptom.name for ds in disease.diseasesymptom_set.all()]
            
            disease_data = {
                'name': disease.name,
                'category': disease.category,
                'description': disease.description,
                'symptoms': symptoms,
                'recommendations': disease.recommendations,
                'severity_level': disease.severity_level
            }
            
            knowledge_items = ml_engine.knowledge_generator.generate_disease_knowledge(disease_data)
            
            for item in knowledge_items:
                kb, created = KnowledgeBase.objects.get_or_create(
                    topic=item['topic'],
                    defaults={
                        'content': item['content'],
                        'confidence': item['confidence'],
                        'source_type': item['source_type']
                    }
                )
                if created:
                    kb.set_embedding(item['embedding'])
                    kb.save()
                    knowledge_count += 1
        
        return {
            'diseases': created_diseases,
            'symptoms': created_symptoms,
            'relations': created_relations,
            'knowledge': knowledge_count
        }
