# Generated by Django 5.1.5 on 2025-02-04 14:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Название чата')),
                ('is_group', models.BooleanField(default=False, verbose_name='Групповой чат')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('participants', models.ManyToManyField(related_name='chats', to=settings.AUTH_USER_MODEL, verbose_name='Участники')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True, verbose_name='Текст сообщения')),
                ('file', models.FileField(blank=True, null=True, upload_to='', verbose_name='Файл или фото')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chat.chat', verbose_name='Чат')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Отправитель')),
            ],
        ),
    ]
