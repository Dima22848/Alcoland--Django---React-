from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

CITY_CHOICES = [
    ('', ''),
    ('kyiv', 'Киев'),
    ('kharkiv', 'Харьков'),
    ('odesa', 'Одесса'),
    ('dnipro', 'Днепр'),
    ('lviv', 'Львов'),
    ('zaporizhzhia', 'Запорожье'),
    ('vinnitsa', 'Винница'),
    ('mykolaiv', 'Николаев'),
    ('cherkasy', 'Черкассы'),
    ('chernihiv', 'Чернигов'),
    ('chernivtsi', 'Черновцы'),
    ('poltava', 'Полтава'),
    ('kherson', 'Херсон'),
    ('sumy', 'Сумы'),
    ('zhytomyr', 'Житомир'),
    ('ivano_frankivsk', 'Ивано-Франковск'),
    ('lutsk', 'Луцк'),
    ('ternopil', 'Тернополь'),
    ('uzhhorod', 'Ужгород'),
    ('kropyvnytskyi', 'Кропивницкий'),
    ('rivno', 'Ровно'),
    ('mariupol', 'Мариуполь'),
    ('sevastopol', 'Севастополь'),
    ('simferopol', 'Симферополь'),
]

class CustomUser(AbstractUser):
    username = None
    nickname = models.CharField(max_length=50, unique=True, verbose_name='Ник пользователя')
    email = models.EmailField(unique=True, verbose_name='Email пользователя')

    def upload_to_path(instance, filename):
        return f'avatars/user_{instance.nickname}/{filename}'

    image = models.ImageField(upload_to=upload_to_path, verbose_name='Аватарка пользователя',blank=True, null=True, validators=[FileExtensionValidator(['jpg', 'png', 'webp', 'jfif'])])

    USERNAME_FIELD = "email"  # Теперь логинимся по email
    REQUIRED_FIELDS = ["nickname"]

    friends = models.ManyToManyField(
        'self',
        symmetrical=True,
        blank=True,
        related_name='user_friends'
    )

    """Добавить друга"""
    def add_friend(self, friend):
        if friend != self and friend not in self.friends.all():
            self.friends.add(friend)

    """Удалить друга"""
    def remove_friend(self, friend):
        if friend in self.friends.all():
            self.friends.remove(friend)

    """Проверить, является ли пользователь другом"""
    def is_friend(self, friend):
        return friend in self.friends.all()


    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True
    )

    """Подписаться на пользователя"""
    def follow(self, user):
        if user != self and user not in self.following.all():
            self.following.add(user)

    """Отписаться от пользователя"""
    def unfollow(self, user):
        if user in self.following.all():
            self.following.remove(user)

    """Проверить, подписан ли текущий пользователь на другого"""
    def is_following(self, user):
        return user in self.following.all()

    """Проверить, подписан ли другой пользователь на текущего"""
    def is_followed_by(self, user):
        return user in self.followers.all()

    age = models.IntegerField(blank=True, null=True)
    city = models.CharField(
        max_length=50,
        choices=CITY_CHOICES,
        default='',
        null=True,
        blank=True,
        verbose_name='Город')
    profession = models.CharField(max_length=100, blank=True, null=True, verbose_name='Профессия')
    hobby = models.CharField(max_length=100, blank=True, null=True, verbose_name='Хобби')
    extra_info = models.TextField(blank=True, null=True, verbose_name='Побольше о себе')

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'

    def save(self, *args, **kwargs):
        if self.image:
            img = Image.open(self.image)

            # Конвертация в RGB (на случай PNG с прозрачностью)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            # Сжатие изображения
            output = BytesIO()
            img.save(output, format="JPEG", quality=70)  # 70 – компромисс между качеством и размером
            output.seek(0)

            # Обновление файла изображения
            self.image = ContentFile(output.read(), self.image.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nickname

class NewsFeed(models.Model):
    text = models.TextField(verbose_name='Текст')
    file = models.FileField(verbose_name='Файл или фото', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    profile = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Запись новостной лента'
        verbose_name_plural = 'Записи новостной ленты'

    def __str__(self):
        return f'{self.profile} at {self.created_at}'

class NewsFeedComments(models.Model):
    text = models.TextField(verbose_name='Текст комментария')
    file = models.FileField(verbose_name='Файл или фото комментария', null=True, blank=True)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now=True)
    profile = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Комментарий пользователя')
    newsfeed = models.ForeignKey(NewsFeed, on_delete=models.CASCADE, verbose_name='Чат')

    class Meta:
        verbose_name = 'Комментарий к записи в новостной лента'
        verbose_name_plural = 'Комментарии к записи в новостной лента'

    def __str__(self):
        return f'{self.profile} at {self.created_at} in new {self.newsfeed}'