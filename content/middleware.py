"""Custom middleware for handling health checks and other special cases."""

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import redirect


class HealthCheckMiddleware:
    """
    Middleware to handle health check requests before ALLOWED_HOSTS validation.
    
    This ensures load balancer health checks always succeed regardless of
    the Host header sent by the load balancer.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Handle health check before any other middleware
        if request.path == '/health/':
            return HttpResponse("OK", content_type="text/plain", status=200)
        
        response = self.get_response(request)
        return response


class CanonicalDomainRedirectMiddleware:
    """Redirect alternate public domains to the canonical host."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        canonical_host = getattr(settings, "CANONICAL_HOST", "")
        redirect_hosts = set(getattr(settings, "CANONICAL_REDIRECT_HOSTS", []))

        if canonical_host and redirect_hosts:
            current_host = request.get_host().split(":", 1)[0].lower()
            # Only redirect if the host is explicitly listed — never redirect
            # internal/origin hostnames (e.g. EB CNAME forwarded by CloudFront)
            if current_host in redirect_hosts and current_host != canonical_host.lower():
                scheme = getattr(settings, "CANONICAL_SCHEME", "https")
                path = request.get_full_path()
                return HttpResponsePermanentRedirect(f"{scheme}://{canonical_host}{path}")

        return self.get_response(request)


class AdminAccessMiddleware:
    """
    Restrict Django admin to password-authenticated superusers only.

    Blocks two categories of authenticated users from /admin/:
      1. Users who authenticated via Google OAuth (have a SocialAccount record).
      2. Authenticated users who are not is_superuser=True.

    Unauthenticated requests pass through so Django's admin login form works normally.
    Must be placed after AuthenticationMiddleware and AccountMiddleware in MIDDLEWARE.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        admin_url = getattr(settings, 'ADMIN_URL', 'admin').strip('/')
        self._admin_prefix = f'/{admin_url}/'

    def __call__(self, request):
        if not request.path.startswith(self._admin_prefix):
            return self.get_response(request)

        user = request.user

        # Unauthenticated — let Django admin show the login form.
        if not user.is_authenticated:
            return self.get_response(request)

        # Gate 1: superuser only.
        if not user.is_superuser:
            logout(request)
            messages.error(request, 'Admin access requires a superuser account.')
            return redirect('/')

        # Gate 2: no Google OAuth sessions.
        try:
            from allauth.socialaccount.models import SocialAccount
            if SocialAccount.objects.filter(user=user).exists():
                logout(request)
                messages.error(
                    request,
                    'Admin access is not available for Google-authenticated accounts. '
                    'Sign in with your username and password.',
                )
                return redirect('/')
        except ImportError:
            pass

        return self.get_response(request)
