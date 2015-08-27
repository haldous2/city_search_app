
# city_search_app
A uwsgi web api that returns json city information. read in a querystring 'city', output a JSON list of cities with region, lat & lon that match search.

### Example
Query:  http://your.api.server/city_search_app_uwsgi_url/?city=Sea

Output: {"qs":"seattle","cities":[{"city":"seattle","region":"WA","lat":"47.xxx","lon":"122.xxx"},{"city"...}]}

### Installation

###### Linux environment
* nginx - or your favorite web server, this one is cool because it proxies your uwsgi requests.
* mysql - or your favorite database. Your mileage may vary
* python - should already be installed in Ubuntu, using version 2.x.x
* python-dev - apt-get install python-dev
* pip - apt-get install python-pip
* virtualenv - apt-get install python-virtualenv; create a virtualenv then switch to it and the following get installed
* uwsgi - pip install uwsgi - web interface between nginx proxy and python
* uwsgi python plugin - apt-get install uwsgi-plugin-python
* libmysqlclient-dev - apt-get install libmysqlclient-dev # need this for mysqldb in virtualenv
* python-mysqldb - apt-get install python-mysqldb

###### Nginx config

Configure nginx .conf by adding something similar to your setup. This might also work in<br/>
Apache but hasn't been tested. This is assuming your nginx config is in the default location of<br/>
/etc/nginx

    location /py/ {
        alias /path/to/your/app/;
        include /etc/nginx/uwsgi_params;
        uwsgi_pass 127.0.0.1:3030;
    }

Just in case you are missing your uwsgi_params

    uwsgi_param	QUERY_STRING		$query_string;
    uwsgi_param	REQUEST_METHOD		$request_method;
    uwsgi_param	CONTENT_TYPE		$content_type;
    uwsgi_param	CONTENT_LENGTH	    $content_length;

    uwsgi_param	REQUEST_URI         $request_uri;
    uwsgi_param	PATH_INFO		    $document_uri;
    uwsgi_param	DOCUMENT_ROOT		$document_root;
    uwsgi_param	SERVER_PROTOCOL		$server_protocol;
    uwsgi_param	UWSGI_SCHEME		$scheme;

    uwsgi_param	REMOTE_ADDR		    $remote_addr;
    uwsgi_param	REMOTE_PORT		    $remote_port;
    uwsgi_param	SERVER_PORT		    $server_port;
    uwsgi_param	SERVER_NAME		    $server_name;

###### Uwsgi config

Create a file @ /etc/uwsgi/apps-enables/name-of-app.ini<br/>
Note: for multiple apps, just create multiple .ini files with different ports<br/>
optionally, symbolic link: ln -s /path/to/app/myapp.ini /etc/uwsgi/apps-enabled/<br/>
Note: environment variables for uwsgi set in uwsgi ini file. For this installation we need mysql user and pass<br/>

    [uwsgi]
    http-socket = :3030
    plugin = python
    wsgi-file = /path/to/your/app.py
    virtualenv = /path/to/your/app/venv/
    process = 3
    env = MYSQL_USER=mysql_user_name
    env = MYSQL_PASS=mysql_user_password

run with: service uwsgi start | stop | restart

Or to test via command line. If you have startup errors this is a good way to debug.<br/>
uwsgi --http :8080 --wsgi-file /path/to/your/app.py --virtualenv /path/to/your/app/venv

logs @ /var/log/uwsgi/app name (in this case /app)

###### MySQL setup

We'll be calling a table loc_cities, you can call it whatever you want<br/>
basic structure is city, region, country, lat, lon - or create structure according to your data

Free data download @ [MaxMind](http://dev.maxmind.com/geoip/legacy/geolite/)

###### City Search App

Since the city_serch_app isn't an installable module, there isn't a way to import it. 
If you just want to run tests then clone the repository and run nosetests.

The actual application that is run via the uwsgi server is located under /city_search_app/app.py.
Copy that application to your web folder where uwsgi.ini points to. That's it! Yer done!
