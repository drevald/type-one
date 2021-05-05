from rest_framework import serializers
from type_one.records.models import Record

    # user = models.ForeignKey(User, on_delete = models.CASCADE)
    # time = models.DateTimeField(auto_now_add=True)
    # type = models.IntegerField(default=0)
    # glucose_level = models.FloatField(null = True, default = 0)
    # glucose_level_unit = models.ForeignKey(GlucoseUnit, on_delete = models.SET_NULL, null = True)
    # insulin_amount = models.IntegerField(null = True, default = 0)
    # insulin = models.ForeignKey(Insulin, on_delete = models.SET_NULL, null = True)
    # bread_units = models.FloatField(null = True, default = 0)
    # notes = models.CharField(max_length = 256, null = True)

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

class RecordSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    time = serializers.DateTimeField(required=True, format="%d-%m-%Y")
    bread_units = serializers.FloatField()
    glucose_level = serializers.FloatField()
    insulin = InsulinSerializer()
    notes = serializers.StringRelatedField()
    glucose_level_unit = GlucoseUnitSerializer()

    def create(self, validated_data):
        return Record.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.time = validated_data.get('time', instance.time)
        instance.save()
        return instance