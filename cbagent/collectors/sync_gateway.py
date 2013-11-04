import requests

from cbagent.collectors import Collector
from cbagent.stores import SerieslyStore
from cbagent.metadata_client import MetadataClient


class SyncGateway(Collector):

    COLLECTOR = "sync_gateway"

    def __init__(self, settings):
        self.interval = settings.interval

        self.cluster = settings.cluster
        self.store = SerieslyStore(settings.seriesly_host)
        self.mc = MetadataClient(settings)

        self.nodes = settings.sync_gateway_nodes
        self.stats_api = "http://{0}:4985/_stats"

    @staticmethod
    def _fetch_stats(node):
        stats_api = "http://{0}:4985/_stats".format(node)
        for _, stats in requests.get(url=stats_api).json().items():
            for metric, value in stats.items():
                if type(value) == int:  # can't use isinstance because of bool
                    yield metric, value

    def update_metadata(self):
        self.mc.add_cluster()
        for node in self.nodes:
            self.mc.add_server(node)
            for metric, _ in self._fetch_stats(node):
                self.mc.add_metric(metric, server=node,
                                   collector=self.COLLECTOR)

    def sample(self):
        for node in self.nodes:
            samples = dict(stats for stats in self._fetch_stats(node))
            self.store.append(samples, cluster=self.cluster, server=node,
                              collector=self.COLLECTOR)
