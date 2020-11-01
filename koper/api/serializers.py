from rest_framework import serializers
from .models import VertexModel, EdgeModel


class VertexSerializer(serializers.ModelSerializer):
    class Meta:
        model = VertexModel
        fields = '__all__'


class EdgeSerializer(serializers.ModelSerializer):

    class Meta:
        model = EdgeModel
        fields = '__all__'


class RouterQueryValidator(serializers.Serializer):
    map = serializers.CharField(required=True)
    source = serializers.CharField(required=True)
    dest = serializers.CharField(required=True)
    range = serializers.DecimalField(required=True, max_digits=10, decimal_places=2)
    price = serializers.DecimalField(required=True, max_digits=10, decimal_places=2)
