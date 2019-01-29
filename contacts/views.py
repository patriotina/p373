from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Names, ContactType, Contacts, Department
from jira import JIRA
from .credentials import *
from datetime import datetime
from contacts.formiss import IssueForm


class CreateIssueView(TemplateView):
    template_name = 'contacts/create_task.html'

    def get(self, request):
        form = IssueForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = IssueForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['post']

        args = {'form': form, 'text': text}
        return render(request, self.template_name, args)


def sendtojira(request):
    issuetext = request.GET['textissue']
    summary = request.GET['summary']
    problemclass = request.GET['prclass']
    city = request.GET['issue-city']


    jira = JIRA(basic_auth=(jira_user, jira_token), options={'server': jira_server})
    issue_dict = {
        'project': {'key': 'SUP'},
        'summary': city + ':' + summary,
        'description': str(issuetext),
        'issuetype': {'name': 'Обращение_клиента'},
        "customfield_10517": {"value": problemclass},
    }

    #new_issue = jira.create_issue(fields=issue_dict)

    return render(request, 'contacts/create_task.html', {'issuetext':issue_dict})


    #jira = JIRA(basic_auth=(jira_user, jira_token), options={'server': jira_server})
    #issues = jira.search_issues('project = SUP AND issuetype=Обращение_клиента order by created desc', maxResults=10)
    #for issue in issues:
    #    issue.fields.created = datetime.strptime(issue.fields.created, '%Y-%m-%dT%H:%M:%S.%f%z')

    #deps = Department.objects.filter().order_by('dep_name')
    #return render(request, 'contacts/issues.html', {'issues': issues, 'deps': deps})


# List of workers.
def names_list(request):
    names = Names.objects.filter().order_by('second_name')
    deps = Department.objects.filter().order_by('dep_name')
    #names = Names.objects.prefetch_related("persona_name")
    #contacts = Contacts.objects.prefetch_related("persona_name")

#    print(names)
    #print(contacts)
    return render(request, 'contacts/names_list.html', {'names': names, 'deps': deps})

# List of persons by departments
def department_list(request, pk):
    names = Names.objects.filter(persona_dep=pk)
    deps = Department.objects.filter().order_by('dep_name')
    #names = Names.objects.filter().order_by('second_name')
    return render(request, 'contacts/names_list.html', {'names': names, 'deps': deps})

#List of user's issues with statuses
def issues_list(request):
    jira = JIRA(basic_auth=(jira_user, jira_token), options = {'server': jira_server})
    issues = jira.search_issues('project = SUP AND issuetype=Обращение_клиента order by created desc',
                                fields= 'created, comment, resolution, description, assignee, customfield_10517, summary, status',
                                expand='changelog',)
    for issue in issues:
        issue.fields.created = datetime.strptime(issue.fields.created, '%Y-%m-%dT%H:%M:%S.%f%z')

    deps = Department.objects.filter().order_by('dep_name')
    return render(request, 'contacts/issues.html', {'issues': issues, 'deps': deps})

#page for getting issue from user
def create_task(request):
    #jira = JIRA(basic_auth=(jira_user, jira_token), options = {'server': jira_server})
    #issue = jira.issue('SUP-721')
    deps = Department.objects.filter().order_by('dep_name')
    return render(request, 'contacts/create_task.html', {'pclass': classification,
                                                         'cities': cities,
                                                         'deps': deps
                                                        },)

