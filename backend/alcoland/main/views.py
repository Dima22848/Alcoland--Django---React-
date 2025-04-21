from rest_framework import viewsets
from rest_framework.response import Response

from .models import Beer, Cognak, Vodka, Vine, Reviews, Basket, PurchaseHistory
from .serializers import BeerSerializer,VineSerializer, VodkaSerializer, CognakSerializer, ReviewsSerializer, BasketSerializer, PurchaseHistorySerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from django.contrib.contenttypes.models import ContentType


class AlcoholViewSet(viewsets.ModelViewSet):


    def get_queryset(self):
        alcohol_type = self.request.query_params.get('type', None)
        if alcohol_type == 'beer':
            return Beer.objects.all()
        elif alcohol_type == 'cognak':
            return Cognak.objects.all()
        elif alcohol_type == 'vodka':
            return Vodka.objects.all()
        elif alcohol_type == 'vino':
            return Vine.objects.all()
        return Beer.objects.all()  # По умолчанию

    def get_serializer_class(self):
        alcohol_type = self.request.query_params.get('type', None)
        if alcohol_type == 'beer':
            return BeerSerializer
        elif alcohol_type == 'cognak':
            return CognakSerializer
        elif alcohol_type == 'vodka':
            return VodkaSerializer
        elif alcohol_type == 'vino':
            return VineSerializer
        return BeerSerializer  # По умолчанию





class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        content_type = self.request.query_params.get('content_type')
        object_id = self.request.query_params.get('object_id')

        queryset = super().get_queryset()

        if content_type and object_id:
            return queryset.filter(content_type_id=content_type, object_id=object_id)

        return queryset


class BasketViewSet(viewsets.ModelViewSet):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def get_user_basket(self, request):
        """Получить корзину текущего пользователя"""
        user_basket = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(user_basket, many=True)
        return Response(serializer.data)


class PurchaseHistoryViewSet(viewsets.ModelViewSet):
    queryset = PurchaseHistory.objects.all()
    serializer_class = PurchaseHistorySerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def get_purchase_history(self, request):
        """Получить историю покупок пользователя"""
        history = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(history, many=True)
        return Response(serializer.data)
