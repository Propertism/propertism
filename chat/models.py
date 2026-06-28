import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class RealBotSession(models.Model):
    """
    Tracks an active realBOT chat session.
    """
    session_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='realbot_sessions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"realBOT Session {self.session_id} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"


class RealBotMessage(models.Model):
    """
    Persists messages for multi-turn conversational history.
    """
    SENDER_CHOICES = (
        ('user', 'Client Consultant'),
        ('assistant', 'realBOT Advisor'),
    )
    session = models.ForeignKey(RealBotSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=15, choices=SENDER_CHOICES)
    text = models.TextField()
    metadata = models.JSONField(null=True, blank=True, help_text="Stores chips, property cards, comparison tables, or citations")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender.upper()}: {self.text[:40]}"
