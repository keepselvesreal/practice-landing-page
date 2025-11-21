# 11.5.2 Testing Django projects with Django's test client (pp.277-280)

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


