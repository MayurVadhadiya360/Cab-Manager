from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),

    path('DriverLogin/', views.DriverLogin, name="DriverLogin"),
    path('UserLogin/', views.UserLogin, name="UserLogin"),

    path('register-user/', views.register_user, name='register_user'),
    path('login-user/', views.login_user, name='login_user'),

    path('register-driver/', views.register_driver, name='register_driver'),
    path('login-driver/', views.login_driver, name='login_driver'),

    path('driver-dashboard/', views.driver_dashboard, name='driver_dashboard'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),

    path('user-history/', views.user_history, name="history"),

    path('book-ride/', views.book_ride, name='book_ride'),
    path('ride-completed/', views.complete_ride, name="complete_ride"),
    path('rate-ride/', views.rate_ride, name="rate_ride"),

    path('user-logout/', views.user_logout, name="user_logout"),
    path('driver-logout/', views.driver_logout, name="driver_logout"),

]