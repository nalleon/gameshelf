from shared.serializers import BaseSerializer
from classifications.serializers import PlatformSerializer, GenreSerializer, DeveloperSerializer, PublisherSerializer, EditionSerializer, RegionSerializer
from users.serializers import UserSerializer
from rest_framework import serializers

class GameSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'title': instance.title,
            'slug': instance.slug,
            'description': instance.description,
            'cover': self.build_url(instance.cover.url),
            'released_at': instance.released_at.isoformat(), #TODO: isoformat hace falta?
            'platforms': PlatformSerializer(
                instance.platforms.all(), request=self.request
            ).serialize(),
            'genres': GenreSerializer(
                instance.genres.all(), request=self.request
            ).serialize(),
            'developers': DeveloperSerializer(
                instance.developers.all(), request=self.request
            ).serialize(),
            'publishers': PublisherSerializer(
                instance.publishers.all(), request=self.request
            ).serialize(),
            'edition': EditionSerializer(instance.edition, request=self.request).serialize(),
            'region': RegionSerializer(instance.region, request=self.request).serialize(),
        }
        
    @classmethod
    def get_schema(cls):
        return { 
            'id': serializers.IntegerField(),
            'title': serializers.CharField(),
            'slug': serializers.CharField(),
            'description': serializers.CharField(),
            'cover': serializers.URLField(),
            'released_at': serializers.DateTimeField(),
            'platforms': PlatformSerializer.get_schema(many=True),
            'genres': GenreSerializer.get_schema(many=True),
            'developers': DeveloperSerializer.get_schema(many=True),
            'publishers': PublisherSerializer.get_schema(many=True),
            'edition': EditionSerializer.get_schema(),
            'region': RegionSerializer.get_schema(),
        }
        

class ReviewSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'content': instance.content,
            'recommend': instance.recommend,
            'game': GameSerializer(instance.game, request=self.request).serialize(),
            'author': UserSerializer(instance.user, request=self.request).serialize(),
            'created_at':  instance.released_at.isoformat(), #TODO: isoformat hace falta?
            'updated_at':  instance.released_at.isoformat(), #TODO: isoformat hace falta?
        }
        
    @classmethod
    def get_schema(cls):
        return {
            'id': serializers.IntegerField(),
            'content': serializers.CharField(),
            'recommend': serializers.BooleanField(),
            'game': GameSerializer.get_schema(),
            'author': UserSerializer.get_schema(),
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
        
    @classmethod
    def get_schema(cls):
        return {
            'id': serializers.IntegerField(),
            'image': serializers.URLField(),
            'review': ReviewSerializer.get_schema(),
        }

class FavoriteItemSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'game': GameSerializer(instance.game, request=self.request).serialize(),
            'user': UserSerializer(instance.user, request=self.request).serialize(),
        }
    
    @classmethod
    def get_schema(cls):
        return {
            'id': serializers.IntegerField(),
            'game': GameSerializer.get_schema(),
            'user': UserSerializer.get_schema(),
        }
