from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrganizationRequestViewSet, OrganizaitonViewSet

router = DefaultRouter()
router.register(r'organization-requests', OrganizationRequestViewSet)
router.register(r'organizations', OrganizaitonViewSet)

urlpatterns = [
    path('', include(router.urls)),
]