from django.contrib import admin
from django.urls import path, include

urlpatterns = [
	path('admin/', admin.site.urls),
	path('', include('home.urls')),
	path('', include('room.urls')),
	path('', include('rooms.urls')),
	path('', include('user.urls')),
	path('', include('youtubeAPI.urls')),
]