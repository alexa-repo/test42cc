from django.conf.urls import patterns, include, url
import django.contrib
from django.contrib import admin
from test42cc.src import views

django.contrib.admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),
)
