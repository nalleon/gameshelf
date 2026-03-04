from shared.serializers import BaseSerializer
from games.serializers import GameSerializer
from users.serializers import UserSerializer
from rest_framework import serializers


class ItemSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'type': instance.get_type_display(),
            'game': GameSerializer(instance.game, request=self.request).serialize(),
            'author': UserSerializer(instance.author, request=self.request).serialize(),
            'created_at': instance.released_at.isoformat(),
        }

    @classmethod
    def get_schema(cls):
        return {
            'id': serializers.IntegerField(),
            'type': serializers.CharField(),
            'game': GameSerializer.get_schema(),
            'author': UserSerializer.get_schema(),
            'created_at': serializers.DateTimeField(),
        }


class CollectionItemSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'game': GameSerializer(instance.game, request=self.request).serialize(),
            'author': UserSerializer(instance.author, request=self.request).serialize(),
        }

    @classmethod
    def get_schema(cls):
        return {
            'id': serializers.IntegerField(),
            'game': GameSerializer.get_schema(),
            'author': UserSerializer.get_schema(),
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

    @classmethod
    def get_schema(cls):
        return {
            'id': serializers.IntegerField(),
            'priority': serializers.IntegerField(),
            'annotation': serializers.CharField(allow_null=True),
            'game': GameSerializer.get_schema(),
            'author': UserSerializer.get_schema(),
        }