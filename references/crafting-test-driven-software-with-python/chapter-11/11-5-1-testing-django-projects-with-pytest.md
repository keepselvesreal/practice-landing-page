# 11.5.1 Testing Django projects with pytest (pp.274-277)

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


