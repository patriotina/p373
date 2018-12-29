from django.shortcuts import render
from .models import Names, ContactType, Contacts, Department

# Create your views here.
def names_list(request):
    names = Names.objects.filter().order_by('second_name')
    deps = Department.objects.filter().order_by('dep_name')
    #names = Names.objects.prefetch_related("persona_name")
    #contacts = Contacts.objects.prefetch_related("persona_name")

#    print(names)
    #print(contacts)
    return render(request, 'contacts/names_list.html', {'names': names, 'deps': deps})


def department_list(request, pk):
    names = Names.objects.filter(persona_dep=pk)
    deps = Department.objects.filter().order_by('dep_name')
    #names = Names.objects.filter().order_by('second_name')
    return render(request, 'contacts/department.html', {'names': names, 'deps': deps})

