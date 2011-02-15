import livetest


def test_unsupported_schema():
    try:
        app = livetest.TestApp('localhost', scheme='ldap')
    except ValueError:
        pass
    else:
        raise AssertionError("unsupported scheme should fail")


def test_https():
    app = livetest.TestApp('www.google.com', scheme='https')
    resp = app.get('https://www.google.com')
    assert resp.status_int == 302
