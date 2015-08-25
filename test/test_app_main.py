
import unittest
import mock
from mock import patch
import webtest
from webtest import TestApp

import city_search_app.city_search_app.app as app
import MySQLdb

class fakeCursor(object):

    def execute(self, *args):
        pass

    def fetchall(self, *args):
        return [{"city":"Seattle", "region":"WA", "lat":"1.00", "lon":"2.00"},{"city":"Seattle Heights", "region":"WA", "lat":"1.00", "lon":"2.00"}]

class fakeDB(object):

    def cursor(self, *args):
        return fakeCursor()

def fake_start_response(status, response_headers, exc_info=None):
    #print status
    #print response_headers
    pass

class TestApp(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    ## Try # 1 using patches and fakeouts
    @patch('city_search_app.city_search_app.app.qdCity')
    @patch('city_search_app.city_search_app.app.dbCity')
    def test_appmksuccess(self, mock_dbcity, mock_qdcity):
        """
        Looking for json output string using mocked data
        """
        mock_dbcity.return_value = [{"city":"Seattle"},{"city":"Seattle Heights"}]
        mock_qdcity.return_value = "Sea"

        self.results = app.application({'QUERY_STRING':'city=Sea'}, fake_start_response)

        self.assertEquals(self.results, ['{"qs":"Sea","cities":[{"city": "Seattle"}, {"city": "Seattle Heights"}]}'])

    ## Try #  using webtest
    def test_appwtstatus200(self):
        """
        Looking for response status 200 OK
        """
        webapp = webtest.TestApp(app.application)
        resp = webapp.get('/')
        self.assertEquals(resp.status, '200 OK')

    def test_appwterror(self):
        """
        Looking for error response when no querystring passed
        """
        webapp = webtest.TestApp(app.application)
        resp = webapp.get('/')
        self.assertEquals(resp.body, "{'error':'city search string not passed'}")

    @patch.object(MySQLdb, 'connect')
    def test_appwtsuccess(self, mockMySqlDb):
        """
        Looking for json output string using mocked data
        """
        mockMySqlDb.return_value = fakeDB()

        webapp = webtest.TestApp(app.application)
        resp = webapp.get('/?city=Sea')

        self.assertEquals(resp.body, '{"qs":"Sea","cities":[{"lat": "1.00", "city": "Seattle", "region": "WA", "lon": "2.00"}, {"lat": "1.00", "city": "Seattle Heights", "region": "WA", "lon": "2.00"}]}')
