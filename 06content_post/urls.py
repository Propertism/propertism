from django.urls import path
from . import views

app_name = '06content_post'

urlpatterns = [
    path('generate/', views.post_generator_view, name='post_generator_view'),
    path('api/generate/', views.post_generate_api, name='post_generate_api'),
]
