from django.urls import path
from . import views

urlpatterns = [
    # Chat session management
    path('api/v1/chatbot/sessions/', views.create_chat_session, name='create-chat-session'),
    path('api/v1/chatbot/sessions/<str:session_id>/', views.get_session_history, name='get-session-history'),
    path('api/v1/chatbot/sessions/<str:session_id>/end/', views.end_chat_session, name='end-chat-session'),
    
    # Message handling
    path('api/v1/chatbot/message/', views.send_message, name='send-chat-message'),
    
    # Medical data endpoints
    path('api/v1/chatbot/symptoms/', views.SymptomListView.as_view(), name='symptom-list'),
    path('api/v1/chatbot/diseases/', views.DiseaseListView.as_view(), name='disease-list'),
    
    # Diagnosis endpoints
    path('api/v1/chatbot/diagnosis/<int:session_id>/', views.get_diagnosis_result, name='get-diagnosis'),
    path('api/v1/chatbot/diagnosis/<int:session_id>/summary/', views.get_diagnosis_summary, name='diagnosis-summary'),
    
    # FAQ endpoints
    path('api/v1/chatbot/faq/', views.FAQListView.as_view(), name='faq-list'),
    path('api/v1/chatbot/faq/search/', views.search_faq, name='search-faq'),
    
    # Health recommendations
    path('api/v1/chatbot/recommendations/', views.get_health_recommendations, name='health-recommendations'),
    
    # Emergency detection
    path('api/v1/chatbot/emergency-check/', views.check_emergency_symptoms, name='emergency-check'),
    
    # Chat analytics (optional)
    path('api/v1/chatbot/analytics/sessions/', views.get_session_analytics, name='session-analytics'),
    path('api/v1/chatbot/analytics/symptoms/', views.get_symptom_analytics, name='symptom-analytics'),
]