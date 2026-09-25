from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

def custom_403(request, exception=None):
    return render(request, 'errors/403.html', status=403)

from django.http import JsonResponse

def health_check(request):
    return JsonResponse({'status': 'ok'})

def custom_404(request, exception=None):
    return render(request, 'errors/404.html', status=404)

handler403 = custom_403
handler404 = custom_404

urlpatterns = [
    path('health/', health_check, name='health'),
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('students/', include('students.urls')),
    path('courses/', include('courses.urls')),
    path('academics/', include('academics.urls')),
    path('api/', include('api.urls')),
]
