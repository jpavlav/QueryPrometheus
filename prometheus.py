"""Prometheus python client."""

import requests
from requests import HTTPError
from requests.compat import urljoin


class Prometheus(object):
    """Simple prometheus querying client."""

    SUCCESS_STATUSES = ['success']
    ERROR_STATUSES = ['error']

    def __init__(self, prom_host, port=9090, req_obj=None,
                 api_version='/api/v1/'):
        """Init method."""
        self.hostname = prom_host
        self.port = port
        self._req_obj = req_obj
        self.api_version = api_version

    @property
    def request_session(self):
        """Work with requests object."""
        if not self._req_obj:
            self._req_obj = requests.Session()
        return self._req_obj

    def _check_response(self, req):
        """Check responses are what we expect."""
        if (req.status_code == requests.codes.ok
                and req.json()['status'] in self.SUCCESS_STATUSES):
            return True
        elif (req.status_code == requests.codes.ok
                and req.json()['status'] in self.ERROR_STATUSES):
            raise ValueError('{} ==> {}'.format(req.json()['errorType'],
                             req.json()['error']))
        else:
            raise HTTPError('{} ==> {}'.format(req.status_code, req.text))

    def _make_request(self, method="GET", route="/", **kwargs):
        _host = "{}:{}".format(self.hostname, self.port)
        route = urljoin(_host, route)
        r = self.request_session.request(method, route, **kwargs)
        return r

    def instant_query(self, query):
        """Query api at single point in time."""
        route = "{}query".format(self.api_version)
        r = self._make_request("GET", route, params=query)
        if self._check_response(r):
            return r.json()

    def range_query(self, query):
        """Query api over a range of time."""
        route = "{}query_range".format(self.api_version)
        r = self._make_request("GET", route, params=query)
        if self._check_response(r):
            return r.json()

    def metadata_series_query(self, query):
        """Query api, return time series that match a certain label set."""
        route = "{}series".format(self.api_version)
        r = self._make_request("GET", route, params=query)
        if self._check_response(r):
            return r.json()

    def metadata_label_query(self, label):
        """Query api for values returned from label matching."""
        route = "{}label/{}/values".format(self.api_version, label)
        r = self._make_request("GET", route)
        if self._check_response(r):
            return r.json()

    def target_query(self):
        """Query api for target discovery."""
        route = "{}targets".format(self.api_version)
        r = self._make_request("GET", route)
        if self._check_response(r):
            return r.json()

    def alertmanager_query(self):
        """Query api for information about existing alertmanagers."""
        route = "{}alertmanagers".format(self.api_version)
        r = self._make_request("GET", route)
        if self._check_response(r):
            return r.json()

    def status_config_query(self):
        """Query prometheus about it's own config."""
        route = "{}status/config".format(self.api_version)
        r = self._make_request("GET", route)
        if self._check_response(r):
            return r.json()

    def status_flag_query(self):
        """Query prometheus about the flags it was configured with."""
        route = "{}status/flags".format(self.api_version)
        r = self._make_request("GET", route)
        if self._check_response(r):
            return r.json()
