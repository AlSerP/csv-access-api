from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from .models import Dataset
from .serializers import DatasetListSerializer, DatasetSerializer


class StandardResultsSetPagination(PageNumberPagination):
    """
    Standard pagination settings class
    """

    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 200


class DatasetViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing datasets.
    """

    parser_classes = (MultiPartParser, FormParser)
    serializer_class = DatasetSerializer
    queryset = Dataset.objects.all()

    def list(self, request):
        """List Datasets with pagination"""
        pagination = StandardResultsSetPagination()
        page = pagination.paginate_queryset(self.get_queryset(), request)
        serializer = DatasetListSerializer(page, many=True)
        return pagination.get_paginated_response(serializer.data)

    @action(methods=["post"], detail=False, url_path="create", url_name="create")
    def new(self, request):
        """Upload new Dataset"""
        return self.create(request)

    @action(methods=["get"], detail=True, url_path="data", url_name="get-data")
    def get_data(self, request, pk):
        """List Dataset data with pagination"""
        if pk:
            dataset = Dataset.objects.get(pk=pk)
            if dataset:
                print(request.query_params)
                sort_params = request.query_params.dict()
                order_param = request.query_params.get("order_by")
                if order_param:
                    del sort_params["order_by"]

                data = dataset.get_data(order_by=order_param, sort_by=sort_params)
                pagination = StandardResultsSetPagination()
                page = pagination.paginate_queryset(data, request)
                return pagination.get_paginated_response(page)
        return Response(status.HTTP_404_NOT_FOUND)
