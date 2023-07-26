import csv

from django.db import models


class Dataset(models.Model):
    """Uploaded csv file"""

    file = models.FileField(upload_to="uploads/%Y/%m/%d/%H_%M_%S")
    columns = models.TextField(blank=True, null=True)  # String of column's names splited by comma
    rows = models.IntegerField(blank=True, null=True)  # Number of rows in file

    def get_data(self):
        with open(self.file.path, newline="") as csvfile:
            lines = []
            reader = csv.reader(csvfile, delimiter=" ", quotechar="|")
            for line in reader:
                line = line[0].split(",")
                lines.append(line)
            return lines

    def update(self):
        """Update Dataset using file info"""
        self.__update_rows()
        self.__update_columns()
        self.save

    def __update_rows(self):
        """Update self.rows from csv file"""
        with open(self.file.path, newline="") as csvfile:
            self.rows = sum(1 for line in csvfile) - 1
            self.save()

    def __update_columns(self):
        """Update self.columns from csv file"""
        with open(self.file.path, newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=" ", quotechar="|")
            self.columns = next(reader)[0]
            self.save()
