# 1.5.1 Integration tests (pp.22-25)

---
**Page 22**

Getting Started with Software Testing
Chapter 1
[ 22 ]
That's exactly what integration tests are expected to do. They take the modules we tested
individually and test them together.
Integration tests
The scope of integration tests is blurry. They might integrate two modules, or they might
integrate tens of them. While they are more effective when integrating fewer modules, it's
also more expensive to move forward as an approach and most developers argue that the
effort of testing all possible combinations of modules in isolation isn't usually worth the
benefit.
The boundary between unit tests made of sociable units and integration tests is not easy to
explain. It usually depends on the architecture of the software itself. We could consider
sociable units tests those tests that test units together that are inside the same architectural
components, while we could consider integration tests those tests that test different
architectural components together.
In an application, two separate services will be involved: Authorization and
Authentication. Authentication takes care of letting the user in and identifying them,
while Authorization tells us what the user can do once it is authenticated. We can see
this in the following code block:
class Authentication:
    USERS = [{"username": "user1",
              "password": "pwd1"}]
    def login(self, username, password):
        u = self.fetch_user(username)
        if not u or u["password"] != password:
            return None
        return u
    def fetch_user(self, username):
        for u in self.USERS:
            if u["username"] == username:
                return u
        else:
            return None
class Authorization:
    PERMISSIONS = [{"user": "user1",
                    "permissions": {"create", "edit", "delete"}}]


---
**Page 23**

Getting Started with Software Testing
Chapter 1
[ 23 ]
    def can(self, user, action):
        for u in self.PERMISSIONS:
            if u["user"] == user["username"]:
                return action in u["permissions"]
        else:
            return False
Our classes are composed of two primary methods: Authentication.login and
Authorization.can. The first is in charge of authenticating the user with a username and
password and returning the authenticated user, while the second is in charge of verifying
that a user can do a specific action. Tests for those methods can be considered unit tests.
So TestAuthentication.test_login will be a unit test that verifies the behavior of the
Authentication.login unit, while TestAuthorization.test_can will be a unit test
that verifies the behavior of the Authorization.can unit:
class TestAuthentication(unittest.TestCase):
    def test_login(self):
        auth = Authentication()
        auth.USERS = [{"username": "testuser", "password": "testpass"}]
        resp = auth.login("testuser", "testpass")
        assert resp == {"username": "testuser", "password": "testpass"}
class TestAuthorization(unittest.TestCase):
    def test_can(self):
        authz = Authorization()
        authz.PERMISSIONS = [{"user": "testuser", "permissions":
                              {"create"}}]
        resp = authz.can({"username": "testuser"}, "create")
        assert resp is True
Here, we have the notable difference that TestAuthentication.test_login is a sociable
unit test as it depends on Authentication.fetch_user while testing
Authentication.login, and TestAuthorization.test_can is instead a solitary unit
test as it doesn't depend on any other unit.
So where is the integration test?


---
**Page 24**

Getting Started with Software Testing
Chapter 1
[ 24 ]
The integration test will happen once we join those two components of our architecture
(authorization and authentication) and test them together to confirm that we can actually
have a user log in and verify their permissions:
class TestAuthorizeAuthenticatedUser(unittest.TestCase):
    def test_auth(self):
        auth = Authentication()
        authz = Authorization()
        auth.USERS = [{"username": "testuser", "password": "testpass"}]
        authz.PERMISSIONS = [{"user": "testuser",
                              "permissions": {"create"}}]
        u = auth.login("testuser", "testpass")
        resp = authz.can(u, "create")
        assert resp is True
Generally, it's important to be able to run your integration tests independently from your
unit tests, as you will want to be able to run the unit tests continuously during development
on every change:
$ python 05_integration.py TestAuthentication TestAuthorization
........
----------------------------------------------------------------------
Ran 8 tests in 0.000s
OK
While unit tests are usually verified frequently during the development cycle, it's common
to run your integration tests only when you've reached a stable point where your unit tests
all pass:
$ python 05_integration.py TestAuthorizeAuthenticatedUser
.
----------------------------------------------------------------------
Ran 1 test in 0.000s
OK
As you know that the units that you wrote or modified do what you expected, running
the TestAuthorizeAuthenticatedUser case only will confirm that those entities work
together as expected.
Integration tests integrate multiple components, but they actually divide themselves into
many different kinds of tests depending on their purpose, with the most common kind
being functional tests.


---
**Page 25**

Getting Started with Software Testing
Chapter 1
[ 25 ]
Functional tests
Integration tests can be very diverse. As you start integrating more and more components,
you move toward a higher level of abstraction, and in the end, you move so far from the
underlying components that people feel the need to distinguish those kinds of tests as they
offer different benefits, complexities, and execution times.
That's why the naming of functional tests, end-to-end tests, system tests, acceptance tests,
and so on all takes place.
Overall, those are all forms of integration tests; what changes are their goal and purpose:
Functional tests tend to verify that we are exposing to our users the feature we
actually intended. They don't care about intermediate results or side-effects; they
just verify that the end result for the user is the one the specifications described,
thus they are always black-box tests.
End-to-End (E2E) tests are a specific kind of functional test that involves the
vertical integration of components. The most common E2E tests are where
technologies such as Selenium are involved in accessing a real application
instance through a web browser.
System tests are very similar to functional tests themselves, but instead of testing
a single feature, they usually test a whole journey of the user across the system.
So they usually simulate real usage patterns of the user to verify that the system
as a whole behaves as expected.
Acceptance tests are a kind of functional test that is meant to confirm that the
implementation of the feature does behave as expected. They usually express the
primary usage flow of the feature, leaving less common flows for other
integration tests, and are frequently provided by the specifications themselves to
help the developer confirm that they implemented what was expected.
But those are not the only kinds of integration that people refer to; new types are
continuously defined in the effort to distinguish the goals of tests and responsibilities.
Component tests, contract tests, and many others are kinds of tests whose goal is to verify
integration between different pieces of the software at different layers. Overall, you
shouldn't be ashamed of asking your colleagues what they mean exactly when they use
those names, because you will notice each one of them will value different properties of
those tests when classifying them into the different categories.
The general distinction to keep in mind when distinguishing between integration tests and
functional tests is that unit and integration tests aim to test the implementation, while
functional tests aim to test the behavior.


