from rest_framework import serializers

from games.serializers import GameSchemaSerializer, GameSerializer
from shared.serializers import BaseSerializer, ShowUsernameSerializer
from users.serializers import ShowUsernameSchemaSerializer


class CollectionItemSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'game': GameSerializer(instance.game, request=self.request).serialize(),
            'collection_id': instance.collection.pk,
        }

class CollectionSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'name': instance.name,
            'user': ShowUsernameSerializer(instance.user, request=self.request).serialize(),
            'items': CollectionItemSerializer(
                instance.items.all(), request=self.request
            ).serialize(),
        }

class WishlistItemSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'priority': instance.priority,
            'annotation': instance.annotation,
            'game': GameSerializer(instance.game, request=self.request).serialize(),
            'wishlist_id': instance.wishlist.pk,
        }

    @staticmethod
    def get_fields_dict():
        return {
            'id': serializers.IntegerField(),
            'priority': serializers.IntegerField(),
            'annotation': serializers.CharField(allow_null=True),
            'game': GameSerializer.get_fields_dict(),
            'wishlist_id': serializers.IntegerField(),
        }


class WishlistSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'name': instance.name,
            'user': ShowUsernameSerializer(instance.user, request=self.request).serialize(),
            'items': WishlistItemSerializer(instance.items.all(), request=self.request).serialize(),
        }

    @staticmethod
    def get_fields_dict():
        return {
            'id': serializers.IntegerField(),
            'name': serializers.CharField(),
            'user': ShowUsernameSerializer.get_fields_dict(),
            'items': WishlistItemSerializer.get_fields_dict(),
        }

# Schemas to view class objects in Swagger


###################################
# Collection Items Schema
###################################
class CollectionItemSchemaSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    game = GameSchemaSerializer()
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
    game_id = serializers.IntegerField()
    is_private = serializers.BooleanField(default=False)

class CreateWishlistItemSchemaSerializer(serializers.Serializer):
    game_id = serializers.IntegerField()
    priority = serializers.IntegerField(required=False)
    annotation = serializers.CharField(required=False, allow_null=True)
    is_private = serializers.BooleanField(default=False)


class UpdateWishlistItemSchemaSerializer(serializers.Serializer):
    priority = serializers.IntegerField(required=False)
    annotation = serializers.CharField(required=False, allow_null=True)
    is_private = serializers.BooleanField(default=False)
