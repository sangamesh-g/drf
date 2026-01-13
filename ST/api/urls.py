from django.urls import path
from .views import employees, employee_detail
from .views import RegisterView as R
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterView,LoginView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import *

urlpatterns = [
    path('employees/',employees.as_view()),
    path('employees/<int:pk>/', employee_detail.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),   # Login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # Refresh
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('start-report/', StartReportAPIView.as_view(), name='start-report'),
    path('report-status/<str:task_id>/', ReportStatusAPIView.as_view(), name='report-status'),
    path('cancel-report/<str:task_id>/', CancelReportAPIView.as_view(), name='cancel-report'),
    path('generate-text/', GenerateTextView.as_view(), name='generate-text'),
    path('task-status/<str:task_id>/', TaskStatusView.as_view(), name='task-status'),
]

urlpatterns += [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]