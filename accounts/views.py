from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from .serializers import GoogleLoginSerializer, ProfileSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, Profile
from attachments.models import Attachment
from .serializers import CustomUserDetailsSerializer
from django.shortcuts import get_object_or_404

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    serializer_class = GoogleLoginSerializer
    
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserDetailsSerializer
    http_method_names = ['get']
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_staff']
    
    @action(detail=False, methods=['get', 'put'], url_path='me')
    def current_user(self, request):
        # Return the current authenticated user
        if request.method == 'GET':
            user = self.request.user
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # Update the current authenticated user profile
        elif request.method == 'PUT':
            profile = get_object_or_404(Profile, user=request.user)
            
            serializer = ProfileSerializer(profile, data=request.data)
            serializer.is_valid(raise_exception=True)
            
            if serializer.validated_data.get('profile_picture'):
                # Delete all the existing profile picture
                profile.attachments.all().delete()
                
                Attachment.objects.create(
                    content_object=profile,
                    file=serializer.validated_data.get('profile_picture')
                )
                
                serializer.validated_data.pop('profile_picture')
            
            serializer.save()
        
        