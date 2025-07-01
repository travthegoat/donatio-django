from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from .models import OrganizationRequest
from .serializers import OrganizationRequestSerializer


class OrganizationRequestViewSet(viewsets.ModelViewSet):
    queryset = OrganizationRequest.objects.all()
    serializer_class = OrganizationRequestSerializer
    permission_classes = [IsAdminUser]  # only staff/superuser can access
