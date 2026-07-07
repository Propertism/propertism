from django.http import JsonResponse
from chat.middleware import correlation_context

def standard_response(success, data=None, error_code=None, error_message=None, status=200):
    """
    Builds a standard API response JSON payload structure with correlation identifier.
    """
    correlation_id = correlation_context.get() or '-'
    payload = {
        "success": success,
        "correlation_id": correlation_id,
    }
    if success:
        if data is not None:
            payload["data"] = data
    else:
        payload["error"] = {
            "code": error_code or "API_ERROR",
            "message": error_message or "An unexpected integration error occurred."
        }
    return JsonResponse(payload, status=status)
