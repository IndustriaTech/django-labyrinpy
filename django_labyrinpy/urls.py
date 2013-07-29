from django.conf.urls import patterns, url

urlpatterns = patterns('django_labyrinpy.views',
    url(r'^create/$', 'create_report', name="create-report"),
)