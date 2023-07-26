from rest_framework import serializers

from .models import Dataset


class DatasetListSerializer(serializers.ModelSerializer):
    """Dataset list serializer"""

    class Meta:
        model = Dataset
        fields = ("id", "columns")


class DatasetSerializer(serializers.ModelSerializer):
    """Adding a new dataset"""

    columns = serializers.SerializerMethodField()

    def get_columns(self, object):
        columns = None
        if object.columns:
            columns = object.columns.split(",")
        return columns

    def create(self, validated_data):
        dataset = Dataset.objects.create(**validated_data)  # saving dataset object
        dataset.update_columns()
        return dataset

    # def get_fields(self, *args, **kwargs):
    #     fields = super().get_fields(*args, **kwargs)
    #     columns = fields["columns"]
    #     print(fields)
    #     fields["columns"] = columns.split(",")
    #     return fields

    class Meta:
        model = Dataset
        fields = ("file", "columns")
        read_only_fields = ["columns"]
