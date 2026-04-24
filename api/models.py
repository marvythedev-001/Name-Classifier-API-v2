from django.db import models

# Create your models here.

from django.db import models
from uuid6 import uuid7

class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid7, editable=False)

    name = models.CharField(max_length=100, unique=True)

    GENDER = (("male", "MALE"), ("female", "FEMALE"))
    gender = models.CharField(max_length=10, choices=GENDER)
    gender_probability = models.FloatField()
    # sample_size = models.IntegerField()

    age = models.IntegerField()
    age_group = models.CharField(max_length=20)

    country_id = models.CharField(max_length=5)
    country_name = models.CharField(max_length=100)
    country_probability = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)