from django.shortcuts import render
from .models import Names, ContactType, Contacts, Department
from jira import JIRA
from .credentials import *
from datetime import datetime


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
    return render(request, 'contacts/names_list.html', {'names': names, 'deps': deps})


def issues_list(request):
    jira = JIRA(basic_auth=(jira_user, jira_token), options = {'server': jira_server})
    issues = jira.search_issues('project = SUP AND issuetype=Обращение_клиента order by created desc', maxResults=10)
    for issue in issues:
        issue.fields.created = datetime.strptime(issue.fields.created, '%Y-%m-%dT%H:%M:%S.%f%z')

    deps = Department.objects.filter().order_by('dep_name')
    return render(request, 'contacts/issues.html', {'issues': issues, 'deps': deps})


def create_task(request):
    return render(request, 'contacts/create_task.html')

