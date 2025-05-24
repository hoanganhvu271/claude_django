from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Notification, NotificationTemplate
from .serializers import NotificationSerializer, NotificationTemplateSerializer

class NotificationListCreateView(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

class UserNotificationsView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Notification.objects.filter(user_id=user_id).order_by('-created_at')

@api_view(['PUT'])
def mark_notification_read(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)
        notification.status = 'read'
        notification.save()
        return Response({'status': 'success'})
    except Notification.DoesNotExist:
        return Response({'error': 'Notification not found'}, status=404)