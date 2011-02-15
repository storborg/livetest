from webob import Request, Response
from fixtures import ServerFixture
from Cookie import CookieError


class TestCookies(ServerFixture):
    def make_app(self):
        def input_app(environ, start_response):
            req = Request(environ)
            res = Response()
            res.body =\
        ("""
        <html>
            <head><title>cookies</title></head>
            <body>
                <pre>Taste: [%s]</pre>
            </body>
        </html>
        """ % req.cookies.get('taste')).encode('ascii')
            if req.params.get('gimme'):
                # Set a new cookie.
                res.set_cookie('taste', 'yummy')
            return res(environ, start_response)
        return input_app

    def test_cookie_roundtrip(self):
        # Should be no cookies.
        resp = self.app.get('/')
        assert 'Taste: [None]' in resp.body

        # Still should be no cookie mentioned in response.
        resp = self.app.get('/?gimme=yes')
        assert 'Taste: [None]' in resp.body

        # Now the server should get the cookie.
        resp = self.app.get('/')
        assert 'Taste: [yummy]' in resp.body


class TestCookiesMalformed(ServerFixture):
    def make_app(self):
        def app(environ, start_response):
            req = Request(environ)
            status = "200 OK"
            body = 'hello'
            headers = [
                ('Content-Type', 'text/html'),
                ('Content-Length', str(len(body))),
                ('Set-Cookie', 'bad:cookie=error')]
            start_response(status, headers)
            return [body]
        return app 

    def test_cookie_malformed(self):
        try:
            self.app.get('/')
        except CookieError:
            pass
        else:
            raise AssertionError("CookieError should result if server sends a "
                                 "malformed Set-Cookie header")
