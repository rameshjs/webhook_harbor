import uuid
from webhook_tester.models import WorkSpace


def generate_random_uuids():
    return str(uuid.uuid4())


def generate_work_space():
    generated_uuid = generate_random_uuids()

    workspace = WorkSpace.objects.filter(session_id=generated_uuid)

    if workspace.exists():
        generate_work_space()

    workspace = WorkSpace.objects.create(session_id=generated_uuid)

    return generated_uuid
