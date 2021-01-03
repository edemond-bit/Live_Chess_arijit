"""hrsuit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),#change url in production --> rabotecsuits.com/_&_wysiwyg-suits_empty-link_url
    path('',views.index_view,name='home'),
    path('accounts/',include('accounts.urls',namespace='accounts')),
    path('dashboard/',include('dashboard.urls',namespace='dashboard')),
    path('gateway/',include('gateway.urls',namespace='gateway')),
    path('forgot_password/', include('django.contrib.auth.urls')),
    path(r'api/login/', views.LoginView.as_view(), name='login'),
    path('api/registration/', views.RegisterView.as_view(), name='registration'),
    path('tournament/', include('tournment.urls')),
    path('users/', include('users.urls')),
    path('dashboard/', views.DashboardViewSet),
    path('file_transfer/', views.file_transfer),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = 'CHESS LIVE ADMINISTRATION'
admin.site.site_title = "Chess Live Admin Portal"
admin.site.index_title = "Welcome to Chess Live Admin Panel"