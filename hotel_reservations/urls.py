from django.urls import path
from . import views

urlpatterns = [
    path('', views.hotel_booking, name='home'),
    path('registration/', views.registration, name='registration'),
    path('accounts/login/', views.user_login, name='login'),
    path('accounts/logout', views.user_logout, name='logout')
]
