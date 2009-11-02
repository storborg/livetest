from webob import Request
from fixtures import ServerFixture


class TestInput(ServerFixture):
    def make_app(self):
        def input_app(environ, start_response):
            req = Request(environ)
            status = "200 OK"
            body =\
        """
        <html>
            <head><title>form page</title></head>
            <body>
                <form method="POST" id="text_input_form">
                    <input name="foo" type="text" value="bar">
                    <input name="button" type="submit" value="text">
                </form>
                <form method="POST" id="radio_input_form">
                    <input name="foo" type="radio" value="bar">
                    <input name="foo" type="radio" value="baz" checked>
                    <input name="button" type="submit" value="radio">
                </form>
                <form method="POST" id="checkbox_input_form">
                    <input name="foo" type="checkbox" value="bar" checked>
                    <input name="button" type="submit" value="text">
                </form>
            </body>
        </html>
        """
            headers = [
                ('Content-Type', 'text/html'),
                ('Content-Length', str(len(body)))]
            start_response(status, headers)
            return [body]
        return input_app

    def test_input(self):
        res = self.app.get('/')
        assert res.status_int == 200
        assert res.headers['content-type'] == 'text/html'
        assert res.content_type == 'text/html'

        form = res.forms['text_input_form']
        assert form['foo'].value == 'bar'
        assert form.submit_fields() == [('foo', 'bar')]

        form = res.forms['radio_input_form']
        assert form['foo'].value == 'baz'
        assert form.submit_fields() == [('foo', 'baz')]

        form = res.forms['checkbox_input_form']
        assert form['foo'].value == 'bar'
        assert form.submit_fields() == [('foo', 'bar')]


class TestInputNoDefault(ServerFixture):
    def make_app(self):
        def input_app_without_default(environ, start_response):
            req = Request(environ)
            status = "200 OK"
            body =\
        """
        <html>
            <head><title>form page</title></head>
            <body>
                <form method="POST" id="text_input_form">
                    <input name="foo" type="text">
                    <input name="button" type="submit" value="text">
                </form>
                <form method="POST" id="radio_input_form">
                    <input name="foo" type="radio" value="bar">
                    <input name="foo" type="radio" value="baz">
                    <input name="button" type="submit" value="radio">
                </form>
                <form method="POST" id="checkbox_input_form">
                    <input name="foo" type="checkbox" value="bar">
                    <input name="button" type="submit" value="text">
                </form>
            </body>
        </html>
        """
            headers = [
                ('Content-Type', 'text/html'),
                ('Content-Length', str(len(body)))]
            start_response(status, headers)
            return [body]
        return input_app_without_default

    def test_input_no_default(self):
        res = self.app.get('/')
        assert res.status_int == 200
        assert res.headers['content-type'] == 'text/html'
        assert res.content_type == 'text/html'

        form = res.forms['text_input_form']
        assert form['foo'].value == ''
        assert form.submit_fields() == [('foo', '')]

        form = res.forms['radio_input_form']
        assert form['foo'].value is None
        assert form.submit_fields() == []

        form = res.forms['checkbox_input_form']
        assert form['foo'].value is None
        assert form.submit_fields() == []
