Line 1: 
Line 2: --- 페이지 252 ---
Line 3: 11
Line 4: Testing for the Web: WSGI
Line 5: versus HTTP
Line 6: In the previous chapter, we saw how to test documentation and implement more advanced
Line 7: testing techniques in our test suites, such as property-based testing.
Line 8: One of the primary use cases for Python has become web development. Python has many
Line 9: very effective and powerful web development frameworks. The most famous one is surely
Line 10: the Django web framework, but many more of them exist, including the Flask framework,
Line 11: the Pyramid framework, TurboGears2, and more. Each web framework has its own
Line 12: peculiarities and unique features that make it easy to build most of the different kinds of
Line 13: web applications using Python itself, but all of them share the same need of having to
Line 14: verify that the applications you built work properly and are tested. Thus in this chapter, we
Line 15: are going to see how we can test HTTP-based applications on both the client and server
Line 16: side, how we can do that using pytest, and how the techniques presented differ from
Line 17: framework-specific tests.
Line 18: In this chapter, we will cover the following topics:
Line 19: Testing HTTP
Line 20: Testing WSGI with WebTest
Line 21: Using WebTest with web frameworks
Line 22: Writing Django tests with Django's test client
Line 23: In this chapter, we are going to reverse the approach a bit and we are going to violate the
Line 24: Test-Driven Development (TDD) principle by implementing the code first and
Line 25: introducing tests for it after. The reason for this is that by introducing the system under test
Line 26: first we can illustrate more clearly some details of the tests. If you already know how the
Line 27: tested software works, it's easier to understand why the tests do the things they do, so for
Line 28: the purposes of this chapter we will briefly abandon our best practices and focus on the
Line 29: code first, and the tests after.
Line 30: 
Line 31: --- 페이지 253 ---
Line 32: Testing for the Web: WSGI versus HTTP
Line 33: Chapter 11
Line 34: [ 243 ]
Line 35: Technical requirements
Line 36: We need a working Python interpreter with pytest, but for some sections in this chapter, we
Line 37: will also have to install other libraries and frameworks. As usual, all of them can be
Line 38: installed with pip:
Line 39: $ pip install pytest
Line 40: For the Testing HTTP section, we are going to need the requests library and the
Line 41: requests-mock testing library:
Line 42: $ pip install requests requests-mock
Line 43: For the Testing WSGI with WebTest section, we are going to need webtest:
Line 44: $ pip install webtest
Line 45: And for the paragraphs regarding testing web frameworks, we are going to need the
Line 46: targeted web frameworks installed, even though you aren't going to use all of them
Line 47: concurrently in a real project:
Line 48: $ pip install flask django pyramid turbogears2
Line 49: The examples have been written on Python 3.7, pytest 6.0.2, Requests 2.24.0, Requests-Mock
Line 50: 1.8.0, WebTest 2.0.35, Django 3.1.4, Flask 1.1.2, Pyramid 1.10.5, and TurboGears 2.4.3, but
Line 51: should work on most modern Python versions. You can find the code files present in this
Line 52: chapter on GitHub at https:/​/​github.​com/​PacktPublishing/​Crafting-​Test-​Driven-
Line 53: Software-​with-​Python/​tree/​main/​Chapter11.
Line 54: Testing HTTP
Line 55: A frequent need when working with networking based applications is that we have to test
Line 56: both the server and client. If we are writing a distributed application, we are probably
Line 57: going to write both the client and the server ourselves, and that means we'll want to test
Line 58: both of them just as we did with our Chat application in previous chapters.
Line 59: 
Line 60: --- 페이지 254 ---
Line 61: Testing for the Web: WSGI versus HTTP
Line 62: Chapter 11
Line 63: [ 244 ]
Line 64: While we might want to have a limited number of tests that connect to a real running
Line 65: server, that quickly becomes too expensive if we involve real networking, and could also
Line 66: result in errors related to the maximum amount of open connections our system can
Line 67: handle, along with the time it takes to actually shut down those connections.
Line 68: So we need to be able to test the client side of the application without having to connect to a
Line 69: real server for the majority of our tests, or our test suite will quickly become
Line 70: unmaintainable.
Line 71: Let's suppose we are writing a very simple httpclient command-line application that
Line 72: will allow us to request any URL that we want with the most common HTTP methods:
Line 73: $ python -m httpclient GET http://www.amazon.com/
Line 74: <!DOCTYPE html>
Line 75: <html class="a-no-js" lang="en-us">
Line 76:     <head>
Line 77:         <title dir="ltr">Amazon.com</title>
Line 78:         ...
Line 79: To do so, we would first need a class able to perform HTTP requests, which we are going to
Line 80: call just HTTPClient. Our HTTPClient exposes support for GET, POST, and DELETE (we
Line 81: could easily expose more, but for the sake of simplicity we will limit our client to those
Line 82: most common methods), and a follow method that allows us to access nested paths
Line 83: relative to the current URL.
Line 84: To implement this object we are going to rely on the requests library for most of the
Line 85: heavy lifting of HTTP processing, thus we can run import requests and rely on it for
Line 86: most of our methods' implementations. Let's create a src/httpclient/__init__.py file
Line 87: where we can place our HTTPClient object:
Line 88: import urllib.parse
Line 89: import requests
Line 90: class HTTPClient:
Line 91:     def __init__(self, url):
Line 92:         self._url = url
Line 93:     def GET(self):
Line 94:         return requests.get(self._url).text
Line 95:     def POST(self, **kwargs):
Line 96:         return requests.post(self._url, data=kwargs).text
Line 97:     def DELETE(self):
Line 98:         return requests.delete(self._url).text
Line 99: 
Line 100: --- 페이지 255 ---
Line 101: Testing for the Web: WSGI versus HTTP
Line 102: Chapter 11
Line 103: [ 245 ]
Line 104:     def follow(self, path):
Line 105:         baseurl = self._url
Line 106:         if not baseurl.endswith("/"):
Line 107:             baseurl += "/"
Line 108:         return HTTPClient(urllib.parse.urljoin(baseurl, path))
Line 109: The only method not directly relying on requests is HTTPClient.follow, which uses the
Line 110: urllib.parse standard library module to navigate the URL tree.
Line 111: Given the current URL, which is used as the base, the method is going to return a new
Line 112: HTTPClient that points to a path nested within the same URL. For example, if we have a
Line 113: client pointing to "http://www.google.com/", then using HTTPClient.follow("me")
Line 114: would give us back a new client instance through which we can request
Line 115: http://www.google.com/me.
Line 116: Notice that this is a very naïve implementation that takes for granted the
Line 117: fact that the base URL doesn't have any parameters. A more robust
Line 118: implementation could be achieved if we actually parsed the URL and
Line 119: encoded it back into a string, so that we can isolate the path from the rest
Line 120: of the URL.
Line 121: Now that we have the client in place, the remaining parts are those involved in exposing it
Line 122: on the command line, so that we can use the python -m httpclient command to
Line 123: perform HTTP requests.
Line 124: The first piece we need to do so is the parse_args function. This function will be in charge
Line 125: of taking arguments from the command line (thus from sys.argv) and converting them to
Line 126: the options for HTTPClient:
Line 127: import sys
Line 128: def parse_args():
Line 129:     cmd = sys.argv[0]
Line 130:     args = sys.argv[1:]
Line 131:     try:
Line 132:         method, url, *params = args
Line 133:     except ValueError:
Line 134:         raise ValueError("Not enough arguments, "
Line 135:                          "at least METHOD URL must be provided")
Line 136:     try:
Line 137:         params = dict((p.split("=", 1) for p in params))
Line 138:     except ValueError:
Line 139:         raise ValueError("Invalid request body parameters. "
Line 140:                          "They must be in name=value format, "
Line 141: 
Line 142: --- 페이지 256 ---
Line 143: Testing for the Web: WSGI versus HTTP
Line 144: Chapter 11
Line 145: [ 246 ]
Line 146:                          f"not {params}")
Line 147:     return method.upper(), url, params
Line 148: The first code block is just going to separate the HTTP method, the URL we want to
Line 149: request, and the various params we want to provide it. The HTTP method accepts any
Line 150: number of params, so we could have zero or many.
Line 151: The second code block is meant to parse params from a "name=value" format to a
Line 152: dictionary we can pass to the HTTPClient.POST method.
Line 153: Finally, the function returns the HTTPClient method we have to invoke (GET, POST, or
Line 154: DELETE), the URL for which we have to invoke it, and the params dictionary containing all
Line 155: parameters.
Line 156: Those three values are useful to the real main function of our application to properly use
Line 157: the HTTPClient object. So the next step is to implement this main function so that we can
Line 158: invoke it from the command line:
Line 159: def main():
Line 160:     try:
Line 161:         method, url, params = parse_args()
Line 162:     except ValueError as err:
Line 163:         print(err)
Line 164:         return
Line 165:     client = HTTPClient(url)
Line 166:     print(getattr(client, method)(**params))
Line 167: main invokes parse_args, creates a client object, and then invokes the method
Line 168: requested by parse_args on it and prints the returned value.
Line 169: The remaining pieces we need to handle are, firstly, to create a
Line 170: src/httpclient/__main__.py file where we invoke the main function:
Line 171: from httpclient import main
Line 172: main()
Line 173: 
Line 174: --- 페이지 257 ---
Line 175: Testing for the Web: WSGI versus HTTP
Line 176: Chapter 11
Line 177: [ 247 ]
Line 178: And then a src/setup.py file that allows us to install the package and invoke it from the
Line 179: command line:
Line 180: from setuptools import setup
Line 181: setup(name='httpclient', packages=['httpclient'])
Line 182: If everything worked as expected, installing our package should allow us to invoke it from
Line 183: the command line to perform HTTP requests:
Line 184: $ pip install -e ./src
Line 185: Obtaining file://./src
Line 186: Installing collected packages: httpclient
Line 187: ...
Line 188: Successfully installed httpclient
Line 189: $ python -m httpclient GET http://httpbin.org/get
Line 190: {
Line 191:   "args": {},
Line 192:   "headers": {
Line 193:     "Accept": "*/*",
Line 194:     "Accept-Encoding": "gzip, deflate",
Line 195:     "Host": "httpbin.org",
Line 196:     "User-Agent": "python-requests/2.24.0",
Line 197:   },
Line 198:   "url": "http://httpbin.org/get"
Line 199: }
Line 200: Now that all the pieces are in place, we can move on to see how to test the HTTPClient
Line 201: object.
Line 202: Testing HTTP clients
Line 203: If we had to test our HTTPClient, we would have to perform HTTP requests through those
Line 204: methods to confirm they actually do what we want. To do so, we could use httpbin.org,
Line 205: which is a service that accepts any kind of request and echoes back what was submitted.
Line 206: This would allow us to verify that we are submitting what we expected we would send to
Line 207: the server:
Line 208: import json
Line 209: from httpclient import HTTPClient
Line 210: class TestHTTPClient:
Line 211:     def test_GET(self):
Line 212: 
Line 213: --- 페이지 258 ---
Line 214: Testing for the Web: WSGI versus HTTP
Line 215: Chapter 11
Line 216: [ 248 ]
Line 217:         client = HTTPClient(url="http://httpbin.org/get")
Line 218:         response = client.GET()
Line 219:         assert '"Host": "httpbin.org"' in response
Line 220:         assert '"args": {}' in response
Line 221:     def test_GET_params(self):
Line 222:         client = HTTPClient(url="http://httpbin.org/get?alpha=1")
Line 223:         response = client.GET()
Line 224:         response = json.loads(response)
Line 225:         assert response["headers"]["Host"] == "httpbin.org"
Line 226:         assert response["args"] == {"alpha": "1"}
Line 227:     def test_POST(self):
Line 228:         client = HTTPClient(url="http://httpbin.org/post?alpha=1")
Line 229:         response = client.POST(beta=2)
Line 230:         response = json.loads(response)
Line 231:         assert response["headers"]["Host"] == "httpbin.org"
Line 232:         assert response["args"] == {"alpha": "1"}
Line 233:         assert response["form"] == {"beta": "2"}
Line 234:     def test_DELETE(self):
Line 235:         client = HTTPClient(url="http://httpbin.org/anything/27")
Line 236:         response = client.DELETE()
Line 237:         assert '"method": "DELETE"' in response
Line 238:         assert '"url": "http://httpbin.org/anything/27"' in response
Line 239:     def test_follow(self):
Line 240:         client = HTTPClient(url="http://httpbin.org/anything")
Line 241:         assert client._url == "http://httpbin.org/anything"
Line 242:         client2 = client.follow("me")
Line 243:         assert client2._url == "http://httpbin.org/anything/me"
Line 244: Saving those tests as tests/test_httpclient.py will provide us with a running test
Line 245: suite that confirms that HTTPClient works as expected. The problem is that running the
Line 246: tests with this approach can take a while. Running just a few simple tests already takes
Line 247: more than a second to run:
Line 248: $ pytest -v -s
Line 249: ====================== test session starts ======================
Line 250: platform linux -- Python 3.8.6, pytest-6.0.2, py-1.9.0, pluggy-0.13.1
Line 251: ...
Line 252: 
Line 253: --- 페이지 259 ---
Line 254: Testing for the Web: WSGI versus HTTP
Line 255: Chapter 11
Line 256: [ 249 ]
Line 257: collected 5 items
Line 258: tests/test_httpclient.py::TestHTTPClient::test_GET PASSED
Line 259: tests/test_httpclient.py::TestHTTPClient::test_GET_params PASSED
Line 260: tests/test_httpclient.py::TestHTTPClient::test_POST PASSED
Line 261: tests/test_httpclient.py::TestHTTPClient::test_DELETE PASSED
Line 262: tests/test_httpclient.py::TestHTTPClient::test_follow PASSED
Line 263: ======================= 5 passed in 1.37s =======================
Line 264: Also, the tests might randomly fail due to network issues or errors on the remote server, so
Line 265: they could easily become flaky. Slow and flaky tests are something we must avoid in a test
Line 266: suite, so this approach of involving real networking is not something we can rely on in our
Line 267: test suite.
Line 268: The solution to both those problems is to replace the remote server, and thus the need for
Line 269: networking, with a fake implementation. In our specific case, as we used the requests
Line 270: library to perform HTTP requests to the server, we can prepare ready-made answers for
Line 271: our requests using the requests-mock library, which allows us to mock requests by
Line 272: replacing them with pre-baked responses.
Line 273: To replace our real requests with fake ones, we just have to wrap them in a
Line 274: requests_mock.Mocker() context manager, which comes from the requests_mock
Line 275: module made available by the requests-mock library. Once we have the mocker object,
Line 276: we can use it to drive what has to be mocked (which URL, method, and so on) and serve
Line 277: ready-made answers for all the requests that match those filters.
Line 278: For example, to mock a GET request, we could create the HTTPClient and before invoking
Line 279: client.GET we could wrap that method with the Mocker and thus set up a ready-made
Line 280: answer for any GET request against the same URL as the client one:
Line 281: client = HTTPClient(url="http://httpbin.org/get")
Line 282: with requests_mock.Mocker() as m:
Line 283:     m.get(client._url, text='{"Host": "httpbin.org", "args": {}}')
Line 284:     response = client.GET()
Line 285: The text, json, and content arguments of the mocker can be used to provide the
Line 286: response (as text, JSON, or binary) we want to serve back when the URL is requested with
Line 287: the specified method. In this case, for example, we provided the response in text format
Line 288: even though it contains a JSON string. In the following examples, we are going to use the
Line 289: json argument, so that we can see both of them in action.
Line 290: 
Line 291: --- 페이지 260 ---
Line 292: Testing for the Web: WSGI versus HTTP
Line 293: Chapter 11
Line 294: [ 250 ]
Line 295: Now we can adapt all our tests to use requests_mock so that they no longer have to take a
Line 296: networking roundtrip to pass:
Line 297: import json
Line 298: from httpclient import HTTPClient
Line 299: import requests_mock
Line 300: class TestHTTPClient:
Line 301:     def test_GET(self):
Line 302:         client = HTTPClient(url="http://httpbin.org/get")
Line 303:         with requests_mock.Mocker() as m:
Line 304:             m.get(client._url,
Line 305:                   text='{"Host": "httpbin.org", "args": {}}')
Line 306:             response = client.GET()
Line 307:         assert '"Host": "httpbin.org"' in response
Line 308:         assert '"args": {}' in response
Line 309:     def test_GET_params(self):
Line 310:         client = HTTPClient(url="http://httpbin.org/get?alpha=1")
Line 311:         with requests_mock.Mocker() as m:
Line 312:             m.get(client._url,
Line 313:                   text='''{"headers": {"Host": "httpbin.org"},
Line 314:                            "args": {"alpha": "1"}}''')
Line 315:             response = client.GET()
Line 316:         response = json.loads(response)
Line 317:         assert response["headers"]["Host"] == "httpbin.org"
Line 318:         assert response["args"] == {"alpha": "1"}
Line 319:     def test_POST(self):
Line 320:         client = HTTPClient(url="http://httpbin.org/post?alpha=1")
Line 321:         with requests_mock.Mocker() as m:
Line 322:             m.post(client._url, json={"headers": {"Host": "httpbin.org"},
Line 323:                                       "args": {"alpha": "1"},
Line 324:                                       "form": {"beta": "2"}})
Line 325:             response = client.POST(beta=2)
Line 326:         response = json.loads(response)
Line 327:         assert response["headers"]["Host"] == "httpbin.org"
Line 328:         assert response["args"] == {"alpha": "1"}
Line 329:         assert response["form"] == {"beta": "2"}
Line 330:     def test_DELETE(self):
Line 331:         client = HTTPClient(url="http://httpbin.org/anything/27")
Line 332:         with requests_mock.Mocker() as m:
Line 333:             m.delete(client._url, json={
Line 334: 
Line 335: --- 페이지 261 ---
Line 336: Testing for the Web: WSGI versus HTTP
Line 337: Chapter 11
Line 338: [ 251 ]
Line 339:                 "method": "DELETE",
Line 340:                 "url": "http://httpbin.org/anything/27"
Line 341:             })
Line 342:             response = client.DELETE()
Line 343:         assert '"method": "DELETE"' in response
Line 344:         assert '"url": "http://httpbin.org/anything/27"' in response
Line 345:     def test_follow(self):
Line 346:         ...
Line 347: The test_follow test remains unchanged as it didn't involve any networking, while the
Line 348: other tests are now wrapped in a requests_mock.Mocker() surrounding the
Line 349: client.GET, client.POST and client.DELETE calls.
Line 350: With those changes, the impact on our test suite is immediately visible. Tests that
Line 351: previously took more than a second to run now take just a few milliseconds:
Line 352: $ pytest -v -s
Line 353: ====================== test session starts ======================
Line 354: platform linux -- Python 3.8.6, pytest-6.0.2, py-1.9.0, pluggy-0.13.1
Line 355: ...
Line 356: collected 5 items
Line 357: tests/test_httpclient.py::TestHTTPClient::test_GET PASSED
Line 358: tests/test_httpclient.py::TestHTTPClient::test_GET_params PASSED
Line 359: tests/test_httpclient.py::TestHTTPClient::test_POST PASSED
Line 360: tests/test_httpclient.py::TestHTTPClient::test_DELETE PASSED
Line 361: tests/test_httpclient.py::TestHTTPClient::test_follow PASSED
Line 362: ======================= 5 passed in 0.03s =======================
Line 363: While this approach is fast, robust, and allows us to test that the client is properly able to
Line 364: process and react to answers, it doesn't really test that the client and the server are able to
Line 365: work together. Yes, we know that the client behaves like we meant it to behave, but it
Line 366: doesn't in any way guarantee that once we put it in front of a real server, the two will speak
Line 367: the same language.
Line 368: If the server changes its responses in a way that differs from the one we hardcoded in our
Line 369: tests, we will notice that the client doesn't work anymore with our server.
Line 370: To address this limitation without having to involve a real networking layer, we are going
Line 371: to see how we can write integration tests using WebTest and the WSGI protocol.
Line 372: 
Line 373: --- 페이지 262 ---
Line 374: Testing for the Web: WSGI versus HTTP
Line 375: Chapter 11
Line 376: [ 252 ]
Line 377: Testing WSGI with WebTest
Line 378: While we have seen how to test client without connecting to a real server, we can't rely only
Line 379: on faked messages to confirm that our application works. If we are going to change server
Line 380: responses, the tests wouldn't even notice and would continue to pass while in reality, the
Line 381: client has stopped working. How can we detect those kinds of issues without involving real
Line 382: networking? The WSGI (Web Server Gateway Interface) protocol and WebTest library
Line 383: come in hand to do exactly that, set up a client-server communication that involves no
Line 384: networking at all.
Line 385: When we create web applications in Python, the most frequent way they work is through
Line 386: an application server. The application server will be the one receiving HTTP requests,
Line 387: decoding them, and forwarding them to the real web application. Forwarding those
Line 388: requests to the web application and receiving back responses via the WSGI protocol is
Line 389: usually the communication channel of choice for Python.
Line 390: The WSGI protocol is a pure Python protocol, thus relies solely on being able to invoke a
Line 391: Python function passing some specific arguments. All the communication in WSGI happens
Line 392: in-memory and involves no dedicated parsing, and thus is very fast and usually suitable for
Line 393: integration in web applications. A complete description of WSGI is available in PEP 333
Line 394: (https:/​/​www.​python.​org/​dev/​peps/​pep-​3333/​).
Line 395: The most basic WSGI application is a simple callable (a function, method, or function
Line 396: object) that accepts two arguments (environ and start_response) and responds with an
Line 397: iterable containing the output to be sent back to the client after having invoked
Line 398: start_response to set up the response headers.
Line 399: So the basic "Hello World" kind of application in WSGI would look as follows:
Line 400: class Application:
Line 401:     def __call__(self, environ, start_response):
Line 402:         start_response(
Line 403:             '200 OK',
Line 404:             [('Content-type', 'text/plain; charset=utf-8')]
Line 405:         )
Line 406:         return ["Hello World".encode("utf-8")]
Line 407: The environ argument will contain all information about the environment within which
Line 408: our request is being processed, including information about the request itself, such as
Line 409: REQUEST_METHOD, HTTP_HOST, PATH_INFO, QUERY_STRING, and many more values.
Line 410: start_response is a function we can invoke to tell the application server that we are
Line 411: ready to send back our response and inform it about the response type and the HTTP
Line 412: headers that have to be sent back.
Line 413: 
Line 414: --- 페이지 263 ---
Line 415: Testing for the Web: WSGI versus HTTP
Line 416: Chapter 11
Line 417: [ 253 ]
Line 418: In our case, for every request, we always send back an HTTP 200 response informing the
Line 419: client that we are going to send some text encoded in UTF-8 by providing a Content-Type
Line 420: header.
Line 421: Then we return the iterable containing the response, which in this case is a list containing
Line 422: the "Hello World" string encoded as UTF-8 as specified in our Content-Type.
Line 423: Now that we have our WSGI application, we can save it in the
Line 424: src/wsgiwebtest/__init__.py file and move forward to see how we can attach it to the
Line 425: application server.
Line 426: For the sake of this example, we are going to use a very basic application server provided
Line 427: by the Python standard library itself in the wsgiref module,
Line 428: simple_server.WSGIServer. To be able to start our application we are going to create a
Line 429: src/wsgiwebtest/__main__.py file where we are going to place a main function that
Line 430: creates the WSGIServer and attaches it to our web application:
Line 431: from wsgiref.simple_server import make_server
Line 432: from wsgiwebtest import Application
Line 433: def main():
Line 434:     app = Application()
Line 435:     with make_server('', 8000, app) as httpd:
Line 436:         print("Serving on port 8000...")
Line 437:         httpd.serve_forever()
Line 438: main()
Line 439: All our main has to do is to create the Application object and pass it to the make_server
Line 440: function, which will create an application server for that application. Once the server is
Line 441: available we can start serving requests through the httpd.server_forever method.
Line 442: The last step before we can actually try our "Hello World application is to create a setup.py
Line 443: file so that we can install our package. So let's save a basic one as src/setup.py,
Line 444: containing the following:
Line 445: from setuptools import setup
Line 446: setup(name='wsgiwebtest', packages=['wsgiwebtest'])
Line 447: Now that we have all the pieces in place, we can install our application and start it:
Line 448: $ pip install -e ./src
Line 449: Obtaining file://./src
Line 450: Installing collected packages: wsgiwebtest
Line 451: 
Line 452: --- 페이지 264 ---
Line 453: Testing for the Web: WSGI versus HTTP
Line 454: Chapter 11
Line 455: [ 254 ]
Line 456: ...
Line 457: Successfully installed wsgiwebtest
Line 458: $ python -m wsgiwebtest
Line 459: Serving on port 8000...
Line 460: Pointing our browser to http://localhost:8000/ should greet us with a simple Hello
Line 461: World phrase:
Line 462: Figure 11.1 – Hello World answer from our WSGI application
Line 463: Now that we have a working web application, we want to evolve it to make it a bit more
Line 464: interesting. We are going to turn it into a simple clone of httpbin.org. To do so we are
Line 465: going to use the same exact tests we wrote for our HTTPClient package, port them to use
Line 466: WebTest, and use them to drive the development of our WSGI application.
Line 467: The first step is to take our existing TestHTTPClient.test_GET test and port it to use
Line 468: webtest to verify our web application, saving it as tests/test_wsgiapp.py:
Line 469: import webtest
Line 470: from wsgiwebtest import Application
Line 471: class TestWSGIApp:
Line 472:     def test_GET(self):
Line 473:         client = webtest.TestApp(Application())
Line 474:         response = client.get("http://httpbin.org/get").text
Line 475:         assert '"Host": "httpbin.org"' in response
Line 476:         assert '"args": {}' in response
Line 477: 
Line 478: --- 페이지 265 ---
Line 479: Testing for the Web: WSGI versus HTTP
Line 480: Chapter 11
Line 481: [ 255 ]
Line 482: The main difference is that instead of building an HTTPClient instance, we build a
Line 483: webtest.TestApp for the application we want to test, which in this case is
Line 484: wsgiwebtest.Application. Then we ask TestApp to perform a GET request against a
Line 485: specific URL using the TestApp.get method. While we can specify a complete URL
Line 486: including the domain, it won't matter too much, as TestApp will always direct the request
Line 487: to the application under test, so even though here we wrote "http://httpbin.org", in
Line 488: reality the request won't go to "httpbin.org" but to wsgiwebtest.Application. This
Line 489: allows us to test our application by simulating whatever domain we want to serve it on.
Line 490: Then the response returned by this request can be decoded as text or JSON as we did for
Line 491: the requests library, using the .text or .json properties. In this case, we are going to
Line 492: retain the existing test behavior and decode it as text even though the response is actually
Line 493: in JSON format.
Line 494: Running the test will obviously fail because right now our web application only responds
Line 495: with "Hello World" to every request, but it proves that our test actually reached our web
Line 496: application and got back the "Hello World" response:
Line 497: ______________________ TestWSGIApp.test_GET ______________________
Line 498: self = <test_wsgiapp.TestWSGIApp object at 0x7fc6d64feaf0>
Line 499:     def test_GET(self):
Line 500:         client = webtest.TestApp(Application())
Line 501:         response = client.get("http://httpbin.org/get")
Line 502: > assert '"Host": "httpbin.org"' in response
Line 503: E assert '"Host": "httpbin.org"' in <200 OK text/plain body=b'Hello World'>
Line 504: Now that we know that webtest is actually working as expected and is doing the GET
Line 505: request against our web application, let's start porting all our other tests to use webtest.
Line 506: The approach is nearly the same for all of them. Instead of building an HTTPClient
Line 507: instance, we are going to build a webtest.TestApp and use its .get, .post, and .delete
Line 508: methods to perform the requests:
Line 509: import webtest
Line 510: from wsgiwebtest import Application
Line 511: class TestWSGIApp:
Line 512:     def test_GET(self):
Line 513:         client = webtest.TestApp(Application())
Line 514:         response = client.get("http://httpbin.org/get").text
Line 515:         assert '"Host": "httpbin.org"' in response
Line 516: 
Line 517: --- 페이지 266 ---
Line 518: Testing for the Web: WSGI versus HTTP
Line 519: Chapter 11
Line 520: [ 256 ]
Line 521:         assert '"args": {}' in response
Line 522:     def test_GET_params(self):
Line 523:         client = webtest.TestApp(Application())
Line 524:         response = client.get(url="http://httpbin.org/get?alpha=1").json
Line 525:         assert response["headers"]["Host"] == "httpbin.org"
Line 526:         assert response["args"] == {"alpha": "1"}
Line 527:     def test_POST(self):
Line 528:         client = webtest.TestApp(Application())
Line 529:         response = client.post(url="http://httpbin.org/get?alpha=1",
Line 530:                                params={"beta": "2"}).json
Line 531:         assert response["headers"]["Host"] == "httpbin.org"
Line 532:         assert response["args"] == {"alpha": "1"}
Line 533:         assert response["form"] == {"beta": "2"}
Line 534:     def test_DELETE(self):
Line 535:         client = webtest.TestApp(Application())
Line 536:         response = client.delete(url="http://httpbin.org/anything/27").text
Line 537:         assert '"method": "DELETE"' in response
Line 538:         assert '"url": "http://httpbin.org/anything/27"' in response
Line 539: The assertion part of the tests remained unmodified from the original tests we copied, the
Line 540: only part that slightly changed is how we perform the requests.
Line 541: Like the first test, those new tests will currently all fail because our web application will
Line 542: always respond with "Hello World" to all of them. So the next step is to change our web
Line 543: application to make it respond as the tests expect.
Line 544: We can open our existing src/wsgiwebtest/__init__.py file and tweak the
Line 545: Application.__call__ method to make it recognize the requested host, URL, and
Line 546: method while also parsing the received request parameters from both the URL and the
Line 547: request body:
Line 548: import urllib.parse
Line 549: class Application:
Line 550:     def __call__(self, environ, start_response):
Line 551:         start_response(
Line 552:             '200 OK',
Line 553:             [('Content-type', 'application/json; charset=utf-8')]
Line 554: 
Line 555: --- 페이지 267 ---
Line 556: Testing for the Web: WSGI versus HTTP
Line 557: Chapter 11
Line 558: [ 257 ]
Line 559:         )
Line 560:         form_params = {}
Line 561:         if environ.get('CONTENT_TYPE') ==
Line 562:                'application/x-www-form-urlencoded':
Line 563:             req_body = environ["wsgi.input"].read().decode("ascii")
Line 564:             form_params = {
Line 565:                 k: v for k, v in urllib.parse.parse_qsl(req_body)
Line 566:             }
Line 567:         if environ.get("SERVER_PORT") == "80":
Line 568:             host = environ["SERVER_NAME"]
Line 569:         else:
Line 570:             host = environ["HTTP_HOST"]
Line 571:         return [json.dumps({
Line 572:             "method": environ["REQUEST_METHOD"],
Line 573:             "headers": {"Host": host},
Line 574:             "url": "{e[wsgi.url_scheme]}://{host}{e[PATH_INFO]}".format(
Line 575:                 e=environ,
Line 576:                 host=host
Line 577:             ),
Line 578:             "args": {
Line 579:                 k: v for k, v in
Line 580:                   urllib.parse.parse_qsl(environ["QUERY_STRING"])
Line 581:             },
Line 582:             "form": form_params
Line 583:         }).encode("utf-8")]
Line 584: The start_response invocation is nearly the same, we just changed the reported
Line 585: Content-Type to be application/json instead of text/plain as we are going to serve
Line 586: back a JSON response.
Line 587: Right after this, form_params is meant to contain all the parameters provided through the
Line 588: request body. If what we received is a POST request, it's probably going to have a request
Line 589: body where the majority of the parameters are provided. The request body could provide
Line 590: those parameters encoded in various ways, but as it's the simplest one (and the one our
Line 591: tests used), we are going to support only the "application/x-www-form-urlencoded"
Line 592: encoding. So if the request we received has that content type, we will also parse the request
Line 593: body (coming from environ["wsgi.input"]) and extract the parameters from there.
Line 594: 
Line 595: --- 페이지 268 ---
Line 596: Testing for the Web: WSGI versus HTTP
Line 597: Chapter 11
Line 598: [ 258 ]
Line 599: The subsequent code block that initializes the host variable is instead meant to find the
Line 600: host and port from which the request came, so that we can send it back into the Host field
Line 601: of the headers dictionary in our response as the tests expect. The test expects that if the
Line 602: request is targeted to the standard HTTP port, 80, the port is omitted in the returned host.
Line 603: So we are going to only report the port when it's not 80 and we are going to limit ourselves
Line 604: to the SERVER_NAME when the port is 80.
Line 605: The last block is actually focused on building back the response, so it uses json.dumps to
Line 606: encode a dictionary with all the data as text. The dictionary is going to contain the fields
Line 607: our tests care about, meaning method and headers.Host for the HTTP method that was
Line 608: used to perform the request, and the Host against which the request was targeted (in our
Line 609: tests, this is httpbin.org). This will also contain the args key for all the parameters
Line 610: provided in the query string, and thus in the URL itself, while separating the parameters
Line 611: that were provided in the request body in the form key. Finally, the url key contains the
Line 612: fully qualified URL that was requested.
Line 613: This should guarantee a behavior very similar to the one that the real httpbin.org
Line 614: provides, albeit heavily simplified. Saving back our new code and trying to rerun the tests
Line 615: should prove that we implemented something that is similar enough to make our tests
Line 616: pass:
Line 617: $ pytest -v -s
Line 618: ====================== test session starts ======================
Line 619: platform linux -- Python 3.8.6, pytest-6.0.2, py-1.9.0, pluggy-0.13.1
Line 620: ...
Line 621: collected 4 items
Line 622: tests/test_wsgiapp.py::TestHTTPClient::test_GET PASSED [ 25%]
Line 623: tests/test_wsgiapp.py::TestHTTPClient::test_GET_params PASSED [ 50%]
Line 624: tests/test_wsgiapp.py::TestHTTPClient::test_POST PASSED [ 75%]
Line 625: tests/test_wsgiapp.py::TestHTTPClient::test_DELETE PASSED [100%]
Line 626: ======================= 4 passed in 0.08s =======================
Line 627: Our tests passed, proving that our web application is similar enough to the original one we
Line 628: meant to copy, and even though there is tons of space for improvement, it demonstrated
Line 629: how we can implement tests for web applications that don't need any networking at all.
Line 630: This is made clear by the fact that our tests using WebTest still complete in a matter of
Line 631: milliseconds, similar to the tests where we used requests-mock, while the tests that
Line 632: involved real networking took more than a second.
Line 633: 
Line 634: --- 페이지 269 ---
Line 635: Testing for the Web: WSGI versus HTTP
Line 636: Chapter 11
Line 637: [ 259 ]
Line 638: If we want to go even further, using a little bit of dependency injection, we could easily
Line 639: modify our HTTPClient object to work with both the requests module and the
Line 640: webtest.TestApp object, as they are similar enough that we could write end-to-end tests
Line 641: that go from HTTPClient down to wsgiwebtest.Application without ever involving
Line 642: any HTTP parsing or networking.
Line 643: Going in this direction requires a brief change to our original HTTPClient to allow us to
Line 644: provide a replacement for the requests module at initialization time. By default, we are
Line 645: going to keep using the requests module, but anyone could pass a different object to
Line 646: HTTPClient.__init__ and replace it:
Line 647: class HTTPClient:
Line 648:     def __init__(self, url, requests=requests):
Line 649:         self._url = url
Line 650:         self._requests = requests
Line 651:     def follow(self, path):
Line 652:         baseurl = self._url
Line 653:         if not baseurl.endswith("/"):
Line 654:             baseurl += "/"
Line 655:         return HTTPClient(urllib.parse.urljoin(baseurl, path))
Line 656:     def GET(self):
Line 657:         return self._requests.get(self._url).text
Line 658:     def POST(self, **kwargs):
Line 659:         return self._requests.post(self._url, kwargs).text
Line 660:     def DELETE(self):
Line 661:         return self._requests.delete(self._url).text
Line 662: Then we have to use self._requests everywhere instead of just requests. The TestApp
Line 663: and requests interfaces are similar enough that the only change we actually need to the
Line 664: rest of the code is to omit the name of the argument (data=) from the post method and
Line 665: invoke it with a positional argument. This is because in requests, the argument is named
Line 666: data, while in TestApp it is named params. Passing it by position means that we don't
Line 667: need to worry about what name it has.
Line 668: 
Line 669: --- 페이지 270 ---
Line 670: Testing for the Web: WSGI versus HTTP
Line 671: Chapter 11
Line 672: [ 260 ]
Line 673: Now our HTTPClient is ready to accept a replacement for requests and we can take back
Line 674: the original version of the tests we wrote for HTTPClient (the one that didn't use
Line 675: requests-mock) and pass an instance of webtest.TestApp(wsgiwebtest.
Line 676: Application) as the replacement for requests:
Line 677: import json
Line 678: import webtest
Line 679: from wsgiwebtest import Application
Line 680: from httpclient import HTTPClient
Line 681: class TestHTTPClientWebTest:
Line 682:     def test_GET(self):
Line 683:         client = HTTPClient(url="http://httpbin.org/get",
Line 684:                             requests=webtest.TestApp(Application()))
Line 685:         response = client.GET()
Line 686:         assert '"Host": "httpbin.org"' in response
Line 687:         assert '"args": {}' in response
Line 688:     def test_GET_params(self):
Line 689:         client = HTTPClient(url="http://httpbin.org/get?alpha=1",
Line 690:                             requests=webtest.TestApp(Application()))
Line 691:         response = client.GET()
Line 692:         response = json.loads(response)
Line 693:         assert response["headers"]["Host"] == "httpbin.org"
Line 694:         assert response["args"] == {"alpha": "1"}
Line 695:     def test_POST(self):
Line 696:         client = HTTPClient(url="http://httpbin.org/post?alpha=1",
Line 697:                             requests=webtest.TestApp(Application()))
Line 698:         response = client.POST(beta=2)
Line 699:         response = json.loads(response)
Line 700:         assert response["headers"]["Host"] == "httpbin.org"
Line 701:         assert response["args"] == {"alpha": "1"}
Line 702:         assert response["form"] == {"beta": "2"}
Line 703:     def test_DELETE(self):
Line 704:         client = HTTPClient(url="http://httpbin.org/anything/27",
Line 705:                             requests=webtest.TestApp(Application()))
Line 706:         response = client.DELETE()
Line 707: 
Line 708: --- 페이지 271 ---
Line 709: Testing for the Web: WSGI versus HTTP
Line 710: Chapter 11
Line 711: [ 261 ]
Line 712:         assert '"method": "DELETE"' in response
Line 713:         assert '"url": "http://httpbin.org/anything/27"' in response
Line 714: If we save those tests as tests/test_client_webtest.py, they will keep working
Line 715: exactly like before, but they will submit real requests to wsgiwebtest.Application
Line 716: through the WSGI protocol, thus making sure that both the server and the client are able to
Line 717: work together:
Line 718: $ pytest -v -s
Line 719: ====================== test session starts ======================
Line 720: platform linux -- Python 3.8.6, pytest-6.0.2, py-1.9.0, pluggy-0.13.1
Line 721: ...
Line 722: collected 4 items
Line 723: tests/test_client_webtest.py::TestHTTPClientWebTest::test_GET PASSED [ 25%]
Line 724: tests/test_client_webtest.py::TestHTTPClientWebTest::test_GET_params PASSED
Line 725: [ 50%]
Line 726: tests/test_client_webtest.py::TestHTTPClientWebTest::test_POST PASSED [
Line 727: 75%]
Line 728: tests/test_client_webtest.py::TestHTTPClientWebTest::test_DELETE PASSED
Line 729: [100%]
Line 730: ======================= 4 passed in 0.08s =======================
Line 731: Any change to one of the two that makes it incompatible with the other would immediately
Line 732: cause the tests to fail, thus verifying that the two work correctly together without any of the
Line 733: overhead of network-based communication or the flakiness that it involves.
Line 734: All this is made possible by the fact that we used the WSGI standard to develop our web
Line 735: application and, as we are going to see in the next section, WSGI is the most widespread
Line 736: web development standard in Python and is supported by all major web frameworks.
Line 737: Using WebTest with web frameworks
Line 738: We have seen how to use WebTest with a plain WSGI application, but thanks to the fact
Line 739: that WSGI is widely adopted by all major web frameworks, it's possible to use WebTest
Line 740: with nearly all Python web frameworks.
Line 741: To showcase how WebTest is able to work with most Python web frameworks, we are
Line 742: going to replicate our httpbin in four web frameworks: Django, Flask, Pyramid, and
Line 743: TurboGears2, and for all of them we are going to use the same exact test suite. So we will
Line 744: share a single test suite between four different frameworks.
Line 745: 
Line 746: --- 페이지 272 ---
Line 747: Testing for the Web: WSGI versus HTTP
Line 748: Chapter 11
Line 749: [ 262 ]
Line 750: The first step is to create a test suite that can verify that our web applications are starting
Line 751: correctly. We are going to do so by adding a test that verifies all four web applications'
Line 752: answering with a "Hello World" message on the index of the website.
Line 753: The first step is to create a tests/test_wsgiapp.py file that's going to contain our only
Line 754: test for now:
Line 755: import webtest
Line 756: class TestWSGIApp:
Line 757:     def test_home(self, wsgiapp):
Line 758:         client = webtest.TestApp(wsgiapp)
Line 759:         response = client.get("http://httpbin.org/").text
Line 760:         assert 'Hello World' in response
Line 761: The test is fairly simple – it takes a WSGI application and checks that, on the index of the
Line 762: website, the response contains the "Hello World" string.
Line 763: The interesting part is how we are going to provide that wsgiapp object, as it has to be
Line 764: different for each web framework. So we are going to add an option to our test suite to
Line 765: choose which web framework to use and thus which application to create.
Line 766: We are going to do so by creating a tests/conftest.py file that is going to contain both
Line 767: the new option and the fixture to create the wsgiapp. The first thing we want to add is
Line 768: support for the new option:
Line 769: import pytest
Line 770: def pytest_addoption(parser):
Line 771:     parser.addoption(
Line 772:         "--framework", action="store",
Line 773:         help="Choose which framework to use for "
Line 774:              "the web application: [tg2, django, flask, pyramid]"
Line 775:     )
Line 776: 
Line 777: --- 페이지 273 ---
Line 778: Testing for the Web: WSGI versus HTTP
Line 779: Chapter 11
Line 780: [ 263 ]
Line 781: If things work correctly, once we save the tests/conftest.py file, running pytest --
Line 782: help will properly show the new option in the custom ones:
Line 783: $ pytest --help
Line 784: ...
Line 785: custom options:
Line 786:   --framework=FRAMEWORK
Line 787:                         Choose which framework to use for the
Line 788:                         web application: [tg2, django, flask, pyramid]
Line 789: Now that we have the option available, we must create the fixture that is going to use the
Line 790: option, the wsgiapp fixture. As it's a fixture available for all our test suites, we can just add
Line 791: it to the conftest.py file under the new option:
Line 792: @pytest.fixture
Line 793: def wsgiapp(request):
Line 794:     framework = request.config.getoption("--framework")
Line 795:     if framework == "tg2":
Line 796:         from wbtframeworks.tg2 import make_application
Line 797:     elif framework == "flask":
Line 798:         from wbtframeworks.flask import make_application
Line 799:     elif framework == "pyramid":
Line 800:         from wbtframeworks.pyramid import make_application
Line 801:     elif framework == "django":
Line 802:         from wbtframeworks.django import make_application
Line 803:     else:
Line 804:         make_application = None
Line 805:     if make_application is not None:
Line 806:         return make_application()
Line 807:     if framework is None:
Line 808:         raise ValueError("Please pick a framework with --framework option")
Line 809:     else:
Line 810:         raise ValueError(f"Invalid framework {framework}")
Line 811: The first thing that the fixture does is retrieve the selected framework through the option.
Line 812: Then, depending on which framework was selected, it's going to import the function that
Line 813: creates a new WSGI application from the module dedicated to that framework.
Line 814: For convenience, we added all four modules (tg2, flask, pyramid, and django) under the
Line 815: same wbtframeworks package, which is the one we are going to install.
Line 816: 
Line 817: --- 페이지 274 ---
Line 818: Testing for the Web: WSGI versus HTTP
Line 819: Chapter 11
Line 820: [ 264 ]
Line 821: Once a framework is selected and the make_application function is imported, the fixture
Line 822: will just return the new application built by the factory function. The remaining lines of
Line 823: code are to handle the case where the user picks an unsupported framework (or no
Line 824: framework at all).
Line 825: Running pytest now should lead to it correctly complaining that we have picked no
Line 826: framework:
Line 827: $ pytest -v
Line 828: ================ test session starts ================
Line 829: platform linux -- Python 3.8.6, pytest-6.0.2, py-1.9.0, pluggy-0.13.1
Line 830: collected 1 item
Line 831: tests/test_wsgiapp.py::TestWSGIApp::test_home ERROR [100%]
Line 832: ======================= ERRORS ======================
Line 833: ______ ERROR at setup of TestWSGIApp.test_home ______
Line 834: request = <SubRequest 'wsgiapp' for <Function test_home>>
Line 835:     @pytest.fixture
Line 836:     def wsgiapp(request):
Line 837:         ...
Line 838:         elif framework is None:
Line 839: > raise ValueError("Please pick a framework with --framework option")
Line 840: E ValueError: Please pick a framework with --framework option
Line 841: tests/conftest.py:31: ValueError
Line 842: =================== short test summary info ===================
Line 843: ERROR tests/test_wsgiapp.py::TestWSGIApp::test_home -
Line 844:         ValueError: Please pick a framework with --framework option
Line 845: ======================= 1 error in 0.15s =======================
Line 846: To confirm that the option is working as expected, we can run pytest with the --
Line 847: framework=flask option to see what happens:
Line 848: $ pytest -v --framework=flask
Line 849: ================ test session starts ================
Line 850: platform linux -- Python 3.8.6, pytest-6.0.2, py-1.9.0, pluggy-0.13.1
Line 851: collected 1 item
Line 852: tests/test_wsgiapp.py::TestWSGIApp::test_home ERROR [100%]
Line 853: ======================= ERRORS ======================
Line 854: ______ ERROR at setup of TestWSGIApp.test_home ______
Line 855: request = <SubRequest 'wsgiapp' for <Function test_home>>
Line 856: 
Line 857: --- 페이지 275 ---
Line 858: Testing for the Web: WSGI versus HTTP
Line 859: Chapter 11
Line 860: [ 265 ]
Line 861:     @pytest.fixture
Line 862:     def wsgiapp(request):
Line 863:         framework = request.config.getoption("--framework")
Line 864:         if framework == "tg2":
Line 865: > from wbtframeworks.tg2 import make_application
Line 866: E ModuleNotFoundError: No module named 'wbtframeworks'
Line 867: tests/conftest.py:31: ValueError
Line 868: =================== short test summary info ===================
Line 869: ERROR tests/test_wsgiapp.py::TestWSGIApp::test_home -
Line 870:         ModuleNotFoundError: No module named 'wbtframeworks'
Line 871: ======================= 1 error in 0.15s =======================
Line 872: In this second case, it recognized the option correctly, but it complained that the
Line 873: wbtframeworks package is not yet installed. That's expected as we haven't yet even
Line 874: created it.
Line 875: First, let's create a src/setup.py file to make the wbtframeworks package installable:
Line 876: from setuptools import setup
Line 877: setup(name='wbtframeworks', packages=['wbtframeworks'])
Line 878: Now that the wbtframeworks package is installable, the next step is to create the package
Line 879: itself, by creating the src/wbtframeworks/__init__.py file and then installing it:
Line 880: $ pip install -e src
Line 881: Obtaining file://src
Line 882: Installing collected packages: wbtframeworks
Line 883:   Running setup.py develop for wbtframeworks
Line 884: Successfully installed wbtframeworks
Line 885: Now that the package is available and installed in editable mode, we have to create the
Line 886: structure for the four frameworks.
Line 887: For the sake of keeping things short, as the sole purpose of those web applications is to
Line 888: showcase how the same test suite can work against the four of them, we are going to use all
Line 889: four frameworks in minimal mode, constraining the application to a single file.
Line 890: The first one we are going to add is the src/wbtframeworks/flask/__init__.py file, to
Line 891: add support for Flask:
Line 892: from flask import Flask
Line 893: app = Flask(__name__)
Line 894: @app.route('/')
Line 895: def hello_world():
Line 896: 
Line 897: --- 페이지 276 ---
Line 898: Testing for the Web: WSGI versus HTTP
Line 899: Chapter 11
Line 900: [ 266 ]
Line 901:     return 'Hello World'
Line 902: def make_application():
Line 903:     return app.wsgi_app
Line 904: We can confirm this minimal application works as expected by running our tests with
Line 905: pytest --frameworks=flask:
Line 906: $ pytest -v --framework=flask
Line 907: ====================== test session starts ======================
Line 908: platform linux -- Python 3.8.6, pytest-6.0.2, py-1.9.0, pluggy-0.13.1
Line 909: collected 1 item
Line 910: tests/test_wsgiapp.py::TestWSGIApp::test_home PASSED [100%]
Line 911: ======================= 1 passed in 0.13s =======================
Line 912: We use the same technique to create a src/wbtframeworks/pyramid/__init__.py file
Line 913: for the Pyramid application:
Line 914: from pyramid.config import Configurator
Line 915: from pyramid.response import Response
Line 916: def hello_world(request):
Line 917:     return Response('Hello World!')
Line 918: def make_application():
Line 919:     with Configurator() as config:
Line 920:         config.add_route('hello', '/')
Line 921:         config.add_view(hello_world, route_name='hello')
Line 922:         return config.make_wsgi_app()
Line 923: Likewise, let's create the src/wbtframeworks/tg2/__init__.py for the TurboGears2
Line 924: application as follows:
Line 925: from tg import expose, TGController
Line 926: from tg import MinimalApplicationConfigurator
Line 927: class RootController(TGController):
Line 928:     @expose()
Line 929:     def index(self):
Line 930:         return 'Hello World'
Line 931: 
Line 932: --- 페이지 277 ---
Line 933: Testing for the Web: WSGI versus HTTP
Line 934: Chapter 11
Line 935: [ 267 ]
Line 936: def make_application():
Line 937:     config = MinimalApplicationConfigurator()
Line 938:     config.update_blueprint({
Line 939:         'root_controller': RootController()
Line 940:     })
Line 941:     return config.make_wsgi_app()
Line 942: And finally, create a src/wbtframeworks/django/__init__.py file for the Django
Line 943: application:
Line 944: import sys
Line 945: import os
Line 946: from django.conf.urls import re_path
Line 947: from django.conf import settings
Line 948: from django.http import HttpResponse
Line 949: settings.configure(
Line 950:     DEBUG=True,
Line 951:     ROOT_URLCONF=sys.modules[__name__],
Line 952:     ALLOWED_HOSTS=["httpbin.org"]
Line 953: )
Line 954: def home(request):
Line 955:     return HttpResponse('Hello World')
Line 956: urlpatterns = [
Line 957:     re_path(r'^$', home),
Line 958: ]
Line 959: def make_application():
Line 960:     from django.core.wsgi import get_wsgi_application
Line 961:     os.environ.setdefault('DJANGO_SETTINGS_MODULE',
Line 962:                           'wbtframeworks.django.settings')
Line 963:     return get_wsgi_application()
Line 964: Once all of them are available, we can see that our test is able to run against all four of them
Line 965: without any difference. It can run against TurboGears2:
Line 966: $ pytest --framework=tg2
Line 967: ====================== test session starts ======================
Line 968: platform linux -- Python 3.8.6, pytest-6.0.2, py-1.9.0, pluggy-0.13.1
Line 969: collected 1 item
Line 970: tests/test_wsgiapp.py .                                    [100%]
Line 971: 
Line 972: --- 페이지 278 ---
Line 973: Testing for the Web: WSGI versus HTTP
Line 974: Chapter 11
Line 975: [ 268 ]
Line 976: ======================= 1 passed in 0.13s =======================
Line 977: And it can be run against Django without any changes:
Line 978: $ pytest --framework=django
Line 979: ====================== test session starts ======================
Line 980: platform linux -- Python 3.8.6, pytest-6.0.2, py-1.9.0, pluggy-0.13.1
Line 981: collected 1 item
Line 982: tests/test_wsgiapp.py .                                    [100%]
Line 983: ======================= 1 passed in 0.13s =======================
Line 984: Now that we are sure that our test suite can run against all four frameworks, we will extend
Line 985: it with the other tests we had for our httpbin.org clone:
Line 986: import webtest
Line 987: class TestWSGIApp:
Line 988:     def test_home(self, wsgiapp):
Line 989:         client = webtest.TestApp(wsgiapp)
Line 990:         response = client.get("http://httpbin.org/").text
Line 991:         assert 'Hello World' in response
Line 992:     def test_GET(self, wsgiapp):
Line 993:         client = webtest.TestApp(wsgiapp)
Line 994:         response = client.get("http://httpbin.org/get").text
Line 995:         assert '"Host": "httpbin.org"' in response
Line 996:         assert '"args": {}' in response
Line 997:     def test_GET_params(self, wsgiapp):
Line 998:         client = webtest.TestApp(wsgiapp)
Line 999:         response = client.get(url="http://httpbin.org/get?alpha=1").json
Line 1000:         assert response["headers"]["Host"] == "httpbin.org"
Line 1001:         assert response["args"] == {"alpha": "1"}
Line 1002:     def test_POST(self, wsgiapp):
Line 1003:         client = webtest.TestApp(wsgiapp)
Line 1004:         response = client.post(url="http://httpbin.org/get?alpha=1",
Line 1005:                                params={"beta": "2"}).json
Line 1006:         assert response["headers"]["Host"] == "httpbin.org"
Line 1007: 
Line 1008: --- 페이지 279 ---
Line 1009: Testing for the Web: WSGI versus HTTP
Line 1010: Chapter 11
Line 1011: [ 269 ]
Line 1012:         assert response["args"] == {"alpha": "1"}
Line 1013:         assert response["form"] == {"beta": "2"}
Line 1014:     def test_DELETE(self, wsgiapp):
Line 1015:         client = webtest.TestApp(wsgiapp)
Line 1016:         response = client.delete(url="http://httpbin.org/anything/27").text
Line 1017:         assert '"method": "DELETE"' in response
Line 1018:         assert '"url": "http://httpbin.org/anything/27"' in response
Line 1019: Running the tests now against any framework will complain that those URLs lead to a 404
Line 1020: error, as we haven't yet implemented them. For example, running the tests for Pyramid
Line 1021: would lead only to the test_home one succeeding and the others failing:
Line 1022: $ pytest --framework=pyramid
Line 1023: ====================== test session starts ======================
Line 1024: platform linux -- Python 3.8.6, pytest-6.0.2, py-1.9.0, pluggy-0.13.1
Line 1025: collected 1 item
Line 1026: tests/test_wsgiapp.py .FFFF                                [100%]
Line 1027: ==================== short test summary info ====================
Line 1028: FAILED test_GET - webtest.app.AppError: 404 Not Found (not 200 OK o...
Line 1029: FAILED test_GET_params - webtest.app.AppError: 404 Not Found (not 2...
Line 1030: FAILED test_POST - webtest.app.AppError: 404 Not Found (not 200 OK ...
Line 1031: FAILED test_DELETE - webtest.app.AppError: 404 Not Found (not 200 O...
Line 1032: ================== 4 failed, 1 passed in 0.37s ==================
Line 1033: Now that our test suite can run for all four implementations of our application, we only
Line 1034: have to proceed with the actual implementation. Given that it doesn't add much value
Line 1035: having the same web application implemented in four different frameworks (outside of
Line 1036: being a good exercise to learn those frameworks), we are going to provide only the
Line 1037: implementation using Django and will leave to the readers the work of implementing it on
Line 1038: the other three frameworks if they wish.
Line 1039: Thus we are going to open our src/wbtframeworks/django/__init__.py file and edit
Line 1040: it to add the remaining routes with the pieces that are lacking:
Line 1041: import sys, json
Line 1042: from django.conf.urls import re_path
Line 1043: from django.conf import settings
Line 1044: from django.http import HttpResponse
Line 1045: settings.configure(
Line 1046:     DEBUG=True,
Line 1047:     ROOT_URLCONF=sys.modules[__name__],
Line 1048:     ALLOWED_HOSTS=["httpbin.org"]
Line 1049: 
Line 1050: --- 페이지 280 ---
Line 1051: Testing for the Web: WSGI versus HTTP
Line 1052: Chapter 11
Line 1053: [ 270 ]
Line 1054: )
Line 1055: def home(request):
Line 1056:     return HttpResponse('Hello World')
Line 1057: def get(request):
Line 1058:     if request.META.get("SERVER_PORT") == "80":
Line 1059:         host_no_default_port = request.META["HTTP_HOST"].replace(":80", "")
Line 1060:         request.META["HTTP_HOST"] = host_no_default_port
Line 1061:     host = request.META["HTTP_HOST"]
Line 1062:     response = HttpResponse(json.dumps({
Line 1063:         "method": request.META["REQUEST_METHOD"],
Line 1064:         "headers": {"Host": host},
Line 1065:         "args": {
Line 1066:             p: v for (p, v) in request.GET.items()
Line 1067:         },
Line 1068:         "form": {
Line 1069:             p: v for (p, v) in request.POST.items()
Line 1070:         },
Line 1071:         "url": request.build_absolute_uri()
Line 1072:     }, sort_keys=True))
Line 1073:     response['Content-Type'] = 'application/json'
Line 1074:     return response
Line 1075: urlpatterns = [
Line 1076:     re_path(r'^get$', get),
Line 1077:     re_path(r"^anything.*$", get),
Line 1078:     re_path(r'^$', home),
Line 1079: ]
Line 1080: def make_application():
Line 1081:     import os
Line 1082:     from django.core.wsgi import get_wsgi_application
Line 1083:     os.environ.setdefault('DJANGO_SETTINGS_MODULE',
Line 1084:                           'wbtframeworks.django.settings')
Line 1085:     return get_wsgi_application()
Line 1086: Running our tests now would confirm that, at least for Django, they are able to pass and
Line 1087: succeed:
Line 1088: $ pytest --framework=django
Line 1089: ====================== test session starts ======================
Line 1090: platform linux -- Python 3.8.6, pytest-6.0.2, py-1.9.0, pluggy-0.13.1
Line 1091: collected 5 items
Line 1092: 
Line 1093: --- 페이지 281 ---
Line 1094: Testing for the Web: WSGI versus HTTP
Line 1095: Chapter 11
Line 1096: [ 271 ]
Line 1097: tests/test_wsgiapp.py .....                                [100%]
Line 1098: ======================= 5 passed in 0.27s =======================
Line 1099: This is a very naïve and basic implementation for the sole purpose of showing that our tests
Line 1100: are able to pass once the application is provided, but it proves that on Django, we are
Line 1101: perfectly able to use WebTest like we would for any other WSGI framework.
Line 1102: But WebTest is not the only way we can test Django applications. Django also provides its
Line 1103: own testing client, so let's see how we would test the same application using Django's test
Line 1104: client instead of WebTest.
Line 1105: Writing Django tests with Django's test
Line 1106: client
Line 1107: While on Python the most widespread testing toolkit is pytest, some web frameworks
Line 1108: provide their own solutions for managing test suites. Django is one such example, even
Line 1109: though it's possible (as we have seen in the previous section), most people tend to run their
Line 1110: tests with the Django test client, which provides the same capabilities as WebTest but is a
Line 1111: solution built explicitly for Django.
Line 1112: In this section, we are going to see how we can create a Django project and then run its tests
Line 1113: using the standard Django testing infrastructure as well as a pytest-based one:
Line 1114: The first step will be to create a new Django project, which we are going to call
Line 1115: 1.
Line 1116: djapp:
Line 1117: $ django-admin startproject djapp
Line 1118: This will create a djapp directory where we can manage our Django project. In
Line 1119: the project directory, we will find a manage.py file, which allows us to run
Line 1120: various management operations for our project, from setting up the database to
Line 1121: starting the web application itself and running tests the Django way.
Line 1122: The next step is to actually put an application inside our project. As our
Line 1123: 2.
Line 1124: application will be the httpbin one we already wrote, we will just call the
Line 1125: application httpbin. To create a new application inside a project, we can use the
Line 1126: manage.py startapp command:
Line 1127: $ python manage.py startapp httpbin
Line 1128: 
Line 1129: --- 페이지 282 ---
Line 1130: Testing for the Web: WSGI versus HTTP
Line 1131: Chapter 11
Line 1132: [ 272 ]
Line 1133: Now that the httpbin application is available, we have to copy the content of
Line 1134: 3.
Line 1135: the wbtframeworks/django/__init__.py file we just wrote in the previous
Line 1136: section. The first things we have to copy are the two home and get views, which 
Line 1137: have to be copied inside the djapp/httpbin/views.py file:
Line 1138: import json
Line 1139: from django.http import HttpResponse
Line 1140: def home(request):
Line 1141:     return HttpResponse('Hello World')
Line 1142: def get(request):
Line 1143:     if request.META.get("SERVER_PORT") == "80":
Line 1144:         http_host = request.META.get("HTTP_HOST", "httpbin.org")
Line 1145:         host_no_default_port = http_host.replace(":80", "")
Line 1146:         request.META["HTTP_HOST"] = host_no_default_port
Line 1147:     host = request.META["HTTP_HOST"]
Line 1148:     response = HttpResponse(json.dumps({
Line 1149:         "method": request.META["REQUEST_METHOD"],
Line 1150:         "headers": {"Host": host},
Line 1151:         "args": {
Line 1152:             p: v for (p, v) in request.GET.items()
Line 1153:         },
Line 1154:         "form": {
Line 1155:             p: v for (p, v) in request.POST.items()
Line 1156:         },
Line 1157:         "url": request.build_absolute_uri()
Line 1158:     }, sort_keys=True))
Line 1159:     response['Content-Type'] = 'application/json'
Line 1160:     return response
Line 1161: Then, once the views are available, we must actually expose them; that is, make
Line 1162: 4.
Line 1163: them accessible through some kind of URL. To do so, we have to add the three
Line 1164: URL paths to the djapp/httpbin/urls.py file:
Line 1165: from django.urls import re_path
Line 1166: from . import views
Line 1167: urlpatterns = [
Line 1168:     re_path(r'^get$', views.get),
Line 1169:     re_path(r"^anything.*$", views.get),
Line 1170:     re_path(r'^$', views.home)
Line 1171: ]
Line 1172: 
Line 1173: --- 페이지 283 ---
Line 1174: Testing for the Web: WSGI versus HTTP
Line 1175: Chapter 11
Line 1176: [ 273 ]
Line 1177: Our application is now fully functional. But if we try to start it now it won't work.
Line 1178: That's because we haven't yet attached the application to the project. So the djapp
Line 1179: project doesn't yet know that it has to serve the httpbin application.
Line 1180: To do this, we can open the djapp/djapp/urls.py file and make sure that all
Line 1181: 5.
Line 1182: the URLs from the httpbin project are correctly included in it:
Line 1183: from django.contrib import admin
Line 1184: from django.urls import path, include
Line 1185: urlpatterns = [
Line 1186:     path('admin/', admin.site.urls),
Line 1187:     path("", include("httpbin.urls"))
Line 1188: ]
Line 1189: The last step is to make sure that our website is accessible on all the hosts that we
Line 1190: 6.
Line 1191: plan to use, so we should set the ALLOWED_HOSTS variable in
Line 1192: djapp/djapp/settings.py:
Line 1193: ALLOWED_HOSTS = ["httpbin.org", "127.0.0.1"]
Line 1194: If we did everything correctly, running manage.py runserver should now run
Line 1195: our website and make it visible on http://127.0.0.1:8000/:
Line 1196: $ python manage.py runserver
Line 1197: ...
Line 1198: Django version 3.1.4, using settings 'djapp.settings'
Line 1199: Starting development server at http://127.0.0.1:8000/
Line 1200: Quit the server with CONTROL-C.
Line 1201: Pointing our web browser to http://127.0.0.1:8000/ should greet us with a
Line 1202: Hello World message as specified by the httpbin.views.home function:
Line 1203: Figure 11.2 – Hello World response from our Django application
Line 1204: Now that we confirmed the application is being correctly served, we have to make sure we
Line 1205: are able to run the tests against it.
Line 1206: 
Line 1207: --- 페이지 284 ---
Line 1208: Testing for the Web: WSGI versus HTTP
Line 1209: Chapter 11
Line 1210: [ 274 ]
Line 1211: Testing Django projects with pytest
Line 1212: The first thing we are going to do is to take our test suite as-is, based on WebTest and
Line 1213: pytest, and make it work against the new Django project we just wrote. This mostly
Line 1214: guarantees that the behavior we have is the same exact behavior we previously had, as the
Line 1215: tests are the same tests we had previously. Also shows how we can use pytest and WebTest
Line 1216: even with a full-fledged Django project.
Line 1217: To do so, we are going to create a pytest-tests directory inside the djapp project. Here
Line 1218: we are going to place the djapp/pytest-tests/test_djapp.py module, which is
Line 1219: mostly a copy of the test module we had in the previous section. The only difference will be
Line 1220: where the wsgiapp object comes from:
Line 1221: import sys
Line 1222: import webtest
Line 1223: sys.path.append(".")
Line 1224: from djapp.wsgi import application as wsgiapp
Line 1225: class TestWSGIApp:
Line 1226:     def test_home(self):
Line 1227:         client = webtest.TestApp(wsgiapp)
Line 1228:         response = client.get("http://httpbin.org/").text
Line 1229:         assert 'Hello World' in response
Line 1230:     def test_GET(self):
Line 1231:         client = webtest.TestApp(wsgiapp)
Line 1232:         response = client.get("http://httpbin.org/get").text
Line 1233:         assert '"Host": "httpbin.org"' in response
Line 1234:         assert '"args": {}' in response
Line 1235:     def test_GET_params(self):
Line 1236:         client = webtest.TestApp(wsgiapp)
Line 1237:         response = client.get(url="http://httpbin.org/get?alpha=1").json
Line 1238:         assert response["headers"]["Host"] == "httpbin.org"
Line 1239:         assert response["args"] == {"alpha": "1"}
Line 1240:     def test_POST(self):
Line 1241:         client = webtest.TestApp(wsgiapp)
Line 1242:         response = client.post(url="http://httpbin.org/get?alpha=1",
Line 1243: 
Line 1244: --- 페이지 285 ---
Line 1245: Testing for the Web: WSGI versus HTTP
Line 1246: Chapter 11
Line 1247: [ 275 ]
Line 1248:                                params={"beta": "2"}).json
Line 1249:         assert response["headers"]["Host"] == "httpbin.org"
Line 1250:         assert response["args"] == {"alpha": "1"}
Line 1251:         assert response["form"] == {"beta": "2"}
Line 1252:     def test_DELETE(self):
Line 1253:         client = webtest.TestApp(wsgiapp)
Line 1254:         response = client.delete(url="http://httpbin.org/anything/27").text
Line 1255:         assert '"method": "DELETE"' in response
Line 1256:         assert '"url": "http://httpbin.org/anything/27"' in response
Line 1257: The two main changes compared to the prior test module are that we removed all the
Line 1258: wsgiapp arguments from the test functions, as the wsgiapp object won't come anymore
Line 1259: from a fixture injecting the dependency, and that we imported it at the top of the file from
Line 1260: the djapp.wsgi module. Different to most web frameworks, in Django the projects are not
Line 1261: Python distributions, and thus can't be installed with pip. This means that we can't directly
Line 1262: import the project from anywhere and refer to its content.
Line 1263: To surpass this limitation we are going to use sys.path.append(".") to make the
Line 1264: current path available to Python. This allows us to import the djapp package inside the
Line 1265: djapp project as if it were a normal Python installed package, thus making accessible the
Line 1266: djapp.wsgi module. Inside that module, Django makes the WSGI application available as
Line 1267: the application object.
Line 1268: To confirm things worked as expected, we are going to run pytest and point it to the
Line 1269: pytest-tests directory. This should run the same exact tests we had before, just against
Line 1270: the new Django project:
Line 1271: $ pytest pytest-tests -v
Line 1272: ======================== test session starts =========================
Line 1273: platform linux -- Python 3.8.6, pytest-6.0.2, py-1.9.0, pluggy-0.13.1 --
Line 1274: collected 5 items
Line 1275: pytest-tests/test_djapp.py::TestWSGIApp::test_home PASSED [ 20%]
Line 1276: pytest-tests/test_djapp.py::TestWSGIApp::test_GET PASSED [ 40%]
Line 1277: pytest-tests/test_djapp.py::TestWSGIApp::test_GET_params PASSED [ 60%]
Line 1278: pytest-tests/test_djapp.py::TestWSGIApp::test_POST FAILED [ 80%]
Line 1279: pytest-tests/test_djapp.py::TestWSGIApp::test_DELETE FAILED [100%]
Line 1280: ============================== FAILURES ==============================
Line 1281: ...
Line 1282: ------------------------ Captured stderr call ------------------------
Line 1283: Forbidden (CSRF cookie not set.): /anything/27
Line 1284: ------------------------- Captured log call --------------------------
Line 1285: 
Line 1286: --- 페이지 286 ---
Line 1287: Testing for the Web: WSGI versus HTTP
Line 1288: Chapter 11
Line 1289: [ 276 ]
Line 1290: WARNING django.security.csrf:log.py:224 Forbidden (CSRF cookie not set.):
Line 1291: /anything/27
Line 1292: ====================== short test summary info =======================
Line 1293: FAILED pytest-tests/test_djapp.py::TestWSGIApp::test_POST - webtest...
Line 1294: FAILED pytest-tests/test_djapp.py::TestWSGIApp::test_DELETE - webte...
Line 1295: ==================== 2 failed, 3 passed in 0.40s =====================
Line 1296: Surprisingly, there were two tests that failed compared to before: test_POST and
Line 1297: test_DELETE.
Line 1298: Both of them failed with a CSRF cookie not set error. This is because Django sets up
Line 1299: support for CSRF attack protection by default in all new projects. The protection works by
Line 1300: using a token provided automatically by forms when they get submitted to other
Line 1301: endpoints. The problem is that in our project, we don't have any forms at all, so the DELETE
Line 1302: and POST requests are not submitting any tokens, thus failing the protection check.
Line 1303: For our kind of application, this kind of protection doesn't make much sense, as we aren't
Line 1304: going to have any forms present. Thus we can edit the djapp/djapp/settings.py file
Line 1305: and remove the django.middleware.csrf.CsrfViewMiddleware line from the
Line 1306: MIDDLEWARES variable:
Line 1307: MIDDLEWARE = [
Line 1308:     'django.middleware.security.SecurityMiddleware',
Line 1309:     'django.contrib.sessions.middleware.SessionMiddleware',
Line 1310:     'django.middleware.common.CommonMiddleware',
Line 1311:     # 'django.middleware.csrf.CsrfViewMiddleware',
Line 1312:     'django.contrib.auth.middleware.AuthenticationMiddleware',
Line 1313:     'django.contrib.messages.middleware.MessageMiddleware',
Line 1314:     'django.middleware.clickjacking.XFrameOptionsMiddleware',
Line 1315: ]
Line 1316: Now that we have disabled the CSRF protection, rerunning the tests should succeed as
Line 1317: expected:
Line 1318: $ pytest pytest-tests -v
Line 1319: ======================== test session starts =========================
Line 1320: collected 5 items
Line 1321: pytest-tests/test_djapp.py::TestWSGIApp::test_home PASSED [ 20%]
Line 1322: pytest-tests/test_djapp.py::TestWSGIApp::test_GET PASSED [ 40%]
Line 1323: pytest-tests/test_djapp.py::TestWSGIApp::test_GET_params PASSED [ 60%]
Line 1324: pytest-tests/test_djapp.py::TestWSGIApp::test_POST PASSED [ 80%]
Line 1325: pytest-tests/test_djapp.py::TestWSGIApp::test_DELETE PASSED [100%]
Line 1326: ========================= 5 passed in 0.21s ==========================
Line 1327: 
Line 1328: --- 페이지 287 ---
Line 1329: Testing for the Web: WSGI versus HTTP
Line 1330: Chapter 11
Line 1331: [ 277 ]
Line 1332: Testing Django projects with Django's test client
Line 1333: We have seen that the application behaves like we expected as the same tests we wrote for
Line 1334: WebTest worked correctly. But running tests using pytest and WebTest is a non-standard
Line 1335: way to test Django projects. Most people would expect to be able to test a Django project
Line 1336: simply using the manage.py test command. But for now, this command runs no tests at
Line 1337: all:
Line 1338: $ python manage.py test
Line 1339: System check identified no issues (0 silenced).
Line 1340: ----------------------------------------------------------------------
Line 1341: Ran 0 tests in 0.000s
Line 1342: OK
Line 1343: This is because for manage.py test itself, we have not yet written any test. manage.py
Line 1344: test is mostly based on the unittest framework we saw at the beginning of the book,
Line 1345: and thus is not compatible with pytest. Also, the tests here are meant to be written slightly
Line 1346: differently without using WebTest.
Line 1347: To migrate our tests to the Django way, we have to create a djapp/httpbin/tests.py file
Line 1348: in which we will put all our tests. For now, in this file, we are going to provide a single test
Line 1349: for the index page of the website, just to make sure that the test suite is able to find our test
Line 1350: and that the web application is correctly starting up:
Line 1351: from django.test import TestCase
Line 1352: class HttpbinTests(TestCase):
Line 1353:     def test_home(self):
Line 1354:         response = self.client.get("/")
Line 1355:         self.assertContains(response, "Hello World")
Line 1356: Django tests will usually inherit from django.test.TestCase, which serves two different
Line 1357: purposes:
Line 1358: First, to make sure that the methods inside the subclass are correctly identified as
Line 1359: tests, and thus run when we start the test suite.
Line 1360: The second purpose is to provide the self.client object, which helps to
Line 1361: perform requests to the web application much like WebTest did.
Line 1362: In this case, the primary difference is that the web application is not explicitly provided to
Line 1363: the client, but is detected based on the project where we are running the tests.
Line 1364: 
Line 1365: --- 페이지 288 ---
Line 1366: Testing for the Web: WSGI versus HTTP
Line 1367: Chapter 11
Line 1368: [ 278 ]
Line 1369: Now that we have a test in place, running the manage.py test command again should
Line 1370: finally find and run the test:
Line 1371: $ python manage.py test
Line 1372: Creating test database for alias 'default'...
Line 1373: System check identified no issues (0 silenced).
Line 1374: .
Line 1375: ----------------------------------------------------------------------
Line 1376: Ran 1 test in 0.004s
Line 1377: OK
Line 1378: Destroying test database for alias 'default'...
Line 1379: The next steps will be to also port the test_GET, test_GET_params, test_POST, and
Line 1380: test_DELETE tests to the Django standard so that our full test suite is available when
Line 1381: running manage.py test.
Line 1382: The main differences when working with Django's test client is that for the responses, it's
Line 1383: going to provide a Django HttpResponse object, thus the content of the response will be
Line 1384: available in binary form in the HttpResponse.content attribute and we will have to
Line 1385: decode it ourselves, while WebTest provided the .text and .json properties, which
Line 1386: handled much of that for us. Apart from these minor differences, the tests mostly look the
Line 1387: same as before:
Line 1388: import json
Line 1389: from django.test import TestCase
Line 1390: class HttpbinTests(TestCase):
Line 1391:     def test_home(self):
Line 1392:         response = self.client.get("/")
Line 1393:         self.assertContains(response, "Hello World")
Line 1394:     def test_GET(self):
Line 1395:         response = self.client.get("/get").content.decode("utf-8")
Line 1396:         assert '"Host": "httpbin.org"' in response
Line 1397:         assert '"args": {}' in response
Line 1398:     def test_GET_params(self):
Line 1399:         response = json.loads(self.client.get("/get?alpha=1").content)
Line 1400:         assert response["headers"]["Host"] == "httpbin.org"
Line 1401:         assert response["args"] == {"alpha": "1"}
Line 1402: 
Line 1403: --- 페이지 289 ---
Line 1404: Testing for the Web: WSGI versus HTTP
Line 1405: Chapter 11
Line 1406: [ 279 ]
Line 1407:     def test_POST(self):
Line 1408:         response = json.loads(self.client.post(
Line 1409:             "/get?alpha=1", {"beta": "2"}
Line 1410:         ).content)
Line 1411:         assert response["headers"]["Host"] == "httpbin.org"
Line 1412:         assert response["args"] == {"alpha": "1"}
Line 1413:         assert response["form"] == {"beta": "2"}
Line 1414:     def test_DELETE(self):
Line 1415:         response = self.client.delete(
Line 1416:             "/anything/27"
Line 1417:         ).content.decode("utf-8")
Line 1418:         assert '"method": "DELETE"' in response
Line 1419:         assert '"url": "http://httpbin.org/anything/27"' in response
Line 1420: Now that we have in place the same tests we had before, but now in the new Django test
Line 1421: client format, we can verify that all five of them pass as expected by rerunning the
Line 1422: manage.py test command:
Line 1423: $ python manage.py test
Line 1424: Creating test database for alias 'default'...
Line 1425: System check identified no issues (0 silenced).
Line 1426: .....
Line 1427: ----------------------------------------------------------------------
Line 1428: Ran 5 tests in 0.010s
Line 1429: OK
Line 1430: Destroying test database for alias 'default'...
Line 1431: This confirms that our tests for the application succeed also in the Django test client
Line 1432: version.
Line 1433: Which format to use (WebTest or Django's test client) can be considered mostly a matter of
Line 1434: preference for skilled Django users, but for most developers out there, using Django's test
Line 1435: client will probably lead to finding more answers to your questions and doubts, as it's the
Line 1436: documented and suggested way that Django developers expect will be used when writing
Line 1437: Django applications.
Line 1438: For people interested in using pytest with Django, a pytest-django package also exists
Line 1439: that tries to fill the gap while hiding most of the machinery necessary to make Django tests
Line 1440: run with pytest.
Line 1441: 
Line 1442: --- 페이지 290 ---
Line 1443: Testing for the Web: WSGI versus HTTP
Line 1444: Chapter 11
Line 1445: [ 280 ]
Line 1446: Summary
Line 1447: In this chapter, we saw how we can test HTTP-based applications and how we can verify
Line 1448: the behavior of HTTP clients, HTTP servers, and even the two of them together. This is all
Line 1449: thanks to the WSGI protocol that powers the Python web ecosystem. We have also seen
Line 1450: how testing works in the Django world when Django's test client is used, thus we are fairly
Line 1451: capable of writing effective test suites for whatever web framework we are going to use.
Line 1452: Our testing isn't fully complete by the way. We are verifying the endpoints, checking that
Line 1453: the web pages contain the responses we expect, but we have no way to check that, once
Line 1454: those responses are read by a web browser, they actually behave as we expected. Even
Line 1455: worse, if there is JavaScript involved, we don't have any way to verify that the JavaScript in
Line 1456: those web pages is actually doing what we want.
Line 1457: So in the next chapter, we are going to see how we can test our web applications with a real
Line 1458: browser while also verifying the JavaScript that our web pages contain, thus completing the
Line 1459: list of skills we might need to develop a fully tested web application.