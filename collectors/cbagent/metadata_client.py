import requests


def post_request(request):
    def wrapper(*args, **kargs):
        url, params = request(*args, **kargs)
        requests.post(url, params)
    return wrapper


class MetadataClient(object):

    def __init__(self, settings, host="127.0.0.1"):
        self.settings = settings
        self.base_url = "http://{0}:8000/cbmonitor".format(host)

    @post_request
    def add_cluster(self):
        url = self.base_url + "/add_cluster/"
        params = {"name": self.settings.cluster,
                  "rest_username": self.settings.rest_username,
                  "rest_password": self.settings.rest_password}
        return url, params

    @post_request
    def add_server(self, address):
        url = self.base_url + "/add_server/"
        params = {"address": address,
                  "cluster": self.settings.cluster,
                  "ssh_username": self.settings.ssh_username,
                  "ssh_password": self.settings.ssh_password}
        return url, params

    @post_request
    def add_bucket(self, name):
        url = self.base_url + "/add_bucket/"
        params = {"name": name, "type": "Couchbase",
                  "cluster": self.settings.cluster}
        return url, params

    @post_request
    def add_metric(self, name, bucket=None, server=None):
        url = self.base_url + "/add_metric_or_event/"
        params = {"name": name, "type": "metric",
                  "cluster": self.settings.cluster}
        if server:
            params["server"] = server
        if bucket:
            params["bucket"] = bucket
        return url, params
