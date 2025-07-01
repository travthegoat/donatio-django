from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrganizationRequestViewSet

router = DefaultRouter()
router.register(r'organization-requests', OrganizationRequestViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]