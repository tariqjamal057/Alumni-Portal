from django.shortcuts import render
from .models import Event

def index(request):
    event = Event.objects.all()
    # mainevent = Event.objects.filter(main_event == 'Yes')
    context = {
        'event':event,
        # 'mainevent':mainevent
    }
    return render(request , 'index.html', context)

# def event(request):
#     event = Event.objects.all()
#     context = {
#         'event':event
#     }
#     return render(request , 'event.html', context)