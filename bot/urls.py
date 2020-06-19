from django.urls import path
from django.conf import settings

from . import views

urlpatterns = [
    path('start', views.start_bot),
    path('post', views.send_post),
    path('' + settings.TG_TOKEN, views.webhook),
]
