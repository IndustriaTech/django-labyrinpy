from datetime import datetime

from django.core.urlresolvers import reverse
from django.test import client, TestCase
from django.utils.timezone import utc

from models import Report, Message

DATA_FOR_REPORT = {
    'msg_id': 1,
    'source': '16130',
    'dest': '359 88 66 66 66',
    'status': 'OK',
    'code': 0,
    'description': 'Message delivered',
    'timestamp': datetime(2013, 0o7, 22, 10, 0o4, 55).replace(tzinfo=utc)
}

SMS_SEND = {
    'destination': 'unknown',
    'message_type': 'text',
    'content': 'some test going around here',

    'source_name': 'Company',
    'source': '16130',
    'service': 'ORDER',
    'header': '060504158A0000',
    'wap_text': '060504158A0000',
    'class': 'normal',
    'concatenate': False,
    'unicode': True,
    'validity': '1440',
    'delivery': '60'
}

INVALID_SMS = {
    'destination': 'unknown',
    # message_type - missing but it's a must
    'content': 'some test going around here',
    'source_name': 'Company',
    'unicode': True
}

VALID_SMS_NO_OPTIONAL = {
    'destination': 'unknown',
    'message_type': 'text',
    'content': 'some test going around here'
}


class CreateReport(TestCase):

    def setUp(self):
        self.query_string = DATA_FOR_REPORT.copy()
        self.client = client.Client()

    def tearDown(self):
        pass

    def test_report_has_been_created(self):
        Message.objects.create(destination="123", message_type="text", id=1)
        reports_before = Report.objects.all().count()
        self.client.get(reverse('create-report'), self.query_string)
        reports_after = Report.objects.all().count()
        self.assertTrue(reports_after > reports_before)

    def test_report_for_nonexistant_message(self):
        Message.objects.create(destination="unkn", message_type="text", id=2)
        respond = self.client.get(reverse('create-report'), self.query_string)
        self.assertEqual(404, respond.status_code)

    def test_report_for_message_that_already_has_report(self):
        Message.objects.create(destination='123', message_type='text', id=1)
        self.client.get(reverse('create-report'), self.query_string)
        respond = self.client.get(reverse('create-report'), self.query_string)
        reports_after = Report.objects.all().count()
        self.assertEqual((2, 200), (reports_after, respond.status_code))


class SendSMS(TestCase):

    def setUp(self):
        self.query_string = SMS_SEND.copy()
        self.invalid_sms = INVALID_SMS.copy()
        self.no_optional = VALID_SMS_NO_OPTIONAL.copy()

    def tearDown(self):
        pass

    def test_send_sms(self):
        messages_before = Message.objects.count()
        Message.send(**self.query_string)
        messages_after = Message.objects.count()
        self.assertTrue(messages_after > messages_before)

    def test_for_invalid_sms(self):
        with self.assertRaises(TypeError):
            Message.send(**self.invalid_sms)

    def test_send_sms_no_optional(self):
        messages_before = Message.objects.count()
        Message.send(**self.no_optional)
        messages_after = Message.objects.count()
        self.assertTrue(messages_after > messages_before)
