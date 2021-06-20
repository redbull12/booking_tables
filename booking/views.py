from rest_framework.generics import UpdateAPIView, get_object_or_404, ListAPIView

from booking.models import Table, Booking
from booking.permissions import IsAdminPermission
from booking.serializers import TableSerializer, TablesListSerializer, BookingSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet


class TableListView(ListAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer


class TableViewSet(ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    lookup_url_kwarg = 'slug'
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter]
    filterset_fields = ['is_booked']
    ordering_fields = ['title']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permissions = [IsAdminPermission]
        else:
            permissions = []
        return [perm() for perm in permissions]

    def get_serializer_class(self):#нужен для разделения листинга и деталей товара
        if self.action == 'list':
            return TablesListSerializer
        return self.serializer_class

    # @action(['POST'], detail=True)
    # def like(self, request, slug=None):
    #     product = self.get_object()
    #     user = request.user
    #     # message = 'liked' if like.is_liked else 'disliked'
    #     try:
    #         like = Like.objects.get(product=product, user=user)
    #         like.is_liked = not like.is_liked
    #         like.save()
    #         message = 'liked' if like.is_liked else 'disliked'
    #     except Like.DoesNotExist:
    #         Like.objects.create(product=product, user=user, is_liked=True)
    #     return Response(message, status=200)

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}
#
class BookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        serializer = BookingSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Подтвердите бронь по почте', status=201)

# Возможны фатальные ошибки из-за ссылания на разные таблицы
# class ConfirmBookingView(APIView):
#     def get(self, request):
#         activation_code = request.query_params.get('u')
#         # booking = get_object_or_404(Table, activation_code=activation_code)
#         booking = get_object_or_404(Booking, activation_code=activation_code)
#         # booking.is_booked = True
#         booking.confirmed = True
#         booking.activation_code = ''
#         booking.save()
#         return Response('Столик забронирован', status=200)

class ConfirmBookingView(APIView):
    def get(self, request):
        activation_code = request.query_params.get('u')
        order = get_object_or_404(Booking,activation_code=activation_code)
        order.confirmed = True
        order.activation_code = ''
        order.save()
        return Response('Заказ подтвержден', status=200)

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'tables': reverse('tables-list', request=request, format=format)
    })

# TODO написать вьшку для брониорвания чтобы было отдельно от ~TableViewSet с подтверждением по почте
# TODO написать сериализаторы к бронированию и подтверждению брони
# бронирование будет по форме, пользователь заполняет форму где указывает все
# нужные данные и после состояние указанного столика меняется на is_booked=True
# TODO
# TODO
# TODO
