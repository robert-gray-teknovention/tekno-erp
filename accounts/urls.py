from django.urls import path

from . import views


urlpatterns = [
    path('login/', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('password', views.change_password, name='change_password'),
    path('recover', views.recover, name='recover'),
    path('reset', views.reset_password, name='reset_password')
]
