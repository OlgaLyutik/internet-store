"""URL configuration for store project."""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('internet_store.urls')),
]

handler404 = 'internet_store.views.page_not_found'
