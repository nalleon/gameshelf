import json
from abc import ABC
from typing import Iterable

from django.http import HttpRequest, JsonResponse
from drf_spectacular.utils import inline_serializer
from rest_framework import serializers


class BaseSerializer(ABC):
    def __init__(
        self,
        to_serialize: object | Iterable[object],
        *,
        fields: Iterable[str] = [],
        request: HttpRequest = None,
    ):
        self.to_serialize = to_serialize
        self.fields = fields
        self.request = request

    def build_url(self, path: str) -> str:
        return self.request.build_absolute_uri(path) if self.request else path

    # To be implemented by subclasses
    def serialize_instance(self, instance: object) -> dict:
        raise NotImplementedError

    def __serialize_instance(self, instance: object) -> dict:
        serialized = self.serialize_instance(instance)
        return {f: v for f, v in serialized.items() if not self.fields or f in self.fields}

    def serialize(self) -> dict | list[dict]:
        if not isinstance(self.to_serialize, Iterable):
            return self.__serialize_instance(self.to_serialize)
        return [self.__serialize_instance(instance) for instance in self.to_serialize]

    def to_json(self) -> str:
        return json.dumps(self.serialize())

    def json_response(self) -> JsonResponse:
        return JsonResponse(self.serialize(), safe=False)

    def serialize_paginated(self, pagination_data: dict) -> dict:
        return {
            'results': self.__class__(
                pagination_data['results'], request=self.request, fields=self.fields
            ).serialize(),
            'count': pagination_data['count'],
            'total_pages': pagination_data['total_pages'],
            'current_page': pagination_data['current_page'],
            'has_next': pagination_data['has_next'],
            'has_previous': pagination_data['has_previous'],
        }

    @classmethod
    def get_schema(cls, name: str = None, many=False):
        if many:
            return inline_serializer(
                name=f'{name or cls.__name__}List',
                fields={'results': cls.get_fields_schema(many=True)},
            )
        return inline_serializer(name=name or cls.__name__, fields=cls.get_fields_schema())

    @classmethod
    def get_fields_dict(cls) -> dict:
        raise NotImplementedError

    @classmethod
    def get_fields_schema(cls, many=False) -> dict | serializers.ListSerializer:
        fields = cls.get_fields_dict()
        if many:
            return serializers.ListSerializer(
                child=inline_serializer(name=f'{cls.__name__}Item', fields=fields)
            )
        return fields

    @classmethod
    def get_paginated_schema(cls, name: str = None):
        return inline_serializer(
            name=f'Paginated{name or cls.__name__}',
            fields={
                'results': cls.get_fields_schema(many=True),
                'total_pages': serializers.IntegerField(),
                'count': serializers.IntegerField(),
                'has_next': serializers.BooleanField(),
                'has_previous': serializers.BooleanField(),
                'current_page': serializers.IntegerField(),
            },
        )


class ShowUsernameSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'username': instance.username,
        }

    @staticmethod
    def get_fields_dict():
        return {
            'username': serializers.CharField(),
        }


class MessageResponseSerializer(serializers.Serializer):
    message = serializers.CharField()


class ErrorResponseSerializer(serializers.Serializer):
    error = serializers.CharField()
