
from credentials import *
from jira import JIRA
from datetime import datetime

jira = JIRA(basic_auth=(jira_user, jira_token), options = {'server': jira_server})
# issues = jira.search_issues('project = SUP AND issuetype=Обращение_клиента order by created desc',
#                                   fields= 'created, comment, resolution, description, assignee, customfield_10517, customfield_10534, summary, status',)
                                # expand='changelog',)

#for issue in issues:
#    issue.fields.created = datetime.strptime(issue.fields.created, '%Y-%m-%dT%H:%M:%S.%f%z')
issue = jira.issue('SUP-1590')
print(issue.fields.comment)
print(issue.fields.assignee.name)
print(issue.fields.attachment)
print(issue.fields.attachment[0])
print(issue.fields.attachment.__len__())

#print(issue.fields.customfield_10534)



#deps = Department.objects.filter().order_by('dep_name')
