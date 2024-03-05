from django.urls import path

from . import views

urlpatterns = [
    path('connect/', views.connect, name="connect"),
    path('my_connections/', views.my_connections, name="my_connections"),
    path('options/', views.options, name="options")
]