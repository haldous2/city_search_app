
import sys
import unittest
import re
import datetime
import json
import urllib2
import MySQLdb
from MySQLdb import cursors
import mock
from mock import patch

def qdCity(qd):

    """
     return qcity string from query data
    """
    qcity = ""

    if "city" in qd:

        # dictionary value returned as a list since querystrings can have multiple values
        # we only need the first one, let's grab that @ 0
        qcity = qd["city"][0][:100]

        # remove leading and trailing spaces
        qcity = qcity.strip(' ')

        # strip
        # clear up any double space(s) that might have occured from previous step
        while len(list(re.finditer('  ', qcity))):
            qcity = re.sub('  ', ' ', qcity)

        # next steps will be to regx out invalid chars
        qcity = ''.join(re.findall( r'[a-zA-Z0-9-_\' ]', qcity))

        # make sure city string is at least 3 alphs long, db will be happier
        if len(qcity) < 3:
            raise SystemError('city search string should be at least three alphanumerics long')

    else:

        raise SystemError('city search string not passed')

    return qcity

def dbCity(qcity):

    cities = []

    db = MySQLdb.connect(host="localhost", user="username", passwd="****supersecret****", db="citydb")

    # Note: DictCursor creates associate 'array' dict rows (yay!)
    # Note: Database driver (MySQLdb in this case) will handle escaping strings to thwart
    #       SQL injection.. no need to addslashes/escape search vars.. cursor.execute is the mechanism
    #cur = db.cursor()
    cur = db.cursor(cursors.DictCursor)
    if len(qcity) > 0:
        cur.execute("SELECT * FROM loc_cities where city like %s", ("" + qcity + "%",))
        rows = cur.fetchall()
    else:
        rows = []

    for row in rows:
        #cities.append({"city":row.get("city",''), "region":row["region"], "lat":str(row["lat"]), "lon":str(row["lon"])})
        cities.append({"city":row.get("city",'')})

    return cities

def application(env, start_response):

    print type(start_response)

    try:

        stime = datetime.datetime.now()

        # extract querystring from uwsgi environment variables
        # convert to dictionary in qd and then cleanup city string
        qs = env["QUERY_STRING"]
        qd = urllib2.urlparse.parse_qs(qs) # returns dict of querystring arguments

        qcity = qdCity(qd)
        cities = dbCity(qcity)

        etime = datetime.datetime.now()
        rtime = etime - stime
        ttime = str(rtime.total_seconds() * 1000) # milliseconds

        # Need this to happen:
        # {"query":"seattle","milliseconds":"2","cities":[{"city":"seattle"},{"city":"seatown"}]}
        html = "{"
        html += "\"qs\":\"{}\",".format(qcity)
        html += "\"ms\":\"{}\",".format(ttime)
        html += "\"cities\":{}".format(json.dumps(cities))
        html += "}"

    except Exception, error:

        html =  "{'error':'" + str(error) + "'}"
        #html =  "{'error':'An error occured'}" # Production error

    finally:

        start_response('200 OK', [('Content-Type','text/html')])
        return html

class TestAPI(unittest.TestCase):

    def setUp(self):
        self.env = {'QUERY_STRING':'city=Sea'}

class fakeQDCity(object):

    def __init__(self):
        return "Sea"

class fakeDBCity(object):

    def __init__(self):
        return "Sea"

class TestApp(unittest.TestCase):

    ## can you tell I'm having issues mock patching functions ?
    ## also, how the heck do I mock the 'start_response' thing.. not sure if that's part of python
    ## or uwsgi (it's not imported)

    ## Try # 1
    ## error: 'app' is not defined - I think app is the base 'module'.. however, qdCity is not a class
    ##        I really think the @patch only works for classes ??
    @patch.object(app,'qdCity')
    def test_application_success(self,mock_qd_city):
        pass

    ## Try # 2
    #@patch('app.qdCity', '')
    #@patch.object('self', 'dbCity')
    #def test_appinit(self, mock_qdcity, mock_dbcity):

     #   mock_dbcity.return_value = [{"city":"Seattle"},{"city":"Seattle Heights"}]
     #   mock_qdcity.return_value = "Sea"

    #    self.results = application({'QUERY_STRING':'city=Sea'}, )

    ## Try # 3
    def test_application(self):

        #self.dbCity=mock(return_value=[{"city":"Seattle"},{"city":"Seattle Heights"}])
        #self.qdCity=mock(return_value="Sea")

        ## Not sure I can call application
        ## start_response is defined as via uwsgi start_response(status, response_headers, exc_info=None)
        self.results = application({'QUERY_STRING':'city=Sea'}, ???)
        self.assertEqual(self.results, "blah")

class TestQDCity(unittest.TestCase):

    def setUp(self):
        self.qd = {'cityx':['Sea']}

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

    def test_citylessthanthree(self):
        """
         testing qdCity exception when 'city' not at least three alpha
        """
        self.qd = {'cityx':['Se']}
        self.assertRaises(SystemError, qdCity, (self.qd))

class fakeCursor(object):

    def execute(self, *args):
        pass

    def fetchall(self, *args):
        return [{"city":"Seattle"},{"city":"Seattle Heights"}]

class fakeDB(object):

    def cursor(self, *args):
        return fakeCursor()

class TestDBCity(unittest.TestCase):

    @patch.object(MySQLdb, 'connect')
    def test_db(self, mockMySqlDb):

        mockMySqlDb.return_value = fakeDB()

        self.results = dbCity('Seattl')

        self.assertEqual(self.results, [{"city":"Seattle"},{"city":"Seattle Heights"}])
