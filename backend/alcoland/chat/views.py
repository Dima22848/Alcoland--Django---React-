from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer, CustomUserSerializer

class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.prefetch_related("participants").all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Фильтруем чаты по chat_id, если передан параметр ?chat=ID"""
        queryset = Chat.objects.filter(participants=self.request.user)
        chat_id = self.request.query_params.get("chat")  # Получаем параметр ?chat=ID

        if chat_id:
            queryset = queryset.filter(id=chat_id)

        return queryset

    @action(detail=True, methods=['get'])
    def participants(self, request, pk=None):
        chat = self.get_object()
        users = chat.participants.all()
        return Response(CustomUserSerializer(users, many=True).data)

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        chat = self.get_object()
        messages = chat.messages.all()
        return Response(MessageSerializer(messages, many=True).data)

    @action(detail=True, methods=['post'])
    def add_participant(self, request, pk=None):
        chat = self.get_object()
        user_id = request.data.get('user_id')
        user = CustomUser.objects.get(id=user_id)
        if user not in chat.participants.all():
            chat.participants.add(user)
            return Response({"status": "Participant added"})
        return Response({"status": "User is already a participant"}, status=400)

    @action(detail=True, methods=['post'])
    def remove_participant(self, request, pk=None):
        chat = self.get_object()
        user_id = request.data.get('user_id')
        user = CustomUser.objects.get(id=user_id)
        if user in chat.participants.all():
            chat.participants.remove(user)
            return Response({"status": "Participant removed"})
        return Response({"status": "User is not a participant"}, status=400)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.select_related("chat", "sender").all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Фильтруем сообщения по chat_id, если передан параметр ?chat=ID"""
        chat_id = self.request.query_params.get('chat')  # Берем chat=ID из URL
        queryset = Message.objects.select_related("chat", "sender").all()  # Получаем полный QuerySet

        if chat_id:
            queryset = queryset.filter(chat_id=chat_id)  # Фильтруем только нужный чат

        return queryset
