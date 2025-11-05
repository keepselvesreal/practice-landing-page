# 2.4.1 End-to-end tests are a subset of integration tests (pp.38-39)

---
**Page 38**

38
CHAPTER 2
What is a unit test?
 Similarly, an outreach to an out-of-process dependency makes the test slow. A call
to a database adds hundreds of milliseconds, potentially up to a second, of additional
execution time. Milliseconds might not seem like a big deal at first, but when your test
suite grows large enough, every second counts.
 In theory, you could write a slow test that works with in-memory objects only, but
it’s not that easy to do. Communication between objects inside the same memory
space is much less expensive than between separate processes. Even if the test works
with hundreds of in-memory objects, the communication with them will still execute
faster than a call to a database.
 Finally, a test is an integration test when it verifies two or more units of behavior.
This is often a result of trying to optimize the test suite’s execution speed. When you
have two slow tests that follow similar steps but verify different units of behavior, it
might make sense to merge them into one: one test checking two similar things runs
faster than two more-granular tests. But then again, the two original tests would have
been integration tests already (due to them being slow), so this characteristic usually
isn’t decisive.
 An integration test can also verify how two or more modules developed by separate
teams work together. This also falls into the third bucket of tests that verify multiple
units of behavior at once. But again, because such an integration normally requires an
out-of-process dependency, the test will fail to meet all three criteria, not just one.
 Integration testing plays a significant part in contributing to software quality by
verifying the system as a whole. I write about integration testing in detail in part 3.
2.4.1
End-to-end tests are a subset of integration tests
In short, an integration test is a test that verifies that your code works in integration with
shared dependencies, out-of-process dependencies, or code developed by other teams
in the organization. There’s also a separate notion of an end-to-end test. End-to-end
tests are a subset of integration tests. They, too, check to see how your code works with
out-of-process dependencies. The difference between an end-to-end test and an inte-
gration test is that end-to-end tests usually include more of such dependencies.
 The line is blurred at times, but in general, an integration test works with only one
or two out-of-process dependencies. On the other hand, an end-to-end test works with
all out-of-process dependencies, or with the vast majority of them. Hence the name
end-to-end, which means the test verifies the system from the end user’s point of view,
including all the external applications this system integrates with (see figure 2.6).
 People also use such terms as UI tests (UI stands for user interface), GUI tests (GUI is
graphical user interface), and functional tests. The terminology is ill-defined, but in gen-
eral, these terms are all synonyms.
 Let’s say your application works with three out-of-process dependencies: a data-
base, the file system, and a payment gateway. A typical integration test would include
only the database and file system in scope and use a test double to replace the pay-
ment gateway. That’s because you have full control over the database and file system,


---
**Page 39**

39
Summary
and thus can easily bring them to the required state in tests, whereas you don’t have
the same degree of control over the payment gateway. With the payment gateway, you
may need to contact the payment processor organization to set up a special test
account. You might also need to check that account from time to time to manually
clean up all the payment charges left over from the past test executions.
 Since end-to-end tests are the most expensive in terms of maintenance, it’s better
to run them late in the build process, after all the unit and integration tests have
passed. You may possibly even run them only on the build server, not on individual
developers’ machines.
 Keep in mind that even with end-to-end tests, you might not be able to tackle all of
the out-of-process dependencies. There may be no test version of some dependencies,
or it may be impossible to bring those dependencies to the required state automati-
cally. So you may still need to use a test double, reinforcing the fact that there isn’t a
distinct line between integration and end-to-end tests. 
Summary
Throughout this chapter, I’ve refined the definition of a unit test:
– A unit test verifies a single unit of behavior,
– Does it quickly,
– And does it in isolation from other tests.
Another class
Unit test
Payment gateway
End-to-end test
Database
System under test
Integration test
Figure 2.6
End-to-end tests normally include all or almost all out-of-process dependencies 
in the scope. Integration tests check only one or two such dependencies—those that are 
easier to set up automatically, such as the database or the file system.


