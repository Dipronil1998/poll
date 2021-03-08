from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "accounts"

urlpatterns=[
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.create_user, name='register'),
    path('changepassword/', views.changepassword, name='changepassword'),
    path('profile/', views.profile, name='profile'),
    path('contact/', views.contact, name='contact'),
    path('user/', views.user, name='user'),
    path('userdetails/<int:id>', views.userdetails, name='userdetails'),
    path('delete_user/<int:id>', views.delete_user, name='delete_user'),


    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
]


