from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('submit/', views.submit_chat_message, name='submit'),
]
