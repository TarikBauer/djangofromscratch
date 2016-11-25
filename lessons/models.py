from django.db import models


class Python(models.Model):
    python_file = models.FileField()


class Django(models.Model):
    django_file = models.FileField()
