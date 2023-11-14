from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:id>", views.webhook_request, name="webhook_request"),
    path("workspace/<str:id>", views.workspace, name="workspace"),
]
