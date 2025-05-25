import re
import json
import uuid
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q, Count
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import (
    ChatSession, ChatMessage, FAQ, Symptom, Disease, DiseaseSymptom,
    DiagnosisSession, ReportedSymptom, ResponseTemplate
)
from .serializers import (
    ChatSessionSerializer, ChatMessageSerializer, FAQSerializer,
    SymptomSerializer, DiseaseSerializer, DiagnosisSessionSerializer,
    ReportedSymptomSerializer, ResponseTemplateSerializer
)
from .diagnosis_engine import DiagnosisEngine

# =================
# Session Management
# =================

@api_view(['POST'])
@permission_classes([AllowAny])
def create_chat_session(request):
    """Tạo phiên chat mới với hỗ trợ chẩn đoán"""
    user_id = request.data.get('user_id', 1)  # Default user if not provided
    session_type = request.data.get('session_type', 'general')
    session_id = str(uuid.uuid4())
    
    session = ChatSession.objects.create(
        user_id=user_id,
        session_id=session_id,
        session_type=session_type
    )
    
    # Tạo phiên chẩn đoán nếu là loại medical
    if session_type == 'medical':
        DiagnosisSession.objects.create(chat_session=session)
        welcome_message = get_medical_welcome_message()
    else:
        welcome_message = "Xin chào! Tôi có thể giúp gì cho bạn hôm nay? Tôi có thể hỗ trợ bạn về thông tin y tế, đặt lịch hẹn, hoặc các câu hỏi chung về bệnh viện."
    
    # Tạo tin nhắn chào mừng
    ChatMessage.objects.create(
        session=session,
        sender='bot',
        message=welcome_message,
        intent='greeting',
        message_type='greeting'
    )
    
    return Response({
        'session_id': session.session_id,
        'session_type': session_type,
        'message': welcome_message,
        'status': 'created'
    }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_session_history(request, session_id):
    """Lấy lịch sử chat của phiên"""
    try:
        session = ChatSession.objects.get(session_id=session_id)
        messages = session.messages.all().order_by('timestamp')
        
        return Response({
            'session': ChatSessionSerializer(session).data,
            'messages': ChatMessageSerializer(messages, many=True).data,
            'total_messages': messages.count()
        })
    except ChatSession.DoesNotExist:
        return Response({'error': 'Session not found'}, status=404)

@api_view(['PUT'])
@permission_classes([AllowAny])
def end_chat_session(request, session_id):
    """Kết thúc phiên chat"""
    try:
        session = ChatSession.objects.get(session_id=session_id)
        session.is_active = False
        session.end_time = timezone.now()
        session.save()
        
        # Tạo tóm tắt nếu là phiên y tế
        summary = None
        if session.session_type == 'medical' and hasattr(session, 'diagnosissession'):
            summary = generate_session_summary(session.diagnosissession)
        
        return Response({
            'status': 'Session ended successfully',
            'summary': summary,
            'duration_minutes': calculate_session_duration(session)
        })
    except ChatSession.DoesNotExist:
        return Response({'error': 'Session not found'}, status=404)

# =================
# Message Handling
# =================

@api_view(['POST'])
@permission_classes([AllowAny])
def send_message(request):
    """Gửi tin nhắn và nhận phản hồi từ chatbot với khả năng chẩn đoán"""
    session_id = request.data.get('session_id')
    message = request.data.get('message', '').strip()
    
    if not session_id or not message:
        return Response({'error': 'Session ID and message are required'}, status=400)
    
    try:
        session = ChatSession.objects.get(session_id=session_id, is_active=True)
        
        # Lưu tin nhắn của người dùng
        user_message = ChatMessage.objects.create(
            session=session,
            sender='user',
            message=message
        )
        
        # Xử lý tin nhắn và tạo phản hồi
        if session.session_type == 'medical':
            bot_response, extracted_symptoms = process_medical_message(session, message)
            user_message.extracted_symptoms = extracted_symptoms
            user_message.message_type = 'symptom_report'
            user_message.save()
        else:
            bot_response = process_general_message(session, message)
        
        # Lưu phản hồi của bot
        bot_message = ChatMessage.objects.create(
            session=session,
            sender='bot',
            message=bot_response['message'],
            intent=bot_response.get('intent', ''),
            confidence_score=bot_response.get('confidence', None),
            message_type=bot_response.get('type', 'general')
        )
        
        return Response({
            'user_message': ChatMessageSerializer(user_message).data,
            'bot_response': ChatMessageSerializer(bot_message).data,
            'session_status': bot_response.get('session_status', 'active'),
            'recommendations': bot_response.get('recommendations', []),
            'follow_up_questions': bot_response.get('follow_up_questions', [])
        })
        
    except ChatSession.DoesNotExist:
        return Response({'error': 'Session not found or inactive'}, status=404)

# =================
# Medical Data Endpoints
# =================

class SymptomListView(generics.ListAPIView):
    """API để lấy danh sách triệu chứng"""
    queryset = Symptom.objects.all().order_by('category', 'name')
    serializer_class = SymptomSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        search = self.request.query_params.get('search')
        
        if category:
            queryset = queryset.filter(category=category)
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(keywords__icontains=search) |
                Q(description__icontains=search)
            )
        
        return queryset

class DiseaseListView(generics.ListAPIView):
    """API để lấy danh sách bệnh"""
    queryset = Disease.objects.all().order_by('category', 'name')
    serializer_class = DiseaseSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        urgency = self.request.query_params.get('urgency')
        
        if category:
            queryset = queryset.filter(category=category)
        
        if urgency:
            queryset = queryset.filter(urgency_level=urgency)
        
        return queryset

# =================
# Diagnosis Endpoints
# =================

@api_view(['GET'])
@permission_classes([AllowAny])
def get_diagnosis_result(request, session_id):
    """Lấy kết quả chẩn đoán của phiên"""
    try:
        session = ChatSession.objects.get(id=session_id)
        if not hasattr(session, 'diagnosissession'):
            return Response({'error': 'No diagnosis session found'}, status=404)
        
        diagnosis_session = session.diagnosissession
        diagnosis_engine = DiagnosisEngine()
        
        # Thực hiện chẩn đoán mới nhất
        diagnosis_result = diagnosis_engine.diagnose(diagnosis_session)
        
        return Response({
            'session_id': session.session_id,
            'diagnosis': diagnosis_result,
            'reported_symptoms': ReportedSymptomSerializer(
                diagnosis_session.reportedsymptom_set.all(), many=True
            ).data,
            'session_info': DiagnosisSessionSerializer(diagnosis_session).data
        })
    except ChatSession.DoesNotExist:
        return Response({'error': 'Session not found'}, status=404)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_diagnosis_summary(request, session_id):
    """Lấy tóm tắt chẩn đoán của phiên"""
    try:
        session = ChatSession.objects.get(id=session_id)
        if not hasattr(session, 'diagnosissession'):
            return Response({'error': 'No diagnosis session found'}, status=404)
        
        summary = generate_session_summary(session.diagnosissession)
        
        return Response({
            'session_id': session.session_id,
            'summary': summary,
            'generated_at': timezone.now().isoformat()
        })
    except ChatSession.DoesNotExist:
        return Response({'error': 'Session not found'}, status=404)

# =================
# FAQ Endpoints
# =================

class FAQListView(generics.ListAPIView):
    """API để lấy danh sách FAQ"""
    queryset = FAQ.objects.filter(is_active=True).order_by('-priority', '-created_at')
    serializer_class = FAQSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        
        if category:
            queryset = queryset.filter(category=category)
        
        return queryset

@api_view(['GET'])
@permission_classes([AllowAny])
def search_faq(request):
    """Tìm kiếm FAQ"""
    query = request.GET.get('q', '').strip()
    
    if not query:
        return Response({'error': 'Query parameter q is required'}, status=400)
    
    # Tìm kiếm trong FAQ
    faqs = FAQ.objects.filter(
        Q(question__icontains=query) |
        Q(answer__icontains=query) |
        Q(tags__icontains=query),
        is_active=True
    ).order_by('-priority')[:10]
    
    return Response({
        'query': query,
        'results': FAQSerializer(faqs, many=True).data,
        'count': faqs.count()
    })

# =================
# Health Recommendations
# =================

@api_view(['POST'])
@permission_classes([AllowAny])
def get_health_recommendations(request):
    """Lấy khuyến nghị sức khỏe dựa trên triệu chứng"""
    symptoms = request.data.get('symptoms', [])
    age = request.data.get('age')
    gender = request.data.get('gender')
    medical_history = request.data.get('medical_history', [])
    
    if not symptoms:
        return Response({'error': 'Symptoms list is required'}, status=400)
    
    # Tạo khuyến nghị dựa trên triệu chứng
    recommendations = generate_health_recommendations(symptoms, age, gender, medical_history)
    
    return Response({
        'recommendations': recommendations,
        'disclaimer': 'Đây chỉ là khuyến nghị tham khảo. Hãy luôn tham khảo ý kiến bác sĩ chuyên khoa.',
        'generated_at': timezone.now().isoformat()
    })

# =================
# Emergency Detection
# =================

@api_view(['POST'])
@permission_classes([AllowAny])
def check_emergency_symptoms(request):
    """Kiểm tra triệu chứng cấp cứu"""
    symptoms = request.data.get('symptoms', [])
    additional_info = request.data.get('additional_info', '')
    
    emergency_result = check_for_emergency(symptoms, additional_info)
    
    return Response({
        'is_emergency': emergency_result['is_emergency'],
        'urgency_level': emergency_result['urgency_level'],
        'emergency_symptoms': emergency_result['emergency_symptoms'],
        'recommendations': emergency_result['recommendations'],
        'emergency_contacts': {
            'ambulance': '115',
            'hospital_hotline': '1900-1234',
            'poison_control': '1900-5678'
        }
    })

# =================
# Analytics Endpoints
# =================

@api_view(['GET'])
@permission_classes([AllowAny])
def get_session_analytics(request):
    """Lấy thống kê phiên chat"""
    days = int(request.GET.get('days', 7))
    start_date = timezone.now() - timedelta(days=days)
    
    # Thống kê phiên chat
    total_sessions = ChatSession.objects.filter(start_time__gte=start_date).count()
    medical_sessions = ChatSession.objects.filter(
        start_time__gte=start_date,
        session_type='medical'
    ).count()
    completed_sessions = ChatSession.objects.filter(
        start_time__gte=start_date,
        end_time__isnull=False
    ).count()
    
    # Thống kê tin nhắn
    total_messages = ChatMessage.objects.filter(
        session__start_time__gte=start_date
    ).count()
    
    # Thống kê theo ngày
    daily_stats = []
    for i in range(days):
        date = start_date + timedelta(days=i)
        daily_sessions = ChatSession.objects.filter(
            start_time__date=date.date()
        ).count()
        daily_stats.append({
            'date': date.date().isoformat(),
            'sessions': daily_sessions
        })
    
    return Response({
        'period_days': days,
        'total_sessions': total_sessions,
        'medical_sessions': medical_sessions,
        'completed_sessions': completed_sessions,
        'total_messages': total_messages,
        'completion_rate': round(completed_sessions / total_sessions * 100, 2) if total_sessions > 0 else 0,
        'daily_stats': daily_stats
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def get_symptom_analytics(request):
    """Lấy thống kê triệu chứng được báo cáo"""
    days = int(request.GET.get('days', 30))
    start_date = timezone.now() - timedelta(days=days)
    
    # Top triệu chứng được báo cáo
    top_symptoms = ReportedSymptom.objects.filter(
        reported_at__gte=start_date
    ).values('symptom__name', 'symptom__category').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    # Thống kê theo mức độ nghiêm trọng
    severity_stats = ReportedSymptom.objects.filter(
        reported_at__gte=start_date
    ).values('severity').annotate(
        count=Count('id')
    ).order_by('severity')
    
    # Thống kê theo danh mục triệu chứng
    category_stats = ReportedSymptom.objects.filter(
        reported_at__gte=start_date
    ).values('symptom__category').annotate(
        count=Count('id')
    ).order_by('-count')
    
    return Response({
        'period_days': days,
        'top_symptoms': list(top_symptoms),
        'severity_distribution': list(severity_stats),
        'category_distribution': list(category_stats),
        'total_reported_symptoms': ReportedSymptom.objects.filter(
            reported_at__gte=start_date
        ).count()
    })

# =================
# Helper Functions
# =================

def process_medical_message(session, message):
    """Xử lý tin nhắn y tế và thực hiện chẩn đoán"""
    diagnosis_engine = DiagnosisEngine()
    
    # Lấy hoặc tạo phiên chẩn đoán
    diagnosis_session, created = DiagnosisSession.objects.get_or_create(
        chat_session=session
    )
    
    # Trích xuất triệu chứng từ tin nhắn
    extracted_symptoms = diagnosis_engine.extract_symptoms_from_text(message)
    
    # Cập nhật triệu chứng đã báo cáo
    for symptom_data in extracted_symptoms:
        symptom = symptom_data['symptom']
        severity = symptom_data.get('severity', 'mild')
        duration = symptom_data.get('duration', '')
        
        reported_symptom, created = ReportedSymptom.objects.get_or_create(
            diagnosis_session=diagnosis_session,
            symptom=symptom,
            defaults={
                'severity': severity,
                'duration': duration,
                'additional_details': message
            }
        )
        
        if not created:
            # Cập nhật thông tin nếu có thêm chi tiết
            reported_symptom.additional_details += f"\n{message}"
            reported_symptom.save()
    
    # Thực hiện chẩn đoán
    diagnosis_result = diagnosis_engine.diagnose(diagnosis_session)
    
    # Cập nhật phiên chẩn đoán
    diagnosis_session.possible_diseases = diagnosis_result['diseases']
    diagnosis_session.confidence_level = diagnosis_result['confidence_level']
    diagnosis_session.needs_urgent_care = diagnosis_result['urgent_care']
    diagnosis_session.save()
    
    # Tạo phản hồi
    if diagnosis_result['urgent_care']:
        response = generate_urgent_care_response(diagnosis_result)
    elif len(extracted_symptoms) > 0:
        response = generate_symptom_acknowledgment_response(extracted_symptoms, diagnosis_result)
    else:
        response = generate_clarification_response(diagnosis_session)
    
    # Thêm câu hỏi follow-up
    follow_up_questions = diagnosis_engine.get_follow_up_questions(diagnosis_session)
    response['follow_up_questions'] = follow_up_questions[:2]  # Giới hạn 2 câu hỏi
    
    return response, [s['symptom'].name for s in extracted_symptoms]

def process_general_message(session, message):
    """Xử lý tin nhắn chung (không phải y tế)"""
    message_lower = message.lower()
    
    # Kiểm tra FAQ
    faq_response = check_faq_match(message_lower)
    if faq_response:
        return {
            'message': faq_response,
            'intent': 'faq_response',
            'confidence': 0.9,
            'type': 'faq'
        }
    
    # Phát hiện ý định chuyển sang chẩn đoán y tế
    medical_keywords = [
        'đau', 'bệnh', 'triệu chứng', 'khó chịu', 'mệt mỏi', 'sốt', 'ho', 
        'chóng mặt', 'buồn nôn', 'khám', 'chuẩn đoán', 'y tế', 'sức khỏe',
        'nhức', 'đau đầu', 'đau bụng', 'khó thở', 'nôn', 'tiêu chảy'
    ]
    
    if any(keyword in message_lower for keyword in medical_keywords):
        return {
            'message': "Tôi nhận thấy bạn có thể đang gặp vấn đề sức khỏe. Bạn có muốn tôi giúp phân tích triệu chứng không? Tôi có thể hỗ trợ chẩn đoán sơ bộ dựa trên những gì bạn mô tả.\n\nHãy mô tả chi tiết triệu chứng bạn đang gặp phải.",
            'intent': 'medical_suggestion',
            'confidence': 0.8,
            'type': 'suggestion'
        }
    
    # Kiểm tra ý định đặt lịch hẹn
    appointment_keywords = ['đặt lịch', 'hẹn', 'khám', 'bác sĩ', 'appointment']
    if any(keyword in message_lower for keyword in appointment_keywords):
        return {
            'message': "Tôi có thể giúp bạn thông tin về việc đặt lịch hẹn. Bạn có thể:\n\n• Gọi hotline: 1900-1234\n• Sử dụng ứng dụng di động\n• Đặt lịch trực tuyến trên website\n• Đến trực tiếp quầy lễ tân\n\nBạn muốn đặt lịch với chuyên khoa nào?",
            'intent': 'appointment_inquiry',
            'confidence': 0.85,
            'type': 'information'
        }
    
    # Phản hồi chung
    general_responses = [
        "Tôi hiểu. Bạn có thể chia sẻ thêm chi tiết không?",
        "Cảm ơn bạn đã chia sẻ. Còn gì khác tôi có thể giúp không?",
        "Tôi ở đây để hỗ trợ bạn. Hãy cho tôi biết nếu bạn cần gì.",
        "Tôi có thể giúp bạn với các câu hỏi về y tế, đặt lịch hẹn, hoặc thông tin chung về bệnh viện."
    ]
    
    import random
    return {
        'message': random.choice(general_responses),
        'intent': 'general_response',
        'confidence': 0.6,
        'type': 'general'
    }

def get_medical_welcome_message():
    """Tin nhắn chào mừng cho phiên chẩn đoán y tế"""
    return """🩺 Xin chào! Tôi là trợ lý y tế AI của bệnh viện.

Tôi có thể giúp bạn:
• Phân tích triệu chứng và đưa ra chẩn đoán sơ bộ
• Đề xuất các bước cần thiết tiếp theo
• Đánh giá mức độ khẩn cấp của tình trạng

⚠️ **Lưu ý quan trọng**: Tôi chỉ cung cấp thông tin tham khảo. Hãy luôn tham khảo ý kiến bác sĩ chuyên khoa cho chẩn đoán chính xác.

Hãy mô tả triệu chứng bạn đang gặp phải một cách chi tiết nhất có thể."""

def generate_urgent_care_response(diagnosis_result):
    """Tạo phản hồi cho trường hợp cần cấp cứu"""
    urgent_diseases = [d for d in diagnosis_result['diseases'] if d.get('urgency') == 'emergency']
    
    response = f"""🚨 **CẢNH BÁO: CẦN CHĂM SÓC Y TẾ KHẨN CẤP**

Dựa trên triệu chứng bạn mô tả, có thể bạn đang gặp tình trạng nghiêm trọng cần được điều trị ngay lập tức.

**Khuyến nghị:**
• Đến phòng cấp cứu NGAY LẬP TỨC
• Gọi 115 nếu cần thiết
• Không trì hoãn việc tìm kiếm sự chăm sóc y tế

**Các tình trạng có thể:**
{chr(10).join([f"• {d['name']} (độ tin cậy: {d['confidence']:.1%})" for d in urgent_diseases[:3]])}

Đây chỉ là đánh giá sơ bộ. Hãy tìm kiếm sự chăm sóc y tế chuyên nghiệp ngay."""
    
    return {
        'message': response,
        'intent': 'urgent_care',
        'confidence': 0.95,
        'type': 'emergency',
        'recommendations': ['emergency_care', 'call_115']
    }

def generate_symptom_acknowledgment_response(symptoms, diagnosis_result):
    """Tạo phản hồi xác nhận triệu chứng và đưa ra chẩn đoán"""
    symptom_names = [s['symptom'].name for s in symptoms]
    diseases = diagnosis_result['diseases'][:3]  # Top 3 bệnh có thể
    
    response = f"""Tôi đã ghi nhận các triệu chứng: **{', '.join(symptom_names)}**

**Phân tích sơ bộ:**"""
    
    if diseases:
        response += f"""
Dựa trên triệu chứng bạn mô tả, các khả năng có thể là:

"""
        for i, disease in enumerate(diseases, 1):
            confidence_text = "cao" if disease['confidence'] > 0.7 else "trung bình" if disease['confidence'] > 0.4 else "thấp"
            response += f"{i}. **{disease['name']}** (độ tin cậy: {confidence_text})\n"
            if disease.get('description'):
                response += f"   - {disease['description'][:100]}...\n"
    
    response += f"""
**Khuyến nghị tiếp theo:**
• {"Nên khám ngay nếu triệu chứng trầm trọng hơn" if diagnosis_result['confidence_level'] == 'high' else "Theo dõi triệu chứng và khám nếu không cải thiện"}
• Uống nhiều nước và nghỉ ngơi đầy đủ
• Ghi lại thêm triệu chứng nếu có

Bạn có triệu chứng nào khác hoặc muốn mô tả chi tiết hơn không?"""
    
    return {
        'message': response,
        'intent': 'diagnosis_result',
        'confidence': 0.85,
        'type': 'diagnosis',
        'recommendations': ['monitor_symptoms', 'rest', 'hydrate']
    }

def generate_clarification_response(diagnosis_session):
    """Tạo phản hồi yêu cầu làm rõ thêm triệu chứng"""
    reported_symptoms = diagnosis_session.reportedsymptom_set.all()
    
    if not reported_symptoms:
        response = """Tôi chưa nhận diện được triệu chứng cụ thể từ mô tả của bạn.

Hãy cho tôi biết:
• Bạn đang cảm thấy đau ở đâu?
• Triệu chứng bắt đầu từ khi nào?
• Mức độ nghiêm trọng từ 1-10?
• Có gì khiến triệu chứng tệ hơn hoặc tốt hơn không?

Ví dụ: "Tôi bị đau đầu từ sáng nay, mức độ 7/10, và cảm thấy buồn nôn."""
    else:
        response = """Tôi cần thêm thông tin để đưa ra đánh giá chính xác hơn.

Bạn có thể mô tả:
• Triệu chứng có thay đổi theo thời gian không?
• Có triệu chứng nào khác kèm theo?
• Bạn đã dùng thuốc gì chưa?
• Có tiền sử bệnh lý nào không?"""
    
    return {
        'message': response,
        'intent': 'clarification_request',
        'confidence': 0.8,
        'type': 'inquiry'
    }

def check_faq_match(message):
    """Kiểm tra tin nhắn có khớp với FAQ không"""
    # Tìm kiếm trong FAQ
    faqs = FAQ.objects.filter(is_active=True)
    
    for faq in faqs:
        # Kiểm tra từ khóa trong tags
        if faq.tags:
            tags = [tag.strip().lower() for tag in faq.tags.split(',')]
            if any(tag in message for tag in tags):
                return faq.answer
        
        # Kiểm tra từ khóa trong câu hỏi
        question_words = faq.question.lower().split()
        if len(set(question_words) & set(message.split())) >= 2:
            return faq.answer
    
    return None

def generate_health_recommendations(symptoms, age=None, gender=None, medical_history=None):
    """Tạo khuyến nghị sức khỏe dựa trên triệu chứng"""
    recommendations = []
    
    # Khuyến nghị chung
    general_recommendations = [
        "Uống nhiều nước (ít nhất 2 lít/ngày)",
        "Nghỉ ngơi đầy đủ, ngủ 7-8 tiếng/đêm",
        "Ăn uống cân bằng, nhiều rau xanh và trái cây",
        "Tránh stress và căng thẳng"
    ]
    
    # Khuyến nghị dựa trên triệu chứng
    symptom_recommendations = {
        'sốt': [
            "Hạ sốt bằng thuốc paracetamol theo chỉ dẫn",
            "Chườm mát trán và cổ tay",
            "Mặc quần áo thoáng mát"
        ],
        'ho': [
            "Uống nước ấm có mật ong",
            "Súc miệng nước muối",
            "Tránh hút thuốc và khói bụi"
        ],
        'đau_đầu': [
            "Nghỉ ngơi trong phòng tối",
            "Massage nhẹ vùng thái dương",
            "Tránh ánh sáng chói và tiếng ồn"
        ],
        'đau_bụng': [
            "Ăn nhẹ, tránh đồ cay nóng",
            "Uống trà gừng hoặc trà bạc hà",
            "Nằm nghỉ với gối ôm bụng"
        ]
    }
    
    # Thêm khuyến nghị chung
    recommendations.extend(general_recommendations)
    
    # Thêm khuyến nghị theo triệu chứng
    for symptom in symptoms:
        symptom_lower = symptom.lower()
        for key, recs in symptom_recommendations.items():
            if key in symptom_lower:
                recommendations.extend(recs)
    
    # Khuyến nghị theo tuổi
    if age:
        if age < 18:
            recommendations.append("Trẻ em cần được giám sát bởi người lớn")
            recommendations.append("Tham khảo bác sĩ nhi khoa nếu cần")
        elif age > 65:
            recommendations.append("Người cao tuổi cần theo dõi sát hơn")
            recommendations.append("Cân nhắc khám bác sĩ sớm hơn")
    
    # Cảnh báo khi cần đi khám
    warning_signs = [
        "Đến bác sĩ ngay nếu:",
        "• Triệu chứng nặng lên đột ngột",
        "• Sốt cao trên 39°C",
        "• Đau ngực hoặc khó thở",
        "• Chảy máu bất thường",
        "• Mất ý thức hoặc co giật"
    ]
    
    recommendations.extend(warning_signs)
    
    return list(set(recommendations))  # Loại bỏ trùng lặp

def check_for_emergency(symptoms, additional_info=''):
    """Kiểm tra triệu chứng cấp cứu"""
    emergency_keywords = [
        'đau ngực dữ dội', 'khó thở nặng', 'đau đầu đột ngột',
        'co giật', 'bất tỉnh', 'chảy máu nhiều', 'sốt cao',
        'không thở được', 'ngừng tim', 'đột quỵ', 'tai nạn',
        'ngộ độc', 'đau bụng dữ dội', 'mất ý thức'
    ]
    
    # Kiểm tra từ khóa cấp cứu
    text_to_check = ' '.join(symptoms).lower() + ' ' + additional_info.lower()
    emergency_symptoms_found = []
    
    for keyword in emergency_keywords:
        if keyword in text_to_check:
            emergency_symptoms_found.append(keyword)
    
    # Xác định mức độ khẩn cấp
    if emergency_symptoms_found:
        urgency_level = 'emergency'
        is_emergency = True
        recommendations = [
            'GỌI 115 NGAY LẬP TỨC',
            'Đến phòng cấp cứu gần nhất',
            'Không trì hoãn việc tìm kiếm chăm sóc y tế',
            'Chuẩn bị giấy tờ tuy thân và thẻ bảo hiểm'
        ]
    elif any(word in text_to_check for word in ['đau nặng', 'khó chịu nhiều', 'không chịu nổi']):
        urgency_level = 'high'
        is_emergency = False
        recommendations = [
            'Nên đến bệnh viện trong vòng 2-4 giờ',
            'Gọi hotline tư vấn y tế: 1900-1234',
            'Theo dõi triệu chứng sát sao'
        ]
    else:
        urgency_level = 'low'
        is_emergency = False
        recommendations = [
            'Theo dõi triệu chứng trong 24-48 giờ',
            'Đặt lịch khám nếu không cải thiện',
            'Nghỉ ngơi và chăm sóc tại nhà'
        ]
    
    return {
        'is_emergency': is_emergency,
        'urgency_level': urgency_level,
        'emergency_symptoms': emergency_symptoms_found,
        'recommendations': recommendations
    }

def generate_session_summary(diagnosis_session):
    """Tạo tóm tắt phiên chẩn đoán"""
    symptoms = diagnosis_session.reportedsymptom_set.all()
    
    summary = {
        'session_id': diagnosis_session.chat_session.session_id,
        'start_time': diagnosis_session.chat_session.start_time.isoformat(),
        'duration_minutes': calculate_session_duration(diagnosis_session.chat_session),
        'reported_symptoms': [
            {
                'name': rs.symptom.name,
                'category': rs.symptom.category,
                'severity': rs.severity,
                'duration': rs.duration,
                'details': rs.additional_details[:100] + '...' if len(rs.additional_details) > 100 else rs.additional_details
            } for rs in symptoms
        ],
        'possible_diseases': diagnosis_session.possible_diseases,
        'confidence_level': diagnosis_session.confidence_level,
        'needs_urgent_care': diagnosis_session.needs_urgent_care,
        'final_recommendations': diagnosis_session.final_recommendations or [],
        'total_messages': diagnosis_session.chat_session.messages.count(),
        'symptom_categories': list(set(rs.symptom.category for rs in symptoms))
    }
    
    return summary

def calculate_session_duration(session):
    """Tính thời gian phiên chat (phút)"""
    if session.end_time:
        duration = session.end_time - session.start_time
        return int(duration.total_seconds() / 60)
    else:
        duration = timezone.now() - session.start_time
        return int(duration.total_seconds() / 60)