from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from type_one.records.models import Record
from type_one.api.serializers import RecordSerializer

@csrf_exempt
def records_list(request):
    """
    List all code records, or create a new record.
    """
    if request.method == 'GET':
        records = Record.objects.all()
        serializer = RecordSerializer(records, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = RecordSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def record_detail(request, pk):
    """
    Retrieve, update or delete a code record.
    """
    try:
        record = Record.objects.get(pk=pk)
    except Record.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = RecordSerializer(record)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = RecordSerializer(record, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        record.delete()
        return HttpResponse(status=204)        