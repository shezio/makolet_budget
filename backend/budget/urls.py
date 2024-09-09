from django.urls import path
from . import views

urlpatterns = [
    path('add_purchase/', views.add_purchase, name='add_purchase'),
    path('get_budget/', views.get_budget, name='get_budget'),
]
