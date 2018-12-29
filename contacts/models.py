from django.db import models
from django.utils import timezone

# Create your models here.


class Department(models.Model):
    dep_name = models.CharField(max_length=100)

    def __str__(self):
        return self.dep_name


class Role(models.Model):
    role_name = models.CharField(max_length=50)

    def __str__(self):
        return self.role_name


class Names(models.Model):
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=80)
    mobile_phone = models.CharField(max_length=11)
    work_phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=50)
    created_date = models.DateTimeField(default=timezone.now)
    persona_dep = models.ForeignKey(Department, on_delete=models.DO_NOTHING)
    persona_role = models.ForeignKey(Role, on_delete=models.DO_NOTHING)

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

