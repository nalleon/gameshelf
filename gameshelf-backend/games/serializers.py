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
            'cover_default': instance.cover_default,
            'cover_detail': instance.cover_detail,
            'released_at': instance.released_at.isoformat(),
            'age_rating': instance.age_rating,
            'mature_content': instance.mature_content,
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
            'cover_default': serializers.URLField(),
            'cover_detail': serializers.URLField(),
            'released_at': serializers.DateField(),
            'age_rating': serializers.CharField(allow_null=True, required=False),
            'mature_content': serializers.BooleanField(),
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
            'author': UserSerializer(instance.author, request=self.request).serialize(),
            'media': [
                MediaSerializer(m, request=self.request).serialize()
                for m in instance.media_items.all()
            ],
            'created_at': instance.created_at.isoformat(),
            'updated_at': instance.updated_at.isoformat(),
        }

    @staticmethod
    def get_fields_dict():
        return {
            'id': serializers.IntegerField(),
            'content': serializers.CharField(),
            'recommend': serializers.BooleanField(),
            'game': GameSerializer.get_fields_dict(),
            'author': UserSerializer.get_fields_dict(),
            'media': MediaSerializer.get_fields_dict(many=True),
            'created_at': serializers.DateTimeField(),
            'updated_at': serializers.DateTimeField(),
        }


class MediaSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'image': (
                self.build_url(instance.image.url)
                if instance.image and hasattr(instance.image, 'url')
                else None
            ),
        }

    @staticmethod
    def get_fields_dict():
        return {
            'id': serializers.IntegerField(),
            'image': serializers.URLField(allow_null=True),
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
    cover_default = serializers.URLField()
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


# IGDB schemas for swagger
class IGBDRequestGameSchema(serializers.Serializer):
    quantity = serializers.IntegerField()


class IGBDRequestGameTitleSchema(serializers.Serializer):
    title = serializers.CharField()


# Schemas to save class objects in Swagger
class SaveGameSchemaSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    cover_default = serializers.URLField()
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
    game_id = serializers.IntegerField()


class SaveFavoriteSchemaSerializer(serializers.Serializer):
    game = id = serializers.IntegerField()
    user = serializers.DictField()


class UpdateFavoriteSchemaSerializer(serializers.Serializer):
    order = serializers.IntegerField(default=1)


class ReviewMediaUploadSerializer(serializers.Serializer):
    images = serializers.ListField(child=serializers.ImageField(), allow_empty=False)
