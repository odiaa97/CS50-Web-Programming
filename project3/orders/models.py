from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return str(self.name)


class Item(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.CharField(max_length=1000)

    def __str__(self):
            return self.name


class Order(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name
