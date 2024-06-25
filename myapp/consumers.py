import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from myapp.models import Data
from myapp.serializers import DataSerializers


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"{self.room_name}"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

        message = "new message"

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def chat_message(self, event):
        # message = event["message"]
        message = self.get_all_data()
        self.send(text_data=json.dumps({"message": message}))

    def get_all_data(self):
        query = Data.objects.all()
        serializer = DataSerializers(query, many=True)
        return serializer.data