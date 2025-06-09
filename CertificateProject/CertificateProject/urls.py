"""
URL configuration for CertificateProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# CertificateProject/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from certification import views as cert_views



from django.shortcuts import redirect, render

# Function-based view to serve a homepage instead of a redirect loop
def home_view(request):
    return render(request, "certification/certificate_success.html")  # Ensure this template exists

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('certificate/', include('certification.urls')),  # Ensure this exists
    path('success/', cert_views.certificate_success, name='certificate_success'),  # Use the actual view
    path('verified/', cert_views.certificate_verified, name='certificate_verified'), 
    
    path('', home_view),  # Serve an actual page, not a redirect loop
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)