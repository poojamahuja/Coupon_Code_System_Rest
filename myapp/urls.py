from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('user', views.UserView)
router.register('coupon', views.CouponView)
router.register('order', views.OrderView)

urlpatterns = [
    path('', include(router.urls)),
]
