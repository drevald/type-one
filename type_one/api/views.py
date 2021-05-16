from rest_framework import generics
from type_one.records.models import Photo
from type_one.records.models import Record
from type_one.records.models import Insulin
from type_one.api.serializers import PhotoSerializer
from type_one.api.serializers import RecordSerializer
from type_one.api.serializers import RecordFullSerializer
from type_one.api import serializers

class RecordDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Record.objects.filter()
    serializer_class = RecordFullSerializer

class RecordsList(generics.ListCreateAPIView):
    serializer_class = RecordSerializer
    def get_queryset(self):
        user = self.request.user
        return Record.objects.filter(user=user).order_by('-time')
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
            glucose_level_unit=user.glucose_level_unit)        

class PhotoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    def get_queryset(self):
        return Photo.objects.all().filter(
            record_id=self.kwargs["record_id"], 
            id=self.kwargs["pk"])

class PhotoCreate(generics.CreateAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer