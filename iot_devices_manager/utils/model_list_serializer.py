from rest_framework import serializers


class ModelListSerializer(serializers.ListSerializer):

    def update(self, instance, validated_data, **kwargs):
        model_mapping = {model.id: model for model in instance}

        invalid_id = -1
        data_mapping = {}
        for item in validated_data:
            if item.get('id'):
                data_mapping[item.get('id')] = item
            else:
                data_mapping[invalid_id] = item
                invalid_id -= 1

        # Perform creations and updates.
        ret = []
        for model_id, data in data_mapping.items():
            model = model_mapping.get(model_id, None)
            if model is None:
                ret.append(self.child.create(data, **kwargs))
            else:
                ret.append(self.child.update(model, data))

        # Perform deletions.
        for model_id, model in model_mapping.items():
            if model_id not in data_mapping:
                model.delete()

        return ret
