from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView, PasswordResetConfirmView
app_name = 'hotel_reservations'

urlpatterns = [
    path('', views.hotel_booking, name='home'),
    path('search/', views.search_hotels, name='search'),
    path('hotel/<int:hotel_id>/', views.hotel_detail, name='hotel_detail'),
    path('accounts/registration/', views.registration, name='registration'),
    path('accounts/login/', views.user_login, name='login'),
    path('accounts/logout', views.user_logout, name='logout'),
    path('user/profile/', views.profile_user, name='profile'),
    path('user/profile/my_orders', views.user_orders, name='orders'),
    path('password-reset/', views.CustomPasswordResetView.as_view(success_url=reverse_lazy("hotel_reservations:password_reset_done")),
        name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name="password_reset_done.html"), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', views.CustomUserPasswordResetConfirmView.as_view(success_url=reverse_lazy("hotel_reservations:password_reset_complete")), 
        name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name='password_reset_complete'),
    
    path('policy_privacy/', views.policy_privacy, name='policy_privacy')
]
