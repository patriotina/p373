from django.db import models
from django.utils import timezone

# Create your models here.

class Names(models.Model):
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=80)
    created_date = models.DateTimeField(default=timezone.now)

    def publish(self):
        seflf.created_date = timezone.now()
        self.save()

    def __str__(self):
        return self.second_name + ' ' + self.first_name

class ContactType(models.Model):
    type_description = models.CharField(max_length=20)

    def __str__(self):
        return self.type_description


class Contacts(models.Model):
    contact_type = models.ForeignKey(ContactType, on_delete=models.DO_NOTHING)
    contact_data = models.CharField(max_length=200)
    persona_name = models.ForeignKey(Names, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.contact_data

