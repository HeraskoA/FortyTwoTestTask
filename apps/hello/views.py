# -*- coding: utf-8 -*-
from django.shortcuts import render
from hello.models import UserData, Request
from django.core.serializers import serialize
from django.http import HttpResponse
import json


def home(request):
    data = UserData.objects.first()
    return render(request, 'user_data.html', {"data": data})


def requests(request):
    requests = list(Request.objects.all().order_by('-id')[:10])
    if request.is_ajax():
        difference = Request.objects.count() - int(request.GET.get('frontend_requests'))
        return HttpResponse(
            json.dumps(serialize("json", requests[:difference])),
            content_type="application/json"
        )
    requests.reverse()
    return render(request, 'requests.html', {
        "requests": requests,
        "count": Request.objects.count()
    })
