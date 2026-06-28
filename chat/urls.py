from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('submit/', views.submit_chat_message, name='submit'),
    path('session/init/', views.init_session, name='init_session'),
    path('query/', views.send_message, name='send_message'),
]
