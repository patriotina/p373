from django.db import models
from django.utils import timezone

# Create your models here.

class Names(models.Model):
    #id = models.Index()
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=80)
    created_date = models.DateTimeField(default=timezone.now)

    def publish(self):
        seflf.created_date = timezone.now()
        self.save()

    def __str__(self):
        return self.second_name + ' ' + self.first_name