from django.db import models
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse

from labyrinpy.request import LabyrinpyRequest


class Message(models.Model):
    MESSAGE_TYPES = (('text', 'Plain text'), (
        'binary', 'Binary'), ('wap_url', 'WAP Push SI Message'))
    _CLASS = (('normal', 'Normal Message'), ('flash', 'Flash Message'))
    BOOLEAN = (('yes', 'yes'), ('no', 'no'))

    destination = models.CharField(max_length=16)
    message_type = models.CharField(max_length=7, choices=MESSAGE_TYPES)
    content = models.CharField(max_length=160)

    source_name = models.CharField(max_length=16, blank=True, null=True)
    source = models.CharField(max_length=6, blank=True, null=True)
    service = models.CharField(max_length=10, blank=True, null=True)
    header = models.CharField(max_length=15, blank=True, null=True)
    wap_text = models.URLField(blank=True, null=True)
    _class = models.CharField(max_length=6, choices=_CLASS,
                              blank=True, null=True)
    concatenate = models.NullBooleanField()
    unicode = models.NullBooleanField()
    validity = models.CharField(max_length=16, blank=True, null=True)
    delivery = models.CharField(max_length=16, blank=True, null=True)
    report = models.URLField(blank=True, null=True)

    def __unicode__(self):
        return u'Message to {}'.format(self.destination)

    @classmethod
    def send(cls, destination, message_type, content, **kwargs):
        try:
            username = settings.LABYRINPY_USERNAME
            password = settings.LABYRINPY_PASSWORD
        except AttributeError:
            raise ImproperlyConfigured("Labyrinpy is improperly configured."
                                       "Please suply LABYRINPY_USERNAME and"
                                       "and LABYRINPY_PASSWORD values")

        request = LabyrinpyRequest(username, password, **kwargs)
        if 'class' in kwargs.keys():
            kwargs['_class'] = kwargs.pop('class')
        kwargs['destination'] = destination
        kwargs['message_type'] = message_type
        kwargs['content'] = content
        kwargs['report'] = reverse('create-report')

        request.send(destination, message_type, content)
        return cls.objects.create(**kwargs)


class Report(models.Model):
    STATUS = (('OK', 'OK'), ('ERROR', 'ERROR'), ('WAITING', 'WAITING'))

    message = models.ForeignKey(Message, related_name='reports')
    source = models.CharField(max_length=6)
    dest = models.CharField(max_length=16)
    status = models.CharField(max_length=7, choices=STATUS)
    code = models.CharField(max_length=2)
    description = models.CharField(max_length=40)
    timestamp = models.DateTimeField()

    def __unicode__(self):
        return u'Report for {}'.format(self.message)
