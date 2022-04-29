import io
import base64
from io import BytesIO
from rest_framework import generics
from type_one.records.models import Photo, Record, Meal
from type_one.ingredients.models import Ingredient, IngredientUnit
from type_one.api import serializers
from type_one.records.views import handle_uploaded_file
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from django.db.models import Q

class LogoutView(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

class RecordDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Record.objects.filter()
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.RecordFullSerializer
        return serializers.RecordUpdateSerializer           

class RecordsList(generics.ListCreateAPIView):
    serializer_class = serializers.RecordListSerializer
    def get_queryset(self):
        user = self.request.user
        return Record.objects.filter(user=user).order_by('-time')[:17]
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.RecordListSerializer
        return serializers.RecordCreateSerializer
    def perform_create(self, serializer):
        user = self.request.user
        if serializer.validated_data['type'] == 0:
            insulin = user.rapid_acting_insulin
        if serializer.validated_data['type'] == 1:
            insulin = user.long_acting_insulin
        serializer.save(
            user=user, 
            insulin=insulin, 
            glucose_level_unit=user.glucose_level_unit,
            show_rapid_insulin=user.show_rapid_insulin,   
            show_long_insulin=user.show_long_insulin,
            show_sugar=user.show_sugar,
            show_calories=user.show_calories,
            show_calories_today=user.show_calories_today,
            show_bread_units=user.show_bread_units)

class PhotoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Photo.objects.all()
    serializer_class = serializers.PhotoSerializer
    def get_queryset(self):
        return Photo.objects.all().filter(
            record_id=self.kwargs["record_id"], 
            id=self.kwargs["pk"])

class PhotoCreate(generics.CreateAPIView):
    queryset = Photo.objects.all()
    serializer_class = serializers.PhotoCreateSerializer    
    def perform_create(self, serializer):
        record = Record.objects.all().filter(id=self.kwargs["pk"]).first()
        in_memory_file = BytesIO(base64.b64decode(serializer.initial_data['data']))
        (thumb, data) = handle_uploaded_file(in_memory_file)
        serializer.save(
            record=record, 
            thumb=thumb,
            data=data)

class MealsList(generics.ListCreateAPIView):
    serializer_class = serializers.MealShortSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.MealSerializer
        return serializers.MealShortSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(
            user=user, 
            record=Record.objects.get(id=serializer.validated_data.get('record_id')),
            ingredient_unit=IngredientUnit.objects.get(id=serializer.validated_data.get('ingredient_unit_id')),
            quantity=serializer.validated_data.get('quantity')
        )


    def get_queryset(self):
        user = self.request.user
        print(f"user={user}")
        record = Record.objects.all().get(id=self.kwargs["pk"])
        return Meal.objects.all().filter(Q(user=None)|Q(user=user)).filter(record=record)


class IngredientsList(generics.ListCreateAPIView):
    serializer_class = serializers.IngredientUnitSerializer
    def get_queryset(self):
        user = self.request.user
        return IngredientUnit.objects.all().filter(Q(user=None)|Q(user=user))

class IngredientsDetails(generics.RetrieveAPIView):
    serializer_class = serializers.IngredientUnitFullSerializer
    def get_queryset(self):
        # user = self.request.user
        # return IngredientUnit.objects.all().filter(ingredient_id=self.kwargs["pk"])
        return IngredientUnit.objects.all()

class MealDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.MealShortSerializer

    def get_queryset(self):
        return Meal.objects.all().filter(id=self.kwargs["pk"])

class IngredientsHintCreate(generics.CreateAPIView):
    serializer_class = serializers.IngredientHintSerializer
    
    def perform_create(self, serializer):
        in_memory_file = BytesIO(base64.b64decode(serializer.initial_data['data']))
        (thumb, data) = handle_uploaded_file(in_memory_file)
        serializer.save(
            user = self.request.user,
            ingredient=Ingredient.objects.get(id=self.kwargs["pk"]),
            thumb=thumb,
            data=data)

class IngredientsHintDelete(generics.DestroyAPIView):
    serializer_class = serializers.IngredientHintSerializer    