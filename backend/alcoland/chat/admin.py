from django.contrib import admin
from .models import Chat, Message

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ("get_chat_name", "is_group", "created_at", "get_image_preview")
    list_filter = ("is_group", "created_at")
    search_fields = ("name", "participants__nickname")
    filter_horizontal = ("participants",)
    readonly_fields = ("created_at", "image")

    def get_chat_name(self, obj):
        """Корректное отображение имени чата в админке"""
        return obj.get_chat_display_name()


    def get_image_preview(self, obj):
        """Отображение аватара в админке"""
        if obj.image:
            return f'<img src="{obj.image.url}" width="50" height="50" style="border-radius: 50%;" />'
        return "Нет фото"

    get_chat_name.short_description = "Название чата"
    get_image_preview.short_description = "Фото"
    get_image_preview.allow_tags = True

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("chat", "sender", "text_preview", "created_at")
    list_filter = ("created_at", "chat")
    search_fields = ("sender__username", "text")
    readonly_fields = ("created_at",)

    def text_preview(self, obj):
        """Отображает только первые 30 символов сообщения или 'Файл'"""
        return obj.text[:30] if obj.text else "Файл"

    text_preview.short_description = "Сообщение"


