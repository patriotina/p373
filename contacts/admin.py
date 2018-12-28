from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Names)
admin.site.register(Contacts)
admin.site.register(ContactType)
admin.site.register(Department)
admin.site.register(Role)

