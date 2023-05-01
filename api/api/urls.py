"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,re_path,include
from django.conf import settings
from django.conf.urls.static import static
from authentication.views import UserView
from crop_data.views import CropView
from fertilizer_data.views import FertilizerView
from yield_data.views import YieldView,QueryView,ChatBotView

urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    re_path(r'^user/', UserView.as_view()),
    re_path(r'^crop/', CropView.as_view()),
    re_path(r'^fertilizer/', FertilizerView.as_view()),
    re_path(r'^yield/', YieldView.as_view()),
    re_path(r'^bot/', QueryView.as_view()),
    re_path(r'^chatbot/', ChatBotView.as_view()),
]


if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)