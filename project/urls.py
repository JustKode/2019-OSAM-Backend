from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', obtain_jwt_token),
    path('auth/verify', verify_jwt_token),
    path('auth/refresh', refresh_jwt_token),
    path('user/', include('user.urls'))
]
