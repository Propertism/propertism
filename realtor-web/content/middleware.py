"""Custom middleware for handling health checks and other special cases."""

from django.conf import settings
from django.http import HttpResponse, HttpResponsePermanentRedirect


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
            if current_host in redirect_hosts and current_host != canonical_host.lower():
                scheme = getattr(settings, "CANONICAL_SCHEME", "https")
                path = request.get_full_path()
                return HttpResponsePermanentRedirect(f"{scheme}://{canonical_host}{path}")

        return self.get_response(request)
