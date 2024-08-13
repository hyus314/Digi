from django.urls import path
from . import views
from .views import get_connection_user, get_logged_in

urlpatterns = [
    path('', views.chat, name="chat"),
    path('get-connection-user/', get_connection_user, name='get_connection_user'),
    path('get-logged-in/', get_logged_in, name='get_logged_in')
]