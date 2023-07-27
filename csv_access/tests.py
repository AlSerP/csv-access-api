from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Dataset


class DatasetTests(APITestCase):
    def setUp(self):
        self.csv_path = str(settings.STATIC_ROOT) + "/tests/test.csv"
        self.test_csv = None

    def create_dataset(self):
        """Create a test dataset."""
        path = Path(self.csv_path)

        dataset = Dataset()
        with path.open(mode="rb") as f:
            dataset.file = File(f, name=path.name)
            dataset.save()
        dataset.update()
        return dataset

    def test_create_dataset(self):
        """Ensure we can create a new account object."""
        url = reverse("datasets-create")
        previous_count = Dataset.objects.all().count()

        file = open(self.csv_path, "r")
        data = {"file": file}
        response = self.client.post(url, data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Dataset.objects.all().count(), previous_count + 1)

        file.close()

    def test_delete_dataset(self):
        """Ensure we can delete the dataset."""
        dataset = self.create_dataset()
        previous_count = Dataset.objects.all().count()
        url = reverse("datasets-detail", kwargs={"pk": dataset.pk})
        response = self.client.delete(url, format="multipart")

        self.assertEqual(Dataset.objects.all().count(), previous_count - 1)

    def test_get_dataset_detail(self):
        """Ensure we get the right dataset details."""
        dataset = self.create_dataset()
        url = reverse("datasets-detail", kwargs={"pk": dataset.pk})
        response = self.client.get(url, format="multipart")
        columns = [
            "hero_id",
            "1_pick",
            "1_win",
            "2_pick",
            "2_win",
            "3_pick",
            "3_win",
            "4_pick",
            "4_win",
            "5_pick",
            "5_win",
            "6_pick",
            "6_win",
            "7_pick",
            "7_win",
            "8_pick",
            "8_win",
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("columns"), columns)
        self.assertEqual(response.data.get("rows"), 124)

    def test_do_not_get_dataset_detail(self):
        """Ensure we can't get the non-existent dataset details."""
        url = reverse("datasets-detail", kwargs={"pk": Dataset.objects.all().count() + 1})
        response = self.client.get(url, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_do_not_delete_dataset(self):
        """Ensure we can't get the non-existent dataset details."""
        url = reverse("datasets-detail", kwargs={"pk": Dataset.objects.all().count() + 1})
        response = self.client.delete(url, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
