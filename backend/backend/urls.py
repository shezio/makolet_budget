from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('budget/', include('budget.urls')),  # Includes URLs from the budget app
]
