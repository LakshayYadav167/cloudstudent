from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    # Courses
    path('', views.CourseListView.as_view(), name='list'),
    path('add/', views.CourseCreateView.as_view(), name='add'),
    path('<int:pk>/', views.CourseDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.CourseUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.CourseDeleteView.as_view(), name='delete'),

    # Enrollments
    path('enrollments/', views.EnrollmentListView.as_view(), name='enrollment_list'),
    path('enrollments/add/', views.EnrollmentCreateView.as_view(), name='enrollment_add'),
    path('enrollments/<int:pk>/', views.EnrollmentDetailView.as_view(), name='enrollment_detail'),
    path('enrollments/<int:pk>/delete/', views.EnrollmentDeleteView.as_view(), name='enrollment_delete'),
]
