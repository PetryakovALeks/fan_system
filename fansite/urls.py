# fansite/urls.py
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def redirect_to_login_or_profile(request):
    if request.user.is_authenticated:
        return redirect('profile')
    return redirect('login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_to_login_or_profile, name='root'),  # Добавляем корневой маршрут
    path('', include('fan.urls')),  # Подключаем маршруты из приложения fan
]