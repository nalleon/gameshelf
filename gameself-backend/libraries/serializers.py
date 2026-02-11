from shared.serializers import BaseSerializer

from games.serializers import GameSerializer
from users.serializers import UserSerializer

class LibraryItemSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'status': instance.get_status_display(),
            'edition': GameSerializer(instance.edition, request=self.request).serialize(),            
            'description': instance.description,
            'hours_played': instance.hours_played,
            'created_at':  instance.released_at.isoformat(), #TODO: isoformat hace falta?
            'updated_at':  instance.released_at.isoformat(), #TODO: isoformat hace falta?
            'author': UserSerializer(instance.user, request=self.request).serialize(),
        }