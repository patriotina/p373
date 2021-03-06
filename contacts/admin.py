from django.contrib import admin
from .models import *
from django.utils.html import format_html


class NamesList(admin.ModelAdmin):
    list_display = [ 'second_name', 'first_name', 'pictumb','email' ]

    def pictumb(self, obj):
        return format_html('<img src="/media/{}" width=50px />'.format(obj.persona_photo))


class AlarmsList(admin.ModelAdmin):
    list_display = ['alrm_msg_id', 'alrm_datetime_start', 'alrm_datetime_end', 'alrm_author', 'alrm_city']

# Register your models here.
admin.site.register(Names, NamesList)
admin.site.register(Contacts)
admin.site.register(ContactType)
admin.site.register(Department)
admin.site.register(Role)
admin.site.register(City)
admin.site.register(Alarms, AlarmsList)




