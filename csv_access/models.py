import csv

from django.db import models


class Dataset(models.Model):
    """Uploaded csv file"""

    file = models.FileField(upload_to="uploads/%Y/%m/%d/%H_%M_%S")
    columns = models.TextField(blank=True, null=True)  # String of column's names splited by comma

    def update_columns(self):
        """Update self.columns from csv file"""
        file_url = self.file.path
        print(file_url)
        with open(file_url, newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=" ", quotechar="|")
            firs_row = next(reader)
            print(firs_row)
            self.columns = firs_row[0]
