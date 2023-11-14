from django.contrib import admin
from webhook_tester.models import WebhookRequest


class WebhookRequestAdmin(admin.ModelAdmin):
    list_display = (
        "headers",
        "query",
        "payload",
        "workspace",
        "created",
    )


admin.site.register(WebhookRequest, WebhookRequestAdmin)
