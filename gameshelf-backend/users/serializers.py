from rest_framework import serializers

from shared.serializers import BaseSerializer
from classifications.serializers import (
    EditionSerializer,
    PlatformSerializer,
    RegionSerializer,
    GenreSerializer
)

class UserSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        profile = getattr(instance, 'profile', None)

        return {
            'id': instance.pk,
            'username': instance.username,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'email': instance.email,
            'avatar': self.build_url(profile.avatar.url) if profile and profile.avatar else None,
        }

    @staticmethod
    def get_fields_dict():
        return {
            'id': serializers.IntegerField(),
            'username': serializers.CharField(),
            'first_name': serializers.CharField(),
            'last_name': serializers.CharField(),
            'email': serializers.EmailField(),
            'avatar': serializers.CharField(allow_null=True),
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
            'favorites': LoggedFavoriteItemSerializer(instance.favorites.all(), request=self.request).serialize(),
            'collections': LoggedCollectionSerializer(instance.collections.all(), request=self.request).serialize(),
            'library': LoggedLibrarySerializer(instance.library, request=self.request).serialize(),
            'wishlist': LoggedWishlistSerializer(instance.wishlist, request=self.request).serialize(),
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
            'user': LoggedUserSerializer(
                instance.user,
                request=self.request
            ).serialize(),
            'avatar': self.build_url(instance.avatar.url) if instance.avatar else None,
            'bio': instance.bio,
            'verified': instance.verified,
            'color_bg': instance.color_bg,
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
        
class LoggedFavoriteItemSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'game': LoggedGameSerializer(instance.game, request=self.request).serialize(),
        }

class LoggedCollectionSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'name': instance.name,
            'is_private': instance.is_private,
            'created_at': instance.created_at,
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
            'platform': PlatformSerializer(instance.platform, request=self.request).serialize(),
            'game': LoggedGameSerializer(instance.game, request=self.request).serialize(),
        }

    @staticmethod
    def get_fields_dict():
        return {
            'id': serializers.IntegerField(),
            'game': LoggedGameSerializer.get_fields_dict(),
        }
        
class LoggedLibrarySerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'is_private': instance.is_private,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at,
            'items': LoggedLibraryItemSerializer(instance.items.all(), request=self.request).serialize(),
        }

    @staticmethod
    def get_fields_dict():
        return {
            'id': serializers.IntegerField(),
            'is_private': serializers.BooleanField(),
            'created_at': serializers.DateTimeField(),
            'updated_at': serializers.DateTimeField(),
            'items': LoggedLibraryItemSerializer.get_fields_dict()
        }

class LoggedLibraryItemSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'game': LoggedGameSerializer(instance.game, request=self.request).serialize(),
            'platform': PlatformSerializer(instance.platform, request=self.request).serialize(),
            'status': instance.get_status_display(),
            'is_private': instance.is_private,
            'hours_played': instance.hours_played,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at,
        }

    @staticmethod
    def get_fields_dict():
        return {
            'id': serializers.IntegerField(),
            'game': LoggedGameSerializer.get_fields_dict(),
            'platform': PlatformSerializer.get_fields_dict(),
            'status': serializers.CharField(),
            'is_private': serializers.BooleanField(),
            'hours_played': serializers.CharField(),
            'created_at': serializers.DateTimeField(),
            'updated_at': serializers.DateTimeField(),
        }
        
class LoggedWishlistSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'name': instance.name,
            'is_private': instance.is_private,
            'created_at': instance.created_at,
            'items': LoggedWishlistItemSerializer(
                instance.items.all(), request=self.request
            ).serialize(),
        }

    @staticmethod
    def get_fields_dict():
        return {
            'id': serializers.IntegerField(),
            'name': serializers.CharField(),
            'is_private': serializers.BooleanField(),
            'created_at': serializers.DateTimeField(),
            'items': LoggedCollectionItemSerializer.get_fields_dict(),
        }

class LoggedWishlistItemSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'priroty': instance.priority,
            'annotation': instance.annotation,
            'is_private': instance.is_private,
            'game': LoggedGameSerializer(instance.game, request=self.request).serialize(),
        }

    @staticmethod
    def get_fields_dict():
        return {
            'id': serializers.IntegerField(),
            'priroty': serializers.IntegerField(),
            'annotation': serializers.CharField(),
            'is_private': serializers.BooleanField(),
            'game': LoggedGameSerializer.get_fields_dict(),
        }

class LoggedGameSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'title': instance.title,
            'slug': instance.slug,
            'description': instance.description,
            'cover_default': self.build_url(instance.cover_default),
            'cover_detail': self.build_url(instance.cover_detail),
            'released_at': instance.released_at.isoformat(),
            # 'platforms': PlatformSerializer(
            #     instance.platforms.all(), request=self.request
            # ).serialize(),
            # 'edition': EditionSerializer(instance.edition, request=self.request).serialize(),
            'region': RegionSerializer(instance.region, request=self.request).serialize(),
            'mature_content': instance.mature_content,
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
            # 'platforms': PlatformSerializer.get_fields_dict(),
            # 'edition': EditionSerializer.get_fields_dict(),
            'region': RegionSerializer.get_fields_dict(),
            'mature_content': serializers.BooleanField(),
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
    
class UpdateProfileSerializer(serializers.Serializer):
    bio = serializers.CharField(required=False)
    avatar = serializers.ImageField(required=False)
    username = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    color_bg = serializers.CharField(required=False)