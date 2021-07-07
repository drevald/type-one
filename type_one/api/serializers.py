import re
from type_one.core.models import GlucoseUnit, Insulin, User
from rest_framework import serializers
from type_one.records.models import Record, Photo, Meal
from type_one.ingredients.models import Ingredient, IngredientUnit, WeightUnit

class PhotoCreateSerializer(serializers.Serializer):
    data = serializers.StringRelatedField()
    def create(self, validated_data):
        return Photo.objects.create(**validated_data)
    def update(self, instance, validated_data):
        instance.data = validated_data.get('data', instance.data)

class PhotoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    thumb = serializers.StringRelatedField()
    data = serializers.StringRelatedField()

    def create(self, validated_data):
        return Photo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.thumb = validated_data.get('thumb', instance.thumb)
        instance.data = validated_data.get('data', instance.data)

class PhotoFullSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    data = serializers.StringRelatedField()

    def create(self, validated_data):
        return Photo.objects.create(**validated_data)

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

class RecordUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    type = serializers.IntegerField(read_only=True)
    time = serializers.DateTimeField(required=True)
    bread_units = serializers.FloatField(required=False, allow_null=True)
    glucose_level = serializers.FloatField(required=False, allow_null=True)
    insulin_amount = serializers.IntegerField(required=True)
    notes = serializers.CharField(required=False, allow_blank=True)

    def create(self, validated_data):
        return Record.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.type = validated_data.get('type', instance.type)
        instance.time = validated_data.get('time', instance.time)
        instance.insulin_amount = validated_data.get('insulin_amount')
        instance.glucose_level = validated_data.get('glucose_level')
        instance.bread_units = validated_data.get('bread_units')
        instance.notes = validated_data.get('notes')        
        instance.save()        
        return instance

class RecordFullSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    time = serializers.DateTimeField(required=True)
    bread_units = serializers.FloatField(required=False, allow_null=True)
    glucose_level = serializers.FloatField(required=False, allow_null=True)
    insulin = InsulinSerializer(many=False, required=True)
    insulin_amount = serializers.IntegerField(required=True)
    notes = serializers.CharField(required=False, allow_blank=True)
    glucose_level_unit = GlucoseUnitSerializer(required=False)
    photos = PhotoFullSerializer(many=True, read_only=True)

    def create(self, validated_data):
        return Record.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.time = validated_data.get('time', instance.time)
        instance.save()
        return instance

class RecordListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    time = serializers.DateTimeField(required=True)
    bread_units = serializers.FloatField(required=False, allow_null=True)
    glucose_level = serializers.FloatField(required=False, allow_null=True)
    insulin = InsulinSerializer(many=False, required=True)
    insulin_amount = serializers.IntegerField(required=True)
    notes = serializers.CharField(required=False, allow_blank=True)
    glucose_level_unit = GlucoseUnitSerializer(required=False, allow_null=True)
    photos = PhotoSerializer(many=True, read_only=True)
    type = serializers.IntegerField(required=True)

    def create(self, validated_data):      
        return Record.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.time = validated_data.get('time', instance.time)
        instance.save()
        return instance
        
class RecordCreateSerializer(serializers.Serializer):
    type = serializers.IntegerField(required=True)
    time = serializers.DateTimeField(required=True)
    bread_units = serializers.FloatField(required=False, allow_null=True)
    glucose_level = serializers.FloatField(required=False, allow_null=True)
    insulin_amount = serializers.IntegerField(required=True)
    notes = serializers.CharField(required=False, allow_blank=True)

    def create(self, validated_data):
        return Record.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.time = validated_data.get('time', instance.time)
        instance.save()
        return instance

# - record type id
# - insulin name
# - insulin units in shot
# - blood glucose level
# - blood glucose unit name
# - bread units amount
# - notes
# - meal photos in original size         
class RecordDetailsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    type = serializers.IntegerField(read_only=True)        
    time = serializers.DateTimeField(required=True)
    insulin = InsulinSerializer(many=False, required=True)
    insulin_amount = serializers.IntegerField(required=True)
    glucose_level = serializers.FloatField(required=False, allow_null=True)
    glucose_level_unit = GlucoseUnitSerializer(required=False, allow_null=True)
    bread_units = serializers.FloatField(required=False, allow_null=True)
    photos = PhotoFullSerializer(many=True, read_only=True)
    notes = serializers.CharField(required=False, allow_blank=True)

    def create(self, validated_data):
        return Record.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.time = validated_data.get('time', instance.time)
        instance.save()
        return instance

class WeightUnitSerializer(serializers.Serializer):
    name = serializers.CharField()
    
    def create(self, validated_data):
        return Ingredient.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance

class IngredientSeralizer(serializers.Serializer):
    name = serializers.CharField()
    bread_units_per_100g = serializers.FloatField()
    
    def create(self, validated_data):
        return Ingredient.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance

class IngredientUnitSerializer(serializers.Serializer):
    ingredient = IngredientSeralizer(required=True, allow_null=False)
    grams_in_unit = serializers.FloatField()
    unit = WeightUnitSerializer(required=True, allow_null=False)

    def create(self, validated_data):
        return IngredientUnit.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.ingredient = validated_data.get('ingredient', instance.ingredient)
        instance.save()
        return instance

class MealSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    ingredient_unit = IngredientUnitSerializer(required=True, allow_null=False)
    quantity = serializers.FloatField()

    def create(self, validated_data):
        return Meal.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.ingredient_unit = validated_data.get('ingredient_unit', instance.ingredient_unit)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance
