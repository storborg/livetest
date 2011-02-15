LiveTest - Like WebTest, but on a live site
===========================================

Inspired by Ian Bicking's excellent `WebTest <http://pythonpaste.org/webtest/>`_, this is an extension to allow the same sort of simple pythonic testing to be used against running sites. Many tests written for WebTest will be able to be used directly on LiveTest.

This enables the full platform (app servers, load balancers, routing, DNS, etc) to be tested rather than just the internal WSGI application.

*Note: File uploads are untested.*

Usage
-----

Setup an app to test against with just a hostname:

>>> import livetest
>>> app = livetest.TestApp('www.google.com')

Make requests just like WebTest:

>>> resp = app.get('/')

Grab forms:

>>> resp.forms
{0: <webtest.Form object at 0x10118ac50>}
>>> form = resp.forms[0]
>>> form.fields
{'btnI': [<webtest.Submit object at 0x10118ae10>],
 'btnG': [<webtest.Submit object at 0x10118add0>],
 'q': [<webtest.Text object at 0x10118ad90>],
 'source': [<webtest.Hidden object at 0x10118ad10>],
 'hl': [<webtest.Hidden object at 0x10118acd0>],
 'ie': [<webtest.Hidden object at 0x10118ad50>]}

Submit forms:

>>> form['q'] = 'python testing'
>>> resp = form.submit()

Test stuff in the response:

>>> resp.mustcontain('Agile', 'unittest', 'PyUnit')
>>> resp
<200 OK text/html body='<!doctype...v>  '/25498>
>>> resp.status
'200 OK'


Credits
-------
Thanks to Edward Dale (scompt) for various fixes.
