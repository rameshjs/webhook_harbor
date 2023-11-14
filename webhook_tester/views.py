from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from webhook_tester.models import WorkSpace, WebhookRequest
from webhook_tester.utils import generate_work_space
import json


def index(request):
    session_code = request.session.get("workspace_id", None)

    if session_code:
        print("existing")
        return redirect("workspace", id=session_code)

    print("new")
    session_code = generate_work_space()

    request.session["workspace_id"] = session_code
    print(session_code)

    return redirect("workspace", id=session_code)


def workspace(request, id):
    workspaces = WorkSpace.objects.filter(session_id=id)
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
    return Response(status=status.HTTP_200_OK)
