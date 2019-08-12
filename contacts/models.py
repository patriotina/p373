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

class City(models.Model):
    city_name = models.CharField(blank=True, null=True, max_length=30)

    def __str__(self):
        return self.city_name


class Names(models.Model):
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=80)
    mobile_phone = models.CharField(max_length=11, blank=True, null=True)
    work_phone = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(max_length=50, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    persona_dep = models.ForeignKey(Department, on_delete=models.DO_NOTHING)
    persona_role = models.ForeignKey(Role, on_delete=models.DO_NOTHING)
    persona_photo = models.ImageField(upload_to='imgs', max_length=50, default='imgs/nophoto.png')
    persona_city = models.ForeignKey(City, on_delete=models.DO_NOTHING, blank=True, null=True)
    employ = models.BooleanField(default=True)


    def publish(self):
        seflf.created_date = timezone.now()
        self.save()


    def __str__(self):
        return self.second_name + ' ' + self.first_name


    def image_tag(self):
        return '<img src="' + str(self.persona_photo) + '" width = "150" height = "150" />'


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

