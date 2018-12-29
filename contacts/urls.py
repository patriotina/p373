from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.names_list, name='names_list'),

    url(r'^department/(?P<pk>\d+)/$', views.department_list, name='departments')
]