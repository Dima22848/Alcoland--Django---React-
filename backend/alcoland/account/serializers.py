from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import CustomUser, NewsFeed, NewsFeedComments


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['nickname'] = user.nickname  # Добавляем nickname в токен
        return token

    def validate(self, attrs):
        email = attrs.get("email")  # Логинимся по email
        password = attrs.get("password")

        user = CustomUser.objects.filter(email=email).first()  # Проверяем пользователя по email
        if user and user.check_password(password):
            return super().validate(attrs)  # Отдаем токен
        raise serializers.ValidationError("Неверный email или пароль")


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CustomUserSerializer(serializers.ModelSerializer):
    friends = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), many=True)
    following = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), many=True)
    followers = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), many=True)
    city_display = serializers.CharField(source="get_city_display", read_only=True)

    class Meta:
        model = CustomUser
        exclude = ("city",)


class NewsFeedSerializer(serializers.ModelSerializer):
    profile_id = serializers.SerializerMethodField()

    class Meta:
        model = NewsFeed
        fields = ['id', 'profile_id', 'text', 'file', 'created_at']

    def get_profile_id(self, obj):
        return obj.profile.id

class NewsFeedCommentsSerializer(serializers.ModelSerializer):
    profile_id = serializers.ReadOnlyField(source='profile.id')
    newsfeed_id = serializers.ReadOnlyField(source='newsfeed.id')

    class Meta:
        model = NewsFeedComments
        fields = ['id', 'profile_id', 'newsfeed_id', 'text', 'created_at']

    def create(self, validated_data):
        request = self.context.get("request")
        profile = request.user  # Получаем текущего пользователя
        newsfeed_id = self.initial_data.get("newsfeed_id")  # Получаем ID из запроса
        newsfeed = NewsFeed.objects.get(id=newsfeed_id)  # Получаем объект NewsFeed
        return NewsFeedComments.objects.create(profile=profile, newsfeed=newsfeed, **validated_data)

