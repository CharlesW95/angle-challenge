from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=10, primary_key=True)
    price = models.IntegerField()
    start_date = models.CharField(max_length=10)  # MM/DD/YYYY
