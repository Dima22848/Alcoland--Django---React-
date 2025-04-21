from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.contenttypes.models import ContentType

from .models import (
    Reviews, AlcoholType, Beer, Cognak, Vodka, Vine, Basket, PurchaseHistory
)

# ====================== INLINE МОДЕЛИ ====================== #


class ReviewInline(GenericTabularInline):
    model = Reviews
    extra = 1
    readonly_fields = ("created_at",)
    # Не нужно указывать ForeignKey напрямую



class BasketInline(GenericTabularInline):
    model = Basket
    extra = 1

    # Фильтрация content_type в зависимости от типа продукта
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "content_type":
            kwargs["queryset"] = ContentType.objects.filter(model__in=[Beer, Cognak, Vodka, Vine])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class PurchaseHistoryInline(GenericTabularInline):
    model = PurchaseHistory
    extra = 1
    readonly_fields = ("purchased_at",)

    # Фильтрация content_type в зависимости от типа продукта
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "content_type":
            kwargs["queryset"] = ContentType.objects.filter(model__in=[Beer, Cognak, Vodka, Vine])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Убираем поле 'product' и работаем с content_type и object_id для правильного отображения
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('product')

# ====================== ОСНОВНЫЕ АДМИНКИ ====================== #
@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("author", "text", "created_at")
    list_filter = ("created_at",)
    search_fields = ("author__username", "text")
    readonly_fields = ("created_at",)


@admin.register(AlcoholType)
class AlcoholTypeAdmin(admin.ModelAdmin):
    list_display = ("type",)
    search_fields = ("type",)


@admin.register(Beer)
class BeerAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "country", "style", "type", "color")
    list_filter = ("type", "color", "country")
    search_fields = ("name", "country", "style")
    inlines = [ReviewInline, BasketInline, PurchaseHistoryInline]


@admin.register(Cognak)
class CognakAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "country", "strength", "excerpt")
    list_filter = ("country", "strength", "excerpt")
    search_fields = ("name", "country", "excerpt")
    inlines = [ReviewInline, BasketInline, PurchaseHistoryInline]


@admin.register(Vodka)
class VodkaAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "country", "strength", "volume")
    list_filter = ("country", "strength")
    search_fields = ("name", "country")
    inlines = [ReviewInline, BasketInline, PurchaseHistoryInline]


@admin.register(Vine)
class VineAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "country", "color", "sugar_supply")
    list_filter = ("country", "color", "sugar_supply")
    search_fields = ("name", "country", "color")
    inlines = [ReviewInline, BasketInline, PurchaseHistoryInline]


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "quantity", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username",)
    readonly_fields = ("created_at",)


@admin.register(PurchaseHistory)
class PurchaseHistoryAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "quantity", "price", "purchased_at")
    list_filter = ("purchased_at",)
    search_fields = ("user__username",)
    readonly_fields = ("purchased_at",)

