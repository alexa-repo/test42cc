from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from test42cc.src import views
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^requests/$', views.stored_requests, name='requests'),
                       url(r'^edit/', views.edit_person_entry, name='edit'),
                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),
) #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += patterns('',
        #(r'^static/(?P<path>.*)$',
        #    'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),

        (r'^media/(?P<path>.*)$',
            'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )