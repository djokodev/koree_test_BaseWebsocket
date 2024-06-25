from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Data

@receiver(post_save, sender=Data)
def handle_data_save(sender, instance, created, **kwargs):
    print("Hello")
    try:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'test', 
            {
                'type': 'chat.message',
                "message": "new message"

            }
        )
        print("message sent")
    except Exception as e:
        print(f"Erreur lors de l'envoi des données : {e}")