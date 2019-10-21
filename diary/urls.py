from django.urls import path
from diary import views

urlpatterns = [
    path('list/', views.get_diary_list),
    path('list/<int:year>/<int:month>/', views.get_diary_list),
    path('write/', views.post_diary),
    path('<int:pk>/', views.diary)
]