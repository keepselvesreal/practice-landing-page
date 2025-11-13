# 11.2.0 Introduction [auto-generated] (pp.243-247)

---
**Page 243**

Testing for the Web: WSGI versus HTTP
Chapter 11
[ 243 ]
Technical requirements
We need a working Python interpreter with pytest, but for some sections in this chapter, we
will also have to install other libraries and frameworks. As usual, all of them can be
installed with pip:
$ pip install pytest
For the Testing HTTP section, we are going to need the requests library and the
requests-mock testing library:
$ pip install requests requests-mock
For the Testing WSGI with WebTest section, we are going to need webtest:
$ pip install webtest
And for the paragraphs regarding testing web frameworks, we are going to need the
targeted web frameworks installed, even though you aren't going to use all of them
concurrently in a real project:
$ pip install flask django pyramid turbogears2
The examples have been written on Python 3.7, pytest 6.0.2, Requests 2.24.0, Requests-Mock
1.8.0, WebTest 2.0.35, Django 3.1.4, Flask 1.1.2, Pyramid 1.10.5, and TurboGears 2.4.3, but
should work on most modern Python versions. You can find the code files present in this
chapter on GitHub at https:/​/​github.​com/​PacktPublishing/​Crafting-​Test-​Driven-
Software-​with-​Python/​tree/​main/​Chapter11.
Testing HTTP
A frequent need when working with networking based applications is that we have to test
both the server and client. If we are writing a distributed application, we are probably
going to write both the client and the server ourselves, and that means we'll want to test
both of them just as we did with our Chat application in previous chapters.


---
**Page 244**

Testing for the Web: WSGI versus HTTP
Chapter 11
[ 244 ]
While we might want to have a limited number of tests that connect to a real running
server, that quickly becomes too expensive if we involve real networking, and could also
result in errors related to the maximum amount of open connections our system can
handle, along with the time it takes to actually shut down those connections.
So we need to be able to test the client side of the application without having to connect to a
real server for the majority of our tests, or our test suite will quickly become
unmaintainable.
Let's suppose we are writing a very simple httpclient command-line application that
will allow us to request any URL that we want with the most common HTTP methods:
$ python -m httpclient GET http://www.amazon.com/
<!DOCTYPE html>
<html class="a-no-js" lang="en-us">
    <head>
        <title dir="ltr">Amazon.com</title>
        ...
To do so, we would first need a class able to perform HTTP requests, which we are going to
call just HTTPClient. Our HTTPClient exposes support for GET, POST, and DELETE (we
could easily expose more, but for the sake of simplicity we will limit our client to those
most common methods), and a follow method that allows us to access nested paths
relative to the current URL.
To implement this object we are going to rely on the requests library for most of the
heavy lifting of HTTP processing, thus we can run import requests and rely on it for
most of our methods' implementations. Let's create a src/httpclient/__init__.py file
where we can place our HTTPClient object:
import urllib.parse
import requests
class HTTPClient:
    def __init__(self, url):
        self._url = url
    def GET(self):
        return requests.get(self._url).text
    def POST(self, **kwargs):
        return requests.post(self._url, data=kwargs).text
    def DELETE(self):
        return requests.delete(self._url).text


---
**Page 245**

Testing for the Web: WSGI versus HTTP
Chapter 11
[ 245 ]
    def follow(self, path):
        baseurl = self._url
        if not baseurl.endswith("/"):
            baseurl += "/"
        return HTTPClient(urllib.parse.urljoin(baseurl, path))
The only method not directly relying on requests is HTTPClient.follow, which uses the
urllib.parse standard library module to navigate the URL tree.
Given the current URL, which is used as the base, the method is going to return a new
HTTPClient that points to a path nested within the same URL. For example, if we have a
client pointing to "http://www.google.com/", then using HTTPClient.follow("me")
would give us back a new client instance through which we can request
http://www.google.com/me.
Notice that this is a very naïve implementation that takes for granted the
fact that the base URL doesn't have any parameters. A more robust
implementation could be achieved if we actually parsed the URL and
encoded it back into a string, so that we can isolate the path from the rest
of the URL.
Now that we have the client in place, the remaining parts are those involved in exposing it
on the command line, so that we can use the python -m httpclient command to
perform HTTP requests.
The first piece we need to do so is the parse_args function. This function will be in charge
of taking arguments from the command line (thus from sys.argv) and converting them to
the options for HTTPClient:
import sys
def parse_args():
    cmd = sys.argv[0]
    args = sys.argv[1:]
    try:
        method, url, *params = args
    except ValueError:
        raise ValueError("Not enough arguments, "
                         "at least METHOD URL must be provided")
    try:
        params = dict((p.split("=", 1) for p in params))
    except ValueError:
        raise ValueError("Invalid request body parameters. "
                         "They must be in name=value format, "


---
**Page 246**

Testing for the Web: WSGI versus HTTP
Chapter 11
[ 246 ]
                         f"not {params}")
    return method.upper(), url, params
The first code block is just going to separate the HTTP method, the URL we want to
request, and the various params we want to provide it. The HTTP method accepts any
number of params, so we could have zero or many.
The second code block is meant to parse params from a "name=value" format to a
dictionary we can pass to the HTTPClient.POST method.
Finally, the function returns the HTTPClient method we have to invoke (GET, POST, or
DELETE), the URL for which we have to invoke it, and the params dictionary containing all
parameters.
Those three values are useful to the real main function of our application to properly use
the HTTPClient object. So the next step is to implement this main function so that we can
invoke it from the command line:
def main():
    try:
        method, url, params = parse_args()
    except ValueError as err:
        print(err)
        return
    client = HTTPClient(url)
    print(getattr(client, method)(**params))
main invokes parse_args, creates a client object, and then invokes the method
requested by parse_args on it and prints the returned value.
The remaining pieces we need to handle are, firstly, to create a
src/httpclient/__main__.py file where we invoke the main function:
from httpclient import main
main()


---
**Page 247**

Testing for the Web: WSGI versus HTTP
Chapter 11
[ 247 ]
And then a src/setup.py file that allows us to install the package and invoke it from the
command line:
from setuptools import setup
setup(name='httpclient', packages=['httpclient'])
If everything worked as expected, installing our package should allow us to invoke it from
the command line to perform HTTP requests:
$ pip install -e ./src
Obtaining file://./src
Installing collected packages: httpclient
...
Successfully installed httpclient
$ python -m httpclient GET http://httpbin.org/get
{
  "args": {},
  "headers": {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Host": "httpbin.org",
    "User-Agent": "python-requests/2.24.0",
  },
  "url": "http://httpbin.org/get"
}
Now that all the pieces are in place, we can move on to see how to test the HTTPClient
object.
Testing HTTP clients
If we had to test our HTTPClient, we would have to perform HTTP requests through those
methods to confirm they actually do what we want. To do so, we could use httpbin.org,
which is a service that accepts any kind of request and echoes back what was submitted.
This would allow us to verify that we are submitting what we expected we would send to
the server:
import json
from httpclient import HTTPClient
class TestHTTPClient:
    def test_GET(self):


