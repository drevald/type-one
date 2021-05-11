from rest_framework import generics
from type_one.records.models import Record
from type_one.records.models import Insulin
from type_one.api.serializers import RecordSerializer
from type_one.api.serializers import RecordFullSerializer
from type_one.api.serializers import InsulinSerializer

class RecordDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordFullSerializer

class RecordsList(generics.ListCreateAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer

class InsulinsList(generics.ListCreateAPIView):
    queryset = Insulin.objects.all()
    serializer_class = InsulinSerializer    