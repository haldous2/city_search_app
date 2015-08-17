
import unittest
import city_search_app.app as app
from city_search_app.app import *

import mock
from mock import patch
import webtest
from webtest import TestApp

def fake_start_response(status, response_headers, exc_info=None):
    print status
    print response_headers

class TestApp(unittest.TestCase):

    ## Try # 1
    ## error: 'app' is not defined - I think app is the base 'module'.. however, qdCity is not a class
    ##        I really think the @patch only works for classes ??
    #@patch.object(app,'qdCity')
    #def test_app001(self, mock_qd_city):
    #    def __init__(self, app):
    #        self.app = app

    ## Try # 2 using patches and fakeouts
    @patch('city_search_app.app.qdCity')
    @patch('city_search_app.app.dbCity')
    def test_app002(self, mock_dbcity, mock_qdcity):

        mock_dbcity.return_value = [{"city":"Seattle"},{"city":"Seattle Heights"}]
        mock_qdcity.return_value = "Sea"

        self.results = app.application({'QUERY_STRING':'cityx=Sea'}, fake_start_response)

    ## Try # 3 using webtest
    def test_app003(self):

        webapp = webtest.TestApp(app.application)
        resp = webapp.get('/')
        self.assertEquals(resp.status, '200 OK')
