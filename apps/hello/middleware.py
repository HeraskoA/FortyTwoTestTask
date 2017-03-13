# -*- coding: utf-8 -*-
from hello.models import Request


class SaveRequestMiddleware(object):
    def process_request(self, request):
        if not (request.is_ajax() and request.GET.get('frontend_requests')):
            data = {}
            data['path'] = request.path
            data['method'] = request.method
            Request.objects.create(**data)
        return None
