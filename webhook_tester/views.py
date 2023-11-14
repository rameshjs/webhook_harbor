from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from rest_framework import status
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from webhook_tester.models import WorkSpace, WebhookRequest
from webhook_tester.utils import generate_work_space
from asgiref.sync import async_to_sync
import json
import channels.layers

channel_layer = channels.layers.get_channel_layer()


def index(request):
    workspaces = request.session.get("workspaces", [])

    if len(workspaces) > 0:
        return redirect("workspace", id=workspaces[0])

    session_code = generate_work_space()

    request.session["workspaces"] = [session_code]

    return redirect("workspace", id=session_code)


def create_workspace(request):
    session_code = generate_work_space()

    workspaces = request.session.get("workspaces", [])

    workspaces.append(session_code)

    request.session["workspaces"] = workspaces

    return redirect("workspace", id=session_code)


def workspace(request, id):
    workspace_ids = request.session.get("workspaces", [id])
    workspaces = WorkSpace.objects.filter(session_id__in=workspace_ids).order_by(
        "-created"
    )
    current_workspace = WorkSpace.objects.get(session_id=id)
    webhook_requests = WebhookRequest.objects.filter(workspace__session_id=id).order_by(
        "-created"
    )
    return render(
        request,
        "webhook_tester/webhook_test.html",
        {
            "workspaces": workspaces,
            "current_workspace": current_workspace,
            "webhook_requests": webhook_requests,
            "workspace_id": id,
        },
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def webhook_request(request, id):
    workspaces = WorkSpace.objects.filter(session_id=id)

    headers_dict = {key: value for key, value in request.headers.items()}
    payload_dict = {key: value for key, value in request.data.items()}

    headers_json = json.dumps(headers_dict, indent=2)
    payload_json = json.dumps(payload_dict, indent=2)

    WebhookRequest.objects.create(
        headers=headers_json,
        payload=payload_json,
        query={},
        workspace=workspaces.first(),
    )
    async_to_sync(channel_layer.group_send)(id, {"type": "new_event", "message": 1})
    return Response(status=status.HTTP_200_OK)


def all_events(request, id):
    webhook_requests = WebhookRequest.objects.filter(workspace__session_id=id).order_by(
        "-created"
    )

    rendered_template = render_to_string(
        "webhook_tester/all_events.html", {"webhook_requests": webhook_requests}
    )

    return JsonResponse({"template": rendered_template})
