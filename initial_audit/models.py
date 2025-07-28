from django.db import models

# Create your models here.
class Corporation(models.Model):
    corp_name = models.CharField(max_length=50)
    search_period = models.PositiveIntegerField(default=1)
    create_date = models.DateTimeField()

