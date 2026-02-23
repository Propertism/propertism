from django.urls import path
from . import views

app_name = 'properties_spa'

urlpatterns = [
    path('', views.react_properties_app, name='react-root'),
    path('map/', views.react_properties_app, name='react-map'),
]
