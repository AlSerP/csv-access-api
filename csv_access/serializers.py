from rest_framework import serializers

from .models import Dataset


class DatasetListSerializer(serializers.ModelSerializer):
    """Dataset list serializer"""

    class Meta:
        model = Dataset
        fields = ("id", "rows", "file")


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
        dataset.update_rows()
        return dataset

    class Meta:
        model = Dataset
        fields = ("file", "rows", "columns")
        read_only_fields = ["rows", "columns"]
