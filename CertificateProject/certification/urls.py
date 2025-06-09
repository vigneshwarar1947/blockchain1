# certification/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_certificate, name='submit_certificate'),
    path('verify/', views.verify_certificate, name='verify_certificate'),
    
    
]


