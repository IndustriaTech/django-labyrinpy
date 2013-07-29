# Create your views here.
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from models import Message, Report
# from forms import SendMessageForm
from django.http import HttpResponseRedirect
# from django.forms.models import inlineformset_factory
# from django.views import generic

# ALL VIEW FUNCTIONS MUST RETURN HttpResponse() as it is
# HttpRequest() we send to them (urls -> funct_from_here -> func does sth)


def home(request):
    pass


def search(request):
    error = False
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            error = True
        else:
            messages = Message.objects.filter(destination__icontains=q)
            return render(request, 'search_result.html',
                          {'messages': messages, 'query': q})
    return render(request, 'search_form.html',
                  {'error': error})


# def message(request):
#     if request.method == 'POST':
#         form = SendMessageForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             Message.objects.create(**cd)
#             return HttpResponseRedirect('/message/thanks/')
#     else:
#         form = SendMessageForm(
#             initial={'message_type': 'text'})
#     return render(request, 'send_message.html', {'form': form})


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
