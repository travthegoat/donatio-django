from rest_framework import serializers
from .models import OrganizationRequest

class OrganizationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationRequest
        fields = '__all__'