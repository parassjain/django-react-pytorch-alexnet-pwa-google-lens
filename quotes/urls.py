from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from core.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
	path('admin/', admin.site.urls),
	path('wel/', ReactView.as_view(), name="something"),
    path('api/posts/', PostView.as_view(), name= 'posts_list'),
]+ static(settings.MEDIA_URL,document_root =settings.MEDIA_ROOT)
