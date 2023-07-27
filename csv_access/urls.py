from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.SimpleRouter()

router.register(r"datasets", views.DatasetViewSet, basename="datasets")

# print(router.urls)

urlpatterns = [
    path("", include(router.urls)),
]
