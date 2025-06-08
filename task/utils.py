import os
import random
from django.conf import settings
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response


class CoreUtils:


    @classmethod
    def serializer_save(cls, serializer_class: type, **kwargs):
        serializer = serializer_class(**kwargs)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return instance, serializer

    @classmethod
    def get_serialized_data(cls, serializer_class: type, instance, **kwargs):
        return serializer_class(instance, **kwargs).data if instance else None


    @classmethod
    def organize_create_update_data(cls, items):
        to_create = list()
        to_update = dict()

        items = [items] if not isinstance(items, (list, set)) else items
        for item in items:
            if 'id' in item:
                item_key = str(item['id'])
                to_update[item_key] = item
            else:
                to_create.append(item) if item else None

        return to_create, to_update

    @classmethod
    def update_existing_items(cls, instance_items, to_update, serializer_class: type, **kwargs):
        for instance_item in instance_items:
            item_key = str(instance_item.pk)
            if item_key in to_update:
                cls.serializer_save(
                    serializer_class,
                    instance=instance_item,
                    data=to_update[item_key],
                    **kwargs
                )

