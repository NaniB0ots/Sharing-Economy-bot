from django.urls import path

from . import views

urlpatterns = [
    path('bot/start', views.start_bot),
    path('bot', views.webhook),
]
