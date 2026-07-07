import uuid
import contextvars
from django.utils.deprecation import MiddlewareMixin

# Define a thread-safe context variable to store correlation ID
correlation_context = contextvars.ContextVar('correlation_id', default='')

class CorrelationIdMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 1. Retrieve correlation ID from headers or generate new one
        correlation_id = request.headers.get('X-Correlation-ID') or request.META.get('HTTP_X_CORRELATION_ID')
        if not correlation_id:
            correlation_id = str(uuid.uuid4())
        
        # 2. Attach correlation ID to request object for easy access
        request.correlation_id = correlation_id
        
        # 3. Store correlation ID in contextvars
        correlation_context.set(correlation_id)

    def process_response(self, request, response):
        # 4. Attach correlation ID header to outbound response
        correlation_id = getattr(request, 'correlation_id', None)
        if correlation_id:
            response['X-Correlation-ID'] = correlation_id
        return response
