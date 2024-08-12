from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat, name="chat"),
    path('get-connection-users/', views.get_connection_users, name='get_connection_users'),
]