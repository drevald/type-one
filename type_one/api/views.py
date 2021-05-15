from rest_framework import generics
from type_one.records.models import Photo
from type_one.records.models import Record
from type_one.records.models import Insulin
from type_one.api.serializers import PhotoSerializer
from type_one.api.serializers import RecordSerializer
from type_one.api.serializers import RecordFullSerializer

class RecordDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Record.objects.filter()
    serializer_class = RecordFullSerializer

class RecordsList(generics.ListCreateAPIView):
    # queryset = Record.objects.all()
    serializer_class = RecordSerializer
    def get_queryset(self):
        user = self.request.user
        return Record.objects.filter(user=user).order_by('-time')

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