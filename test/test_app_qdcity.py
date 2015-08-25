
import unittest

import city_search_app.city_search_app.app as app
from city_search_app.city_search_app.app import qdCity

import urllib2

class TestQDCity(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_nocityinqd(self):
        """
         testing qdCity exception when 'city' not in querydata string dict
        """
        self.qd = {'cityx':['Sea']}
        self.assertRaises(SystemError, qdCity, (self.qd))

    def test_parseqscity(self):
        """
         testing qdCity urllib2 to see if it parses %20 and + to spaces
         urllib2.urlparse.parse_qs returns a dict
        """
        self.qcity = "city=S %20e +a"
        self.assertEqual(urllib2.urlparse.parse_qs(self.qcity), {"city":["S  e  a"]})

    def test_cityinqd(self):
        """
         testing qdCity positive test for city in query dict
        """
        self.qd = {'city':['Sea']}
        self.assertEqual(qdCity(self.qd), "Sea")

    def test_qcitysinglespaces(self):
        """
        test qdCity returns city string with only single spaces in string
        """
        self.qd = {'city':['Se   a   tt']}
        self.assertEqual(qdCity(self.qd), "Se a tt")

    def test_qcitytrimspaces(self):
        """
        test qdCity returns city string with spaces trimmed from ends
        """
        self.qd = {'city':[' Sea ']}
        self.assertEqual(qdCity(self.qd), "Sea")

    def test_cityempty(self):
        """
         testing qdCity exception when 'city' is blank
        """
        self.qd = {'city':[' ']}
        self.assertRaises(SystemError, qdCity, (self.qd))
