from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('ledger.urls')),
    path('/', include('ledger.urls')),
    path('user/', include('user.urls')),
    path('ledger', include('ledger.urls')),
    path('admin/', admin.site.urls, name='admin'),
]
