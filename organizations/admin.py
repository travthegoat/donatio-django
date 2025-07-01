from django.contrib import admin
from .models import Organization, OrganizationRequest

# Register your models here.
admin.site.register(Organization)
admin.site.register(OrganizationRequest)
