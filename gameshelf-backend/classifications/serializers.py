from rest_framework import serializers

from shared.serializers import BaseSerializer


class PlatformSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'name': instance.name,
            'slug': instance.slug,
            'slug_aliases': PlatformSlugAliasSerializer(
                instance.slug_aliases.filter(deleted_at__isnull=True),
                request=self.request
            ).serialize(),
        }

    @staticmethod
    def get_fields_dict():
        return {
            'id': serializers.IntegerField(),
            'name': serializers.CharField(),
            'slug': serializers.SlugField(),
            'slug_aliases': PlatformSlugAliasSerializer.get_fields_dict(),
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
        }

    @staticmethod
    def get_fields_dict():
        return {
            'id': serializers.IntegerField(),
            'name': serializers.CharField(),
            'slug': serializers.SlugField(),
            'acronym': serializers.CharField(),
        }


class DeveloperSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'name': instance.name,
            'slug': instance.slug,
        }

    @staticmethod
    def get_fields_dict():
        return {
            'id': serializers.IntegerField(),
            'name': serializers.CharField(),
            'slug': serializers.SlugField(),
        }


class PublisherSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'name': instance.name,
            'slug': instance.slug,
        }

    @staticmethod
    def get_fields_dict():
        return {
            'id': serializers.IntegerField(),
            'name': serializers.CharField(),
            'slug': serializers.SlugField(),
        }


class EditionSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'name': instance.name,
            'slug': instance.slug,
            'description': instance.description
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
            'acronym': instance.acronym,
            # rating     
        }

    @staticmethod
    def get_fields_dict():
        return {
            'id': serializers.IntegerField(),
            'name': serializers.CharField(),
            'slug': serializers.SlugField(),
            'acronym': serializers.CharField(),
        }


# Schemas to view the items in Swagger
class ClassificationSchemaSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    slug = serializers.SlugField()


class EditionSchemaSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    slug = serializers.SlugField()
    description = serializers.CharField()



class GenreSchemaSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    slug = serializers.SlugField()
    acronym = serializers.CharField()


class RegionSchemaSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    slug = serializers.SlugField()
    acronym = serializers.CharField()


class PlatformSchemaSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    slug = serializers.SlugField()
    aliases = serializers.ListField(child=serializers.SlugField(), required=False)
    


# Schemas to save class objects in Swagger
class SaveClassificationSchemaSerializer(serializers.Serializer):
    name = serializers.CharField()
    
class SaveEditionSchemaSerializer(serializers.Serializer):
    name = serializers.CharField()  
    descrption = serializers.CharField()

class SaveGenreSchemaSerializer(serializers.Serializer):
    name = serializers.CharField()
    acronym = serializers.CharField()


class SaveRegionSchemaSerializer(serializers.Serializer):
    name = serializers.CharField()
    acronym = serializers.CharField()

class SavePlatformSchemaSerializer(serializers.Serializer):
    name = serializers.CharField()
    aliases = serializers.ListField(child=serializers.SlugField(), required=False)
    
