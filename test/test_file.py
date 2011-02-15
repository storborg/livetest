from webob import Request
from fixtures import ServerFixture


class TestFileUpload(ServerFixture):
    def make_app(self):
        def app(environ, start_response):
            req = Request(environ)
            status = "200 OK"
            if req.method == 'POST':
                body =\
            """
            <html>
                <head><title>result</title></head>
                <body>
                    <pre>%s</pre>
                </body>
            </html>
            """ % req.params['up'].value
            else:
                body =\
            """
            <html>
                <head><title>form page</title></head>
                <body>
                    <form method="POST" enctype="multipart/form-data">
                        <input type="file" name="up">
                        <input type="submit" value="go">
                    </form>
                </body>
            </html>
            """
            headers = [
                ('Content-Type', 'text/html'),
                ('Content-Length', str(len(body)))]
            start_response(status, headers)
            return [body]
        return app

    def test_file_upload(self):
        resp = self.app.get('/')
        form = resp.forms[0]
        form['up'] = ('test_file.py', file(__file__).read())
        resp = form.submit()
        assert 'TestFileUpload' in resp.body
