from rest_framework import serializers

from shared.serializers import BaseSerializer


class PlatformSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'name': instance.name,
            'slug': instance.slug,
            'aliases': [a.slug for a in instance.slug_aliases.all()],
            'description': instance.description,
        }

    @staticmethod
    def get_fields_dict():
        return {
            'id': serializers.IntegerField(),
            'name': serializers.CharField(),
            'slug': serializers.SlugField(),
            'aliases': serializers.ListField(child=serializers.SlugField()),
            'description': serializers.CharField(),
        }


class GenreSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'name': instance.name,
            'slug': instance.slug,
            'description': instance.description,
        }

    @staticmethod
    def get_fields_dict():
        return {
            'id': serializers.IntegerField(),
            'name': serializers.CharField(),
            'slug': serializers.SlugField(),
            'description': serializers.CharField(),
        }


class DeveloperSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'name': instance.name,
            'slug': instance.slug,
            'description': instance.description,
        }

    @staticmethod
    def get_fields_dict():
        return {
            'id': serializers.IntegerField(),
            'name': serializers.CharField(),
            'slug': serializers.SlugField(),
            'description': serializers.CharField(),
        }


class PublisherSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'name': instance.name,
            'slug': instance.slug,
            'description': instance.description,
        }

    @staticmethod
    def get_fields_dict():
        return {
            'id': serializers.IntegerField(),
            'name': serializers.CharField(),
            'slug': serializers.SlugField(),
            'description': serializers.CharField(),
        }


class EditionSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'name': instance.name,
            'slug': instance.slug,
            'description': instance.description,
        }

    @staticmethod
    def get_fields_dict():
        return {
            'id': serializers.IntegerField(),
            'name': serializers.CharField(),
            'slug': serializers.SlugField(),
            'description': serializers.CharField(),
        }


class RegionSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'name': instance.name,
            'slug': instance.slug,
            'description': instance.description,
            'acronym': instance.acronym,
            'icon': self.build_url(instance.icon.url),
        }

    @staticmethod
    def get_fields_dict():
        return {
            'id': serializers.IntegerField(),
            'name': serializers.CharField(),
            'slug': serializers.SlugField(),
            'description': serializers.CharField(),
            'acronym': serializers.CharField(),
            'icon': serializers.URLField(),
        }


class ClassificationSchemaSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    slug = serializers.SlugField()


class RegionSchemaSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    slug = serializers.SlugField()
    acronym = serializers.CharField()
    icon = serializers.URLField()


class PlatformSchemaSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    slug = serializers.SlugField()
    aliases = serializers.ListField(child=serializers.SlugField(), required=False)
    description = serializers.CharField()
