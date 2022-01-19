from .serializers import CouponSerializer, UserSerializer, OrderSerializer
from .models import Coupon, Order, Userprofile
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .permissions import IsOwnerOrReadOnly
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('UserView', request=request, format=format),
        'coupons': reverse('CouponView', request=request, format=format),
        'orders': reverse('OrderView', request=request, format=format)
    })


class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]   # It allows anonymous user to read data but can not create, put, delete data
    #permission_classes = [IsAuthenticated]            # It does not allow anonymous user to read, create, update, delete data
    authentication_classes = [TokenAuthentication]

class CouponView(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class UserView(viewsets.ModelViewSet):
    queryset = Userprofile.objects.all()
    serializer_class = UserSerializer
