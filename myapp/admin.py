from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Userprofile, Coupon, Order


class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'gender', 'date_of_birth', 'used',
    )


admin.site.register(Userprofile)
admin.site.register(Coupon)
admin.site.register(Order)