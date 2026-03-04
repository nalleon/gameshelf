from rest_framework import serializers

from games.serializers import GameSerializer
from shared.serializers import BaseSerializer
from users.serializers import UserSerializer


class LibraryItemSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'status': instance.get_status_display(),
            'edition': GameSerializer(instance.edition, request=self.request).serialize(),
            'description': instance.description,
            'hours_played': instance.hours_played,
            'created_at': instance.released_at.isoformat(),
            'updated_at': instance.released_at.isoformat(),
            'author': UserSerializer(instance.user, request=self.request).serialize(),
        }

    @staticmethod
    def get_fields_dict():
        return {
            'id': serializers.IntegerField(),
            'status': serializers.CharField(),
            'edition': GameSerializer.get_fields_dict(),
            'description': serializers.CharField(),
            'hours_played': serializers.FloatField(),
            'created_at': serializers.DateTimeField(),
            'updated_at': serializers.DateTimeField(),
            'author': UserSerializer.get_fields_dict(),
        }
