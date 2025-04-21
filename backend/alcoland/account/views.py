from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import CustomTokenObtainPairSerializer

from .models import CustomUser, NewsFeed, NewsFeedComments
from .serializers import CustomUserSerializer, NewsFeedSerializer, NewsFeedCommentsSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(CustomUserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    # permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def add_friend(self, request, pk=None):
        """Добавление друга"""
        user = self.get_object()
        friend_id = request.data.get('friend_id')
        friend = CustomUser.objects.get(id=friend_id)
        user.add_friend(friend)
        return Response({"status": "Friend added"})

    @action(detail=True, methods=['post'])
    def remove_friend(self, request, pk=None):
        """Удаление друга"""
        user = self.get_object()
        friend_id = request.data.get('friend_id')
        friend = CustomUser.objects.get(id=friend_id)
        user.remove_friend(friend)
        return Response({"status": "Friend removed"})

    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        """Подписка на пользователя"""
        user = self.get_object()
        follow_id = request.data.get('follow_id')
        follow_user = CustomUser.objects.get(id=follow_id)
        user.follow(follow_user)
        return Response({"status": "Following"})

    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk=None):
        """Отписка от пользователя"""
        user = self.get_object()
        unfollow_id = request.data.get('unfollow_id')
        unfollow_user = CustomUser.objects.get(id=unfollow_id)
        user.unfollow(unfollow_user)
        return Response({"status": "Unfollowed"})

class NewsFeedViewSet(viewsets.ModelViewSet):
    queryset = NewsFeed.objects.all()
    serializer_class = NewsFeedSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = NewsFeed.objects.all()
        profile_id = self.request.query_params.get('profile')
        if profile_id:
            queryset = queryset.filter(profile_id=profile_id)
        return queryset


class NewsFeedCommentsViewSet(viewsets.ModelViewSet):
    queryset = NewsFeedComments.objects.all()
    serializer_class = NewsFeedCommentsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = NewsFeedComments.objects.all()
        newsfeed_id = self.request.query_params.get('newsfeed')
        if newsfeed_id:
            queryset = queryset.filter(newsfeed_id=newsfeed_id)
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request  # Передаем request в сериализатор
        return context