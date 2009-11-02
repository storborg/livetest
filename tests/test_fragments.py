from webob import Request
from fixtures import ServerFixture
from webtest.debugapp import debug_app


class TestInput(ServerFixture):
    def make_app(self):
        return debug_app

    def test_url_without_fragments(self):
        res = self.app.get('http://localhost/')
        assert res.status_int == 200

    def test_url_with_fragments(self):
        res = self.app.get('http://localhost/#ananchor')
        assert res.status_int == 200
