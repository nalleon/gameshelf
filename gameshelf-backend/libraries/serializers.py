from rest_framework import serializers

from classifications.serializers import PlatformSerializer
from games.serializers import GameSerializer
from shared.serializers import BaseSerializer, ShowUsernameSerializer


class LibraryItemSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'status': instance.get_status_display(),
            'game': GameSerializer(instance.game, request=self.request).serialize(),
            'platform': PlatformSerializer(instance.platform, request=self.request).serialize(),
            'hours_played': instance.hours_played,
            'is_private': instance.is_private,
            'created_at': instance.created_at.isoformat(),
            'updated_at': instance.updated_at.isoformat(),
            'library_id': instance.library.pk,
        }

    @staticmethod
    def get_fields_dict():
        return {
            'id': serializers.IntegerField(),
            'status': serializers.CharField(),
            'game': GameSerializer.get_fields_dict(),
            'platform': PlatformSerializer.get_fields_dict(),
            'hours_played': serializers.FloatField(),
            'is_private': serializers.BooleanField(),
            'created_at': serializers.DateTimeField(),
            'updated_at': serializers.DateTimeField(),
            'library_id': serializers.IntegerField(),
        }


class LibrarySerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'user': ShowUsernameSerializer(instance.user, request=self.request).serialize(),
            'is_private': instance.is_private,
            'total_all': getattr(instance, 'total_all', 0),
            'total_public': getattr(instance, 'total_public', 0),
            'total_private': getattr(instance, 'total_private', 0),
            'items': LibraryItemSerializer(instance.items.all(), request=self.request).serialize(),
        }


class AddLibraryItemSchemaSerializer(serializers.Serializer):
    game_id = serializers.IntegerField(required=True)
    platform_id = serializers.IntegerField(required=True)
    status = serializers.CharField(required=True)
    hours_played = serializers.FloatField(required=False)
    is_private = serializers.BooleanField(required=False)

class UpdateLibraryItemSchemaSerializer(serializers.Serializer):
    platform_id = serializers.IntegerField(required=False)
    status = serializers.CharField(required=False)
    hours_played = serializers.FloatField(required=False)
    is_private = serializers.BooleanField(required=False)


class LibrarySchemaSerializer(serializers.Serializer):
    is_private = serializers.BooleanField()
