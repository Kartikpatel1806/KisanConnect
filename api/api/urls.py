"""api URL Configuration"""

from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

from authentication.views import UserView
from crop_data.views import CropView
from fertilizer_data.views import FertilizerView
from yield_data.views import YieldView, QueryView, ChatBotView


# 👇 Define a simple homepage view
def home(request):
    return HttpResponse("<h2>Welcome to the API Home Page</h2><p>Use /auth/, /user/, /crop/, etc.</p>")


urlpatterns = [
    path("", home),  # 👈 Root URL to prevent 404
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


# Serve media files in debug mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
