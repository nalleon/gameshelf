from shared.serializers import BaseSerializer


class PlatformSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'name': instance.name,
            'description': instance.description,
        }
        
class GenreSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'name': instance.name,
            'description': instance.description,
        }
        
class DeveloperSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'name': instance.name,
            'description': instance.description,
        }
        
class PublisherSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'name': instance.name,
            'description': instance.description,
        }
        
class EditionSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'name': instance.name,
            'description': instance.description,
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