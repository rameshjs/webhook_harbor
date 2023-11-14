from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("workspace/<str:id>", views.workspace, name="workspace"),
    path("create_workspace", views.create_workspace, name="create_workspace"),
    path("<str:id>/all_events", views.all_events, name="all_events"),
    path("<str:id>", views.webhook_request, name="webhook_request"),
]
