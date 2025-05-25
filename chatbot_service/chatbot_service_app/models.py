from django.db import models

class ChatSession(models.Model):
    user_id = models.IntegerField()
    session_id = models.CharField(max_length=100, unique=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    session_type = models.CharField(max_length=50, default='general')
    # Thêm thông tin chẩn đoán
    current_symptoms = models.JSONField(default=dict, blank=True)  # Lưu triệu chứng hiện tại
    preliminary_diagnosis = models.TextField(blank=True)  # Chẩn đoán sơ bộ
    confidence_score = models.FloatField(null=True, blank=True)  # Độ tin cậy chẩn đoán

    def __str__(self):
        return f"Session {self.session_id} - User {self.user_id}"

class ChatMessage(models.Model):
    SENDER_CHOICES = [
        ('user', 'User'),
        ('bot', 'Bot'),
    ]
    
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    intent = models.CharField(max_length=100, blank=True)  # For bot responses
    confidence_score = models.FloatField(null=True, blank=True)
    # Thêm metadata cho tin nhắn chẩn đoán
    message_type = models.CharField(max_length=50, default='general')  # 'symptom', 'diagnosis', 'recommendation'
    extracted_symptoms = models.JSONField(default=list, blank=True)  # Triệu chứng được trích xuất

    def __str__(self):
        return f"{self.sender}: {self.message[:50]}..."

class FAQ(models.Model):
    question = models.TextField()
    answer = models.TextField()
    category = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Thêm tags cho tìm kiếm tốt hơn
    tags = models.CharField(max_length=200, blank=True)
    priority = models.IntegerField(default=0)  # Ưu tiên hiển thị

    def __str__(self):
        return self.question[:100]

# Model mới cho hệ thống chẩn đoán
class Symptom(models.Model):
    """Triệu chứng bệnh"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    category = models.CharField(max_length=50)  # 'general', 'respiratory', 'cardiovascular', etc.
    keywords = models.TextField(help_text="Từ khóa để nhận diện triệu chứng, phân cách bằng dấu phẩy")
    severity_levels = models.JSONField(default=list)  # ['mild', 'moderate', 'severe']
    is_critical = models.BooleanField(default=False)  # Triệu chứng nguy hiểm cần cấp cứu
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['category', 'name']

class Disease(models.Model):
    """Bệnh"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    category = models.CharField(max_length=50)
    symptoms = models.ManyToManyField(Symptom, through='DiseaseSymptom')
    common_age_groups = models.CharField(max_length=100, blank=True)  # 'children', 'adults', 'elderly'
    prevalence = models.CharField(max_length=20, default='common')  # 'rare', 'uncommon', 'common'
    urgency_level = models.CharField(max_length=20, default='low')  # 'low', 'medium', 'high', 'emergency'
    recommendations = models.TextField(blank=True)  # Khuyến nghị điều trị ban đầu
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['category', 'name']

class DiseaseSymptom(models.Model):
    """Mối quan hệ giữa bệnh và triệu chứng với trọng số"""
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    symptom = models.ForeignKey(Symptom, on_delete=models.CASCADE)
    weight = models.FloatField(default=1.0)  # Trọng số quan trọng của triệu chứng với bệnh
    is_required = models.BooleanField(default=False)  # Triệu chứng bắt buộc
    frequency = models.CharField(max_length=20, default='common')  # 'rare', 'common', 'very_common'

    class Meta:
        unique_together = ['disease', 'symptom']

class DiagnosisSession(models.Model):
    """Phiên chẩn đoán"""
    chat_session = models.OneToOneField(ChatSession, on_delete=models.CASCADE)
    reported_symptoms = models.ManyToManyField(Symptom, through='ReportedSymptom')
    possible_diseases = models.JSONField(default=list)  # Danh sách bệnh có thể với điểm số
    final_recommendations = models.TextField(blank=True)
    confidence_level = models.CharField(max_length=20, default='low')  # 'low', 'medium', 'high'
    needs_urgent_care = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Diagnosis for session {self.chat_session.session_id}"

class ReportedSymptom(models.Model):
    """Triệu chứng được báo cáo trong phiên chẩn đoán"""
    diagnosis_session = models.ForeignKey(DiagnosisSession, on_delete=models.CASCADE)
    symptom = models.ForeignKey(Symptom, on_delete=models.CASCADE)
    severity = models.CharField(max_length=20, default='mild')  # 'mild', 'moderate', 'severe'
    duration = models.CharField(max_length=50, blank=True)  # 'hours', 'days', 'weeks', 'months'
    additional_details = models.TextField(blank=True)
    reported_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['diagnosis_session', 'symptom']

# Template cho câu trả lời chatbot
class ResponseTemplate(models.Model):
    """Template cho các loại phản hồi của chatbot"""
    name = models.CharField(max_length=100, unique=True)
    template_text = models.TextField()
    category = models.CharField(max_length=50)  # 'greeting', 'symptom_inquiry', 'diagnosis', 'recommendation'
    variables = models.JSONField(default=list)  # Danh sách biến có thể thay thế trong template
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def render(self, **kwargs):
        """Render template với các biến"""
        text = self.template_text
        for key, value in kwargs.items():
            text = text.replace(f"{{{key}}}", str(value))
        return text