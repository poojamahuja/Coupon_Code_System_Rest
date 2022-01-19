from .models import Coupon, Order, Userprofile
from rest_framework import serializers
import datetime


class CouponSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Coupon
        fields = ['promo_code', 'discount', 'discounttype', 'start_date', 'end_date', 'owner']
        # read_only_fields = ['owner']

    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("Starting date of coupon must be smaller than end date.")

        if data['discount'] > 100:
            if data['discounttype'] == "PERCENT":
                raise serializers.ValidationError("Percentage can not be grater than 100.")

        return data


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    total_amount = serializers.SerializerMethodField('get_total')
    discount_amount = serializers.SerializerMethodField('get_discount')

    class Meta:
        model = Order
        fields = ['coupon', 'order_amount', 'discount_amount', 'total_amount', 'user']
        read_only_fields = ['discount_amount', 'total_amount']

    def get_total(self, coupon):
        discount = coupon.coupon.discount
        discounttype = coupon.coupon.discounttype
        orderamount = coupon.order_amount

        user = Userprofile.objects.filter(username=coupon.user).first()

        birthdate = datetime.datetime.strftime(user.date_of_birth, "%d-%m")
        today_date = datetime.date.today()
        valid_date = datetime.datetime.strftime(today_date, "%d-%m")

        if discounttype == "FLAT":
            if birthdate == valid_date:
                total = orderamount - discount
                totalamount = total - (total * 0.1)
            else:
                totalamount = orderamount - discount
        else:
            if birthdate == valid_date:
                dis = orderamount * (discount / 100)
                total = orderamount - dis
                totalamount = total - (total * 0.1)
            else:
                dis = orderamount * (discount / 100)
                totalamount = orderamount - dis

        coupon.total_amount = totalamount
        coupon.save()
        return coupon.total_amount

    def get_discount(self, coupon):
        discount = coupon.coupon.discount
        discounttype = coupon.coupon.discounttype
        orderamount = coupon.order_amount

        discount_amount = 0

        user = Userprofile.objects.filter(username=coupon.user).first()
        # print(user.date_of_birth)

        birthdate = datetime.datetime.strftime(user.date_of_birth, "%d-%m")
        today_date = datetime.date.today()
        valid_date = datetime.datetime.strftime(today_date, "%d-%m")

        if discounttype == "FLAT":
            if birthdate == valid_date:
                total = orderamount - discount
                discount_amount = discount + (total * 0.1)
            else:
                discount_amount = discount
        else:
            if birthdate == valid_date:
                dis = orderamount * (discount / 100)
                total = orderamount - dis
                discount_amount = dis + (total * 0.1)
            else:
                dis = orderamount * (discount / 100)
                discount_amount = dis
        return discount_amount


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Userprofile
        fields = ['username', 'gender', 'date_of_birth']
