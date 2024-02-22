from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('profile/', views.profile, name="profile"),
    path('profile/token_exists/', views.token_exists, name="token_exists"),
    path('profile/get_token/', views.get_token, name="get_token"),
]