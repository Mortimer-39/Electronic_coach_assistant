from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserRegistrationView  # Создадим его сейчас

app_name = 'users'

urlpatterns = [
    # Логин (получение токена). Использует email и password
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # Обновление токена (refresh)
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Регистрация нового тренера/клиента
    path('api/register/', UserRegistrationView.as_view(), name='register'),
]