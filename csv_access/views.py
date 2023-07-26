from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from .models import Dataset
from .serializers import DatasetListSerializer, DatasetSerializer


class DatasetViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing datasets.
    """

    parser_classes = (MultiPartParser, FormParser)
    serializer_class = DatasetSerializer
    queryset = Dataset.objects.all()

    def list(self, request):
        serializer = DatasetListSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    @action(methods=["post"], detail=False, url_path="create", url_name="create-dataset")
    def new(self, request):
        return self.create(request)

    @action(methods=["get"], detail=True, url_path="data", url_name="get-data")
    def get_data(self, request, pk):
        if pk:
            dataset = Dataset.objects.get(pk=pk)
            if dataset:
                print(dataset)
                return Response(dataset.get_data())
        return Response(404)
