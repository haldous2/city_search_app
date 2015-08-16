
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
import webtest
from webtest import TestApp

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

    #print type(start_response)
    #print dir(start_response)
    print env["QUERY_STRING"]

    try:

        stime = datetime.datetime.now()

        # extract querystring from uwsgi environment variables
        # convert to dictionary in qd and then cleanup city string
        qs = env["QUERY_STRING"]
        qd = urllib2.urlparse.parse_qs(qs) # returns dict of querystring arguments

        qcity = qdCity(qd)
        print qcity
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
        return [html]
