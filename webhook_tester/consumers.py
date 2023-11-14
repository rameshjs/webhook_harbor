import json

from channels.generic.websocket import AsyncWebsocketConsumer


class NotifyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["workspace_id"]
        self.room_group_name = self.room_name
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        await self.channel_layer.group_send(
            self.room_group_name, {"type": "new.event", "message": message}
        )

    async def new_event(self, event):
        message = event["message"]

        await self.send(text_data=json.dumps({"message": message}))
