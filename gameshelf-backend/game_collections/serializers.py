from rest_framework import serializers

from classifications.serializers import PlatformSerializer
from games.serializers import GameSchemaSerializer, GameSerializer
from shared.serializers import BaseSerializer, ShowUsernameSerializer
from users.serializers import ShowUsernameSchemaSerializer

from .models import Item


class CollectionItemSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'game': GameSerializer(instance.game, request=self.request).serialize(),
            'platform': PlatformSerializer(instance.platform, request=self.request).serialize(),
            'type': instance.type,
            'is_private': instance.is_private,
            'collection_id': instance.collection.pk,
        }

    @staticmethod
    def get_fields_dict():
        return {
            'id': serializers.IntegerField(),
            'game': GameSerializer.get_fields_dict(),
            'platform': PlatformSerializer.get_fields_dict(),
            'type': serializers.ChoiceField(choices=['P', 'D']),
            'is_private': serializers.BooleanField(),
            'collection_id': serializers.IntegerField(),
        }


class CollectionSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'name': instance.name,
            'user': ShowUsernameSerializer(instance.user, request=self.request).serialize(),
            'total_all': getattr(instance, 'total_all', 0),
            'total_public': getattr(instance, 'total_public', 0),
            'total_private': getattr(instance, 'total_private', 0),
            'items': CollectionItemSerializer(
                instance.items.all(), request=self.request
            ).serialize(),
        }

    @staticmethod
    def get_fields_dict():
        return {
            'id': serializers.IntegerField(),
            'name': serializers.CharField(),
            'user': ShowUsernameSerializer.get_fields_dict(),
            'total_all': serializers.IntegerField(),
            'total_public': serializers.IntegerField(),
            'total_private': serializers.IntegerField(),
            'items': CollectionItemSerializer.get_fields_dict(),
        }


class WishlistItemSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'priority': instance.priority,
            'annotation': instance.annotation,
            'game': GameSerializer(instance.game, request=self.request).serialize(),
            'platform': PlatformSerializer(instance.platform, request=self.request).serialize(),
            'type': instance.type,
            'wishlist_id': instance.wishlist.pk,
        }

    @staticmethod
    def get_fields_dict():
        return {
            'id': serializers.IntegerField(),
            'priority': serializers.IntegerField(),
            'annotation': serializers.CharField(allow_null=True),
            'game': GameSerializer.get_fields_dict(),
            'platform': PlatformSerializer.get_fields_dict(),
            'type': serializers.ChoiceField(choices=['P', 'D']),
            'wishlist_id': serializers.IntegerField(),
        }


class WishlistSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'name': instance.name,
            'is_private': instance.is_private,
            'user': ShowUsernameSerializer(instance.user, request=self.request).serialize(),
            'total_all': getattr(instance, 'total_all', 0),
            'total_public': getattr(instance, 'total_public', 0),
            'total_private': getattr(instance, 'total_private', 0),
            'items': WishlistItemSerializer(instance.items.all(), request=self.request).serialize(),
        }

    @staticmethod
    def get_fields_dict():
        return {
            'id': serializers.IntegerField(),
            'name': serializers.CharField(),
            'user': ShowUsernameSerializer.get_fields_dict(),
            'total_all': serializers.IntegerField(),
            'total_public': serializers.IntegerField(),
            'total_private': serializers.IntegerField(),
            'items': WishlistItemSerializer.get_fields_dict(),
        }


# Schemas to view class objects in Swagger


###################################
# Collection Items Schema
###################################
class CollectionItemSchemaSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    game = GameSchemaSerializer()
    platform_id = serializers.IntegerField(required=True)

    type = serializers.ChoiceField(choices=Item.Type.choices)
    is_private = serializers.BooleanField()
    collection_id = serializers.IntegerField()


###################################
# Collection Schema
###################################
class CollectionSchemaSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    user = ShowUsernameSchemaSerializer()
    items = CollectionItemSchemaSerializer(many=True)


###################################
# Wishlist Items Schema
###################################
class WishlistItemSchemaSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    priority = serializers.IntegerField()
    annotation = serializers.CharField(allow_null=True)
    game = GameSchemaSerializer()
    type = serializers.ChoiceField(choices=Item.Type.choices)
    wishlist_id = serializers.IntegerField()


###################################
# Wishlist Schema
###################################
class WishlistSchemaSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    user = ShowUsernameSchemaSerializer()
    items = WishlistItemSchemaSerializer(many=True)


###################################
# Schemas to save class objects in Swagger
###################################


class SaveListSchemaSerializer(serializers.Serializer):
    name = serializers.CharField()
    is_private = serializers.BooleanField(default=False)


class SaveCollectionItemSchemaSerializer(serializers.Serializer):
    game_id = serializers.IntegerField(required=True)
    platform_id = serializers.IntegerField(required=True)
    type = serializers.ChoiceField(choices=Item.Type.choices)
    is_private = serializers.BooleanField(default=False)


class CreateWishlistItemSchemaSerializer(serializers.Serializer):
    game_id = serializers.IntegerField()
    platform_id = serializers.IntegerField(required=True)
    priority = serializers.IntegerField(required=False)
    annotation = serializers.CharField(required=False, allow_null=True)
    type = serializers.ChoiceField(choices=Item.Type.choices)
    is_private = serializers.BooleanField(default=False)


class UpdateWishlistItemSchemaSerializer(serializers.Serializer):
    platform_id = serializers.IntegerField(required=False)
    priority = serializers.IntegerField(required=False)
    annotation = serializers.CharField(required=False, allow_null=True)
    type = serializers.ChoiceField(choices=Item.Type.choices)
    is_private = serializers.BooleanField(default=False)
