from rest_framework import serializers
from type_one.records.models import Record

class RecordSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    time = serializers.DateTimeField(required=True)

    def create(self, validated_data):
        return Record.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.time = validated_data.get('time', instance.time)
        instance.save()
        return instance