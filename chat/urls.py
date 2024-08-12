from django.urls import path
from . import views
from .views import get_connection_user


urlpatterns = [
    path('', views.chat, name="chat"),
    path('get-connection-user/', get_connection_user, name='get_connection_user'),
]