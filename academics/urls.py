from django.urls import path
from . import views

app_name = 'academics'

urlpatterns = [
    path('', views.AcademicRecordListView.as_view(), name='list'),
    path('add/', views.AcademicRecordCreateView.as_view(), name='add'),
    path('<int:pk>/', views.AcademicRecordDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.AcademicRecordUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.AcademicRecordDeleteView.as_view(), name='delete'),
]
