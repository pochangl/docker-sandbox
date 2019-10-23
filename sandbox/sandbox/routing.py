from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url
from problem import consumers

application = ProtocolTypeRouter({
    'websocket': URLRouter([
        url(r'^ws/problem/submission/$', consumers.SubmissionConsumer),
    ])
    # Empty for now (http->django views is added by default)
})
