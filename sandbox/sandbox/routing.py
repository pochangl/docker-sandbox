from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from problem import consumers as pconsumers
from worker import consumers as wconsumers

application = ProtocolTypeRouter({
    'websocket': URLRouter([
        path('ws/problem/submission/', pconsumers.SubmissionConsumer),
        path('ws/worker/', wconsumers.SandboxWorkerConsumer),
    ])
    # Empty for now (http->django views is added by default)
})
