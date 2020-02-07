from __future__ import print_function, unicode_literals
import inspect

from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ListSerializer


class BulkSerializerMixin(object):
    def to_internal_value(self, data):
        ret = super(BulkSerializerMixin, self).to_internal_value(data)

        id_attr = getattr(self.Meta, "update_lookup_field", "id")
        request_method = getattr(
            getattr(self.context.get("view"), "request"), "method", ""
        )

        if (
            isinstance(self.root, BulkListSerializer)
            and id_attr
            and request_method in ("PUT", "PATCH")
        ):
            id_field = self.fields[id_attr]
            id_value = id_field.get_value(data)

            if isinstance(id_value, int):
                ret[id_attr] = id_value

        return ret


class BulkListSerializer(ListSerializer):
    update_lookup_field = "id"

    def update(self, queryset, all_validated_data):
        id_attr = getattr(self.child.Meta, "update_lookup_field", "id")

        all_validated_data_by_id = {}
        data_for_create = []

        for i in all_validated_data:
            if i.get(id_attr, None):
                all_validated_data_by_id[i.pop(id_attr)] = i
            else:
                data_for_create.append(i)

        if not all(
            (bool(i) and not inspect.isclass(i) for i in all_validated_data_by_id)
        ):
            raise ValidationError("")

        objects_to_update = queryset.filter(
            **{"{}__in".format(id_attr): all_validated_data_by_id.keys()}
        )

        if len(all_validated_data_by_id) != objects_to_update.count():
            raise ValidationError("Could not find all objects to update.")

        updated_objects = []

        for obj in objects_to_update:
            obj_id = getattr(obj, id_attr)
            obj_validated_data = all_validated_data_by_id.get(obj_id)

            updated_objects.append(self.child.update(obj, obj_validated_data))

        created_objects = []
        for i in data_for_create:
            created_objects.append(self.child.create(i))

        return updated_objects + created_objects
