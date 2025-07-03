from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings


class CustomAccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        key = emailconfirmation.key
        frontend_url = getattr(settings, "FRONTEND_URL", "http://localhost:3000")
        return f"{frontend_url}/activate/{key}"

    def is_open_for_signup(self, request):
        # Allow superusers to bypass email verification
        if request.user and request.user.is_superuser:
            return True
        return super().is_open_for_signup(request)
