from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'students', views.StudentViewSet, basename='student')
router.register(r'courses', views.CourseViewSet, basename='course')
router.register(r'enrollments', views.EnrollmentViewSet, basename='enrollment')
router.register(r'academic-records', views.AcademicRecordViewSet, basename='academic-record')

from rest_framework.authtoken import views as auth_views

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', views.DashboardAPIView.as_view(), name='dashboard-api'),
    path('api-token-auth/', auth_views.obtain_auth_token, name='api-token-auth'),
]
