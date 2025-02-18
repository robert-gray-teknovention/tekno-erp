from django.urls import path

from . import views


urlpatterns = [
    path('login/', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    # path('dashboard', views.dashboard, name='dashboard'),
    path('dashboard', views.dashboard_main, name='dashboard'),
    path('dashboard_detail', views.dashboard_detail, name='dashboard_detail'),
    path('password', views.change_password, name='change_password'),
    path('recover', views.recover, name='recover'),
    path('reset', views.reset_password, name='reset_password')
]
