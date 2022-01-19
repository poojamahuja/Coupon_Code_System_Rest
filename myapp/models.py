from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from datetime import date
from django.core.exceptions import ValidationError


class Userprofile(AbstractUser):
    gender_choice = (
        ("MALE", "Male"),
        ("FEMALE", "Female"),
    )

    gender = models.CharField(choices=gender_choice, default="MALE", max_length=6)
    date_of_birth = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.username)


class Coupon(models.Model):
    type_choice = (
        ("FLAT", "Flat"),
        ("PERCENT", "Percent"),
    )

    def validate_date(end_date):
        today = date.today()
        if end_date < today:
            raise ValidationError("You can not enter past dates because coupon is expired.")

    promo_code = models.CharField(max_length=10,
                                  validators=[
                                      RegexValidator('^[A-Z0-9]*$', 'Only uppercase letters & numbers are allowed.')])
    discount = models.IntegerField()
    discounttype = models.CharField(choices=type_choice, default="FLAT", max_length=7)
    start_date = models.DateField()
    end_date = models.DateField(validators=[validate_date])
    owner = models.ForeignKey(Userprofile, related_name='user', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.promo_code


class Order(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name='coupon_related')
    order_amount = models.IntegerField(validators=[MinValueValidator(100), MaxValueValidator(1500000)])
    total_amount = models.IntegerField(null=True)
    user = models.ForeignKey(Userprofile, on_delete=models.CASCADE, related_name='user_related', null=True)
