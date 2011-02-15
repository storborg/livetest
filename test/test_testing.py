from webtest.debugapp import debug_app
from fixtures import ServerFixture


def raises(exc, func, *args, **kw):
    try:
        func(*args, **kw)
    except exc:
        pass
    else:
        raise AssertionError(
            "Expected exception %s from %s"
            % (exc, func))


class TestBasic(ServerFixture):
    def make_app(self):
        return debug_app

    def test_testing(self):
        res = self.app.get('/')
        assert res.status_int == 200
        assert res.headers['content-type'] == 'text/plain'
        assert res.content_type == 'text/plain'
        res = self.app.request('/', method='GET')
        assert res.status_int == 200
        assert res.headers['content-type'] == 'text/plain'
        assert res.content_type == 'text/plain'
        self.app.get('/?status=404%20Not%20Found', status=404)

        class FakeDict(object):
            def items(self):
                return [('a', '10'), ('a', '20')]
        res = self.app.post('/params', params=FakeDict())
