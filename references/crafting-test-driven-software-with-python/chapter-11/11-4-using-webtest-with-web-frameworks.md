# 11.4 Using WebTest with web frameworks (pp.261-271)

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


