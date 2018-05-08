from django.contrib import admin
from .models import Names, Contacts, ContactType

# Register your models here.
admin.site.register(Names)
admin.site.register(Contacts)
admin.site.register(ContactType)
