"""Category serializers."""

from apps.sports.models import Category, Modality
from rest_framework import serializers


class ModalityModelSerializer(serializers.ModelSerializer):
    """Modality model serializer."""

    class Meta:
        model = Modality
        fields = [
            'id', 'name', 'slug'
        ]


class CategoryModelSerializer(serializers.ModelSerializer):
    """Category model serializer."""

    modality = ModalityModelSerializer(read_only=True)
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return obj.__str__()

    class Meta:
        model = Category
        fields = [
            'id', 'name',
            'full_name', 'slug',
            'modality', 'gender', 'type'
        ]
        read_only_fields = ['full_name', 'modality']
