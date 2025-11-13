# 11.2.1 Testing HTTP clients (pp.247-252)

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


