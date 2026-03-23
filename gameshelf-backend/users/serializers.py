from rest_framework import serializers

from shared.serializers import BaseSerializer


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
            'avatar': self.build_url(instance.cover.url),
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

# Schemas to create an user in Swagger
class LoginSchemaSerializer(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField()
    
class RegisterSchemaSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    
class ShowUsernameSchemaSerializer(serializers.Serializer):
    username = serializers.CharField()