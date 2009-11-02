import os
import signal
import time
import sys
import unittest
from wsgiref.simple_server import make_server
import livetest
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

class ServerFixture(unittest.TestCase):
    def setUp(self):
        pid = os.fork()
        if pid > 0:
            self.pid = pid
            self.app = livetest.TestApp('localhost:8000')
            # Wait a sec for the server to start. This will actually make the
            # tests faster, too.
            time.sleep(0.1)
        else:
            sys.stderr = StringIO()
            httpd = make_server('', 8000, self.make_app())
            httpd.serve_forever()

    def tearDown(self):
        os.kill(self.pid, signal.SIGKILL)

