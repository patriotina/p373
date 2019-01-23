from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    url(r'^$', views.names_list, name='names_list'),
    url(r'^department/(?P<pk>\d+)/$', views.department_list, name='departments'),
    url(r'^issues/$', views.issues_list, name='issues'),
    url(r'^create_task/$', views.create_task, name='create_task'),
    url(r'^createissue/$', views.sendtojira),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)