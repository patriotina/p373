from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Names, ContactType, Contacts, Department, Alarms
from jira import JIRA
from .credentials import *
from datetime import datetime
from contacts.formiss import IssueForm

from django.http import HttpResponseRedirect
from django.urls import reverse
import requests
from youtrack.connection import Connection as YouTrack


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


def statistic(request):
    dif = []
    alarms = Alarms.objects.filter()
    for alarm in alarms:
        dif.append(alarm.alrm_datetime_end - alarm.alrm_datetime_start)
        print(dif)
#    names = Names.objects.filter(employ=True).order_by('second_name')
#    deps = Department.objects.filter().order_by('dep_name')
    return render(request, 'contacts/statistic.html', {'alarms': alarms, 'diff':dif})


def calendar(request):
    return render(request, 'contacts/calendar.html')



def alarm(request):
    al_id = int(request.GET['alrm_msg_id'])
    al_city = int(request.GET['alrm_city'])
    check = Alarms.objects.filter(alrm_msg_id=al_id, alrm_city=al_city)
    if check:
        al_end = datetime.now()
        Alarms.objects.filter(alrm_msg_id=al_id, alrm_city=al_city).update(alrm_datetime_end=al_end)
        url = url_telega + '/bot' + ttalarm
        method = '/deleteMessage?chat_id='
        #chatid = str(al_city)
        chatid = Alarms.objects.get(alrm_msg_id=al_id, alrm_city=al_city)
        url = url + method + str(chatid.alrm_city) + '&message_id=' + str(al_id)
        res = requests.get(url)
    else:
        al_start = datetime.now()
        al_author = int(request.GET['alrm_author'])
        alr = Alarms(alrm_msg_id=al_id,
                     alrm_datetime_start=al_start,
                     alrm_author=al_author,
                     alrm_city=al_city)
        alr.save()

    #bot = telebot.TeleBot(ttalarm)
    #alm_message = 'AlarmOn;'
    #city_alarm_list[c.message.chat.id] = 1
        url = url_telega + '/bot' + ttalarm
        method = '/editMessageText?chat_id='
        # chatid = city_chat_id[city]
        chatid = str(al_city)
        style = '&parse_mode=Markdown'
        inline_url = '&reply_markup={"inline_keyboard":[[{"text":"Исправлено ✅", "callback_data":"AlarmDone"}]]}'
        #inline_url = '&reply_markup={"inline_keyboard":[[{"text":"Исправлено ✅", "url":"help.373soft.ru/alarm?alrm_msg_id=' + str(al_id) + '"}]]}'
        # '&alrm_author=' + str(al_author) + '&alrm_city=' +str(al_city) +
        #+ str(al_id) + '&alrm_author=' + str(al_author) + '&alrm_city=' +str(al_city) +
        text = 'Взято в работу'
        url = url + method + chatid + '&text=' + text + '&message_id=' + str(al_id) + style + inline_url
        res = requests.get(url)

#http://help.373soft.ru/alarm?alrm_msg_id=372&alrm_author=65774702&alrm_city=-1001129544717
    # reply_keyboard = types.InlineKeyboardMarkup()
    # inl_button = types.InlineKeyboardButton(text="Исправлено", url='ya.ru')
    # reply_keyboard.row(inl_button)
    # bot.edit_message_text(chat_id=al_city, message_id=al_id, text='Взято в работу',
    #                       reply_markup=reply_keyboard)

    return HttpResponseRedirect(reverse('create_task'))


#submit creation form and create an issue
def sendtojira(request):
    issuetext = request.GET['textissue']
    summary = request.GET['summary']
    problemclass = request.GET['prclass']
    city = request.GET['issue-city']
    author = request.GET['author']
    #attach_path = request.GET['attachfile']
    b2p = request.GET['b2p']
    print(b2p)


    jira = JIRA(basic_auth=(jira_user, jira_token), options={'server': jira_server})
    issue_dict = {
        'project': {'key': 'SUP'},
        'summary': city + ': ' + summary,
        'description': str(issuetext + '\n Заявитель:' + author),
        'issuetype': {'name': 'Обращение_клиента'},
        'customfield_10517': {'value': problemclass},
        'customfield_10534': {'value': city},
        #'assignee': {'name': 'eh'},
    }
    if problemclass == 'Оператор - исходящая телефония' or problemclass == 'Оператор - входящая телефония':
        issue_dict['assignee'] = {'name': 'guru'}
        assignee = 'Guru'
    else:
        issue_dict['assignee'] = {'name': 'sterhov.a'}
        assignee = 'sterhov.a'



    ##new_issue = jira.create_issue(fields=issue_dict)

    #Добавить аттач к таске если таковой имеется
    #print(new_issue)
    #print(attach_path)
    #jira.add_attachment(issue=new_issue, attachment=attach_path)

    ##key = str(new_issue.key)
    key = str(99999)
    sendtotelega(city, summary, issuetext, author, assignee, key)


    #return render(request, 'contacts/create_task.html', {'issuetext':issue_dict})
    issues = jira.search_issues('project = SUP AND issuetype=Обращение_клиента order by created desc',
                                fields='created, comment, resolution, description, assignee, customfield_10517, customfield_10534, summary, status',
                                expand='changelog',)
    for issue in issues:
        issue.fields.created = datetime.strptime(issue.fields.created, '%Y-%m-%dT%H:%M:%S.%f%z')

    deps = Department.objects.filter().order_by('dep_name')

    #issues_list(request)
    return HttpResponseRedirect(reverse('issues'))
    #return render(request, 'contacts/issues.html', {'issues': issues, 'deps': deps})



    #jira = JIRA(basic_auth=(jira_user, jira_token), options={'server': jira_server})
    #issues = jira.search_issues('project = SUP AND issuetype=Обращение_клиента order by created desc', maxResults=10)
    #for issue in issues:
    #    issue.fields.created = datetime.strptime(issue.fields.created, '%Y-%m-%dT%H:%M:%S.%f%z')

    #deps = Department.objects.filter().order_by('dep_name')
    #return render(request, 'contacts/issues.html', {'issues': issues, 'deps': deps})


def sendtotelega(city, summary, issuetext, author, assignee, key):
    url = url_telega + '/bot' + tapsup_token
    method = '/sendmessage?chat_id='
    #chatid = city_chat_id[city]
    chatid = city_chat_id['Support']
    style = '&parse_mode=Markdown'
    inline_url = '&reply_markup={"inline_keyboard":[[{"text":"issue", "url":"https://taptaxi.atlassian.net/browse/' + key + '"}]]}'
    text = 'Создана задача по обращению: *' + author + '*\n *' + city + '*: ' + summary + '\n *Содержание обращения*: ' + issuetext + '\n' + 'Автоматически назначено на исполнителя: *' + assignee + '*'
    url = url + method + chatid + '&text=' + text + style + inline_url
    res = requests.get(url)


# List of workers.
def names_list(request):
    names = Names.objects.filter(employ=True).order_by('second_name')
    deps = Department.objects.filter().order_by('dep_name')
    return render(request, 'contacts/names_list.html', {'names': names, 'deps': deps})


# List of persons by departments
def department_list(request, pk):
    names = Names.objects.filter(persona_dep=pk, employ=True).order_by('second_name')
    deps = Department.objects.filter().order_by('dep_name')
    return render(request, 'contacts/names_list.html', {'names': names, 'deps': deps})


#List of user's issues with statuses
def issues_list(request):
    jira = JIRA(basic_auth=(jira_user, jira_token), options = {'server': jira_server})
    issues = jira.search_issues('project = SUP AND issuetype=Обращение_клиента order by created desc',
                                fields= 'created, comment, resolution, description, assignee, customfield_10517, customfield_10534, summary, status',
                                expand='changelog',)
    for issue in issues:
        issue.fields.created = datetime.strptime(issue.fields.created, '%Y-%m-%dT%H:%M:%S.%f%z')

    deps = Department.objects.filter().order_by('dep_name')
    return render(request, 'contacts/issues.html', {'issues': issues, 'deps': deps})


#List of user's issues with statuses from YouTrack
def issues_list_yt(request):
    yt = YouTrack('https://taptaxi.myjetbrains.com/youtrack/', token=ytt)
    issues = yt.getIssues('SUP', 'Тип: Обращение_клиента сортировать: создана по убыв.', '', '50')

    #for issue in issues:
        #issue.created = datetime.strptime(issue.created, '%Y-%m-%dT%H:%M:%S.%f%z')

    deps = Department.objects.filter().order_by('dep_name')
    return render(request, 'contacts/issues_yt.html', {'issues': issues, 'deps': deps})



#page for getting issue from user
def create_task(request):
    #jira = JIRA(basic_auth=(jira_user, jira_token), options = {'server': jira_server})
    #issue = jira.issue('SUP-721')
    deps = Department.objects.filter().order_by('dep_name')
    return render(request, 'contacts/create_task.html', {'pclass': classification,
                                                         'cities': cities,
                                                         'deps': deps
                                                        },)
