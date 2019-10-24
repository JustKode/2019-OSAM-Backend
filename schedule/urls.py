from django.urls import path
from schedule import views

urlpatterns = [
    path('list/', views.get_schedule_list),
    path('list/<int:year>/<int:month>/', views.get_schedule_list),
    path('write/', views.post_schedule),
    path('<int:pk>/', views.schedule),
    path('near/', views.get_near_schedule)
]