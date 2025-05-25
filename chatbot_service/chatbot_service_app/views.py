import re
import json
import uuid
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import (
    ChatSession, ChatMessage, FAQ, Symptom, Disease, DiseaseSymptom,
    DiagnosisSession, ReportedSymptom, ResponseTemplate
)
from .serializers import (
    ChatSessionSerializer, ChatMessageSerializer, FAQSerializer,
    SymptomSerializer, DiseaseSerializer, DiagnosisSessionSerializer
)
from .diagnosis_engine import DiagnosisEngine

class ChatSessionListCreateView(generics.ListCreateAPIView):
    queryset = ChatSession.objects.all()
    serializer_class = ChatSessionSerializer

class SymptomListView(generics.ListAPIView):
    """API để lấy danh sách triệu chứng"""
    queryset = Symptom.objects.all()
    serializer_class = SymptomSerializer

class DiseaseListView(generics.ListAPIView):
    """API để lấy danh sách bệnh"""
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer

@api_view(['POST'])
def create_chat_session(request):
    """Tạo phiên chat mới với hỗ trợ chẩn đoán"""
    user_id = request.data.get('user_id')
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
        welcome_message = "Xin chào! Tôi có thể giúp gì cho bạn hôm nay?"
    
    # Tạo tin nhắn chào mừng
    ChatMessage.objects.create(
        session=session,
        sender='bot',
        message=welcome_message,
        intent='greeting'
    )
    
    return Response({
        'session_id': session.session_id,
        'session_type': session_type,
        'message': welcome_message
    }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def send_message(request):
    """Gửi tin nhắn và nhận phản hồi từ chatbot với khả năng chẩn đoán"""
    session_id = request.data.get('session_id')
    message = request.data.get('message')
    
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
            bot_response = process_general_message(message)
        
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
            'recommendations': bot_response.get('recommendations', [])
        })
        
    except ChatSession.DoesNotExist:
        return Response({'error': 'Session not found'}, status=404)

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
    
    return response, [s['symptom'].name for s in extracted_symptoms]

def process_general_message(message):
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
        'chóng mặt', 'buồn nôn', 'khám', 'chuẩn đoán', 'y tế', 'sức khỏe'
    ]
    
    if any(keyword in message_lower for keyword in medical_keywords):
        return {
            'message': "Tôi nhận thấy bạn có thể đang gặp vấn đề sức khỏe. Bạn có muốn tôi giúp phân tích triệu chứng không? Tôi có thể hỗ trợ chẩn đoán sơ bộ dựa trên những gì bạn mô tả.",
            'intent': 'medical_suggestion',
            'confidence': 0.8,
            'type': 'suggestion'
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

@api_view(['PUT'])
def end_chat_session(request, session_id):
    """Kết thúc phiên chat"""
    try:
        session = ChatSession.objects.get(session_id=session_id)
        session.is_active = False
        session.end_time = timezone.now()
        session.save()
        
        # Tạo tóm tắt nếu là phiên y tế
        if session.session_type == 'medical' and hasattr(session, 'diagnosissession'):
            summary = generate_session_summary(session.diagnosissession)
            return Response({
                'status': 'Session ended successfully',
                'summary': summary
            })
        
        return Response({'status': 'Session ended successfully'})
    except ChatSession.DoesNotExist:
        return Response({'error': 'Session not found'}, status=404)

def generate_session_summary(diagnosis_session):
    """Tạo tóm tắt phiên chẩn đoán"""
    symptoms = diagnosis_session.reportedsymptom_set.all()
    
    summary = {
        'reported_symptoms': [
            {
                'name': rs.symptom.name,
                'severity': rs.severity,
                'duration': rs.duration
            } for rs in symptoms
        ],
        'possible_diseases': diagnosis_session.possible_diseases,
        'confidence_level': diagnosis_session.confidence_level,
        'needs_urgent_care': diagnosis_session.needs_urgent_care,
        'recommendations': diagnosis_session.final_recommendations
    }
    
    return summary

@api_view(['GET'])
def get_session_history(request, session_id):
    """Lấy lịch sử chat của phiên"""
    try:
        session = ChatSession.objects.get(session_id=session_id)
        messages = session.messages.all().order_by('timestamp')
        
        return Response({
            'session': ChatSessionSerializer(session).data,
            'messages': ChatMessageSerializer(messages, many=True).data
        })
    except ChatSession.DoesNotExist:
        return Response({'error': 'Session not found'}, status=404)