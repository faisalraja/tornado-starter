from authomatic.adapters import BaseAdapter


class TornadoWebAdapter(BaseAdapter):
    """Authomatic Adapter for Tornado"""
    def __init__(self, handler):
        self.request = handler.request
        self.handler = handler

    @property
    def url(self):
        return self.request.full_url().split('?').pop(0)

    @property
    def params(self):
        return dict((k, self.handler.get_argument(k, None)) for k in self.request.arguments)

    @property
    def cookies(self):
        cookies = dict(self.request.cookies)
        return dict((k, str(cookies[k].value)) for k in cookies)

    def write(self, value):
        self.handler.write(value)

    def set_header(self, key, value):
        self.handler.set_header(key, value)

    def set_status(self, status):
        status_code, reason = status.split(' ', 1)
        self.handler.set_status(int(status_code), status)
