from rest_framework import serializers

from shared.serializers import BaseSerializer


class PlatformSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'name': instance.name,
            'slug': instance.slug,
            'aliases': PlatformSlugAliasSerializer(
                instance.slug_aliases.filter(deleted_at__isnull=True),
                request=self.request
            ).serialize(),
            'description': instance.description,
        }

    @staticmethod
    def get_fields_dict():
        return {
            'id': serializers.IntegerField(),
            'name': serializers.CharField(),
            'slug': serializers.SlugField(),
            'aliases': PlatformSlugAliasSerializer.get_fields_dict(),
            'description': serializers.CharField(),
        }
        
class PlatformSlugAliasSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'slug': instance.slug,
        }

    @staticmethod
    def get_fields_dict():
        return {
            'id': serializers.IntegerField(),
            'slug': serializers.SlugField(),
        }
    


class GenreSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'name': instance.name,
            'slug': instance.slug,
            'acronym': instance.acronym,
            'description': instance.description,
        }

    @staticmethod
    def get_fields_dict():
        return {
            'id': serializers.IntegerField(),
            'name': serializers.CharField(),
            'slug': serializers.SlugField(),
            'acronym': serializers.CharField(),
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


# Schemas to view the items in Swagger
class ClassificationSchemaSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    slug = serializers.SlugField()
    description = serializers.CharField()


class GenreSchemaSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    slug = serializers.SlugField()
    acronym = serializers.CharField()
    description = serializers.CharField()


class RegionSchemaSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    slug = serializers.SlugField()
    acronym = serializers.CharField()
    icon = serializers.URLField()
    description = serializers.CharField()


class PlatformSchemaSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    slug = serializers.SlugField()
    aliases = serializers.ListField(child=serializers.SlugField(), required=False)
    description = serializers.CharField()
    


# Schemas to save class objects in Swagger
class SaveClassificationSchemaSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()

class SaveGenreSchemaSerializer(serializers.Serializer):
    name = serializers.CharField()
    acronym = serializers.CharField()
    description = serializers.CharField()


class SaveRegionSchemaSerializer(serializers.Serializer):
    name = serializers.CharField()
    acronym = serializers.CharField()
    icon = serializers.URLField()
    description = serializers.CharField()

class SavePlatformSchemaSerializer(serializers.Serializer):
    name = serializers.CharField()
    aliases = serializers.ListField(child=serializers.SlugField(), required=False)
    description = serializers.CharField()
    
