from shared.serializers import BaseSerializer
from games.serializers import GameSerializer
from users.serializers import UserSerializer
from rest_framework import serializers


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

    @classmethod
    def get_schema(cls):
        return {
            'id': serializers.IntegerField(),
            'status': serializers.CharField(),
            'edition': GameSerializer.get_schema(),
            'description': serializers.CharField(),
            'hours_played': serializers.FloatField(),
            'created_at': serializers.DateTimeField(),
            'updated_at': serializers.DateTimeField(),
            'author': UserSerializer.get_schema(),
        }