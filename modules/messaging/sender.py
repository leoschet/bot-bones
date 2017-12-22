import os

class Sender(object):
    _request_uri = 'https://graph.facebook.com/v2.6/me/messages?access_token=<PAGE_ACCESS_TOKEN>'

    @property
    def request_uri(self):
        return self._request_uri.replace('<PAGE_ACCESS_TOKEN>', os.environ["PAGE_ACCESS_TOKEN"])