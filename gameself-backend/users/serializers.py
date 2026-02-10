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