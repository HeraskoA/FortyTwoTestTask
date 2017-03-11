from django.shortcuts import render
from datetime import time
from django.contrib.auth.models import User
from chat.models import Dialog, Message
import json
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def chat(request):
    users = User.objects.all()
    return render(request, 'chat.html', {'users': users})


def ajax(request, user1, dialog):
    response_data = []
    if request.method == 'POST':
        text = request.POST.get('message').strip()
        if text != '':
            Message.objects.create(
                text=text,
                sender=user1,
                dialog=dialog
                )
        return HttpResponse()
    else:
        count = int(request.GET.get('count'))
        messages = Message.objects.filter(dialog=dialog)
        if count < len(messages):
            messages = messages[count:]
            for message in messages:
                response_data.append({
                    'text': message.text,
                    'sender': message.sender.username,
                    'time': time.strftime(message.date, "%H:%M")
                })
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
            )


@login_required
def dialog(request, pk):
    user1 = request.user
    user2 = User.objects.get(id=int(pk))
    try:
        dialog = Dialog.objects.get(user1=user1, user2=user2)
    except Exception:
        dialog, created = Dialog.objects.get_or_create(
                                                user1=user2,
                                                user2=user1
                                                )
    if request.is_ajax():
        return ajax(request, user1, dialog)
    else:
        messages = Message.objects.filter(dialog=dialog)
        count = len(messages)
        return render(request, 'dialog.html', {
            'messages': messages,
            'interlocutor': user2,
            'count': count})
