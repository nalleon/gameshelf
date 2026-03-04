from shared.serializers import BaseSerializer
from rest_framework import serializers

class PlatformSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'name': instance.name,
            'description': instance.description,
        }

    @classmethod
    def get_schema(cls):
        return {
            'id': serializers.IntegerField(),
            'name': serializers.CharField(),
            'description': serializers.CharField(),
        }


class GenreSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'name': instance.name,
            'description': instance.description,
        }

    @classmethod
    def get_schema(cls):
        return {
            'id': serializers.IntegerField(),
            'name': serializers.CharField(),
            'description': serializers.CharField(),
        }


class DeveloperSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'name': instance.name,
            'description': instance.description,
        }

    @classmethod
    def get_schema(cls):
        return {
            'id': serializers.IntegerField(),
            'name': serializers.CharField(),
            'description': serializers.CharField(),
        }


class PublisherSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'name': instance.name,
            'description': instance.description,
        }

    @classmethod
    def get_schema(cls):
        return {
            'id': serializers.IntegerField(),
            'name': serializers.CharField(),
            'description': serializers.CharField(),
        }


class EditionSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'name': instance.name,
            'description': instance.description,
        }

    @classmethod
    def get_schema(cls):
        return {
            'id': serializers.IntegerField(),
            'name': serializers.CharField(),
            'description': serializers.CharField(),
        }


class RegionSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'name': instance.name,
            'description': instance.description,
            'acronym': instance.acronym,
            'icon': self.build_url(instance.icon.url),
        }

    @classmethod
    def get_schema(cls):
        return {
            'id': serializers.IntegerField(),
            'name': serializers.CharField(),
            'description': serializers.CharField(),
            'acronym': serializers.CharField(),
            'icon': serializers.URLField(),
        }