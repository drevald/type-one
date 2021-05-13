from type_one.core.models import GlucoseUnit, Insulin, User
from rest_framework import serializers
from type_one.records.models import Record, Photo

class PhotoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    thumb = serializers.StringRelatedField()

    def create(self, validated_data):
        return Photo.objects.created(**validated_data)

    def update(self, instance, validated_data):
        instance.data = validated_data.get('thumb', instance.thumb)

class PhotoFullSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    data = serializers.StringRelatedField()

    def create(self, validated_data):
        return Photo.objects.created(**validated_data)

    def update(self, instance, validated_data):
        instance.data = validated_data.get('data', instance.data)        

class GlucoseUnitSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.StringRelatedField()
    ratio_to_mmol_l = serializers.FloatField()

    def create(self, validated_data):
        return GlucoseUnit.objects.created(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.ratio_to_mmol_l = validated_data.get('ratio_to_mmol_l', instance.ratio_to_mmol_l)

class InsulinSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.StringRelatedField()   

    def create(self, validated_data):
        return Insulin.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance

class UserSerializer(serializers.Serializer):
    glucose_level_unit = GlucoseUnitSerializer()
    long_acting_insulin = InsulinSerializer()
    rapid_acting_insulin = InsulinSerializer()

    def create(self, validated_data):
        return Photo.objects.created(**validated_data)

    def update(self, instance, validated_data):
        instance.data = validated_data.get('thumb', instance.thumb)

class RecordSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    time = serializers.DateTimeField(required=True, format='%B %d %H:%M')
    bread_units = serializers.FloatField()
    glucose_level = serializers.FloatField(required=True)
    insulin = InsulinSerializer(many=False, required=True)
    insulin_amount = serializers.IntegerField()
    notes = serializers.StringRelatedField()
    glucose_level_unit = GlucoseUnitSerializer(required=True)
    photos = PhotoSerializer(many=True, read_only=True)
    user = UserSerializer()

    def create(self, validated_data):

        insulin_data = validated_data.pop('insulin', None)
        if insulin_data:
            insulin = Insulin.objects.get_or_create(**insulin_data)[0]
            validated_data['insulin'] = insulin

        glucose_level_unit_data = validated_data.pop('glucose_level_unit', None)
        if glucose_level_unit_data:
            glucose_level_unit = GlucoseUnit.objects.get_or_create(**glucose_level_unit_data)[0]
            validated_data['glucose_level_unit'] = glucose_level_unit
        
        user_data = validated_data.pop('user', None)
        if user_data:
            user=User.objects.get_or_create(**user_data)[0]
            validated_data['user'] = user

        return Record.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.time = validated_data.get('time', instance.time)
        instance.save()
        return instance

class RecordFullSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    time = serializers.DateTimeField(required=True, format='%B %d %H:%M')
    bread_units = serializers.FloatField()
    glucose_level = serializers.FloatField(required=True)
    insulin = InsulinSerializer(many=False, required=True)
    insulin_amount = serializers.IntegerField()
    notes = serializers.StringRelatedField()
    glucose_level_unit = GlucoseUnitSerializer(required=True)
    photos = PhotoFullSerializer(many=True, read_only=True)

    def create(self, validated_data):
        return Record.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.time = validated_data.get('time', instance.time)
        instance.save()
        return instance