from django.urls import path

from . import views

urlpatterns = [
    path('token_exists/', views.token_exists, name="token_exists"),
    path('get_token/', views.get_token, name="get_token")
]