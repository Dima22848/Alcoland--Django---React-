from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import Reviews, Beer, Cognak, Vodka, Vine, Basket, PurchaseHistory

class BeerSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source="get_type_display", read_only=True)
    color_display = serializers.CharField(source="get_color_display", read_only=True)

    class Meta:
        model = Beer
        exclude = ("type", "color")

class CognakSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cognak
        fields = '__all__'

class VodkaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vodka
        fields = '__all__'

class VineSerializer(serializers.ModelSerializer):
    color_display = serializers.CharField(source="get_color_display", read_only=True)
    sugar_supply_display = serializers.CharField(source="get_sugar_supply_display", read_only=True)

    class Meta:
        model = Vine
        exclude = ("color", "sugar_supply")


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    content_type = serializers.PrimaryKeyRelatedField(queryset=ContentType.objects.all())

    class Meta:
        model = Reviews
        fields = '__all__'

class BasketSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()
    content_type = serializers.PrimaryKeyRelatedField(queryset=ContentType.objects.all())

    class Meta:
        model = Basket
        fields = '__all__'

class PurchaseHistorySerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()
    content_type = serializers.PrimaryKeyRelatedField(queryset=ContentType.objects.all())

    class Meta:
        model = PurchaseHistory
        fields = '__all__'
