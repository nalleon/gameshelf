from rest_framework import serializers

from classifications.serializers import (
    DeveloperSerializer,
    EditionSerializer,
    GenreSerializer,
    PlatformSerializer,
    PublisherSerializer,
    RegionSerializer,
)
from shared.serializers import BaseSerializer
from users.serializers import UserSerializer


class GameSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'title': instance.title,
            'slug': instance.slug,
            'description': instance.description,
            'cover': self.build_url(instance.cover.url),
            'released_at': instance.released_at.isoformat(),
            'platforms': PlatformSerializer(
                instance.platforms.all(), request=self.request
            ).serialize(),
            'genres': GenreSerializer(instance.genres.all(), request=self.request).serialize(),
            'developers': DeveloperSerializer(
                instance.developers.all(), request=self.request
            ).serialize(),
            'publishers': PublisherSerializer(
                instance.publishers.all(), request=self.request
            ).serialize(),
            'edition': EditionSerializer(instance.edition, request=self.request).serialize(),
            'region': RegionSerializer(instance.region, request=self.request).serialize(),
        }

    @staticmethod
    def get_fields_dict():
        return {
            'id': serializers.IntegerField(),
            'title': serializers.CharField(),
            'slug': serializers.SlugField(),
            'description': serializers.CharField(),
            'cover': serializers.URLField(),
            'released_at': serializers.DateTimeField(),
            'platforms': PlatformSerializer.get_fields_dict(),
            'genres': GenreSerializer.get_fields_dict(),
            'developers': DeveloperSerializer.get_fields_dict(),
            'publishers': PublisherSerializer.get_fields_dict(),
            'edition': EditionSerializer.get_fields_dict(),
            'region': RegionSerializer.get_fields_dict(),
        }


class ReviewSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'content': instance.content,
            'recommend': instance.recommend,
            'game': GameSerializer(instance.game, request=self.request).serialize(),
            'author': UserSerializer(instance.user, request=self.request).serialize(),
            'created_at': instance.released_at.isoformat(),
            'updated_at': instance.released_at.isoformat(),
        }

    @staticmethod
    def get_fields_dict():
        return {
            'id': serializers.IntegerField(),
            'content': serializers.CharField(),
            'recommend': serializers.BooleanField(),
            'game': GameSerializer.get_fields_dict(),
            'author': UserSerializer.get_fields_dict(),
            'created_at': serializers.DateTimeField(),
            'updated_at': serializers.DateTimeField(),
        }


class MediaSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'image': self.build_url(instance.cover.url),
            'review': ReviewSerializer(instance.review, request=self.request).serialize(),
        }

    @staticmethod
    def get_fields_dict():
        return {
            'id': serializers.IntegerField(),
            'image': serializers.URLField(),
            'review': ReviewSerializer.get_fields_dict(),
        }


class FavoriteItemSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'game': GameSerializer(instance.game, request=self.request).serialize(),
            'user': UserSerializer(instance.user, request=self.request).serialize(),
        }

    @staticmethod
    def get_fields_dict():
        return {
            'id': serializers.IntegerField(),
            'game': GameSerializer.get_fields_dict(),
            'user': UserSerializer.get_fields_dict(),
        }


# Serializers for documentation via Swagger

class GameSchemaSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    slug = serializers.SlugField()
    description = serializers.CharField()
    cover = serializers.URLField()
    released_at = serializers.DateTimeField()
    pk_platforms_list = serializers.ListField(child=serializers.IntegerField())
    pk_genres_list = serializers.ListField(child=serializers.IntegerField())
    pk_developers_list = serializers.ListField(child=serializers.IntegerField())
    pk_publishers_list = serializers.ListField(child=serializers.IntegerField())
    pk_edition = serializers.IntegerField()
    pk_region = serializers.IntegerField()


class ReviewSchemaSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    content = serializers.CharField()
    recommend = serializers.BooleanField()
    game = id = serializers.IntegerField()
    author = serializers.DictField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class MediaSchemaSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    image = serializers.URLField()
    review = ReviewSchemaSerializer()


class FavoriteSchemaSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    game = id = serializers.IntegerField()
    user = serializers.DictField()


class IGBDRequestGameSchema(serializers.Serializer):
    quantity = serializers.IntegerField()
    
# Schemas to save class objects in Swagger
class SaveGameSchemaSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    cover = serializers.URLField()
    released_at = serializers.DateTimeField()
    pk_platforms_list = serializers.ListField(child=serializers.IntegerField())
    pk_genres_list = serializers.ListField(child=serializers.IntegerField())
    pk_developers_list = serializers.ListField(child=serializers.IntegerField())
    pk_publishers_list = serializers.ListField(child=serializers.IntegerField())
    pk_edition = serializers.IntegerField()
    pk_region = serializers.IntegerField()


class SaveReviewSchemaSerializer(serializers.Serializer):
    content = serializers.CharField()
    recommend = serializers.BooleanField()
    game = id = serializers.IntegerField()
    author = serializers.DictField()
    updated_at = serializers.DateTimeField()


class SaveMediaSchemaSerializer(serializers.Serializer):
    image = serializers.URLField()
    review = ReviewSchemaSerializer()


class SaveFavoriteSchemaSerializer(serializers.Serializer):
    game = id = serializers.IntegerField()
    user = serializers.DictField()
