from django.shortcuts import render
from .models import Names, ContactType, Contacts

# Create your views here.
def names_list(request):
    names = Names.objects.all().order_by('second_name')
    print(names)
    return render(request, 'contacts/names_list.html', {'names': names})