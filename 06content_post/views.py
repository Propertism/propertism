import logging
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .services.generator import generate_post

logger = logging.getLogger(__name__)

@login_required
def post_generator_view(request):
    """View to render the internal Post Generator tool."""
    context = {
        "breadcrumbs": [
            {"name": "Home", "url": "/"},
            {"name": "06content.post", "url": None}
        ]
    }
    return render(request, "post_generator.html", context)

@require_POST
@login_required
def post_generate_api(request):
    """API endpoint to generate content posts."""
    platform = request.POST.get("platform", "linkedin")
    intent = (request.POST.get("intent") or "sell").lower()
    geo = request.POST.get("geo", "USA")
    
    try:
        generated_text = generate_post(platform, intent, geo)
        
        # Log usage
        logger.info(f"06CONTENT_POST_GENERATE: user={request.user.username}, platform={platform}, intent={intent}, geo={geo}")
        
        return JsonResponse({"ok": True, "generated_text": generated_text})
    except Exception as e:
        logger.error(f"Error in post_generate_api: {e}")
        return JsonResponse({"ok": False, "error": str(e)}, status=500)
