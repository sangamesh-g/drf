from django.urls import path
from .views import employees, employee_detail

urlpatterns = [
    path('',employees.as_view()),
    path('<int:pk>/', employee_detail.as_view()),

]