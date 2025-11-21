# 7.5.0 Introduction [auto-generated] (pp.161-163)

---
**Page 161**

161
7.5
Dealing with flaky tests
 Another huge potential issue with dynamically generated values is that if we don’t
know ahead of time what the input into the system might be, we also have to compute
the expected output of the system, and that can lead to a buggy test that depends on
repeating production logic, as mentioned in section 7.3. 
7.5
Dealing with flaky tests
I’m not sure who came up with the term flaky tests, but it does fit the bill. It’s used to
describe tests that, given no changes to the code, return inconsistent results. This
might happen frequently or very rarely, but it does happen. 
 Figure 7.1 illustrates where flakiness comes from. The figure is based on the num-
ber of real dependencies the tests have. Another way to think about this is how many
moving parts the tests have. For this book, we’re mostly concerning ourselves with the
Flakiness caused by
• Shared memory resources
• Threads
• Random values
• Dynamically generated inputs/outputs
• Time
• Logic bugs
Flakiness also caused by
• Shared resources
• Network issues
• Conﬁguration issues
• Permission issues
• Load issues
• Security issues
• Other systems are down
• And more...
Conﬁdence/Flakiness
E2E/UI system tests
E2E/UI isolated tests
API tests (out of process)
Integration tests (in memory)
Component tests (in memory)
Unit tests (in memory)
Figure 7.1
The higher the level of the tests, the more real dependencies they use, which 
gives us confidence in the overall system correctness but results in more flakiness.


---
**Page 162**

162
CHAPTER 7
Trustworthy tests
bottom third of this diagram: unit and component tests. However, I want to touch on
the higher-level flakiness so I can give you some pointers on what to research.
 At the lowest level, our tests have full control over all of their dependencies and
therefore have no moving parts, either because they’re faking them or because they
run purely in memory and can be configured. We did this in chapters 3 and 4. Execu-
tion paths in the code are fully deterministic because all the initial states and expected
return values from various dependencies have been predetermined. The code path is
almost static—if it returns the wrong expected result, then something important
might have changed in the production code’s execution path or logic. 
 As we go up the levels, our tests shed more and more stubs and mocks and start
using more and more real dependencies, such as databases, networks, configura-
tion, and more. This, in turn, means more moving parts that we have less control
over and that might change our execution path, return unexpected values, or fail to
execute at all. 
 At the highest level, there are no fake dependencies. Everything our tests rely on
is real, including any third-party services, security and network layers, and configura-
tion. These types of tests usually require us to set up an environment that is as close
to a production scenario as possible, if they’re not running right on the production
environments.
 The higher up we go in the test diagram, we should get higher confidence that our
code works, unless we don’t trust the tests’ results. Unfortunately, the higher up we go
in the diagram, the more chances there are for our tests to become flaky because of
how many moving parts are involved.
 We might assume that tests at the lowest level shouldn’t have any flakiness issues
because there shouldn’t be any moving parts that cause flakiness. That’s theoretically
true, but in reality people still manage to add moving parts in lower-level tests: using
the current date and time, the machine name, the network, the filesystem, and more
can cause a test to be flaky.
 A test fails sometimes without us touching production code. For example:
A test fails every third run.
A test fails once every unknown number of times.
A test fails when various external conditions fail, such as network or database
availability, other APIs not being available, environment configuration, and more.
To add to that salad of pain, each dependency the test uses (network, filesystem,
threads, etc.) usually adds time to the test run. Calls to the network and the database
take time. The same goes for waiting for threads to finish, reading configurations, and
waiting for asynchronous tasks.
 It also takes longer to figure out why a test is failing. Debugging a test or reading
through huge amounts of logs is heartbreakingly time consuming and will drain your
soul slowly into the abyss of “time to update my resume” land.


---
**Page 163**

163
7.5
Dealing with flaky tests
7.5.1
What can you do once you’ve found a flaky test?
It’s important to realize that flaky tests can be costly to an organization. You should
aim to have zero flaky tests as a long-term goal. Here are some ways to reduce the costs
associated with handling flaky tests:
Define—Agree on what “flaky” means to your organization. For example, run
your test suite 10 times without any production code changes, and count all the
tests that were not consistent in their results (i.e., ones that did not fail all 10
times or did not pass all 10 times).
Place any test deemed flaky in a special category or folder of tests that can be
run separately. I recommend removing all flaky tests from the regular delivery
build so they do not create noise, and quarantining them in their own little
pipeline temporarily. Then, go over each of the flaky tests and play my favorite
flaky game, “fix, convert, or kill”:
– Fix—Make the test not flaky by controlling its dependencies, if possible. For
example, if it requires data in the database, insert the data into the database
as part of the test. 
– Convert—Remove flakiness by converting the test into a lower-level test by
removing and controlling one or more of its dependencies. For example,
simulate a network endpoint with a stub instead of using a real one. 
– Kill—Seriously consider whether the value the test brings is enough to con-
tinue to run it and pay the maintenance costs it creates. Sometimes old flaky
tests are better off dead and buried. Sometimes they are already covered by
newer, better tests, and the old tests are pure technical debt that we can get
rid of. Sadly, many engineering managers are reluctant to remove these old
tests because of the sunken cost fallacy—there was so much effort put into
them that it would be a waste to delete them. However, at this point, it might
cost you more to keep the test than to delete it, so I recommend seriously
considering this option for many of your flaky tests. 
7.5.2
Preventing flakiness in higher-level tests
If you’re interested in preventing flakiness in higher-level tests, your best bet is to
make sure that your tests are repeatable on any environment after any deployment.
That could involve the following:
Roll back any changes your tests have made to external shared resources.
Do not depend on other tests changing external state.
Gain some control over external systems and dependencies by ensuring you
have the ability to recreate them at will (do an internet search on “infrastruc-
ture as code”), creating dummies of them that you can control, or creating spe-
cial test accounts on them and pray that they stay safe.


