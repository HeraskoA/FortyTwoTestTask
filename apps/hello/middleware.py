# -*- coding: utf-8 -*-
from hello.models import Request
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

pnconfig = PNConfiguration()
pnconfig.subscribe_key = "sub-c-49c47702-067f-11e7-b34d-02ee2ddab7fe"
pnconfig.publish_key = "pub-c-154a7313-6d0a-4b45-bc9a-4464eb536bc8"
pnconfig.ssl = False

pubnub = PubNub(pnconfig)


class SaveRequestMiddleware(object):
    def process_request(self, request):
        if not (request.is_ajax() and request.GET.get('frontend_requests')):
            data = {}
            data['path'] = request.path
            data['method'] = request.method
            Request.objects.create(**data)
            pubnub.publish().channel('requests').message("1").sync()
        return None
