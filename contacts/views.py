from django.shortcuts import render
from .models import Names, ContactType, Contacts

# Create your views here.
def names_list(request):
    names = Names.objects.filter().order_by('second_name')
    #names = Names.objects.prefetch_related("persona_name")
    #contacts = Contacts.objects.prefetch_related("persona_name")

    print(names)
    #print(contacts)
    return render(request, 'contacts/names_list.html', {'names': names})