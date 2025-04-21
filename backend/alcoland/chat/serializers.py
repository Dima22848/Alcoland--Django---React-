from rest_framework import serializers
from .models import Chat, Message
from account.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'nickname']


class ChatSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        many=True, queryset=CustomUser.objects.all(), required=False
    )
    image = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()  # Используем кастомный метод для имени

    class Meta:
        model = Chat
        fields = ['id', 'name', 'is_group', 'participants', 'image', 'created_at']

    def get_image(self, obj):
        """Если чат групповой — берем его изображение, если личный — аватар собеседника"""
        request = self.context.get("request")
        if not request or not hasattr(request, "user"):
            print("⚠️ Ошибка: request или request.user не найден!")
            return None

        user = request.user

        if obj.is_group:
            return obj.image.url if obj.image else "/media/default_chat.png"

        # Получаем собеседника
        participants = obj.participants.exclude(id=user.id)
        if participants.exists():
            sobesednik = participants.first()
            print(f"🔹 Собеседник: {sobesednik.nickname or sobesednik.username}, фото: {sobesednik.image}")

            return sobesednik.image.url if sobesednik.image else "/media/default_avatar.png"

        print("⚠️ Ошибка: Личный чат, но нет собеседника!")
        return "/media/default_avatar.png"

    def get_name(self, obj):
        """Формируем корректное имя личного чата для текущего пользователя"""
        if obj.is_group:
            return obj.name  # Для группового чата оставляем оригинальное имя

        request = self.context.get("request")
        if not request or not hasattr(request, "user"):
            print("⚠️ Ошибка: request или request.user не найден!")  # Логируем проблему
            return None

        user = request.user
        participants = obj.participants.exclude(id=user.id)  # Получаем собеседника

        if participants.exists():
            sobesednik = participants.first()
            print(f"🔹 Собеседник найден: {sobesednik.nickname or sobesednik.username}")
            return sobesednik.nickname or sobesednik.username  # Берем никнейм или имя пользователя

        print("⚠️ Ошибка: Личный чат, но нет собеседника!")
        return "Неизвестный собеседник"



class MessageSerializer(serializers.ModelSerializer):
    # sender = serializers.HiddenField(default=serializers.CurrentUserDefault())
    chat = serializers.PrimaryKeyRelatedField(queryset=Chat.objects.all())
    sender = CustomUserSerializer(read_only=True)
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'chat', 'sender', 'text', 'file', 'file_url', 'created_at']

    def get_file_url(self, obj):
        if obj.file:
            return obj.file.url
        return None

