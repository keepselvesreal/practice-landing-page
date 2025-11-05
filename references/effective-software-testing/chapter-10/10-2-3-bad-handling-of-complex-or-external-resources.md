# 10.2.3 Bad handling of complex or external resources (pp.268-269)

---
**Page 268**

268
CHAPTER 10
Test code quality
10.2.2
Unclear assertions
Assertions are the first thing a developer looks at when a test fails. A good assertion
clearly reveals its reason for failure, is legible, and is as specific as possible. The test smell
emerges when it is hard to understand the assertions or the reason for their failure.
 There are several reasons for this smell to happen. Some features or business rules are
so complex that they require a complex set of assertions to ensure their behavior. In
these situations, we end up writing complex assert instructions that are not easy to under-
stand. To help with such cases, I recommend writing customized assert instructions that
abstract away part of the complexity of the assertion code, and writing code comments
that explain quickly and in natural language what those assertions are about. The latter
mainly applies when the assertions are not self-explanatory. Do not be afraid to write a
comment in your code if it will help future developers understand what is going on.
 Interestingly, a common best practice in the test best practice literature is the “one
assertion per method” strategy. The idea is that a test with a single assertion can only
focus on a single behavior, and it is easier for developers to understand if the assertion
fails. I strongly disagree with this rule. If my test is cohesive enough and focuses on a
single feature, the assertions should ensure that the entire behavior is as expected.
This may mean asserting that many fields were updated and have a new value. It may
also mean asserting that the mock interacted with other dependencies properly.
There are many cases in which using multiple assertions in a single test is useful. Forc-
ing developers to have a single assertion per test method is extreme—but your tests
also should not have useless assertions.
 Frameworks often offer the possibility of doing soft assertions: assertions that do
not stop the test if they fail but are reported only at the very end of the test execu-
tion (which is still considered a failed test). For example, AssertJ offers this ability
(http://mng.bz/aDeo).
 Finally, even if you know what to assert for, picking the right assertion method pro-
vided by whatever test framework you are using can make a difference. Using the
wrong or not ideal assert instruction may lead to imprecise assertion error messages. I
strongly suggest using AssertJ and its extensive collection of assertions. 
10.2.3
Bad handling of complex or external resources
Understanding test code that uses external resources can be difficult. The test should
ensure that the resource is readily available and prepared for it. The test should also
clean up its mess afterward.
 A common smell is to be optimistic about the external resource. Resource optimism
happens when a test assumes that a necessary resource (such as a database) is readily
available at the start of its execution. The problem is that when the resource is not avail-
able, the test fails, often without a clear message that explains the reason. This can con-
fuse developers, who may think a new bug has been introduced in the system.
 To avoid such resource optimism, a test should not assume that the resource is
already in the correct state. The test should be responsible for setting up the state


---
**Page 269**

269
Test smells
itself. This can mean the test is responsible for populating a database, writing the
required files to the disk, or starting up a Tomcat server. This setup may require com-
plex code, and you should also make your best effort to abstract away such complexity
by, for example, moving such code to other classes (like DatabaseInitialization or
TomcatLoader) and allowing the test code to focus on the test cases.
 Another common test smell happens when the test assumes that the resource is
available all the time. Imagine a test method that interacts with a web service, which
may be down for reasons we do not control. To avoid this test smell, you have two
options: avoid depending on external resources by using stubs and mocks or, if the
test cannot avoid using the external dependency, make the test suite robust enough.
For example, make your test suite skip that test when the resource is unavailable, and
provide an alert explaining why that was the case. This may seem counterintuitive, but
remember that developers trust their test suites. Having a single test fail for the wrong
reasons can make you lose confidence in the entire test suite.
 From a readability perspective, it should be easy to understand all the (external)
resources required and used by the test. Imagine that a test requires a test file in some
directory. If the file is not there, the test fails. A first-time developer may have difficulty
understanding this prerequisite. Avoid having such mystery guests in your test suite.
The test code should be explicit about all its external dependencies.  
10.2.4
Fixtures that are too general
A fixture is the set of input values used to exercise the component under test. As you
may have noticed, fixtures are the stars of the test method, as they derive naturally
from the test cases we engineer using any of the techniques we have discussed.
 When testing more complex components, you may need to build several different
fixtures: one for each partition you want to exercise. These fixtures can then become
complex. And to make the situation worse, while tests are different from each other,
their fixtures may intersect. Given this possible intersection among the different fix-
tures, as well as the difficulty with building complex entities and fixtures, you may
decide to declare a large fixture that works for many different tests. Each test would
then use a small part of this large fixture.
 While this approach may work, and the tests may correctly implement the test
cases, they quickly become hard to maintain. Once a test fails, you will find yourself
with a large fixture that may not be completely relevant for that particular failing test.
You then must manually filter out parts of the fixture that are not exercised by the fail-
ing test. That is an unnecessary cost.
 Making sure the fixture of a test is as specific and cohesive as possible helps you com-
prehend the essence of a test (which is, again, highly relevant when the test starts to fail).
Build patterns (focusing on building test data) can help you avoid generic fixtures. More
specifically, the Test Data Builder pattern we discussed is often used in the test code of
enterprise applications. Such applications often deal with creating complex sets of inter-
related business entities, which can easily lead developers to write general fixtures. 


