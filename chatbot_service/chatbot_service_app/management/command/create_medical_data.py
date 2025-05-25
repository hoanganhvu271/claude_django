# Management command để tạo dữ liệu mẫu cho hệ thống chẩn đoán
# Lưu file này tại: chatbot_service/chatbot_service_app/management/commands/create_medical_data.py

from django.core.management.base import BaseCommand
from chatbot_service_app.models import (
    Symptom, Disease, DiseaseSymptom, ResponseTemplate, FAQ
)

class Command(BaseCommand):
    help = 'Tạo dữ liệu mẫu cho hệ thống chẩn đoán y tế'

    def handle(self, *args, **options):
        self.stdout.write('Đang tạo dữ liệu mẫu...')
        
        # Tạo triệu chứng
        self.create_symptoms()
        
        # Tạo bệnh
        self.create_diseases()
        
        # Tạo mối quan hệ bệnh-triệu chứng
        self.create_disease_symptoms()
        
        # Tạo response templates
        self.create_response_templates()
        
        # Tạo FAQ
        self.create_faqs()
        
        self.stdout.write(
            self.style.SUCCESS('Đã tạo xong dữ liệu mẫu cho hệ thống chẩn đoán!')
        )

    def create_symptoms(self):
        symptoms_data = [
            {
                'name': 'Đau đầu',
                'description': 'Cảm giác đau, nhức hoặc khó chịu ở vùng đầu',
                'category': 'neurological',
                'keywords': 'đau đầu, nhức đầu, đầu đau, cứng đầu, đau nửa đầu',
                'is_critical': False
            },
            {
                'name': 'Sốt',
                'description': 'Nhiệt độ cơ thể tăng cao hơn bình thường (>37.5°C)',
                'category': 'general',
                'keywords': 'sốt, nóng người, ấm người, nhiệt độ cao, bị nóng',
                'is_critical': True
            },
            {
                'name': 'Ho',
                'description': 'Phản xạ tự nhiên để làm sạch đường hô hấp',
                'category': 'respiratory',
                'keywords': 'ho, ke, ho khan, ho có đờm, bị ho',
                'is_critical': False
            },
            {
                'name': 'Buồn nôn',
                'description': 'Cảm giác khó chịu ở dạ dày, muốn nôn',
                'category': 'gastrointestinal',
                'keywords': 'buồn nôn, nôn, muốn nôn, cảm giác nôn, ợt',
                'is_critical': False
            },
            {
                'name': 'Chóng mặt',
                'description': 'Cảm giác mất thăng bằng, hoa mắt',
                'category': 'neurological',
                'keywords': 'chóng mặt, hoa mắt, choáng váng, lảo đảo',
                'is_critical': False
            },
            {
                'name': 'Đau ngực',
                'description': 'Đau hoặc khó chịu ở vùng ngực',
                'category': 'cardiovascular',
                'keywords': 'đau ngực, tức ngực, ngực đau, đau tim',
                'is_critical': True
            },
            {
                'name': 'Khó thở',
                'description': 'Cảm giác thiếu không khí, thở khó khăn',
                'category': 'respiratory',
                'keywords': 'khó thở, thở khó, ngạt thở, thở gấp, hụt hơi',
                'is_critical': True
            },
            {
                'name': 'Đau bụng',
                'description': 'Đau hoặc khó chịu ở vùng bụng',
                'category': 'gastrointestinal',
                'keywords': 'đau bụng, đau dạ dày, quặn bụng, bụng đau',
                'is_critical': False
            },
            {
                'name': 'Mệt mỏi',
                'description': 'Cảm giác kiệt sức, không có năng lượng',
                'category': 'general',
                'keywords': 'mệt mỏi, mệt, uể oải, kiệt sức, không có sức',
                'is_critical': False
            },
            {
                'name': 'Tiêu chảy',
                'description': 'Đi ngoài nhiều lần với phân lỏng',
                'category': 'gastrointestinal',
                'keywords': 'tiêu chảy, đi lỏng, đi ngoài nhiều, lỏng bụng',
                'is_critical': False
            },
            {
                'name': 'Đau họng',
                'description': 'Đau, rát hoặc khó chịu ở cổ họng',
                'category': 'respiratory',
                'keywords': 'đau họng, rát họng, khàn giọng, nuốt đau',
                'is_critical': False
            },
            {
                'name': 'Phát ban',
                'description': 'Xuất hiện các đốm đỏ hoặc thay đổi trên da',
                'category': 'dermatological',
                'keywords': 'phát ban, nổi mề đay, ngứa, da đỏ, ban đỏ',
                'is_critical': False
            }
        ]
        
        for symptom_data in symptoms_data:
            symptom, created = Symptom.objects.get_or_create(
                name=symptom_data['name'],
                defaults=symptom_data
            )
            if created:
                self.stdout.write(f'Đã tạo triệu chứng: {symptom.name}')

    def create_diseases(self):
        diseases_data = [
            {
                'name': 'Cảm lạnh thông thường',
                'description': 'Nhiễm virus đường hô hấp trên, thường tự khỏi',
                'category': 'respiratory',
                'urgency_level': 'low',
                'prevalence': 'common',
                'recommendations': 'Nghỉ ngơi, uống nhiều nước, dùng thuốc hạ sốt nếu cần'
            },
            {
                'name': 'Viêm họng',
                'description': 'Viêm nhiễm ở cổ họng do virus hoặc vi khuẩn',
                'category': 'respiratory',
                'urgency_level': 'low',
                'prevalence': 'common',
                'recommendations': 'Súc miệng nước muối, uống nhiều nước ấm, khám bác sĩ nếu không khỏi'
            },
            {
                'name': 'Đau nửa đầu (Migraine)',
                'description': 'Đau đầu một bên, thường kèm buồn nôn',
                'category': 'neurological',
                'urgency_level': 'medium',
                'prevalence': 'common',
                'recommendations': 'Nghỉ ngơi trong phòng tối, tránh ánh sáng, dùng thuốc giảm đau'
            },
            {
                'name': 'Viêm dạ dày',
                'description': 'Viêm niêm mạc dạ dày gây đau bụng',
                'category': 'gastrointestinal',
                'urgency_level': 'medium',
                'prevalence': 'common',
                'recommendations': 'Ăn nhẹ, tránh đồ cay nóng, uống thuốc kháng acid'
            },
            {
                'name': 'Nhiễm khuẩn đường tiết niệu',
                'description': 'Nhiễm khuẩn ở bàng quang hoặc thận',
                'category': 'urological',
                'urgency_level': 'medium',
                'prevalence': 'common',
                'recommendations': 'Uống nhiều nước, đi tiểu thường xuyên, khám bác sĩ để dùng kháng sinh'
            },
            {
                'name': 'Đau tim (Nhồi máu cơ tim)',
                'description': 'Tắc nghẽn động mạch cung cấp máu cho tim',
                'category': 'cardiovascular',
                'urgency_level': 'emergency',
                'prevalence': 'uncommon',
                'recommendations': 'GỌI CẤP CỨU 115 NGAY LẬP TỨC!'
            },
            {
                'name': 'Hen suyễn',
                'description': 'Viêm và co thắt đường hô hấp',
                'category': 'respiratory',
                'urgency_level': 'high',
                'prevalence': 'common',
                'recommendations': 'Dùng thuốc xịt giãn phế quản, tránh tác nhân gây dị ứng'
            },
            {
                'name': 'Viêm phế quản',
                'description': 'Viêm các ống phế quản trong phổi',
                'category': 'respiratory',
                'urgency_level': 'medium',
                'prevalence': 'common',
                'recommendations': 'Nghỉ ngơi, uống nhiều nước, dùng thuốc long đờm'
            },
            {
                'name': 'Rối loạn tiêu hóa',
                'description': 'Vấn đề về tiêu hóa gây đau bụng, tiêu chảy',
                'category': 'gastrointestinal',
                'urgency_level': 'low',
                'prevalence': 'common',
                'recommendations': 'Ăn nhẹ, uống nhiều nước, tránh đồ ăn có dầu mỡ'
            },
            {
                'name': 'Đột quỵ',
                'description': 'Thiếu máu não hoặc xuất huyết não',
                'category': 'neurological',
                'urgency_level': 'emergency',
                'prevalence': 'uncommon',
                'recommendations': 'GỌI CẤP CỨU 115 NGAY LẬP TỨC!'
            }
        ]
        
        for disease_data in diseases_data:
            disease, created = Disease.objects.get_or_create(
                name=disease_data['name'],
                defaults=disease_data
            )
            if created:
                self.stdout.write(f'Đã tạo bệnh: {disease.name}')

    def create_disease_symptoms(self):
        # Định nghĩa mối quan hệ bệnh-triệu chứng
        disease_symptoms_mapping = {
            'Cảm lạnh thông thường': [
                ('Ho', 2.0, False, 'very_common'),
                ('Đau họng', 1.8, False, 'common'),
                ('Sốt', 1.5, False, 'common'),
                ('Mệt mỏi', 1.3, False, 'common'),
                ('Đau đầu', 1.0, False, 'common')
            ],
            'Viêm họng': [
                ('Đau họng', 3.0, True, 'very_common'),
                ('Sốt', 2.0, False, 'common'),
                ('Đau đầu', 1.5, False, 'common'),
                ('Mệt mỏi', 1.2, False, 'common')
            ],
            'Đau nửa đầu (Migraine)': [
                ('Đau đầu', 3.0, True, 'very_common'),
                ('Buồn nôn', 2.5, False, 'very_common'),
                ('Chóng mặt', 2.0, False, 'common'),
                ('Mệt mỏi', 1.5, False, 'common')
            ],
            'Viêm dạ dày': [
                ('Đau bụng', 3.0, True, 'very_common'),
                ('Buồn nôn', 2.5, False, 'very_common'),
                ('Mệt mỏi', 1.5, False, 'common')
            ],
            'Nhiễm khuẩn đường tiết niệu': [
                ('Đau bụng', 2.5, False, 'common'),
                ('Sốt', 2.0, False, 'common'),
                ('Mệt mỏi', 1.5, False, 'common')
            ],
            'Đau tim (Nhồi máu cơ tim)': [
                ('Đau ngực', 3.0, True, 'very_common'),
                ('Khó thở', 2.8, False, 'very_common'),
                ('Buồn nôn', 2.0, False, 'common'),
                ('Chóng mặt', 2.0, False, 'common'),
                ('Mệt mỏi', 1.8, False, 'common')
            ],
            'Hen suyễn': [
                ('Khó thở', 3.0, True, 'very_common'),
                ('Ho', 2.5, False, 'very_common'),
                ('Đau ngực', 2.0, False, 'common'),
                ('Mệt mỏi', 1.5, False, 'common')
            ],
            'Viêm phế quản': [
                ('Ho', 3.0, True, 'very_common'),
                ('Sốt', 2.0, False, 'common'),
                ('Mệt mỏi', 1.8, False, 'common'),
                ('Đau ngực', 1.5, False, 'common')
            ],
            'Rối loạn tiêu hóa': [
                ('Đau bụng', 2.5, False, 'very_common'),
                ('Tiêu chảy', 2.8, False, 'very_common'),
                ('Buồn nôn', 2.0, False, 'common'),
                ('Mệt mỏi', 1.5, False, 'common')
            ],
            'Đột quỵ': [
                ('Đau đầu', 3.0, False, 'common'),
                ('Chóng mặt', 2.8, False, 'very_common'),
                ('Buồn nôn', 2.0, False, 'common'),
                ('Mệt mỏi', 2.0, False, 'common')
            ]
        }
        
        for disease_name, symptoms in disease_symptoms_mapping.items():
            try:
                disease = Disease.objects.get(name=disease_name)
                for symptom_name, weight, is_required, frequency in symptoms:
                    try:
                        symptom = Symptom.objects.get(name=symptom_name)
                        disease_symptom, created = DiseaseSymptom.objects.get_or_create(
                            disease=disease,
                            symptom=symptom,
                            defaults={
                                'weight': weight,
                                'is_required': is_required,
                                'frequency': frequency
                            }
                        )
                        if created:
                            self.stdout.write(f'Đã liên kết {disease_name} - {symptom_name}')
                    except Symptom.DoesNotExist:
                        self.stdout.write(f'Không tìm thấy triệu chứng: {symptom_name}')
            except Disease.DoesNotExist:
                self.stdout.write(f'Không tìm thấy bệnh: {disease_name}')

    def create_response_templates(self):
        templates_data = [
            {
                'name': 'medical_welcome',
                'template_text': """🩺 Xin chào! Tôi là trợ lý y tế AI của bệnh viện.

Tôi có thể giúp bạn:
• Phân tích triệu chứng và đưa ra chẩn đoán sơ bộ
• Đề xuất các bước cần thiết tiếp theo
• Đánh giá mức độ khẩn cấp của tình trạng

⚠️ **Lưu ý quan trọng**: Tôi chỉ cung cấp thông tin tham khảo. Hãy luôn tham khảo ý kiến bác sĩ chuyên khoa cho chẩn đoán chính xác.

Hãy mô tả triệu chứng bạn đang gặp phải một cách chi tiết nhất có thể.""",
                'category': 'greeting',
                'variables': []
            },
            {
                'name': 'symptom_inquiry',
                'template_text': """Tôi đã ghi nhận triệu chứng: **{symptoms}**

Để đưa ra đánh giá chính xác hơn, bạn có thể cho tôi biết:
• Mức độ nghiêm trọng từ 1-10?
• Triệu chứng bắt đầu từ khi nào?
• Có gì khiến triệu chứng tệ hơn hoặc tốt hơn không?
• Bạn có triệu chứng nào khác kèm theo không?""",
                'category': 'symptom_inquiry',
                'variables': ['symptoms']
            },
            {
                'name': 'diagnosis_result',
                'template_text': """📋 **Kết quả phân tích sơ bộ:**

Dựa trên triệu chứng bạn mô tả, các khả năng có thể là:

{possible_diseases}

**Mức độ tin cậy:** {confidence_level}

**Khuyến nghị tiếp theo:**
{recommendations}

⚠️ Đây chỉ là đánh giá sơ bộ. Hãy tham khảo ý kiến bác sĩ chuyên khoa để có chẩn đoán chính xác.""",
                'category': 'diagnosis',
                'variables': ['possible_diseases', 'confidence_level', 'recommendations']
            },
            {
                'name': 'emergency_alert',
                'template_text': """🚨 **CẢNH BÁO: CẦN CHĂM SÓC Y TẾ KHẨN CẤP**

Dựa trên triệu chứng bạn mô tả, có thể bạn đang gặp tình trạng nghiêm trọng cần được điều trị ngay lập tức.

**Khuyến nghị:**
• Đến phòng cấp cứu NGAY LẬP TỨC
• Gọi 115 nếu cần thiết
• Không trì hoãn việc tìm kiếm sự chăm sóc y tế

**Các tình trạng có thể:**
{emergency_conditions}

Đây chỉ là đánh giá sơ bộ. Hãy tìm kiếm sự chăm sóc y tế chuyên nghiệp ngay.""",
                'category': 'emergency',
                'variables': ['emergency_conditions']
            },
            {
                'name': 'clarification_request',
                'template_text': """Tôi cần thêm thông tin để đưa ra đánh giá chính xác hơn.

Bạn có thể mô tả:
• Triệu chứng có thay đổi theo thời gian không?
• Có triệu chứng nào khác kèm theo?
• Bạn đã dùng thuốc gì chưa?
• Có tiền sử bệnh lý nào không?

Thông tin càng chi tiết sẽ giúp tôi đưa ra đánh giá càng chính xác.""",
                'category': 'clarification',
                'variables': []
            },
            {
                'name': 'general_health_advice',
                'template_text': """💡 **Lời khuyên chung về sức khỏe:**

{advice_content}

**Những dấu hiệu cần đến bác sĩ ngay:**
• Triệu chứng nặng lên đột ngột
• Sốt cao không hạ (>39°C)
• Đau ngực hoặc khó thở
• Chảy máu bất thường
• Mất ý thức hoặc co giật

Hãy luôn chú ý đến cơ thể và không ngần ngại tìm kiếm sự chăm sóc y tế khi cần thiết.""",
                'category': 'advice',
                'variables': ['advice_content']
            }
        ]
        
        for template_data in templates_data:
            template, created = ResponseTemplate.objects.get_or_create(
                name=template_data['name'],
                defaults=template_data
            )
            if created:
                self.stdout.write(f'Đã tạo template: {template.name}')

    def create_faqs(self):
        faqs_data = [
            {
                'question': 'Làm thế nào để đặt lịch khám?',
                'answer': 'Bạn có thể đặt lịch khám bằng cách gọi điện thoại đến số hotline, sử dụng ứng dụng di động hoặc website của bệnh viện, hoặc đến trực tiếp quầy lễ tân.',
                'category': 'appointment',
                'tags': 'đặt lịch, khám bệnh, hẹn, appointment',
                'priority': 5
            },
            {
                'question': 'Giờ làm việc của bệnh viện?',
                'answer': 'Bệnh viện làm việc từ 7:00 - 18:00 các ngày trong tuần và 8:00 - 16:00 vào cuối tuần. Phòng cấp cứu hoạt động 24/7.',
                'category': 'general',
                'tags': 'giờ làm việc, thời gian, mở cửa',
                'priority': 4
            },
            {
                'question': 'Tôi có thể thanh toán bằng thẻ không?',
                'answer': 'Có, chúng tôi chấp nhận thanh toán bằng thẻ tín dụng, thẻ ghi nợ, chuyển khoản ngân hàng và tiền mặt.',
                'category': 'payment',
                'tags': 'thanh toán, thẻ, tiền',
                'priority': 3
            },
            {
                'question': 'Kết quả xét nghiệm có sẵn khi nào?',
                'answer': 'Kết quả xét nghiệm thường có trong vòng 24-48 giờ cho các xét nghiệm thông thường. Xét nghiệm cấp cứu có kết quả trong 2-4 giờ. Bạn sẽ nhận được thông báo khi kết quả đã sẵn sàng.',
                'category': 'laboratory',
                'tags': 'xét nghiệm, kết quả, thời gian',
                'priority': 4
            },
            {
                'question': 'Tôi quên mang thẻ bảo hiểm thì sao?',
                'answer': 'Bạn vẫn có thể khám và thanh toán trước. Sau đó có thể nộp hồ sơ bảo hiểm trong vòng 15 ngày để được hoàn lại tiền theo quy định.',
                'category': 'insurance',
                'tags': 'bảo hiểm, thẻ, quên mang',
                'priority': 3
            },
            {
                'question': 'Làm sao để biết khi nào cần đến cấp cứu?',
                'answer': 'Hãy đến cấp cứu ngay khi có: đau ngực dữ dội, khó thở nặng, đau đầu đột ngột, co giật, bất tỉnh, chảy máu nhiều, sốt cao liên tục >39°C.',
                'category': 'emergency',
                'tags': 'cấp cứu, khẩn cấp, triệu chứng nguy hiểm',
                'priority': 5
            },
            {
                'question': 'Tôi có thể tham khảo ý kiến bác sĩ online không?',
                'answer': 'Có, bệnh viện có dịch vụ tư vấn online 24/7 qua chatbot AI và video call với bác sĩ vào các khung giờ nhất định.',
                'category': 'telemedicine',
                'tags': 'online, tư vấn, video call, chatbot',
                'priority': 4
            },
            {
                'question': 'Làm thế nào để chuẩn bị cho việc khám bệnh?',
                'answer': 'Hãy mang theo giấy tờ tuy thân, thẻ bảo hiểm, kết quả xét nghiệm cũ (nếu có), danh sách thuốc đang dùng và ghi chú các triệu chứng.',
                'category': 'preparation',
                'tags': 'chuẩn bị, khám bệnh, giấy tờ',
                'priority': 3
            },
            {
                'question': 'Bệnh viện có dịch vụ đưa đón không?',
                'answer': 'Có, chúng tôi có dịch vụ xe cấp cứu và xe đưa đón cho bệnh nhân trong một số trường hợp đặc biệt. Vui lòng liên hệ để biết thêm chi tiết.',
                'category': 'transport',
                'tags': 'đưa đón, xe cấp cứu, di chuyển',
                'priority': 2
            },
            {
                'question': 'Tôi có thể xin giấy nghỉ ốm không?',
                'answer': 'Có, bác sĩ sẽ cấp giấy nghỉ ốm nếu tình trạng sức khỏe của bạn cần nghỉ ngơi điều trị. Giấy nghỉ ốm có thể được lấy tại quầy lễ tân sau khi khám.',
                'category': 'certificate',
                'tags': 'giấy nghỉ ốm, chứng nhận y tế',
                'priority': 3
            }
        ]
        
        for faq_data in faqs_data:
            faq, created = FAQ.objects.get_or_create(
                question=faq_data['question'],
                defaults=faq_data
            )
            if created:
                self.stdout.write(f'Đã tạo FAQ: {faq.question[:50]}...')

        self.stdout.write('Hoàn thành việc tạo dữ liệu mẫu!')