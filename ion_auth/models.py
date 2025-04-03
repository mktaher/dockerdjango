from django.db import models

# Create your models here.
class ionUser(models.Model):
    id = models.BigIntegerField(primary_key=True)
    ion_username = models.CharField(max_length=100)