# 10.2.1 Excessive duplication (pp.267-268)

---
**Page 267**

267
Test smells
change happens and you are forced to change that code snippet, you now only have
to change it in 1 place rather than 10.
 Your tests are coupled to the production code in one way or another. That is a fact.
The more your tests know about how the production code works, the harder it is to
change them. As we discussed in chapter 6, a clear disadvantage of using mocks is the
significant coupling with the production code. Determining how much your tests
need to know about the production code to test it properly is a significant challenge. 
10.2
Test smells
In the previous sections, we discussed some best practices for writing good test code.
Now let’s discuss test smells. The term code smell indicates symptoms that may indicate
deeper problems in the system’s source code. Some well-known examples are Long
Method, Long Class, and God Class. Several research papers show that code smells hin-
der the comprehensibility and maintainability of software systems (such as the work by
Khomh and colleagues [2009]).
 While the term has long been applied to production code, our community has
been developing catalogs of smells that are specific to test code. Research has also
shown that test smells are prevalent in real life and, unsurprisingly, often hurt the
maintenance and comprehensibility of the test suite (Spadini et al., 2020).
 The following sections examine several well-known test smells. A more compre-
hensive list can be found in xUnit Test Patterns by Meszaros (2007). I also recommend
reading the foundational paper on test smells by Deursen and colleagues (2001).
10.2.1
Excessive duplication
It is not surprising that code duplication can happen in test code since it is widespread
in production code. Tests are often similar in structure, as you may have noticed in
several of the code examples in this book. We even used parameterized tests to reduce
duplication. A less attentive developer may end up writing duplicate code (copy-pasting
often happens in real life, as Treude, Zaidman, and I observed in an empirical study
[2021]) instead of putting some effort into implementing a better solution.
 Duplicated code can reduce the productivity of software developers. If we need to
change a duplicated piece of code, we must apply the same change in all the places
where the code is duplicated. In practice, it is easy to forget one of these places and end
up with problematic test code. Duplicating code may also hinder the ability to evolve the
test suite, as mentioned earlier. If the production code changes, you do not want to have
to change too much test code. Isolating duplicated code reduces this pain.
 I advise you to refactor your test code often. Extracting duplicate code to private
methods or external classes is often a good, quick, cheap solution to the problem. But
being pragmatic is key: a little duplication may not harm you, and you should use your
experience to judge when refactoring is needed. 


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


