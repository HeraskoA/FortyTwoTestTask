# -*- coding: utf-8 -*-
from django.shortcuts import render
from hello.models import UserData


def home(request):
    data = UserData.objects.first()
    return render(request, 'user_data.html', {"data": data})
