from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.SimpleRouter()

router.register(r"datasets", views.DatasetViewSet, basename="datasets")

urlpatterns = [
    path("", include(router.urls)),
    # path("datasets/create", views.DatasetCreateView.as_view()),
]
