from django.urls import path
from django.conf import settings

from . import views

urlpatterns = [
    path('bot/start', views.start_bot),
    path('bot/' + settings.TG_TOKEN, views.webhook),
]
