from rest_framework import serializers
from . models import SchoolFeeBalance, StudentPaymentInfo


class PaymentInfoSerilalizer(serializers.ModelSerializer):
    class Meta:
        model = StudentPaymentInfo
        fields = '__all__'
