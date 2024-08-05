from django.urls import path
from django.urls import re_path
from . import consumers
from . import views

urlpatterns = [
    path('', views.chat, name="chat"),
]