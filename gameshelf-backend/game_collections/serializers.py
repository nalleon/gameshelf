from rest_framework import serializers

from games.serializers import GameSerializer
from shared.serializers import BaseSerializer
from users.serializers import UserSerializer


class ItemSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'type': instance.get_type_display(),
            'game': GameSerializer(instance.game, request=self.request).serialize(),
            'author': UserSerializer(instance.author, request=self.request).serialize(),
            'created_at': instance.released_at.isoformat(),
        }

    @staticmethod
    def get_fields_dict():
        return {
            'id': serializers.IntegerField(),
            'type': serializers.CharField(),
            'game': GameSerializer.get_fields_dict(),
            'author': UserSerializer.get_fields_dict(),
            'created_at': serializers.DateTimeField(),
        }


class CollectionItemSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'game': GameSerializer(instance.game, request=self.request).serialize(),
            'author': UserSerializer(instance.author, request=self.request).serialize(),
        }

    @staticmethod
    def get_fields_dict():
        return {
            'id': serializers.IntegerField(),
            'game': GameSerializer.get_fields_dict(),
            'author': UserSerializer.get_fields_dict(),
        }


class WishlistItemSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'priority': instance.priority,
            'annotation': instance.annotation,
            'game': GameSerializer(instance.game, request=self.request).serialize(),
            'author': UserSerializer(instance.author, request=self.request).serialize(),
        }

    @staticmethod
    def get_fields_dict():
        return {
            'id': serializers.IntegerField(),
            'priority': serializers.IntegerField(),
            'annotation': serializers.CharField(allow_null=True),
            'game': GameSerializer.get_fields_dict(),
            'author': UserSerializer.get_fields_dict(),
        }
        
class ClassificationSchemaSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    slug = serializers.SlugField()
    description = serializers.CharField()
