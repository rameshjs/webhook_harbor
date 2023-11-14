from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class WorkSpace(models.Model):
    session_id = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(default=timezone.now, editable=False)
    updated = models.DateTimeField(auto_now=True)


class WebhookRequest(models.Model):
    headers = models.JSONField()
    query = models.JSONField()
    payload = models.JSONField()
    workspace = models.ForeignKey(WorkSpace, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now, editable=False)
    updated = models.DateTimeField(auto_now=True)
