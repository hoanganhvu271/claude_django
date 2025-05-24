from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
import uuid
from .models import ChatSession, ChatMessage, FAQ
from .serializers import ChatSessionSerializer, ChatMessageSerializer, FAQSerializer

class ChatSessionListCreateView(generics.ListCreateAPIView):
    queryset = ChatSession.objects.all()
    serializer_class = ChatSessionSerializer

@api_view(['POST'])
def create_chat_session(request):
    user_id = request.data.get('user_id')
    session_id = str(uuid.uuid4())
    
    session = ChatSession.objects.create(
        user_id=user_id,
        session_id=session_id
    )
    
    return Response({
        'session_id': session.session_id,
        'message': 'Hello! How can I help you today?'
    }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def send_message(request):
    session_id = request.data.get('session_id')
    message = request.data.get('message')
    
    try:
        session = ChatSession.objects.get(session_id=session_id, is_active=True)
        
        # Save user message
        user_message = ChatMessage.objects.create(
            session=session,
            sender='user',
            message=message
        )
        
        # Simple bot response logic (in real implementation, this would use AI/ML)
        bot_response = generate_bot_response(message)
        
        # Save bot response
        bot_message = ChatMessage.objects.create(
            session=session,
            sender='bot',
            message=bot_response
        )
        
        return Response({
            'user_message': ChatMessageSerializer(user_message).data,
            'bot_response': ChatMessageSerializer(bot_message).data
        })
        
    except ChatSession.DoesNotExist:
        return Response({'error': 'Session not found'}, status=404)

def generate_bot_response(message):
    """Simple bot response logic - in real implementation, this would use AI/ML"""
    message_lower = message.lower()
    
    if 'appointment' in message_lower:
        return "I can help you book an appointment. Please provide your preferred date and time."
    elif 'symptoms' in message_lower:
        return "I understand you're concerned about symptoms. I recommend consulting with a doctor for proper medical advice."
    elif 'prescription' in message_lower:
        return "For prescription-related queries, please contact your doctor or pharmacist."
    elif 'hello' in message_lower or 'hi' in message_lower:
        return "Hello! I'm here to help you with your healthcare needs. What can I assist you with today?"
    else:
        return "I'm here to help! Could you please provide more details about what you need assistance with?"

@api_view(['PUT'])
def end_chat_session(request, session_id):
    try:
        session = ChatSession.objects.get(session_id=session_id)
        session.is_active = False
        session.end_time = timezone.now()
        session.save()
        return Response({'status': 'Session ended successfully'})
    except ChatSession.DoesNotExist:
        return Response({'error': 'Session not found'}, status=404)