from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from content.models import CompanyInfo, Statistic, Service, CoreValue, HomepageCard
from properties.models import Property


def home(request):
    """Homepage with dynamic content from database - Stunning Design"""
    company = CompanyInfo.objects.first()
    stats = Statistic.objects.all()[:4]  # Get 4 stats for the new design
    services = Service.objects.all()[:3]
    featured_properties = Property.objects.filter(status='available').prefetch_related('photos')[:6]  # Show more properties
    
    context = {
        'company': company,
        'stats': stats,
        'services': services,
        'featured_properties': featured_properties,
        'core_values': CoreValue.objects.filter(is_active=True)[:3],
        'homepage_cards': HomepageCard.objects.filter(is_active=True)[:3],
    }
    
    return render(request, 'home-premium.html', context)


@login_required
def dashboard(request):
    return render(request, 'users/dashboard.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def user_login(request):
    """Redirect to allauth login for unified auth experience (Google Sign-In)."""
    return redirect('account_login')


def user_register(request):
    """Redirect to allauth signup for unified auth experience (Google Sign-Up)."""
    return redirect('account_signup')


def user_logout(request):
    """Redirect to allauth logout for proper session termination."""
    return redirect('account_logout')
