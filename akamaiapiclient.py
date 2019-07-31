import requests
from akamai.edgegrid import EdgeGridAuth, EdgeRc
#from urllib.parse import urljoin
from urlparse import urljoin
import socket
import json


class AkamaiApiClient:
    edgerc = EdgeRc('.edgerc')
    section = 'default'
    baseurl = 'https://%s' % edgerc.get(section, 'host')

    def __init__(self):
        return

    def dig(self, hostname, location, querytype='A'):
        r""" Run dig on a hostname to get DNS information, associating hostnames and IP addresses

        :param location: location where to run Dig from. IP or location ID
        :param hostname: The hostname to which to run the test.
        :param querytype: The type of DNS record, either A, AAAA, CNAME, MX, NS, PTR, or SOA. The default is A.
        :return: digInfo
        """

        s = requests.Session()
        s.auth = EdgeGridAuth.from_edgerc(self.edgerc, self.section)
        params = {'hostName': hostname,
                  'queryType': querytype}

        try:
            socket.inet_aton(location)
            results = s.get(urljoin(self.baseurl, '/diagnostic-tools/v2/ip-addresses/'+location+'/dig-info'), params=params)
        except socket.error:
            results = s.get(urljoin(self.baseurl, '/diagnostic-tools/v2/ghost-locations/'+location+'/dig-info'), params=params)
        return results

    def estats(self, cpcode):
        r""" Get error statistics on a CP code's traffic from edge servers to both clients and the origin.
        Specify a cpCode parameter in the request.
        HTTP/1.1 202 Accepted
        Connection: keep-alive
        Content-Length: 93
        Content-Type: application/json;charset=UTF-8
        Date: Mon, 20 May 2019 04:58:10 GMT
        X-IDS-SESSION-ID: c0370dd8-6c00-43ba-b729-103481ac9c3c
        X-RateLimit-Limit: 10
        X-RateLimit-Remaining: 9
        X-Trace-Id: 99fe5ce233e101d5

        {
            "link": "/diagnostic-tools/v2/estats-requests/5366734",
            "requestId": "5366734",
            "retryAfter": 10
        }


        :param cpcode: The CP code for which to retrieve error statistics.
        :return:
        """
        if not cpcode:
            return "Please enter valid CP Code"
        s = requests.Session()
        s.auth = EdgeGridAuth.from_edgerc(self.edgerc, self.section)
        results = s.post(urljoin(self.baseurl, '/diagnostic-tools/v2/cpcodes/'+cpcode+'/estats'))
        return results

    def check_asyncresults(self, link):
        r""" After running the Launch an Error Stats Request operation, this checks the status of an asynchronous request for data.
        A 200 PollResponse with a Retry-After header indicates the request is still processing.
        When the data is ready, a 303 response provides a Location header where you can GET the data using the Get Error Statistics
        Asynchronously operation.
        HTTP/1.1 200 OK
        Connection: keep-alive
        Content-Length: 93
        Content-Type: application/json;charset=UTF-8
        Date: Mon, 20 May 2019 04:58:45 GMT
        X-IDS-SESSION-ID: bd6130b5-0a0f-48a6-8c80-9ff9bdfc6fab
        X-Trace-Id: 9a745ce2340305a9

        {
            "link": "/diagnostic-tools/v2/estats-requests/5366734",
            "requestId": "5366734",
            "retryAfter": 10
        }

        :param link: Unique identifier for each asynchronous error statistics request, used to track progress.
        For details, see Asynchronous Requests.
        :return:
        """
        if not link:
            return "Provide a correct request ID"

        s = requests.Session()
        s.auth = EdgeGridAuth.from_edgerc(self.edgerc, self.section)
        results = s.get(urljoin(self.baseurl, link), allow_redirects=False)
        return results

    def get_asyncresponse(self, link):
        r""" Shared method to get asynchronous response from API


        :param link: end point. Will be in the previos response body
        :return: JSON
        """
        if not link:
            return "Empty URL"
        s = requests.Session()
        s.auth = EdgeGridAuth.from_edgerc(self.edgerc, self.section)
        results = s.get(urljoin(self.baseurl, link))
        return results

    def error_translate(self, errorcode):
        r""" Get information about error strings produced by edge servers when a request to retrieve content fails.

        :param errorcode: The error reference code to translate. 9.6f64d440.1318965461.2f2b078
        :return: JSON
        """
        if not errorcode:
            return "Enter valid error code"

        s = requests.Session()
        s.auth = EdgeGridAuth.from_edgerc(self.edgerc, self.section)
        results = s.post(urljoin(self.baseurl, '/diagnostic-tools/v2/errors/'+errorcode+'/translate-error'))
        return results

    def get_ghost_locations(self):
        r""" Lists active Akamai edge server locations from which you can run diagnostic tools.
        Use any id value from the response object for use in other ghost location-based operations.

        :return: JSON
        """
        s = requests.Session()
        s.auth = EdgeGridAuth.from_edgerc(self.edgerc, self.section)
        results = s.get(urljoin(self.baseurl, '/diagnostic-tools/v2/ghost-locations/available'))
        return results

    def debug_url(self, url, edgeip=None, headers=None):
        r""" Get various HTTP and DNS information for a URL.
        Specify a url query parameter, and optionally test a specific edgeIp with a given header.

        :param url: The URL for which to gather error statistics.
        :param edgeip: The edge server IP address to test the URL against, otherwise a random server by default.
        :param headers: Any additional headers to add to the request. Repeat the parameter to specify more than one header.
        :return:
        """

        if not url:
            return "Please enter a valid URL"

        request_body = {'url': url,
                        'edgeIp': edgeip,
                        'headers': headers}
        header = {'content-type': 'application/json'}

        s = requests.Session()
        s.auth = EdgeGridAuth.from_edgerc(self.edgerc, self.section)
        results = s.post(urljoin(self.baseurl, '/diagnostic-tools/v2/url-debug'), data=json.dumps(request_body), headers=header)
        return results


    def mtr(self, location=None, destinationdomain=None, resolvedns='false'):
        r""" Run mtr to check connectivity between a domain and an IP address/location within the Akamai network.

        :param location: location where to run MTR from. IP or location ID
        :param destinationdomain: The domain name to which to test connectivity..
        :param resolvedns: Whether to use DNS to resolve hostnames. When disabled, output features only IP addresses.
        :return: mtrData.json
        """
        if not location:
            return "Please input location"
        if not destinationdomain:
            return "Please enter valid destination domain name"
        s = requests.Session()
        s.auth = EdgeGridAuth.from_edgerc(self.edgerc, self.section)
        params = {'destinationDomain': destinationdomain,
                  'resolveDns': resolvedns}
        try:
            socket.inet_aton(location)
            results = s.get(urljoin(self.baseurl, '/diagnostic-tools/v2/ip-addresses/'+location+'/mtr-data'), params=params)
        except socket.error:
            results = s.get(urljoin(self.baseurl, '/diagnostic-tools/v2/ghost-locations/'+location+'/mtr-data'), params=params)
        return results

    def get_logs(self, locationid, endtime, **kwargs):
        if not endtime:
            return "Please enter end time"

        params = {'locationId': locationid,
                  'endTime': endtime,
                  'arl': kwargs.get("arl"),
                  'clientIp': kwargs.get("clientOp"),
                  'cpCode': kwargs.get("cpCode"),
                  'duration': kwargs.get("duration"),
                  'hostHeader': kwargs.get("hostHeader"),
                  'httpStatusCode': kwargs.get("httpStatusCode"),
                  'logType': kwargs.get("logType"),
                  'maxLogLines': kwargs.get("maxLogLines"),
                  'objStatus': kwargs.get("objStatus"),
                  'requestId': kwargs.get("requestId"),
                  'userAgent': kwargs.get("userAgent")}
        s = requests.Session()
        s.auth = EdgeGridAuth.from_edgerc(self.edgerc, self.section)
        results = s.post(urljoin(self.baseurl, '/diagnostic-tools/v2/ghost-locations/'+locationid+'/log-lines'), params=params)
        return results

    def get_diagnostic_url(self, url, edgeip):
        request_body = {'endUserName': url,
                        'url': edgeip}

        s = requests.Session()

        s.auth = EdgeGridAuth.from_edgerc(self.edgerc, self.section)
        results = s.post(urljoin(self.baseurl, '/diagnostic-tools/v2/end-users/diagnostic-url'), data=request_body)
        return results
