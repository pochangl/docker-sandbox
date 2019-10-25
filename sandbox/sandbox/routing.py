from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url
from problem import consumers as pconsumers
from worker import consumers as wconsumers

application = ProtocolTypeRouter({
    'websocket': URLRouter([
        url(r'^ws/problem/submission/$', pconsumers.SubmissionConsumer),
        url(r'^ws/worker/$', wconsumers.SandboxWorkerConsumer),
    ])
    # Empty for now (http->django views is added by default)
})
