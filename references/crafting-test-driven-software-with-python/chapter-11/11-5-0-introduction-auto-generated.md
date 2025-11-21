# 11.5.0 Introduction [auto-generated] (pp.271-274)

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


