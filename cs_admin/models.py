from django.db import models

# Create your models here.


class Admin(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    class Meta:
        db_table = 'cs_admin'