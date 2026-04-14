from rest_framework import serializers

from shared.serializers import BaseSerializer
from classifications.serializers import (
    EditionSerializer,
    PlatformSerializer,
    RegionSerializer,
)

class UserSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'username': instance.username,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'email': instance.email,
        }

    @staticmethod
    def get_fields_dict():
        return {
            'id': serializers.IntegerField(),
            'username': serializers.CharField(),
            'first_name': serializers.CharField(),
            'last_name': serializers.CharField(),
            'email': serializers.EmailField(),
        }


class ProfileSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'user': UserSerializer(instance.user, request=self.request).serialize(),
            'avatar': self.build_url(instance.avatar.url),
            'bio': instance.bio,
            'verified': instance.verified,
            'role': instance.get_role_display(),
        }

    @staticmethod
    def get_fields_dict():
        return {
            'id': serializers.IntegerField(),
            'user': UserSerializer.get_fields_dict(),
            'avatar': serializers.URLField(),
            'bio': serializers.CharField(),
            'verified': serializers.BooleanField(),
            'role': serializers.CharField(),
        }
        
class LoggedUserSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'username': instance.username,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'email': instance.email,
            'collections': LoggedCollectionSerializer(instance.collections, request=self.request)
        }

    @staticmethod
    def get_fields_dict():
        return {
            'id': serializers.IntegerField(),
            'username': serializers.CharField(),
            'first_name': serializers.CharField(),
            'last_name': serializers.CharField(),
            'email': serializers.EmailField(),
        }

class LoggedProfileSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'user': LoggedUserSerializer(instance.user, request=self.request).serialize(),
            'avatar': self.build_url(instance.avatar.url),
            'bio': instance.bio,
            'verified': instance.verified,
            'role': instance.get_role_display(),
        }

    @staticmethod
    def get_fields_dict():
        return {
            'id': serializers.IntegerField(),
            'user': UserSerializer.get_fields_dict(),
            'avatar': serializers.URLField(),
            'bio': serializers.CharField(),
            'verified': serializers.BooleanField(),
            'role': serializers.CharField(),
        }

class LoggedCollectionSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'name': instance.name,
            'items': LoggedCollectionItemSerializer(
                instance.items.all(), request=self.request
            ).serialize(),
        }

    @staticmethod
    def get_fields_dict():
        return {
            'id': serializers.IntegerField(),
            'name': serializers.CharField(),
            'items': LoggedCollectionItemSerializer.get_fields_dict(),
        }

class LoggedCollectionItemSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'game': LoggedGameSerializer(instance.game, request=self.request).serialize(),
        }

    @staticmethod
    def get_fields_dict():
        return {
            'id': serializers.IntegerField(),
            'game': LoggedGameSerializer.get_fields_dict(),
        }

class LoggedGameSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'title': instance.title,
            'slug': instance.slug,
            'description': instance.description,
            'cover_default': self.build_url(instance.cover_default.url),
            'released_at': instance.released_at.isoformat(),
            'platforms': PlatformSerializer(
                instance.platforms.all(), request=self.request
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
            'released_at': serializers.DateTimeField(),
            'platforms': PlatformSerializer.get_fields_dict(),
            'edition': EditionSerializer.get_fields_dict(),
            'region': RegionSerializer.get_fields_dict(),
        }

# Schemas to create an user in Swagger
class LoginSchemaSerializer(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField()
    
class RegisterSchemaSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField()
    
class ShowUsernameSchemaSerializer(serializers.Serializer):
    username = serializers.CharField()
    
class TokenResponseSerializer(serializers.Serializer):
    token = serializers.CharField()



class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    
class EmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()