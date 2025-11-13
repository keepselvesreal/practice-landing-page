# Chapter 11: Testing for the Web: WSGI versus HTTP (pp.242-281)

---
**Page 242**

11
Testing for the Web: WSGI
versus HTTP
In the previous chapter, we saw how to test documentation and implement more advanced
testing techniques in our test suites, such as property-based testing.
One of the primary use cases for Python has become web development. Python has many
very effective and powerful web development frameworks. The most famous one is surely
the Django web framework, but many more of them exist, including the Flask framework,
the Pyramid framework, TurboGears2, and more. Each web framework has its own
peculiarities and unique features that make it easy to build most of the different kinds of
web applications using Python itself, but all of them share the same need of having to
verify that the applications you built work properly and are tested. Thus in this chapter, we
are going to see how we can test HTTP-based applications on both the client and server
side, how we can do that using pytest, and how the techniques presented differ from
framework-specific tests.
In this chapter, we will cover the following topics:
Testing HTTP
Testing WSGI with WebTest
Using WebTest with web frameworks
Writing Django tests with Django's test client
In this chapter, we are going to reverse the approach a bit and we are going to violate the
Test-Driven Development (TDD) principle by implementing the code first and
introducing tests for it after. The reason for this is that by introducing the system under test
first we can illustrate more clearly some details of the tests. If you already know how the
tested software works, it's easier to understand why the tests do the things they do, so for
the purposes of this chapter we will briefly abandon our best practices and focus on the
code first, and the tests after.


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


---
**Page 248**

Testing for the Web: WSGI versus HTTP
Chapter 11
[ 248 ]
        client = HTTPClient(url="http://httpbin.org/get")
        response = client.GET()
        assert '"Host": "httpbin.org"' in response
        assert '"args": {}' in response
    def test_GET_params(self):
        client = HTTPClient(url="http://httpbin.org/get?alpha=1")
        response = client.GET()
        response = json.loads(response)
        assert response["headers"]["Host"] == "httpbin.org"
        assert response["args"] == {"alpha": "1"}
    def test_POST(self):
        client = HTTPClient(url="http://httpbin.org/post?alpha=1")
        response = client.POST(beta=2)
        response = json.loads(response)
        assert response["headers"]["Host"] == "httpbin.org"
        assert response["args"] == {"alpha": "1"}
        assert response["form"] == {"beta": "2"}
    def test_DELETE(self):
        client = HTTPClient(url="http://httpbin.org/anything/27")
        response = client.DELETE()
        assert '"method": "DELETE"' in response
        assert '"url": "http://httpbin.org/anything/27"' in response
    def test_follow(self):
        client = HTTPClient(url="http://httpbin.org/anything")
        assert client._url == "http://httpbin.org/anything"
        client2 = client.follow("me")
        assert client2._url == "http://httpbin.org/anything/me"
Saving those tests as tests/test_httpclient.py will provide us with a running test
suite that confirms that HTTPClient works as expected. The problem is that running the
tests with this approach can take a while. Running just a few simple tests already takes
more than a second to run:
$ pytest -v -s
====================== test session starts ======================
platform linux -- Python 3.8.6, pytest-6.0.2, py-1.9.0, pluggy-0.13.1
...


---
**Page 249**

Testing for the Web: WSGI versus HTTP
Chapter 11
[ 249 ]
collected 5 items
tests/test_httpclient.py::TestHTTPClient::test_GET PASSED
tests/test_httpclient.py::TestHTTPClient::test_GET_params PASSED
tests/test_httpclient.py::TestHTTPClient::test_POST PASSED
tests/test_httpclient.py::TestHTTPClient::test_DELETE PASSED
tests/test_httpclient.py::TestHTTPClient::test_follow PASSED
======================= 5 passed in 1.37s =======================
Also, the tests might randomly fail due to network issues or errors on the remote server, so
they could easily become flaky. Slow and flaky tests are something we must avoid in a test
suite, so this approach of involving real networking is not something we can rely on in our
test suite.
The solution to both those problems is to replace the remote server, and thus the need for
networking, with a fake implementation. In our specific case, as we used the requests
library to perform HTTP requests to the server, we can prepare ready-made answers for
our requests using the requests-mock library, which allows us to mock requests by
replacing them with pre-baked responses.
To replace our real requests with fake ones, we just have to wrap them in a
requests_mock.Mocker() context manager, which comes from the requests_mock
module made available by the requests-mock library. Once we have the mocker object,
we can use it to drive what has to be mocked (which URL, method, and so on) and serve
ready-made answers for all the requests that match those filters.
For example, to mock a GET request, we could create the HTTPClient and before invoking
client.GET we could wrap that method with the Mocker and thus set up a ready-made
answer for any GET request against the same URL as the client one:
client = HTTPClient(url="http://httpbin.org/get")
with requests_mock.Mocker() as m:
    m.get(client._url, text='{"Host": "httpbin.org", "args": {}}')
    response = client.GET()
The text, json, and content arguments of the mocker can be used to provide the
response (as text, JSON, or binary) we want to serve back when the URL is requested with
the specified method. In this case, for example, we provided the response in text format
even though it contains a JSON string. In the following examples, we are going to use the
json argument, so that we can see both of them in action.


---
**Page 250**

Testing for the Web: WSGI versus HTTP
Chapter 11
[ 250 ]
Now we can adapt all our tests to use requests_mock so that they no longer have to take a
networking roundtrip to pass:
import json
from httpclient import HTTPClient
import requests_mock
class TestHTTPClient:
    def test_GET(self):
        client = HTTPClient(url="http://httpbin.org/get")
        with requests_mock.Mocker() as m:
            m.get(client._url,
                  text='{"Host": "httpbin.org", "args": {}}')
            response = client.GET()
        assert '"Host": "httpbin.org"' in response
        assert '"args": {}' in response
    def test_GET_params(self):
        client = HTTPClient(url="http://httpbin.org/get?alpha=1")
        with requests_mock.Mocker() as m:
            m.get(client._url,
                  text='''{"headers": {"Host": "httpbin.org"},
                           "args": {"alpha": "1"}}''')
            response = client.GET()
        response = json.loads(response)
        assert response["headers"]["Host"] == "httpbin.org"
        assert response["args"] == {"alpha": "1"}
    def test_POST(self):
        client = HTTPClient(url="http://httpbin.org/post?alpha=1")
        with requests_mock.Mocker() as m:
            m.post(client._url, json={"headers": {"Host": "httpbin.org"},
                                      "args": {"alpha": "1"},
                                      "form": {"beta": "2"}})
            response = client.POST(beta=2)
        response = json.loads(response)
        assert response["headers"]["Host"] == "httpbin.org"
        assert response["args"] == {"alpha": "1"}
        assert response["form"] == {"beta": "2"}
    def test_DELETE(self):
        client = HTTPClient(url="http://httpbin.org/anything/27")
        with requests_mock.Mocker() as m:
            m.delete(client._url, json={


---
**Page 251**

Testing for the Web: WSGI versus HTTP
Chapter 11
[ 251 ]
                "method": "DELETE",
                "url": "http://httpbin.org/anything/27"
            })
            response = client.DELETE()
        assert '"method": "DELETE"' in response
        assert '"url": "http://httpbin.org/anything/27"' in response
    def test_follow(self):
        ...
The test_follow test remains unchanged as it didn't involve any networking, while the
other tests are now wrapped in a requests_mock.Mocker() surrounding the
client.GET, client.POST and client.DELETE calls.
With those changes, the impact on our test suite is immediately visible. Tests that
previously took more than a second to run now take just a few milliseconds:
$ pytest -v -s
====================== test session starts ======================
platform linux -- Python 3.8.6, pytest-6.0.2, py-1.9.0, pluggy-0.13.1
...
collected 5 items
tests/test_httpclient.py::TestHTTPClient::test_GET PASSED
tests/test_httpclient.py::TestHTTPClient::test_GET_params PASSED
tests/test_httpclient.py::TestHTTPClient::test_POST PASSED
tests/test_httpclient.py::TestHTTPClient::test_DELETE PASSED
tests/test_httpclient.py::TestHTTPClient::test_follow PASSED
======================= 5 passed in 0.03s =======================
While this approach is fast, robust, and allows us to test that the client is properly able to
process and react to answers, it doesn't really test that the client and the server are able to
work together. Yes, we know that the client behaves like we meant it to behave, but it
doesn't in any way guarantee that once we put it in front of a real server, the two will speak
the same language.
If the server changes its responses in a way that differs from the one we hardcoded in our
tests, we will notice that the client doesn't work anymore with our server.
To address this limitation without having to involve a real networking layer, we are going
to see how we can write integration tests using WebTest and the WSGI protocol.


---
**Page 252**

Testing for the Web: WSGI versus HTTP
Chapter 11
[ 252 ]
Testing WSGI with WebTest
While we have seen how to test client without connecting to a real server, we can't rely only
on faked messages to confirm that our application works. If we are going to change server
responses, the tests wouldn't even notice and would continue to pass while in reality, the
client has stopped working. How can we detect those kinds of issues without involving real
networking? The WSGI (Web Server Gateway Interface) protocol and WebTest library
come in hand to do exactly that, set up a client-server communication that involves no
networking at all.
When we create web applications in Python, the most frequent way they work is through
an application server. The application server will be the one receiving HTTP requests,
decoding them, and forwarding them to the real web application. Forwarding those
requests to the web application and receiving back responses via the WSGI protocol is
usually the communication channel of choice for Python.
The WSGI protocol is a pure Python protocol, thus relies solely on being able to invoke a
Python function passing some specific arguments. All the communication in WSGI happens
in-memory and involves no dedicated parsing, and thus is very fast and usually suitable for
integration in web applications. A complete description of WSGI is available in PEP 333
(https:/​/​www.​python.​org/​dev/​peps/​pep-​3333/​).
The most basic WSGI application is a simple callable (a function, method, or function
object) that accepts two arguments (environ and start_response) and responds with an
iterable containing the output to be sent back to the client after having invoked
start_response to set up the response headers.
So the basic "Hello World" kind of application in WSGI would look as follows:
class Application:
    def __call__(self, environ, start_response):
        start_response(
            '200 OK',
            [('Content-type', 'text/plain; charset=utf-8')]
        )
        return ["Hello World".encode("utf-8")]
The environ argument will contain all information about the environment within which
our request is being processed, including information about the request itself, such as
REQUEST_METHOD, HTTP_HOST, PATH_INFO, QUERY_STRING, and many more values.
start_response is a function we can invoke to tell the application server that we are
ready to send back our response and inform it about the response type and the HTTP
headers that have to be sent back.


---
**Page 253**

Testing for the Web: WSGI versus HTTP
Chapter 11
[ 253 ]
In our case, for every request, we always send back an HTTP 200 response informing the
client that we are going to send some text encoded in UTF-8 by providing a Content-Type
header.
Then we return the iterable containing the response, which in this case is a list containing
the "Hello World" string encoded as UTF-8 as specified in our Content-Type.
Now that we have our WSGI application, we can save it in the
src/wsgiwebtest/__init__.py file and move forward to see how we can attach it to the
application server.
For the sake of this example, we are going to use a very basic application server provided
by the Python standard library itself in the wsgiref module,
simple_server.WSGIServer. To be able to start our application we are going to create a
src/wsgiwebtest/__main__.py file where we are going to place a main function that
creates the WSGIServer and attaches it to our web application:
from wsgiref.simple_server import make_server
from wsgiwebtest import Application
def main():
    app = Application()
    with make_server('', 8000, app) as httpd:
        print("Serving on port 8000...")
        httpd.serve_forever()
main()
All our main has to do is to create the Application object and pass it to the make_server
function, which will create an application server for that application. Once the server is
available we can start serving requests through the httpd.server_forever method.
The last step before we can actually try our "Hello World application is to create a setup.py
file so that we can install our package. So let's save a basic one as src/setup.py,
containing the following:
from setuptools import setup
setup(name='wsgiwebtest', packages=['wsgiwebtest'])
Now that we have all the pieces in place, we can install our application and start it:
$ pip install -e ./src
Obtaining file://./src
Installing collected packages: wsgiwebtest


---
**Page 254**

Testing for the Web: WSGI versus HTTP
Chapter 11
[ 254 ]
...
Successfully installed wsgiwebtest
$ python -m wsgiwebtest
Serving on port 8000...
Pointing our browser to http://localhost:8000/ should greet us with a simple Hello
World phrase:
Figure 11.1 – Hello World answer from our WSGI application
Now that we have a working web application, we want to evolve it to make it a bit more
interesting. We are going to turn it into a simple clone of httpbin.org. To do so we are
going to use the same exact tests we wrote for our HTTPClient package, port them to use
WebTest, and use them to drive the development of our WSGI application.
The first step is to take our existing TestHTTPClient.test_GET test and port it to use
webtest to verify our web application, saving it as tests/test_wsgiapp.py:
import webtest
from wsgiwebtest import Application
class TestWSGIApp:
    def test_GET(self):
        client = webtest.TestApp(Application())
        response = client.get("http://httpbin.org/get").text
        assert '"Host": "httpbin.org"' in response
        assert '"args": {}' in response


---
**Page 255**

Testing for the Web: WSGI versus HTTP
Chapter 11
[ 255 ]
The main difference is that instead of building an HTTPClient instance, we build a
webtest.TestApp for the application we want to test, which in this case is
wsgiwebtest.Application. Then we ask TestApp to perform a GET request against a
specific URL using the TestApp.get method. While we can specify a complete URL
including the domain, it won't matter too much, as TestApp will always direct the request
to the application under test, so even though here we wrote "http://httpbin.org", in
reality the request won't go to "httpbin.org" but to wsgiwebtest.Application. This
allows us to test our application by simulating whatever domain we want to serve it on.
Then the response returned by this request can be decoded as text or JSON as we did for
the requests library, using the .text or .json properties. In this case, we are going to
retain the existing test behavior and decode it as text even though the response is actually
in JSON format.
Running the test will obviously fail because right now our web application only responds
with "Hello World" to every request, but it proves that our test actually reached our web
application and got back the "Hello World" response:
______________________ TestWSGIApp.test_GET ______________________
self = <test_wsgiapp.TestWSGIApp object at 0x7fc6d64feaf0>
    def test_GET(self):
        client = webtest.TestApp(Application())
        response = client.get("http://httpbin.org/get")
> assert '"Host": "httpbin.org"' in response
E assert '"Host": "httpbin.org"' in <200 OK text/plain body=b'Hello World'>
Now that we know that webtest is actually working as expected and is doing the GET
request against our web application, let's start porting all our other tests to use webtest.
The approach is nearly the same for all of them. Instead of building an HTTPClient
instance, we are going to build a webtest.TestApp and use its .get, .post, and .delete
methods to perform the requests:
import webtest
from wsgiwebtest import Application
class TestWSGIApp:
    def test_GET(self):
        client = webtest.TestApp(Application())
        response = client.get("http://httpbin.org/get").text
        assert '"Host": "httpbin.org"' in response


---
**Page 256**

Testing for the Web: WSGI versus HTTP
Chapter 11
[ 256 ]
        assert '"args": {}' in response
    def test_GET_params(self):
        client = webtest.TestApp(Application())
        response = client.get(url="http://httpbin.org/get?alpha=1").json
        assert response["headers"]["Host"] == "httpbin.org"
        assert response["args"] == {"alpha": "1"}
    def test_POST(self):
        client = webtest.TestApp(Application())
        response = client.post(url="http://httpbin.org/get?alpha=1",
                               params={"beta": "2"}).json
        assert response["headers"]["Host"] == "httpbin.org"
        assert response["args"] == {"alpha": "1"}
        assert response["form"] == {"beta": "2"}
    def test_DELETE(self):
        client = webtest.TestApp(Application())
        response = client.delete(url="http://httpbin.org/anything/27").text
        assert '"method": "DELETE"' in response
        assert '"url": "http://httpbin.org/anything/27"' in response
The assertion part of the tests remained unmodified from the original tests we copied, the
only part that slightly changed is how we perform the requests.
Like the first test, those new tests will currently all fail because our web application will
always respond with "Hello World" to all of them. So the next step is to change our web
application to make it respond as the tests expect.
We can open our existing src/wsgiwebtest/__init__.py file and tweak the
Application.__call__ method to make it recognize the requested host, URL, and
method while also parsing the received request parameters from both the URL and the
request body:
import urllib.parse
class Application:
    def __call__(self, environ, start_response):
        start_response(
            '200 OK',
            [('Content-type', 'application/json; charset=utf-8')]


---
**Page 257**

Testing for the Web: WSGI versus HTTP
Chapter 11
[ 257 ]
        )
        form_params = {}
        if environ.get('CONTENT_TYPE') ==
               'application/x-www-form-urlencoded':
            req_body = environ["wsgi.input"].read().decode("ascii")
            form_params = {
                k: v for k, v in urllib.parse.parse_qsl(req_body)
            }
        if environ.get("SERVER_PORT") == "80":
            host = environ["SERVER_NAME"]
        else:
            host = environ["HTTP_HOST"]
        return [json.dumps({
            "method": environ["REQUEST_METHOD"],
            "headers": {"Host": host},
            "url": "{e[wsgi.url_scheme]}://{host}{e[PATH_INFO]}".format(
                e=environ,
                host=host
            ),
            "args": {
                k: v for k, v in
                  urllib.parse.parse_qsl(environ["QUERY_STRING"])
            },
            "form": form_params
        }).encode("utf-8")]
The start_response invocation is nearly the same, we just changed the reported
Content-Type to be application/json instead of text/plain as we are going to serve
back a JSON response.
Right after this, form_params is meant to contain all the parameters provided through the
request body. If what we received is a POST request, it's probably going to have a request
body where the majority of the parameters are provided. The request body could provide
those parameters encoded in various ways, but as it's the simplest one (and the one our
tests used), we are going to support only the "application/x-www-form-urlencoded"
encoding. So if the request we received has that content type, we will also parse the request
body (coming from environ["wsgi.input"]) and extract the parameters from there.


---
**Page 258**

Testing for the Web: WSGI versus HTTP
Chapter 11
[ 258 ]
The subsequent code block that initializes the host variable is instead meant to find the
host and port from which the request came, so that we can send it back into the Host field
of the headers dictionary in our response as the tests expect. The test expects that if the
request is targeted to the standard HTTP port, 80, the port is omitted in the returned host.
So we are going to only report the port when it's not 80 and we are going to limit ourselves
to the SERVER_NAME when the port is 80.
The last block is actually focused on building back the response, so it uses json.dumps to
encode a dictionary with all the data as text. The dictionary is going to contain the fields
our tests care about, meaning method and headers.Host for the HTTP method that was
used to perform the request, and the Host against which the request was targeted (in our
tests, this is httpbin.org). This will also contain the args key for all the parameters
provided in the query string, and thus in the URL itself, while separating the parameters
that were provided in the request body in the form key. Finally, the url key contains the
fully qualified URL that was requested.
This should guarantee a behavior very similar to the one that the real httpbin.org
provides, albeit heavily simplified. Saving back our new code and trying to rerun the tests
should prove that we implemented something that is similar enough to make our tests
pass:
$ pytest -v -s
====================== test session starts ======================
platform linux -- Python 3.8.6, pytest-6.0.2, py-1.9.0, pluggy-0.13.1
...
collected 4 items
tests/test_wsgiapp.py::TestHTTPClient::test_GET PASSED [ 25%]
tests/test_wsgiapp.py::TestHTTPClient::test_GET_params PASSED [ 50%]
tests/test_wsgiapp.py::TestHTTPClient::test_POST PASSED [ 75%]
tests/test_wsgiapp.py::TestHTTPClient::test_DELETE PASSED [100%]
======================= 4 passed in 0.08s =======================
Our tests passed, proving that our web application is similar enough to the original one we
meant to copy, and even though there is tons of space for improvement, it demonstrated
how we can implement tests for web applications that don't need any networking at all.
This is made clear by the fact that our tests using WebTest still complete in a matter of
milliseconds, similar to the tests where we used requests-mock, while the tests that
involved real networking took more than a second.


---
**Page 259**

Testing for the Web: WSGI versus HTTP
Chapter 11
[ 259 ]
If we want to go even further, using a little bit of dependency injection, we could easily
modify our HTTPClient object to work with both the requests module and the
webtest.TestApp object, as they are similar enough that we could write end-to-end tests
that go from HTTPClient down to wsgiwebtest.Application without ever involving
any HTTP parsing or networking.
Going in this direction requires a brief change to our original HTTPClient to allow us to
provide a replacement for the requests module at initialization time. By default, we are
going to keep using the requests module, but anyone could pass a different object to
HTTPClient.__init__ and replace it:
class HTTPClient:
    def __init__(self, url, requests=requests):
        self._url = url
        self._requests = requests
    def follow(self, path):
        baseurl = self._url
        if not baseurl.endswith("/"):
            baseurl += "/"
        return HTTPClient(urllib.parse.urljoin(baseurl, path))
    def GET(self):
        return self._requests.get(self._url).text
    def POST(self, **kwargs):
        return self._requests.post(self._url, kwargs).text
    def DELETE(self):
        return self._requests.delete(self._url).text
Then we have to use self._requests everywhere instead of just requests. The TestApp
and requests interfaces are similar enough that the only change we actually need to the
rest of the code is to omit the name of the argument (data=) from the post method and
invoke it with a positional argument. This is because in requests, the argument is named
data, while in TestApp it is named params. Passing it by position means that we don't
need to worry about what name it has.


---
**Page 260**

Testing for the Web: WSGI versus HTTP
Chapter 11
[ 260 ]
Now our HTTPClient is ready to accept a replacement for requests and we can take back
the original version of the tests we wrote for HTTPClient (the one that didn't use
requests-mock) and pass an instance of webtest.TestApp(wsgiwebtest.
Application) as the replacement for requests:
import json
import webtest
from wsgiwebtest import Application
from httpclient import HTTPClient
class TestHTTPClientWebTest:
    def test_GET(self):
        client = HTTPClient(url="http://httpbin.org/get",
                            requests=webtest.TestApp(Application()))
        response = client.GET()
        assert '"Host": "httpbin.org"' in response
        assert '"args": {}' in response
    def test_GET_params(self):
        client = HTTPClient(url="http://httpbin.org/get?alpha=1",
                            requests=webtest.TestApp(Application()))
        response = client.GET()
        response = json.loads(response)
        assert response["headers"]["Host"] == "httpbin.org"
        assert response["args"] == {"alpha": "1"}
    def test_POST(self):
        client = HTTPClient(url="http://httpbin.org/post?alpha=1",
                            requests=webtest.TestApp(Application()))
        response = client.POST(beta=2)
        response = json.loads(response)
        assert response["headers"]["Host"] == "httpbin.org"
        assert response["args"] == {"alpha": "1"}
        assert response["form"] == {"beta": "2"}
    def test_DELETE(self):
        client = HTTPClient(url="http://httpbin.org/anything/27",
                            requests=webtest.TestApp(Application()))
        response = client.DELETE()


---
**Page 261**

Testing for the Web: WSGI versus HTTP
Chapter 11
[ 261 ]
        assert '"method": "DELETE"' in response
        assert '"url": "http://httpbin.org/anything/27"' in response
If we save those tests as tests/test_client_webtest.py, they will keep working
exactly like before, but they will submit real requests to wsgiwebtest.Application
through the WSGI protocol, thus making sure that both the server and the client are able to
work together:
$ pytest -v -s
====================== test session starts ======================
platform linux -- Python 3.8.6, pytest-6.0.2, py-1.9.0, pluggy-0.13.1
...
collected 4 items
tests/test_client_webtest.py::TestHTTPClientWebTest::test_GET PASSED [ 25%]
tests/test_client_webtest.py::TestHTTPClientWebTest::test_GET_params PASSED
[ 50%]
tests/test_client_webtest.py::TestHTTPClientWebTest::test_POST PASSED [
75%]
tests/test_client_webtest.py::TestHTTPClientWebTest::test_DELETE PASSED
[100%]
======================= 4 passed in 0.08s =======================
Any change to one of the two that makes it incompatible with the other would immediately
cause the tests to fail, thus verifying that the two work correctly together without any of the
overhead of network-based communication or the flakiness that it involves.
All this is made possible by the fact that we used the WSGI standard to develop our web
application and, as we are going to see in the next section, WSGI is the most widespread
web development standard in Python and is supported by all major web frameworks.
Using WebTest with web frameworks
We have seen how to use WebTest with a plain WSGI application, but thanks to the fact
that WSGI is widely adopted by all major web frameworks, it's possible to use WebTest
with nearly all Python web frameworks.
To showcase how WebTest is able to work with most Python web frameworks, we are
going to replicate our httpbin in four web frameworks: Django, Flask, Pyramid, and
TurboGears2, and for all of them we are going to use the same exact test suite. So we will
share a single test suite between four different frameworks.


---
**Page 262**

Testing for the Web: WSGI versus HTTP
Chapter 11
[ 262 ]
The first step is to create a test suite that can verify that our web applications are starting
correctly. We are going to do so by adding a test that verifies all four web applications'
answering with a "Hello World" message on the index of the website.
The first step is to create a tests/test_wsgiapp.py file that's going to contain our only
test for now:
import webtest
class TestWSGIApp:
    def test_home(self, wsgiapp):
        client = webtest.TestApp(wsgiapp)
        response = client.get("http://httpbin.org/").text
        assert 'Hello World' in response
The test is fairly simple – it takes a WSGI application and checks that, on the index of the
website, the response contains the "Hello World" string.
The interesting part is how we are going to provide that wsgiapp object, as it has to be
different for each web framework. So we are going to add an option to our test suite to
choose which web framework to use and thus which application to create.
We are going to do so by creating a tests/conftest.py file that is going to contain both
the new option and the fixture to create the wsgiapp. The first thing we want to add is
support for the new option:
import pytest
def pytest_addoption(parser):
    parser.addoption(
        "--framework", action="store",
        help="Choose which framework to use for "
             "the web application: [tg2, django, flask, pyramid]"
    )


---
**Page 263**

Testing for the Web: WSGI versus HTTP
Chapter 11
[ 263 ]
If things work correctly, once we save the tests/conftest.py file, running pytest --
help will properly show the new option in the custom ones:
$ pytest --help
...
custom options:
  --framework=FRAMEWORK
                        Choose which framework to use for the
                        web application: [tg2, django, flask, pyramid]
Now that we have the option available, we must create the fixture that is going to use the
option, the wsgiapp fixture. As it's a fixture available for all our test suites, we can just add
it to the conftest.py file under the new option:
@pytest.fixture
def wsgiapp(request):
    framework = request.config.getoption("--framework")
    if framework == "tg2":
        from wbtframeworks.tg2 import make_application
    elif framework == "flask":
        from wbtframeworks.flask import make_application
    elif framework == "pyramid":
        from wbtframeworks.pyramid import make_application
    elif framework == "django":
        from wbtframeworks.django import make_application
    else:
        make_application = None
    if make_application is not None:
        return make_application()
    if framework is None:
        raise ValueError("Please pick a framework with --framework option")
    else:
        raise ValueError(f"Invalid framework {framework}")
The first thing that the fixture does is retrieve the selected framework through the option.
Then, depending on which framework was selected, it's going to import the function that
creates a new WSGI application from the module dedicated to that framework.
For convenience, we added all four modules (tg2, flask, pyramid, and django) under the
same wbtframeworks package, which is the one we are going to install.


---
**Page 264**

Testing for the Web: WSGI versus HTTP
Chapter 11
[ 264 ]
Once a framework is selected and the make_application function is imported, the fixture
will just return the new application built by the factory function. The remaining lines of
code are to handle the case where the user picks an unsupported framework (or no
framework at all).
Running pytest now should lead to it correctly complaining that we have picked no
framework:
$ pytest -v
================ test session starts ================
platform linux -- Python 3.8.6, pytest-6.0.2, py-1.9.0, pluggy-0.13.1
collected 1 item
tests/test_wsgiapp.py::TestWSGIApp::test_home ERROR [100%]
======================= ERRORS ======================
______ ERROR at setup of TestWSGIApp.test_home ______
request = <SubRequest 'wsgiapp' for <Function test_home>>
    @pytest.fixture
    def wsgiapp(request):
        ...
        elif framework is None:
> raise ValueError("Please pick a framework with --framework option")
E ValueError: Please pick a framework with --framework option
tests/conftest.py:31: ValueError
=================== short test summary info ===================
ERROR tests/test_wsgiapp.py::TestWSGIApp::test_home -
        ValueError: Please pick a framework with --framework option
======================= 1 error in 0.15s =======================
To confirm that the option is working as expected, we can run pytest with the --
framework=flask option to see what happens:
$ pytest -v --framework=flask
================ test session starts ================
platform linux -- Python 3.8.6, pytest-6.0.2, py-1.9.0, pluggy-0.13.1
collected 1 item
tests/test_wsgiapp.py::TestWSGIApp::test_home ERROR [100%]
======================= ERRORS ======================
______ ERROR at setup of TestWSGIApp.test_home ______
request = <SubRequest 'wsgiapp' for <Function test_home>>


---
**Page 265**

Testing for the Web: WSGI versus HTTP
Chapter 11
[ 265 ]
    @pytest.fixture
    def wsgiapp(request):
        framework = request.config.getoption("--framework")
        if framework == "tg2":
> from wbtframeworks.tg2 import make_application
E ModuleNotFoundError: No module named 'wbtframeworks'
tests/conftest.py:31: ValueError
=================== short test summary info ===================
ERROR tests/test_wsgiapp.py::TestWSGIApp::test_home -
        ModuleNotFoundError: No module named 'wbtframeworks'
======================= 1 error in 0.15s =======================
In this second case, it recognized the option correctly, but it complained that the
wbtframeworks package is not yet installed. That's expected as we haven't yet even
created it.
First, let's create a src/setup.py file to make the wbtframeworks package installable:
from setuptools import setup
setup(name='wbtframeworks', packages=['wbtframeworks'])
Now that the wbtframeworks package is installable, the next step is to create the package
itself, by creating the src/wbtframeworks/__init__.py file and then installing it:
$ pip install -e src
Obtaining file://src
Installing collected packages: wbtframeworks
  Running setup.py develop for wbtframeworks
Successfully installed wbtframeworks
Now that the package is available and installed in editable mode, we have to create the
structure for the four frameworks.
For the sake of keeping things short, as the sole purpose of those web applications is to
showcase how the same test suite can work against the four of them, we are going to use all
four frameworks in minimal mode, constraining the application to a single file.
The first one we are going to add is the src/wbtframeworks/flask/__init__.py file, to
add support for Flask:
from flask import Flask
app = Flask(__name__)
@app.route('/')
def hello_world():


---
**Page 266**

Testing for the Web: WSGI versus HTTP
Chapter 11
[ 266 ]
    return 'Hello World'
def make_application():
    return app.wsgi_app
We can confirm this minimal application works as expected by running our tests with
pytest --frameworks=flask:
$ pytest -v --framework=flask
====================== test session starts ======================
platform linux -- Python 3.8.6, pytest-6.0.2, py-1.9.0, pluggy-0.13.1
collected 1 item
tests/test_wsgiapp.py::TestWSGIApp::test_home PASSED [100%]
======================= 1 passed in 0.13s =======================
We use the same technique to create a src/wbtframeworks/pyramid/__init__.py file
for the Pyramid application:
from pyramid.config import Configurator
from pyramid.response import Response
def hello_world(request):
    return Response('Hello World!')
def make_application():
    with Configurator() as config:
        config.add_route('hello', '/')
        config.add_view(hello_world, route_name='hello')
        return config.make_wsgi_app()
Likewise, let's create the src/wbtframeworks/tg2/__init__.py for the TurboGears2
application as follows:
from tg import expose, TGController
from tg import MinimalApplicationConfigurator
class RootController(TGController):
    @expose()
    def index(self):
        return 'Hello World'


---
**Page 267**

Testing for the Web: WSGI versus HTTP
Chapter 11
[ 267 ]
def make_application():
    config = MinimalApplicationConfigurator()
    config.update_blueprint({
        'root_controller': RootController()
    })
    return config.make_wsgi_app()
And finally, create a src/wbtframeworks/django/__init__.py file for the Django
application:
import sys
import os
from django.conf.urls import re_path
from django.conf import settings
from django.http import HttpResponse
settings.configure(
    DEBUG=True,
    ROOT_URLCONF=sys.modules[__name__],
    ALLOWED_HOSTS=["httpbin.org"]
)
def home(request):
    return HttpResponse('Hello World')
urlpatterns = [
    re_path(r'^$', home),
]
def make_application():
    from django.core.wsgi import get_wsgi_application
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          'wbtframeworks.django.settings')
    return get_wsgi_application()
Once all of them are available, we can see that our test is able to run against all four of them
without any difference. It can run against TurboGears2:
$ pytest --framework=tg2
====================== test session starts ======================
platform linux -- Python 3.8.6, pytest-6.0.2, py-1.9.0, pluggy-0.13.1
collected 1 item
tests/test_wsgiapp.py .                                    [100%]


---
**Page 268**

Testing for the Web: WSGI versus HTTP
Chapter 11
[ 268 ]
======================= 1 passed in 0.13s =======================
And it can be run against Django without any changes:
$ pytest --framework=django
====================== test session starts ======================
platform linux -- Python 3.8.6, pytest-6.0.2, py-1.9.0, pluggy-0.13.1
collected 1 item
tests/test_wsgiapp.py .                                    [100%]
======================= 1 passed in 0.13s =======================
Now that we are sure that our test suite can run against all four frameworks, we will extend
it with the other tests we had for our httpbin.org clone:
import webtest
class TestWSGIApp:
    def test_home(self, wsgiapp):
        client = webtest.TestApp(wsgiapp)
        response = client.get("http://httpbin.org/").text
        assert 'Hello World' in response
    def test_GET(self, wsgiapp):
        client = webtest.TestApp(wsgiapp)
        response = client.get("http://httpbin.org/get").text
        assert '"Host": "httpbin.org"' in response
        assert '"args": {}' in response
    def test_GET_params(self, wsgiapp):
        client = webtest.TestApp(wsgiapp)
        response = client.get(url="http://httpbin.org/get?alpha=1").json
        assert response["headers"]["Host"] == "httpbin.org"
        assert response["args"] == {"alpha": "1"}
    def test_POST(self, wsgiapp):
        client = webtest.TestApp(wsgiapp)
        response = client.post(url="http://httpbin.org/get?alpha=1",
                               params={"beta": "2"}).json
        assert response["headers"]["Host"] == "httpbin.org"


---
**Page 269**

Testing for the Web: WSGI versus HTTP
Chapter 11
[ 269 ]
        assert response["args"] == {"alpha": "1"}
        assert response["form"] == {"beta": "2"}
    def test_DELETE(self, wsgiapp):
        client = webtest.TestApp(wsgiapp)
        response = client.delete(url="http://httpbin.org/anything/27").text
        assert '"method": "DELETE"' in response
        assert '"url": "http://httpbin.org/anything/27"' in response
Running the tests now against any framework will complain that those URLs lead to a 404
error, as we haven't yet implemented them. For example, running the tests for Pyramid
would lead only to the test_home one succeeding and the others failing:
$ pytest --framework=pyramid
====================== test session starts ======================
platform linux -- Python 3.8.6, pytest-6.0.2, py-1.9.0, pluggy-0.13.1
collected 1 item
tests/test_wsgiapp.py .FFFF                                [100%]
==================== short test summary info ====================
FAILED test_GET - webtest.app.AppError: 404 Not Found (not 200 OK o...
FAILED test_GET_params - webtest.app.AppError: 404 Not Found (not 2...
FAILED test_POST - webtest.app.AppError: 404 Not Found (not 200 OK ...
FAILED test_DELETE - webtest.app.AppError: 404 Not Found (not 200 O...
================== 4 failed, 1 passed in 0.37s ==================
Now that our test suite can run for all four implementations of our application, we only
have to proceed with the actual implementation. Given that it doesn't add much value
having the same web application implemented in four different frameworks (outside of
being a good exercise to learn those frameworks), we are going to provide only the
implementation using Django and will leave to the readers the work of implementing it on
the other three frameworks if they wish.
Thus we are going to open our src/wbtframeworks/django/__init__.py file and edit
it to add the remaining routes with the pieces that are lacking:
import sys, json
from django.conf.urls import re_path
from django.conf import settings
from django.http import HttpResponse
settings.configure(
    DEBUG=True,
    ROOT_URLCONF=sys.modules[__name__],
    ALLOWED_HOSTS=["httpbin.org"]


---
**Page 270**

Testing for the Web: WSGI versus HTTP
Chapter 11
[ 270 ]
)
def home(request):
    return HttpResponse('Hello World')
def get(request):
    if request.META.get("SERVER_PORT") == "80":
        host_no_default_port = request.META["HTTP_HOST"].replace(":80", "")
        request.META["HTTP_HOST"] = host_no_default_port
    host = request.META["HTTP_HOST"]
    response = HttpResponse(json.dumps({
        "method": request.META["REQUEST_METHOD"],
        "headers": {"Host": host},
        "args": {
            p: v for (p, v) in request.GET.items()
        },
        "form": {
            p: v for (p, v) in request.POST.items()
        },
        "url": request.build_absolute_uri()
    }, sort_keys=True))
    response['Content-Type'] = 'application/json'
    return response
urlpatterns = [
    re_path(r'^get$', get),
    re_path(r"^anything.*$", get),
    re_path(r'^$', home),
]
def make_application():
    import os
    from django.core.wsgi import get_wsgi_application
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          'wbtframeworks.django.settings')
    return get_wsgi_application()
Running our tests now would confirm that, at least for Django, they are able to pass and
succeed:
$ pytest --framework=django
====================== test session starts ======================
platform linux -- Python 3.8.6, pytest-6.0.2, py-1.9.0, pluggy-0.13.1
collected 5 items


---
**Page 271**

Testing for the Web: WSGI versus HTTP
Chapter 11
[ 271 ]
tests/test_wsgiapp.py .....                                [100%]
======================= 5 passed in 0.27s =======================
This is a very naïve and basic implementation for the sole purpose of showing that our tests
are able to pass once the application is provided, but it proves that on Django, we are
perfectly able to use WebTest like we would for any other WSGI framework.
But WebTest is not the only way we can test Django applications. Django also provides its
own testing client, so let's see how we would test the same application using Django's test
client instead of WebTest.
Writing Django tests with Django's test
client
While on Python the most widespread testing toolkit is pytest, some web frameworks
provide their own solutions for managing test suites. Django is one such example, even
though it's possible (as we have seen in the previous section), most people tend to run their
tests with the Django test client, which provides the same capabilities as WebTest but is a
solution built explicitly for Django.
In this section, we are going to see how we can create a Django project and then run its tests
using the standard Django testing infrastructure as well as a pytest-based one:
The first step will be to create a new Django project, which we are going to call
1.
djapp:
$ django-admin startproject djapp
This will create a djapp directory where we can manage our Django project. In
the project directory, we will find a manage.py file, which allows us to run
various management operations for our project, from setting up the database to
starting the web application itself and running tests the Django way.
The next step is to actually put an application inside our project. As our
2.
application will be the httpbin one we already wrote, we will just call the
application httpbin. To create a new application inside a project, we can use the
manage.py startapp command:
$ python manage.py startapp httpbin


---
**Page 272**

Testing for the Web: WSGI versus HTTP
Chapter 11
[ 272 ]
Now that the httpbin application is available, we have to copy the content of
3.
the wbtframeworks/django/__init__.py file we just wrote in the previous
section. The first things we have to copy are the two home and get views, which 
have to be copied inside the djapp/httpbin/views.py file:
import json
from django.http import HttpResponse
def home(request):
    return HttpResponse('Hello World')
def get(request):
    if request.META.get("SERVER_PORT") == "80":
        http_host = request.META.get("HTTP_HOST", "httpbin.org")
        host_no_default_port = http_host.replace(":80", "")
        request.META["HTTP_HOST"] = host_no_default_port
    host = request.META["HTTP_HOST"]
    response = HttpResponse(json.dumps({
        "method": request.META["REQUEST_METHOD"],
        "headers": {"Host": host},
        "args": {
            p: v for (p, v) in request.GET.items()
        },
        "form": {
            p: v for (p, v) in request.POST.items()
        },
        "url": request.build_absolute_uri()
    }, sort_keys=True))
    response['Content-Type'] = 'application/json'
    return response
Then, once the views are available, we must actually expose them; that is, make
4.
them accessible through some kind of URL. To do so, we have to add the three
URL paths to the djapp/httpbin/urls.py file:
from django.urls import re_path
from . import views
urlpatterns = [
    re_path(r'^get$', views.get),
    re_path(r"^anything.*$", views.get),
    re_path(r'^$', views.home)
]


---
**Page 273**

Testing for the Web: WSGI versus HTTP
Chapter 11
[ 273 ]
Our application is now fully functional. But if we try to start it now it won't work.
That's because we haven't yet attached the application to the project. So the djapp
project doesn't yet know that it has to serve the httpbin application.
To do this, we can open the djapp/djapp/urls.py file and make sure that all
5.
the URLs from the httpbin project are correctly included in it:
from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("httpbin.urls"))
]
The last step is to make sure that our website is accessible on all the hosts that we
6.
plan to use, so we should set the ALLOWED_HOSTS variable in
djapp/djapp/settings.py:
ALLOWED_HOSTS = ["httpbin.org", "127.0.0.1"]
If we did everything correctly, running manage.py runserver should now run
our website and make it visible on http://127.0.0.1:8000/:
$ python manage.py runserver
...
Django version 3.1.4, using settings 'djapp.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
Pointing our web browser to http://127.0.0.1:8000/ should greet us with a
Hello World message as specified by the httpbin.views.home function:
Figure 11.2 – Hello World response from our Django application
Now that we confirmed the application is being correctly served, we have to make sure we
are able to run the tests against it.


---
**Page 274**

Testing for the Web: WSGI versus HTTP
Chapter 11
[ 274 ]
Testing Django projects with pytest
The first thing we are going to do is to take our test suite as-is, based on WebTest and
pytest, and make it work against the new Django project we just wrote. This mostly
guarantees that the behavior we have is the same exact behavior we previously had, as the
tests are the same tests we had previously. Also shows how we can use pytest and WebTest
even with a full-fledged Django project.
To do so, we are going to create a pytest-tests directory inside the djapp project. Here
we are going to place the djapp/pytest-tests/test_djapp.py module, which is
mostly a copy of the test module we had in the previous section. The only difference will be
where the wsgiapp object comes from:
import sys
import webtest
sys.path.append(".")
from djapp.wsgi import application as wsgiapp
class TestWSGIApp:
    def test_home(self):
        client = webtest.TestApp(wsgiapp)
        response = client.get("http://httpbin.org/").text
        assert 'Hello World' in response
    def test_GET(self):
        client = webtest.TestApp(wsgiapp)
        response = client.get("http://httpbin.org/get").text
        assert '"Host": "httpbin.org"' in response
        assert '"args": {}' in response
    def test_GET_params(self):
        client = webtest.TestApp(wsgiapp)
        response = client.get(url="http://httpbin.org/get?alpha=1").json
        assert response["headers"]["Host"] == "httpbin.org"
        assert response["args"] == {"alpha": "1"}
    def test_POST(self):
        client = webtest.TestApp(wsgiapp)
        response = client.post(url="http://httpbin.org/get?alpha=1",


---
**Page 275**

Testing for the Web: WSGI versus HTTP
Chapter 11
[ 275 ]
                               params={"beta": "2"}).json
        assert response["headers"]["Host"] == "httpbin.org"
        assert response["args"] == {"alpha": "1"}
        assert response["form"] == {"beta": "2"}
    def test_DELETE(self):
        client = webtest.TestApp(wsgiapp)
        response = client.delete(url="http://httpbin.org/anything/27").text
        assert '"method": "DELETE"' in response
        assert '"url": "http://httpbin.org/anything/27"' in response
The two main changes compared to the prior test module are that we removed all the
wsgiapp arguments from the test functions, as the wsgiapp object won't come anymore
from a fixture injecting the dependency, and that we imported it at the top of the file from
the djapp.wsgi module. Different to most web frameworks, in Django the projects are not
Python distributions, and thus can't be installed with pip. This means that we can't directly
import the project from anywhere and refer to its content.
To surpass this limitation we are going to use sys.path.append(".") to make the
current path available to Python. This allows us to import the djapp package inside the
djapp project as if it were a normal Python installed package, thus making accessible the
djapp.wsgi module. Inside that module, Django makes the WSGI application available as
the application object.
To confirm things worked as expected, we are going to run pytest and point it to the
pytest-tests directory. This should run the same exact tests we had before, just against
the new Django project:
$ pytest pytest-tests -v
======================== test session starts =========================
platform linux -- Python 3.8.6, pytest-6.0.2, py-1.9.0, pluggy-0.13.1 --
collected 5 items
pytest-tests/test_djapp.py::TestWSGIApp::test_home PASSED [ 20%]
pytest-tests/test_djapp.py::TestWSGIApp::test_GET PASSED [ 40%]
pytest-tests/test_djapp.py::TestWSGIApp::test_GET_params PASSED [ 60%]
pytest-tests/test_djapp.py::TestWSGIApp::test_POST FAILED [ 80%]
pytest-tests/test_djapp.py::TestWSGIApp::test_DELETE FAILED [100%]
============================== FAILURES ==============================
...
------------------------ Captured stderr call ------------------------
Forbidden (CSRF cookie not set.): /anything/27
------------------------- Captured log call --------------------------


---
**Page 276**

Testing for the Web: WSGI versus HTTP
Chapter 11
[ 276 ]
WARNING django.security.csrf:log.py:224 Forbidden (CSRF cookie not set.):
/anything/27
====================== short test summary info =======================
FAILED pytest-tests/test_djapp.py::TestWSGIApp::test_POST - webtest...
FAILED pytest-tests/test_djapp.py::TestWSGIApp::test_DELETE - webte...
==================== 2 failed, 3 passed in 0.40s =====================
Surprisingly, there were two tests that failed compared to before: test_POST and
test_DELETE.
Both of them failed with a CSRF cookie not set error. This is because Django sets up
support for CSRF attack protection by default in all new projects. The protection works by
using a token provided automatically by forms when they get submitted to other
endpoints. The problem is that in our project, we don't have any forms at all, so the DELETE
and POST requests are not submitting any tokens, thus failing the protection check.
For our kind of application, this kind of protection doesn't make much sense, as we aren't
going to have any forms present. Thus we can edit the djapp/djapp/settings.py file
and remove the django.middleware.csrf.CsrfViewMiddleware line from the
MIDDLEWARES variable:
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
Now that we have disabled the CSRF protection, rerunning the tests should succeed as
expected:
$ pytest pytest-tests -v
======================== test session starts =========================
collected 5 items
pytest-tests/test_djapp.py::TestWSGIApp::test_home PASSED [ 20%]
pytest-tests/test_djapp.py::TestWSGIApp::test_GET PASSED [ 40%]
pytest-tests/test_djapp.py::TestWSGIApp::test_GET_params PASSED [ 60%]
pytest-tests/test_djapp.py::TestWSGIApp::test_POST PASSED [ 80%]
pytest-tests/test_djapp.py::TestWSGIApp::test_DELETE PASSED [100%]
========================= 5 passed in 0.21s ==========================


---
**Page 277**

Testing for the Web: WSGI versus HTTP
Chapter 11
[ 277 ]
Testing Django projects with Django's test client
We have seen that the application behaves like we expected as the same tests we wrote for
WebTest worked correctly. But running tests using pytest and WebTest is a non-standard
way to test Django projects. Most people would expect to be able to test a Django project
simply using the manage.py test command. But for now, this command runs no tests at
all:
$ python manage.py test
System check identified no issues (0 silenced).
----------------------------------------------------------------------
Ran 0 tests in 0.000s
OK
This is because for manage.py test itself, we have not yet written any test. manage.py
test is mostly based on the unittest framework we saw at the beginning of the book,
and thus is not compatible with pytest. Also, the tests here are meant to be written slightly
differently without using WebTest.
To migrate our tests to the Django way, we have to create a djapp/httpbin/tests.py file
in which we will put all our tests. For now, in this file, we are going to provide a single test
for the index page of the website, just to make sure that the test suite is able to find our test
and that the web application is correctly starting up:
from django.test import TestCase
class HttpbinTests(TestCase):
    def test_home(self):
        response = self.client.get("/")
        self.assertContains(response, "Hello World")
Django tests will usually inherit from django.test.TestCase, which serves two different
purposes:
First, to make sure that the methods inside the subclass are correctly identified as
tests, and thus run when we start the test suite.
The second purpose is to provide the self.client object, which helps to
perform requests to the web application much like WebTest did.
In this case, the primary difference is that the web application is not explicitly provided to
the client, but is detected based on the project where we are running the tests.


---
**Page 278**

Testing for the Web: WSGI versus HTTP
Chapter 11
[ 278 ]
Now that we have a test in place, running the manage.py test command again should
finally find and run the test:
$ python manage.py test
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.
----------------------------------------------------------------------
Ran 1 test in 0.004s
OK
Destroying test database for alias 'default'...
The next steps will be to also port the test_GET, test_GET_params, test_POST, and
test_DELETE tests to the Django standard so that our full test suite is available when
running manage.py test.
The main differences when working with Django's test client is that for the responses, it's
going to provide a Django HttpResponse object, thus the content of the response will be
available in binary form in the HttpResponse.content attribute and we will have to
decode it ourselves, while WebTest provided the .text and .json properties, which
handled much of that for us. Apart from these minor differences, the tests mostly look the
same as before:
import json
from django.test import TestCase
class HttpbinTests(TestCase):
    def test_home(self):
        response = self.client.get("/")
        self.assertContains(response, "Hello World")
    def test_GET(self):
        response = self.client.get("/get").content.decode("utf-8")
        assert '"Host": "httpbin.org"' in response
        assert '"args": {}' in response
    def test_GET_params(self):
        response = json.loads(self.client.get("/get?alpha=1").content)
        assert response["headers"]["Host"] == "httpbin.org"
        assert response["args"] == {"alpha": "1"}


---
**Page 279**

Testing for the Web: WSGI versus HTTP
Chapter 11
[ 279 ]
    def test_POST(self):
        response = json.loads(self.client.post(
            "/get?alpha=1", {"beta": "2"}
        ).content)
        assert response["headers"]["Host"] == "httpbin.org"
        assert response["args"] == {"alpha": "1"}
        assert response["form"] == {"beta": "2"}
    def test_DELETE(self):
        response = self.client.delete(
            "/anything/27"
        ).content.decode("utf-8")
        assert '"method": "DELETE"' in response
        assert '"url": "http://httpbin.org/anything/27"' in response
Now that we have in place the same tests we had before, but now in the new Django test
client format, we can verify that all five of them pass as expected by rerunning the
manage.py test command:
$ python manage.py test
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.....
----------------------------------------------------------------------
Ran 5 tests in 0.010s
OK
Destroying test database for alias 'default'...
This confirms that our tests for the application succeed also in the Django test client
version.
Which format to use (WebTest or Django's test client) can be considered mostly a matter of
preference for skilled Django users, but for most developers out there, using Django's test
client will probably lead to finding more answers to your questions and doubts, as it's the
documented and suggested way that Django developers expect will be used when writing
Django applications.
For people interested in using pytest with Django, a pytest-django package also exists
that tries to fill the gap while hiding most of the machinery necessary to make Django tests
run with pytest.


---
**Page 280**

Testing for the Web: WSGI versus HTTP
Chapter 11
[ 280 ]
Summary
In this chapter, we saw how we can test HTTP-based applications and how we can verify
the behavior of HTTP clients, HTTP servers, and even the two of them together. This is all
thanks to the WSGI protocol that powers the Python web ecosystem. We have also seen
how testing works in the Django world when Django's test client is used, thus we are fairly
capable of writing effective test suites for whatever web framework we are going to use.
Our testing isn't fully complete by the way. We are verifying the endpoints, checking that
the web pages contain the responses we expect, but we have no way to check that, once
those responses are read by a web browser, they actually behave as we expected. Even
worse, if there is JavaScript involved, we don't have any way to verify that the JavaScript in
those web pages is actually doing what we want.
So in the next chapter, we are going to see how we can test our web applications with a real
browser while also verifying the JavaScript that our web pages contain, thus completing the
list of skills we might need to develop a fully tested web application.


---
**Page 281**

12
End-to-End Testing with the
Robot Framework
In the previous chapter, we saw how to test web applications and, in general, applications
that rely on the HTTP protocol, both client and server side, but we were unable to test how
they perform in a real browser. With their complex layouts, the fact that CSS and JavaScript
are heavily involved in testing your application with WebTest or a similar solution might
not be sufficient to guarantee users that they are actually able to work with it. What if a
button is created by JavaScript or it's disabled by CSS? Those conditions are hard to test
using WebTest and we might easily end up with a test that clicks that button even though
the button wasn't actually usable by users.
To guarantee that our applications behave properly, it is a good idea to have a few tests that
verify at least the more important areas of the application using a real browser. As those
kinds of tests tend to be very slow and fragile, you still want to have the majority of your
tests written using solutions such as WebTest or even unit tests, which don't involve the
whole application life cycle, but having the most important parts of the web application
verified using real browsers will guarantee that at least the critical path of your web
application works on all major browsers. 
The Robot framework is one of the most solid solutions for writing the end-to-end tests that
drive web browsers and mobile applications in the Python world. It was originally
developed by Nokia and evolved under the open source community, and is a long-standing
and solid solution with tons of documentation and plugins. It is therefore battle tested and
ready for your daily projects.
In this chapter, we will cover the following topics:
Introducing the Robot framework
Testing with web browsers
Extending the Robot framework


