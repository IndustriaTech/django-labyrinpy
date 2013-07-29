from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from models import Message, Report


def create_report(request):
    msg_id = request.GET.get('msg_id')
    if msg_id:
        report_dict = {
            'message': get_object_or_404(Message, id=msg_id),
            'source': request.GET['source'],
            'dest': request.GET['dest'],
            'status': request.GET['status'],
            'code': request.GET['code'],
            'description': request.GET['description'],
            'timestamp': request.GET['timestamp']}

        Report.objects.create(**report_dict)
    return HttpResponse()
