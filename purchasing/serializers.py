from rest_framework import serializers
from .models import Vendor, Manufacturer


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id', 'name', 'email', 'website', 'phone',]


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ['id', 'name', 'email', 'website', 'phone', 'notes',]
