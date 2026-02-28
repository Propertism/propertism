from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Agent, Buyer
from properties.models import Inquiry, MaintenanceRequest, SupportTicket

@api_view(['POST'])
def login_api(request):
    """JWT login endpoint"""
    user = authenticate(
        username=request.data.get('username'),
        password=request.data.get('password')
    )
    if not user:
        return Response({'error': 'Invalid credentials'}, status=400)
    
    refresh = RefreshToken.for_user(user)
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh)
    })

def agent_list(request):
    """List all agents"""
    agents = Agent.objects.select_related('user').all()
    return render(request, 'users/agent_list.html', {'agents': agents})


def agent_detail(request, pk):
    """Show agent details"""
    agent = get_object_or_404(Agent.objects.select_related('user'), pk=pk)
    return render(request, 'users/agent_detail.html', {'agent': agent})


@login_required
def dashboard(request):
    """User dashboard with quick stats"""
    user = request.user
    
    # Get user's inquiries
    inquiries = Inquiry.objects.filter(user=user) if hasattr(user, 'inquiry_set') else []
    
    # Get user's maintenance requests
    maintenance = MaintenanceRequest.objects.filter(user=user) if hasattr(user, 'maintenance_request_set') else []
    
    # Get user's tickets
    tickets = SupportTicket.objects.filter(user=user) if hasattr(user, 'ticket_set') else []
    
    context = {
        'user': user,
        'inquiries_count': inquiries.count() if inquiries else 0,
        'maintenance_count': maintenance.count() if maintenance else 0,
        'tickets_count': tickets.count() if tickets else 0,
    }
    return render(request, 'users/dashboard.html', context)


@login_required
def my_inquiries(request):
    """List user's property inquiries"""
    user = request.user
    inquiries = Inquiry.objects.filter(user=user) if hasattr(user, 'inquiry_set') else []
    
    context = {
        'inquiries': inquiries,
    }
    return render(request, 'users/my_inquiries.html', context)


@login_required
def my_maintenance(request):
    """List user's maintenance requests"""
    user = request.user
    maintenance = MaintenanceRequest.objects.filter(user=user) if hasattr(user, 'maintenance_request_set') else []
    
    context = {
        'maintenance': maintenance,
    }
    return render(request, 'users/my_maintenance.html', context)


@login_required
def my_tickets(request):
    """List user's support tickets"""
    user = request.user
    tickets = SupportTicket.objects.filter(user=user) if hasattr(user, 'ticket_set') else []
    
    context = {
        'tickets': tickets,
    }
    return render(request, 'users/my_tickets.html', context)


@login_required
def profile(request):
    """User profile page"""
    user = request.user
    
    # Get or create user profile (Agent/Buyer)
    try:
        agent = Agent.objects.get(user=user)
        profile = agent
    except Agent.DoesNotExist:
        try:
            buyer = Buyer.objects.get(user=user)
            profile = buyer
        except Buyer.DoesNotExist:
            profile = None
    
    context = {
        'user': user,
        'profile': profile,
    }
    return render(request, 'users/profile.html', context)
