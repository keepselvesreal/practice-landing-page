# 1.5.0 Introduction [auto-generated] (pp.21-22)

---
**Page 21**

Getting Started with Software Testing
Chapter 1
[ 21 ]
While addition can be tested in isolation, multiply must use addition to work.
multiply is thus defined as a sociable unit, while addition is a solitary unit.
Sociable unit tests are frequently also referred to as component tests. Your architecture 
mostly defines the distinction between a sociable unit test and a component test and it's
hard to state exactly when one name should be preferred over the other.
While sociable units usually lead to more complete testing, they are slower, require more
effort during the Arrange phase, and are less isolated. This means that a change in
addition can make a test of multiply fail, which tells us that there is a problem, but also
makes it harder to guess where the problem lies exactly.
In the subsequent chapters, we will see how sociable units can be converted into solitary
units by using test doubles. If you have complete testing coverage for the underlying units,
solitary unit tests can reach a level of guarantee that is similar to that of sociable units with
must less effort and a faster test suite.
Test units are usually great at testing software from a white-box perspective, but that's not
the sole point of view we should account for in our testing strategy. Test units guarantee
that the code does what the developer meant it to, but do little to guarantee that the code
does what the user needs. Integration and functional tests are usually more effective in
terms of testing at that level of abstraction.
Understanding integration and functional
tests
Testing all our software with solitary units can't guarantee that it's really working as
expected. Unit testing confirms that the single components are working as expected, but
doesn't give us any confidence about their effectiveness when paired together.
It's like testing an engine by itself, testing the wheels by themselves, testing the gears, and
then expecting the car to work. We wouldn't be accounting for any issues introduced in the
assembly process.
So we have a need to verify that those modules do work as expected when paired together.


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


