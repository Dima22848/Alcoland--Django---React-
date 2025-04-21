from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.timezone import now
from django.core.validators import MinValueValidator, MaxValueValidator

from account.models import CustomUser


class Reviews(models.Model):
    text = models.TextField(verbose_name='Отзыв')
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='user_reviews')
    rate = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])

    # добавляем GenericForeignKey для связи с любым типом алкоголя
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    product = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = 'Отзывы'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'{self.author} at {self.created_at}'


class AlcoholType(models.Model):
    TYPE_CHOICES = [
        ('beer', 'Пиво'),
        ('cognak', 'Коньяк'),
        ('vodka', 'Водка'),
        ('vine', 'Вино'),
    ]
    type = models.CharField(choices=TYPE_CHOICES, verbose_name='Тип алкоголя')

    class Meta:
        verbose_name = 'Тип алкоголя'
        verbose_name_plural = 'Типы алкоголя'

    def __str__(self):
        return dict(self.TYPE_CHOICES).get(self.type, self.type)


class Beer(models.Model):
    name = models.CharField(verbose_name='Название')
    slug = models.SlugField(unique=True, max_length=100, blank=True, null=True, default="", verbose_name='URL')
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Цена')
    description = models.TextField(verbose_name='Описание')
    aroma = models.CharField(blank=True, null=True, verbose_name='Аромат')
    taste = models.CharField(blank=True, null=True, verbose_name='Вкус')
    aftertaste = models.CharField(blank=True, null=True, verbose_name='Послевкусие')
    composition = models.CharField(blank=True, null=True, verbose_name='Состав')
    combition_with = models.CharField(blank=True, null=True, verbose_name='С чем сочитается')
    country = models.CharField(verbose_name='Страна')
    style = models.CharField(verbose_name='Стиль')

    TYPE_CHOICES = [
        ('filter', 'Фильтрованное'),
        ('no-filter', 'Нефильтрованное'),
    ]
    type = models.CharField(choices=TYPE_CHOICES, verbose_name='Вид')

    COLOR_CHOICES = [
        ('light', 'Светлое'),
        ('semi-dark', 'Полутемное'),
        ('dark', 'Темное')
    ]
    color = models.CharField(choices=COLOR_CHOICES, verbose_name='Цвет')
    alcoholtype = models.ForeignKey(AlcoholType, on_delete=models.CASCADE, verbose_name='Тип алкоголя')

    def upload_to_path(instance, filename):
        return now().strftime(f"alcohol_images/beer/%Y/%m/%d/{filename}")

    image = models.ImageField(upload_to=upload_to_path, verbose_name='Изображение', blank=True, null=True)

    class Meta:
        verbose_name = 'Пиво'
        verbose_name_plural = 'Пиво'

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Cognak(models.Model):
    name = models.CharField(verbose_name='Название')
    slug = models.SlugField(unique=True, max_length=100, blank=True, null=True, default="", verbose_name='URL')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Цена')
    country = models.CharField(verbose_name='Страна')
    strength = models.DecimalField(max_digits=4, decimal_places=2,verbose_name='Крепкость')
    volume = models.DecimalField(max_digits=4, decimal_places=3, verbose_name='Обьем')
    excerpt = models.CharField(verbose_name='Выдержка')
    supply_temperature = models.CharField(verbose_name='Температура подачи')
    alcoholtype = models.ForeignKey(AlcoholType, on_delete=models.CASCADE, verbose_name='Тип алкоголя')

    def upload_to_path(instance, filename):
        return now().strftime(f"alcohol_images/cognak/%Y/%m/%d/{filename}")

    image = models.ImageField(upload_to=upload_to_path, verbose_name='Изображение', blank=True, null=True)

    class Meta:
        verbose_name = 'Коньяк'
        verbose_name_plural = 'Коньяк'

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Vodka(models.Model):
    name = models.CharField(verbose_name='Название')
    slug = models.SlugField(unique=True, max_length=100, blank=True, null=True, default="", verbose_name='URL')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Цена')
    country = models.CharField(verbose_name='Страна')
    strength = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Крепкость')
    volume = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Обьем')
    serving_temperature = models.CharField(verbose_name='Температура серверовки')
    alcoholtype = models.ForeignKey(AlcoholType, on_delete=models.CASCADE, verbose_name='Тип алкоголя')

    def upload_to_path(instance, filename):
        return now().strftime(f"alcohol_images/vodka/%Y/%m/%d/{filename}")

    image = models.ImageField(upload_to=upload_to_path, verbose_name='Изображение', blank=True, null=True)

    class Meta:
        verbose_name = 'Водка'
        verbose_name_plural = 'Водка'

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Vine(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    slug = models.SlugField(unique=True, max_length=150, blank=True, null=True, default="", verbose_name='URL')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Цена')
    country = models.CharField(verbose_name='Страна')
    volume = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Обьем')
    supply_temperature = models.CharField(verbose_name='Температура подачи')
    taste = models.CharField(blank=True, null=True, verbose_name='Вкус')

    COLOR_TYPES = [
        ('pink', 'Розовое'),
        ('red', 'Красное'),
        ('white', 'Белое'),
    ]
    color = models.CharField(choices=COLOR_TYPES, verbose_name='Цвет')

    SUGAR_SUPPLY_CHOICES = [
        ('dry', 'Сухое'),
        ('semi-dry', 'Полусухое'),
        ('semi-sweet', 'Полусладкое'),
        ('sweet', 'Сладкое'),
    ]
    sugar_supply = models.CharField(choices=SUGAR_SUPPLY_CHOICES, verbose_name='Содержание сахара')
    alcoholtype = models.ForeignKey(AlcoholType, on_delete=models.CASCADE, verbose_name='Тип алкоголя')

    def upload_to_path(instance, filename):
        return now().strftime(f"alcohol_images/vine/%Y/%m/%d/{filename}")

    image = models.ImageField(upload_to=upload_to_path, verbose_name='Изображение', blank=True, null=True)

    class Meta:
        verbose_name = 'Вино'
        verbose_name_plural = 'Вина'

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Basket(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE) # Хранит тип модели (Beer, Cognak и т. д.)
    object_id = models.PositiveIntegerField()  # ID объекта конкретной модели
    product = GenericForeignKey('content_type', 'object_id') # Связь с конкретным товаром
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')


    def get_total_price(self):
        return self.product.price * self.quantity

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f"{self.user.username} - {self.product} ({self.quantity} шт.)"


class PurchaseHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    product = GenericForeignKey('content_type', 'object_id')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за единицу')
    purchased_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата покупки')

    def get_total_price(self):
        return self.price * self.quantity

    class Meta:
        verbose_name = 'История покупок'
        verbose_name_plural = 'Истории покупок'

    def __str__(self):
        return f"{self.user.username} купил {self.product} ({self.quantity} шт.)"


# from django.contrib.contenttypes.models import ContentType
# from myapp.models import Cart, Beer, User
#
# user = User.objects.get(id=1)  # Например, текущий пользователь
# beer = Beer.objects.get(id=2)  # Выбранное пиво
#
# cart_item = Cart.objects.create(
#     user=user,
#     content_type=ContentType.objects.get_for_model(Beer),  # Указываем тип модели
#     object_id=beer.id,  # ID конкретного продукта
#     quantity=3
# )



# cognak = Cognak.objects.get(id=1)
#
# cart_item = Cart.objects.create(
#     user=user,
#     content_type=ContentType.objects.get_for_model(Cognak),
#     object_id=cognak.id,
#     quantity=1
# )


# cart_items = Cart.objects.filter(user=user)
#
# for item in cart_items:
#     print(f"{item.product.name} - {item.quantity} шт. - {item.get_total_price()} руб.")


# Перенос товаров из корзины в историю покупок
# При успешной оплате все товары из корзины переносятся в PurchaseHistory.

# from django.contrib.contenttypes.models import ContentType
# from myapp.models import Cart, PurchaseHistory
#
#
# def process_payment(user):
#     cart_items = Cart.objects.filter(user=user)
#
#     if not cart_items:
#         return "Корзина пуста"
#
#     # Переносим товары в историю покупок
#     for item in cart_items:
#         PurchaseHistory.objects.create(
#             user=user,
#             content_type=item.content_type,
#             object_id=item.object_id,
#             product=item.product,
#             quantity=item.quantity,
#             price=item.product.price  # Фиксируем цену на момент покупки
#         )
#
#     # Очищаем корзину
#     cart_items.delete()
#
#     return "Покупка успешно завершена!"



# history_items = PurchaseHistory.objects.filter(user=user)
#
# for item in history_items:
#     print(f"{item.purchased_at}: {item.product.name} - {item.quantity} шт. - {item.get_total_price()} руб.")
