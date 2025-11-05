# 8.2.1 Avoid testing private or protected methods (pp.173-175)

---
**Page 173**

173
8.2
Refactoring to increase maintainability
describe("Test Dependence v2", () => {
  beforeEach(() => getUserCache().reset());      
  describe("user cache", () => {                   
    test("can only add cache use once", () => {
      addDefaultUser();    
      expect(() => addDefaultUser())
        .toThrowError("already exists");
    });
  });
  describe("loginUser with loggedInUser", () => {  
    test("user exists, login succeeds", () => {
      addDefaultUser();    
      const app = makeSpecialApp();
      const result = app.loginUser("a", "abc");
      expect(result).toBe(true);
    });
    test("user missing, login fails", () => {
      const app = makeSpecialApp();
      const result = app.loginUser("a", "abc");
      expect(result).toBe(false);
    });
  });
});
There are several things going on here. First, we extracted two helper functions: a
makeSpecialApp factory function and an addDefaultUser helper function that we can
reuse. Next, we created a very important beforeEach function that resets the user
cache before each test. Whenever I have a shared resource like that, I almost always
have a beforeEach or afterEach function that resets it to its original condition before
or after the test runs.
 The first and the third tests now run in their own little nested describe structure.
They also both use the makeSpecialApp factory function, and one of them is using
addDefaultUser to make sure it does not require any other test to run first. The sec-
ond test also runs in its own nested describe function and reuses the addDefaultUser
function.
8.2
Refactoring to increase maintainability
Up until now, I’ve discussed test failures that force us to make changes. Let’s now dis-
cuss changes that we choose to make, to make tests easier to maintain over time.
8.2.1
Avoid testing private or protected methods
This section applies more to object-oriented languages as well as TypeScript. Private
or protected methods are usually private for a good reason in the developer’s mind.
Sometimes it’s to hide implementation details, so that the implementation can
Resets user cache 
between tests
New nested 
describe 
functions
Calls
reusable
helper
functions


---
**Page 174**

174
CHAPTER 8
Maintainability
change later without changing the observable behavior. It could also be for security-
related or IP-related reasons (obfuscation, for example).
 When you test a private method, you’re testing against a contract internal to the
system. Internal contracts are dynamic, and they can change when you refactor the
system. When they change, your test could fail because some internal work is being
done differently, even though the overall functionality of the system remains the
same. For testing purposes, the public contract (the observable behavior) is all you
need to care about. Testing the functionality of private methods may lead to breaking
tests, even though the observable behavior is correct. 
 Think of it this way: no private method exists in a vacuum. Somewhere down the
line, something has to call it, or it will never get triggered. Usually there’s a public
method that ends up invoking this private one, and if not, there’s always a public
method up the chain of calls that gets invoked. This means that any private method is
always part of a bigger unit of work, or use case in the system, that starts out with a
public API and ends with one of the three end results: return value, state change, or
third-party call (or all three).
 So if you see a private method, find the public use case in the system that will exer-
cise it. If you test only the private method and it works, that doesn’t mean that the rest
of the system is using this private method correctly or handles the results it provides
correctly. You might have a system that works perfectly on the inside, but all that nice
inside stuff is used incorrectly from the public APIs.
 Sometimes, if a private method is worth testing, it might be worth making it public,
static, or at least internal, and defining a public contract against any code that uses it.
In some cases, the design may be cleaner if you put the method in a different class
altogether. We’ll look at those approaches in a moment.
 Does this mean there should eventually be no private methods in the codebase?
No. With test-driven design, you usually write tests against methods that are public,
and those public methods are later refactored into calling smaller, private methods.
All the while, the tests against the public methods continue to pass.
MAKING METHODS PUBLIC
Making a method public isn’t necessarily a bad thing. In a more functional world, it’s
not even an issue. This practice may seem to go against the object-oriented principles
many of us were raised on, but that’s not always the case. 
 Consider that wanting to test a method could mean that the method has a known
behavior or contract against the calling code. By making it public, you’re making this
official. By keeping the method private, you tell all the developers who come after you
that they can change the implementation of the method without worrying about
unknown code that uses it.
EXTRACTING METHODS TO NEW CLASSES OR MODULES
If your method contains a lot of logic that can stand on its own, or it uses specialized
state variables in the class or module that are relevant only to the method in question,
it may be a good idea to extract the method into a new class or its own module with a


---
**Page 175**

175
8.2
Refactoring to increase maintainability
specific role in the system. You can then test that class separately. Michael Feathers’
Working Effectively with Legacy Code (Pearson, 2004) has some good examples of this
technique, and Clean Code by Robert Martin (Pearson, 2008) can help you figure out
when this is a good idea.
MAKING STATELESS PRIVATE METHODS PUBLIC AND STATIC
If your method is completely stateless, some people choose to refactor the method by
making it static (in languages that support this feature). That makes it much more
testable but also states that the method is a sort of utility method that has a known
public contract specified by its name.
8.2.2
Keep tests DRY
Duplication in your unit tests can hurt you, as a developer, just as much as, if not more
than, duplication in production code. That’s because any change in a piece of code
that has duplicates will force you to change all the duplicates as well. When you’re
dealing with tests, there’s more risk of the developer just avoiding this trouble and
deleting or ignoring tests instead of fixing them.
 The DRY (don’t repeat yourself) principle should be in effect in test code just as in
production code. Duplicated code means there’s more code to change when one
aspect you test against changes. Changing a constructor or changing the semantics of
using a class can have a major effect on tests that have a lot of duplicated code.
 As we’ve seen in previous examples in this chapter, using helper functions can help
to reduce duplication in tests. 
WARNING
Removing duplication can also go too far and hurt readability.
We’ll talk about that in the next chapter, on readability.
8.2.3
Avoid setup methods
I’m not a fan of the beforeEach function (also called a setup function) that happens
once before each test and is often used to remove duplication. I much prefer using
helper functions. Setup functions are too easy to abuse. Developers tend to use them
for things they weren’t meant for, and tests become less readable and less maintain-
able as a result. 
 Many developers abuse setup methods in several ways:
Initializing objects in the setup method that are used in only some tests in the file
Having setup code that’s lengthy and hard to understand
Setting up mocks and fake objects within the setup method
Also, setup methods have limitations, which you can get around by using simple
helper methods:
Setup methods can only help when you need to initialize things.
Setup methods aren’t always the best candidates for duplication removal.
Removing duplication isn’t always about creating and initializing new instances


