
import os
import sys
import unittest
import re
import datetime
import json
import urllib2
import MySQLdb
from MySQLdb import cursors

def qdCity(qd):

    """
    return qcity string from query data

    fun with doctests!
    command line: python -m doctest -v doctest_simple.py, or right click run qdCity doctest via pycharm (cool!)
    >>> qdCity({'city':['Se   a   tt']})
    'Se a tt'
    >>> qdCity({})
    Traceback (most recent call last):
    ...
    SystemError: city search string not passed

    """

    qcity = ""

    if "city" in qd:

        # dictionary vlue returned as a list since querystrings can have multiple values
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

        # city string might be blank after house cleaning
        if len(qcity) == 0:
            raise SystemError('empty city string')

    else:

        raise SystemError('city search string not passed')

    return qcity

def dbCity(qcity):

    cities = []

    db = MySQLdb.connect(host="localhost", user=os.environ.get('MYSQL_USER', ''), passwd=os.environ.get('MYSQL_PASS', ''), db="n2local")

    # Note: DictCursor creates associate 'array' dict rows (yay!)
    # Note: Database driver (MySQLdb in this case) will handle escaping strings to thwart
    #       SQL injection.. no need to addslashes/escape search vars.. cursor.execute is the mechanism
    cur = db.cursor(cursors.DictCursor)
    if len(qcity) > 0:
        cur.execute("SELECT * FROM loc_cities where city like %s limit 25", ("" + qcity + "%",))
        rows = cur.fetchall()
    else:
        rows = []

    for row in rows:
        cities.append({"city":row.get("city",''), "region":row["region"], "lat":str(row["lat"]), "lon":str(row["lon"])})

    return cities

def application(env, start_response):

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
        ## To return milliseconds, add this to output below
        #html += "\"ms\":\"{}\",".format(ttime)

        # Need this to happen:
        # {"qs":"seattle","cities":[{"city":"seattle","region":"WA","lat":"46.xxx","lon":"122.xx"},{"city":...}]}
        html = "{"
        html += "\"qs\":\"{}\",".format(qcity)
        html += "\"cities\":{}".format(json.dumps(cities))
        html += "}"

    except Exception, error:

        html =  "{'error':'" + str(error) + "'}"

    finally:

        start_response('200 OK', [('Content-Type','text/html')])
        return [html]
