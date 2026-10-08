#маршрутизацию HTTP-запросов
from django.urls import path
from .views import StudentListView, StudentDetailView

urlpatterns = [
    path('requests', StudentListView.as_view()),
    path('requests/<int:student_id>', StudentDetailView.as_view()),
]