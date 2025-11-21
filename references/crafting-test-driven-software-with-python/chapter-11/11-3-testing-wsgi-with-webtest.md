# 11.3 Testing WSGI with WebTest (pp.252-261)

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


