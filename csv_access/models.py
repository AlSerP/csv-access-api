import csv
import operator

from django.db import models

OPS = {
    ">": operator.gt,
    ">=": operator.ge,
    "<": operator.lt,
    "<=": operator.le,
    "=": operator.eq,
}


class Dataset(models.Model):
    """Uploaded csv file"""

    file = models.FileField(upload_to="uploads/%Y/%m/%d/%H_%M_%S")
    columns = models.TextField(blank=True, null=True)  # String of column's names splited by comma
    rows = models.IntegerField(blank=True, null=True)  # Number of rows in file

    def get_data(self, order_by=None, sort_by=None):
        with open(self.file.path, newline="") as csvfile:
            lines = []
            reader = csv.reader(csvfile, delimiter=" ", quotechar="|")
            for line in reader:
                line = line[0].split(",")
                lines.append(line)

            header = lines[0]
            data = lines[1:]

            print(sort_by)
            if sort_by:
                for field in sort_by.keys():
                    if field in header:
                        field_id = header.index(field)
                        sort_param = sort_by[field]
                        operator = sort_param[:2]
                        value = sort_param[2:]
                        if operator not in OPS:
                            operator = sort_param[0]
                            value = sort_param[1:]
                            if operator not in OPS:
                                operator = "="
                                value = sort_param

                        operation = OPS[operator]

                        try:
                            value = float(value)
                            data = filter(lambda x: operation(float(x[field_id]), value), data)
                        except ValueError:
                            return [f"ValueError: Can't sort by this parameter:  {field}{operator}{value}"]

            if order_by and order_by in header:
                ordering_id = header.index(order_by)
                data = sorted(data, key=lambda x: x[ordering_id], reverse=True)

            return [header] + data

    # def (self)

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
