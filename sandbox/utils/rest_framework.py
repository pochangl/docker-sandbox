import json
from functools import wraps
from django.urls import reverse
from rest_framework.test import APIClient


class APIMixin:
    def get_client(self):
        return APIClient()


def default_client(func):
    ''' decorator for providing default client if not given '''
    @wraps(func)
    def wrapper(self, **kwargs):
        kwargs['client'] = kwargs.get('client', self.get_client())
        return func(self=self, **kwargs)
    return wrapper


def enrich_content(func):
    ''' convert response.content to ptyhon primitive types '''

    @wraps(func)
    def wrapper(self, **kwargs):
        response = func(self=self, **kwargs)
        json_text = str(response.content, encoding='utf8')
        response.json = json.loads(json_text)
        return response
    return wrapper


class ViewsetTestMixin(APIMixin):
    view_name = None
    request_format = 'json'

    def get_detail_url(self, pk):
        return reverse('{}-detail'.format(self.view_name), kwargs=dict(pk=pk))

    def get_list_url(self):
        return reverse('{}-list'.format(self.view_name))

    @enrich_content
    @default_client
    def api_retrieve(self, client: APIClient, pk: int):
        return client.get(self.get_detail_url(pk), format=self.request_format)

    @enrich_content
    @default_client
    def api_list(self, client: APIClient):
        return client.get(self.get_list_url(), format=self.request_format)

    @enrich_content
    @default_client
    def api_create(self, client: APIClient, data: dict):
        return client.post(self.get_list_url(), data, format=self.request_format)

    @enrich_content
    @default_client
    def api_update(self, client: APIClient, pk: int, data: dict):
        return client.put(self.get_detail_url(pk), data, format=self.request_format)

    @default_client
    def api_delete(self, client: APIClient, pk: int):
        return client.put(self.get_detail_url(pk), format=self.request_format)
