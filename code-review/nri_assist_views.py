import logging
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import NRIService, NRIAssistEvent

logger = logging.getLogger(__name__)

CATEGORY_META = {
    'PROPERTY_CARE':  {'label': 'Property Care',          'order': 0},
    'SALE':           {'label': 'Sale Assistance',         'order': 1},
    'ACQUISITION':    {'label': 'Acquisition Assistance',  'order': 2},
    'PRIORITY':       {'label': 'Priority Coordination',   'order': 3},
}


def nri_assist(request):
    _log_event(request, NRIAssistEvent.PAGE_VISIT)

    # Build category sections from DB; fall back to empty service list per category
    db_services = NRIService.objects.filter(is_active=True)
    grouped = {}
    for svc in db_services:
        grouped.setdefault(svc.category, []).append(svc)

    categories = []
    for cat_key, meta in sorted(CATEGORY_META.items(), key=lambda x: x[1]['order']):
        categories.append({
            'key': cat_key,
            'label': meta['label'],
            'services': grouped.get(cat_key, []),
        })

    return render(request, 'nri_assist/nri_assist.html', {'categories': categories})


@csrf_exempt
@require_POST
def log_cta(request):
    category = request.POST.get('category', '')
    _log_event(request, NRIAssistEvent.CTA_CLICK, service_category=category)
    return JsonResponse({'ok': True})


def _log_event(request, event_type, service_category='', metadata=None):
    try:
        forwarded = request.META.get('HTTP_X_FORWARDED_FOR', '')
        ip = forwarded.split(',')[0].strip() if forwarded else request.META.get('REMOTE_ADDR')
        NRIAssistEvent.objects.create(
            event_type=event_type,
            user=request.user if request.user.is_authenticated else None,
            service_category=service_category,
            metadata=metadata or {},
            ip_address=ip or None,
        )
    except Exception:
        logger.exception('NRIAssistEvent log failed')
