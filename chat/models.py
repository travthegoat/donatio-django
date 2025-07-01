from django.db import models
from uuid import uuid4
from accounts.models import User
from organizations.models import Organization

class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donor_chats')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='organization_chats')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('donor', 'organization')
        
class ChatMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']