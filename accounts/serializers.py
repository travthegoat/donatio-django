from dj_rest_auth.registration.serializers import SocialLoginSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers
from .models import User, Profile

class GoogleLoginSerializer(SocialLoginSerializer):
    def validate(self, attrs):
        # Use id_token as access_token if needed
        if not attrs.get('access_token') and 'id_token' in self.context['request'].data:
            attrs['access_token'] = self.context['request'].data['id_token']
        return super().validate(attrs)
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['full_name', 'phone_number']
    
class CustomUserDetailsSerializer(UserDetailsSerializer):   
    profile = ProfileSerializer(read_only=True)
    
    class Meta(UserDetailsSerializer.Meta):
        fields = ['id', 'username', 'email', 'is_staff', 'profile', 'joined_at']
        read_only_fields = ['is_staff']