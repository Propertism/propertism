from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import (
    CompanyInfo, Statistic, Service, CoreValue, TeamMember,
    ExpertiseArea, BlogPost, Newsletter, ContactInquiry
)
from properties.models import Property
import logging

# Configure logger
logger = logging.getLogger(__name__)


def get_company_context():
    """Get company info for all pages"""
    try:
        company = CompanyInfo.objects.first()
    except CompanyInfo.DoesNotExist:
        company = None
    return {'company': company}


def home(request):
    """Homepage view - Stunning Design"""
    from django.utils import translation
    
    context = get_company_context()
    
    # Debug: Print current language
    current_lang = translation.get_language()
    print(f"🌍 Current Language: {current_lang}")
    if context.get('company'):
        print(f"📝 Hero Title: {context['company'].hero_title}")
    
    context.update({
        'stats': Statistic.objects.filter(is_active=True)[:4],  # Get 4 stats for new design
        'services': Service.objects.filter(is_active=True)[:3],
        'featured_properties': Property.objects.filter(status='available')[:6],  # Show more properties
        'breadcrumbs': [
            {'name': 'Home', 'url': None}
        ]
    })
    return render(request, 'home-hybrid.html', context)


def services(request):
    """Services page view"""
    context = get_company_context()
    context.update({
        'services': Service.objects.filter(is_active=True),
        'breadcrumbs': [
            {'name': 'Home', 'url': '/'},
            {'name': 'Services', 'url': None}
        ]
    })
    return render(request, 'services.html', context)


def about(request):
    """About page view"""
    context = get_company_context()
    context.update({
        'stats': Statistic.objects.filter(is_active=True),
        'values': CoreValue.objects.filter(is_active=True),
    })
    return render(request, 'about.html', context)


def management(request):
    """Management page view"""
    context = get_company_context()
    context.update({
        'team_members': TeamMember.objects.filter(is_active=True),
        'expertise_areas': ExpertiseArea.objects.filter(is_active=True),
    })
    return render(request, 'management.html', context)


def blog(request):
    """Blog listing page view"""
    context = get_company_context()
    context.update({
        'posts': BlogPost.objects.filter(is_published=True),
    })
    return render(request, 'blog.html', context)


def blog_post(request, slug):
    """Individual blog post view"""
    context = get_company_context()
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    context.update({
        'post': post,
        'recent_posts': BlogPost.objects.filter(is_published=True).exclude(id=post.id)[:3],
    })
    return render(request, 'blog_post.html', context)


def contact(request):
    """Contact page view with form handling"""
    context = get_company_context()
    
    if request.method == 'POST':
        # Handle contact form submission
        try:
            inquiry = ContactInquiry.objects.create(
                name=request.POST.get('name'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone'),
                service=request.POST.get('service'),
                property_type=request.POST.get('property_type', ''),
                message=request.POST.get('message'),
            )
            logger.info(f"Contact inquiry received from {inquiry.email}")
            messages.success(request, 'Thank you for your inquiry! We will get back to you soon.')
            return redirect('contact')
        except Exception as e:
            logger.exception(f"Error processing contact form: {str(e)}")
            messages.error(request, 'There was an error submitting your inquiry. Please try again or call us directly.')
    
    context.update({
        'breadcrumbs': [
            {'name': 'Home', 'url': '/'},
            {'name': 'Contact', 'url': None}
        ]
    })
    return render(request, 'contact.html', context)


def newsletter_subscribe(request):
    """Newsletter subscription handler"""
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            try:
                Newsletter.objects.get_or_create(email=email)
                messages.success(request, 'Thank you for subscribing to our newsletter!')
            except Exception as e:
                messages.error(request, 'There was an error. Please try again.')
        else:
            messages.error(request, 'Please provide a valid email address.')
    
    # Redirect back to the referring page or home
    return redirect(request.META.get('HTTP_REFERER', 'home'))


# ==============================================================================
# ERROR HANDLERS
# ==============================================================================

def custom_404(request, exception=None):
    """Custom 404 error handler"""
    return render(request, '404.html', status=404)


def custom_500(request):
    """Custom 500 error handler"""
    return render(request, '500.html', status=500)
