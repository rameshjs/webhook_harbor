from django.urls import path
from . import views

urlpatterns = [path("", views.webhook_tester, name="webhook_tester")]
