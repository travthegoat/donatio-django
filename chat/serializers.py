from rest_framework import serializers
from .models import Chat, ChatMessage
from accounts.serializers import CustomUserDetailsSerializer

class ChatSerializer(serializers.ModelSerializer):
    donor = CustomUserDetailsSerializer(read_only=True)
    
    class Meta:
        model = Chat
        fields = '__all__'

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__'
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['sender'] = {
            'id': instance.sender.id,
            'username': instance.sender.username,
            'profile_picture': instance.sender.profile.attachments.first().file.url if instance.sender.profile.attachments.exists() else None
        }
        return representation