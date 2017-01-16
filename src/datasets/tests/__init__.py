"""
Because some views are dependent on the presence of values from previous form
submissions, we need to fake the function called at runtime to say we always
want the addfile_weekly form to be showed
"""
def _show_weekly_for_test(x):
    return True

import datasets.views as v
v.show_weekly_frequency = _show_weekly_for_test



from urllib.parse import parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
import cgi
import json
import os
import requests
import socket


class MockCKANRequestHandler(BaseHTTPRequestHandler):

    def load_file(self, name):
        fname = os.path.dirname(__file__)
        fname = os.path.join(fname, 'data/', name + '.json')
        fname = os.path.abspath(fname)
        return open(fname, 'r').read().strip()

    def log_message(self, fmt, *kwargs):
        pass


    def do_POST(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len).decode("utf-8")
        params = json.loads(str(post_body))

        name = self.path.split('/')[-1]
        response = self.load_file(name)

        if name == 'package_show' \
                and (params.get('id') == 'a-test-dataset-for-create' or
                    params.get('id') == 'a-test-dataset-for-edit'):
            err = {"success": False,
            "error": {
                "message": "Not found",
                "__type": "Not Found Error"
            }}
            response = json.dumps(err)

        if name == 'package_show' \
                and (params.get('id').startswith('new') or
                    params.get('id').startswith('edit')):
            err = {"success": False,
            "error": {
                "message": "Not found",
                "__type": "Not Found Error"
            }}
            response = json.dumps(err)


        self.send_response(requests.codes.ok)
        self.end_headers()

        self.wfile.write(response.encode())

        return


def get_free_port():
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    address, port = s.getsockname()
    s.close()
    return port

mock_port = get_free_port()
mock_server = HTTPServer(('localhost', mock_port), MockCKANRequestHandler)
mock_server_thread = Thread(target=mock_server.serve_forever)
mock_server_thread.setDaemon(True)
mock_server_thread.start()


from django.conf import settings

settings.CKAN_HOST = 'http://localhost:{}'.format(mock_port)
