"""
LiveTest - Like WebTest, but on a live site.

Setup an app to test against with just a hostname:

>>> import livetest
>>> app = livetest.TestApp('www.google.com')

Make requests just like WebTest:

>>> resp = app.get('/')

Grab forms:

>>> resp.forms # doctest: +ELLIPSIS
{0: <webtest.Form object at 0x...>}
>>> form = resp.forms[0]
>>> form.fields # doctest: +ELLIPSIS
{'btnI': [<webtest.Submit object at 0x...>], 'btnG': [<webtest.Submit object at 0x...>], 'q': [<webtest.Text object at 0x...>], 'source': [<webtest.Hidden object at 0x...>], 'hl': [<webtest.Hidden object at 0x...>], 'ie': [<webtest.Hidden object at 0x...>]}

Submit forms:

>>> form['q'] = 'python testing'
>>> resp = form.submit()

Test stuff in the response:

>>> resp.mustcontain('Agile', 'unittest', 'PyUnit')
>>> resp.status
'200 OK'

"""

__author__ = 'scott@crookedmedia.com'

import webtest
import httplib
from webtest import BaseCookie, CookieError


class TestApp(webtest.TestApp):
    def __init__(self, host, schema='http'):
        if schema == 'http':
            self.conn = httplib.HTTPConnection(host)
        elif schema == 'https':
            self.conn = httplib.HTTPSConnection(host)
        else:
            raise ValueError("Schema '%s' is not supported." % schema)
        self.extra_environ = {}
        self.reset()

    def _send_httplib_request(self, req):
        "Convert WebOb Request to httplib request."
        headers = dict((name, val) for name, val in req.headers.iteritems()
                       if name != 'Host')
        self.conn.request(req.method, req.path_qs, req.body, headers)

    def _receive_httplib_request(self):
        "Convert httplib response to WebOb Response."
        webresp = self.conn.getresponse()
        res = webtest.TestResponse()
        res.status = '%s %s' % (webresp.status, webresp.reason)
        res.body = webresp.read()
        res.headerlist = webresp.getheaders()
        res.errors = ''
        return res

    def do_request(self, req, status, expect_errors):
        """
        Override webtest.TestApp's method so that we do real HTTP requests
        instead of WSGI calls.
        """
        headers = {}
        if self.cookies:
            c = BaseCookie()
            for name, value in self.cookies.items():
                c[name] = value
            headers['HTTP_COOKIE'] = str(c).split(': ', 1)[1]

        self._send_httplib_request(req)

        res = self._receive_httplib_request()
        # Set these attributes for consistency with webtest.
        res.request = req
        res.test_app = self

        if not expect_errors:
            self._check_status(res.status_int, res)
            self._check_errors(res)
        res.cookies_set = {}

        for header in res.headers.getall('set-cookie'):
            try:
                c = BaseCookie(header)
            except CookieError, e:
                raise CookieError(
                    "Could not parse cookie header %r: %s" % (header, e))
            for key, morsel in c.items():
                self.cookies[key] = morsel.value
                res.cookies_set[key] = morsel.value
        return res
