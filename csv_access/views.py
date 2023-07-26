from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from .models import Dataset
from .serializers import DatasetListSerializer, DatasetSerializer

# class UserViewSet(viewsets.ViewSet):
#     """
#     A simple ViewSet for listing or retrieving users.
#     """

#     def list(self, request):
#         queryset = User.objects.all()
#         serializer = UserSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = User.objects.all()
#         user = get_object_or_404(queryset, pk=pk)
#         serializer = UserSerializer(user)
#         return Response(serializer.data)


class DatasetViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing datasets.
    """

    parser_classes = (MultiPartParser, FormParser)
    serializer_class = DatasetSerializer
    queryset = Dataset.objects.all()

    def list(self, request):
        # serializer = self.get_serializer(self.get_queryset(), many=True)
        # return self.get_paginated_response(self.paginate_queryset(serializer.data))
        queryset = Dataset.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # @action(detail=True, methods=["post"])
    @action(methods=["post"], detail=False, url_path="create", url_name="create-dataset")
    def new(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dataset = serializer.save()
        dataset.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# class DatasetCreateView(ModelViewSet):
#     """Adding a new dataset"""

#     def post(self, request):
#         dataset = DatasetSerializer(data=request.data)
#         if dataset.is_valid():
#             dataset.save()
#         return Response(status=201)
