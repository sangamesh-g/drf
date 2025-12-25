from django.urls import path
from .views import employees, employee_detail
from .views import RegisterView as R
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterView,LoginView

urlpatterns = [
    path('employees/',employees.as_view()),
    path('employees/<int:pk>/', employee_detail.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),   # Login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # Refresh
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]