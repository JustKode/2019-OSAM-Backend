from django.urls import path
from user import views

urlpatterns = [
    path('register/', views.register),
    path('info_register/', views.info_register),
    path('info/', views.info)
]