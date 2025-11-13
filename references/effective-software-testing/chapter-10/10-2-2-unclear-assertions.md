# 10.2.2 Unclear assertions (pp.268-268)

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


