"""
URL configuration for proyecto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('transfers/', views.transfers, name='transfers'),
    path('procesar_reserva/', views.procesar_reserva, name='procesar_reserva'),
    path('reserva/<int:reserva_id>/', views.reserva, name='reserva'),
    path('login-user/', views.login_user, name='login-user'),
    path('nuevo_transfer/', views.nuevo_transfer, name='nuevo_transfer'),
    path('guardar_transfer', views.guardar_transfer, name='guardar_transfer'),
    path('nuevo/<int:id_transfer>/', views.nuevo, name='nuevo'),
]
