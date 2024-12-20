from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('polls/', include('polls.urls')),  # el 'pools' puede ser cualquier cosa
    path('admin/', admin.site.urls),
]
