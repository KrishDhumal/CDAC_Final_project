from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # 👇 This makes login view appear at root ( / )
    path('', include('expenses.urls')),
]
