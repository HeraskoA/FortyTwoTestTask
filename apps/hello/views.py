# -*- coding: utf-8 -*-
from django.shortcuts import render
from hello.models import UserData, Request
from django.core.serializers import serialize
from django.http import HttpResponse
import json
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView
from hello.forms import UserDataForm


def home(request):
    data = UserData.objects.first()
    return render(request, 'user_data.html', {"data": data})


def requests_post(request):
    instance_id = int(request.POST.get('req_id'))
    instance = Request.objects.get(id=instance_id)
    try:
        instance.priority = int(request.POST.get('priority'))
        if instance.priority < 1:
            raise Exception()
    except Exception:
        return HttpResponse(
            json.dumps(0),
            content_type="application/json"
        )
    else:
        instance.save()
        return HttpResponse(
            json.dumps(1),
            content_type="application/json"
        )


def requests(request):
    requests = list(Request.objects.all().order_by('-id')[:10])
    if request.is_ajax():
        if request.method == "POST":
            return requests_post(request)
        else:
            frontend_requests = int(request.GET.get('frontend_requests'))
            difference = Request.objects.count() - frontend_requests
            return HttpResponse(
                json.dumps(serialize("json", requests[:difference])),
                content_type="application/json"
            )
    else:
        if request.GET.get('order'):
            sort = int(request.GET.get('order'))
            requests = sorted(requests, key=lambda k: k.priority)
            if sort == 0:
                requests.reverse()
        requests.reverse()
        return render(request, 'requests.html', {
            'count': Request.objects.count(),
            'requests': requests
            })


class Edit(UpdateView):
    model = UserData
    form_class = UserDataForm
    template_name = 'edit.html'

    def json_response(self, context):
        return HttpResponse(
            json.dumps(context),
            content_type="application/json"
        )

    def form_invalid(self, form):
        if self.request.is_ajax():
            return self.json_response(form.errors)
        return super(UpdateView, self).form_invalid(form)

    def form_valid(self, form):
        if self.request.is_ajax():
            form.save()
            return self.json_response([1])
        return super(UpdateView, self).form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UpdateView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('home')
