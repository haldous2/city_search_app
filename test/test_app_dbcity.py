
import unittest
import mock
from mock import patch

import city_search_app.city_search_app as app
from city_search_app.city_search_app.app import dbCity, MySQLdb

class fakeCursor(object):

    def execute(self, *args):
        pass

    def fetchall(self, *args):
        return [{"city":"Seattle", "region":"WA", "lat":"1.00", "lon":"2.00"},{"city":"Seattle Heights", "region":"WA", "lat":"1.00", "lon":"2.00"}]

class fakeDB(object):

    def cursor(self, *args):
        return fakeCursor()

class TestDBCity(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch.object(MySQLdb, 'connect')
    def test_db(self, mockMySqlDb):

        mockMySqlDb.return_value = fakeDB()

        self.results = dbCity('Seattl')

        self.assertEqual(self.results, [{"city":"Seattle", "region":"WA", "lat":"1.00", "lon":"2.00"},{"city":"Seattle Heights", "region":"WA", "lat":"1.00", "lon":"2.00"}])
