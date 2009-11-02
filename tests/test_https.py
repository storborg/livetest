import livetest

def test_unsupported_schema():
    try:
        app = livetest.TestApp('localhost', schema='ldap')
    except ValueError:
        pass
    else:
        raise AssertionError("unsupported schema should fail")


def test_https():
    app = livetest.TestApp('www.google.com', schema='https')
    resp = app.get('/')
    assert resp.status_int == 302
