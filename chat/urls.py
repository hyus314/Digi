from django.urls import path
from django.urls import re_path
from . import consumers
from . import views

urlpatterns = [
    path('', views.chat, name="chat"),
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi())
]