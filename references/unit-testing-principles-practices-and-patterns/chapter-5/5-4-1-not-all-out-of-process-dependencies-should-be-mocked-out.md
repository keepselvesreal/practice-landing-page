# 5.4.1 Not all out-of-process dependencies should be mocked out (pp.115-116)

---
**Page 115**

115
The classical vs. London schools of unit testing, revisited
5.4.1
Not all out-of-process dependencies should be mocked out
Before we discuss out-of-process dependencies and mocking, let me give you a quick
refresher on types of dependencies (refer to chapter 2 for more details):
Shared dependency—A dependency shared by tests (not production code)
Out-of-process dependency—A dependency hosted by a process other than the pro-
gram’s execution process (for example, a database, a message bus, or an SMTP
service)
Private dependency—Any dependency that is not shared
The classical school recommends avoiding shared dependencies because they provide
the means for tests to interfere with each other’s execution context and thus prevent
those tests from running in parallel. The ability for tests to run in parallel, sequen-
tially, and in any order is called test isolation.
 If a shared dependency is not out-of-process, then it’s easy to avoid reusing it in
tests by providing a new instance of it on each test run. In cases where the shared
dependency is out-of-process, testing becomes more complicated. You can’t instanti-
ate a new database or provision a new message bus before each test execution; that
would drastically slow down the test suite. The usual approach is to replace such
dependencies with test doubles—mocks and stubs.
 Not all out-of-process dependencies should be mocked out, though. If an out-of-
process dependency is only accessible through your application, then communications with such a
dependency are not part of your system’s observable behavior. An out-of-process dependency
that can’t be observed externally, in effect, acts as part of your application (figure 5.14).
 Remember, the requirement to always preserve the communication pattern
between your application and external systems stems from the necessity to maintain
backward compatibility. You have to maintain the way your application talks to external
Third-party
system
(external
client)
SMTP service
Observable behavior (contract)
Application
database
(accessible
only by the
application)
Implementation details
Figure 5.14
Communications with an out-of-process dependency that can’t be 
observed externally are implementation details. They don’t have to stay in place 
after refactoring and therefore shouldn’t be verified with mocks.


---
**Page 116**

116
CHAPTER 5
Mocks and test fragility
systems. That’s because you can’t change those external systems simultaneously with
your application; they may follow a different deployment cycle, or you might simply
not have control over them.
 But when your application acts as a proxy to an external system, and no client can
access it directly, the backward-compatibility requirement vanishes. Now you can deploy
your application together with this external system, and it won’t affect the clients. The
communication pattern with such a system becomes an implementation detail.
 A good example here is an application database: a database that is used only by
your application. No external system has access to this database. Therefore, you can
modify the communication pattern between your system and the application database
in any way you like, as long as it doesn’t break existing functionality. Because that data-
base is completely hidden from the eyes of the clients, you can even replace it with an
entirely different storage mechanism, and no one will notice.
 The use of mocks for out-of-process dependencies that you have a full control over
also leads to brittle tests. You don’t want your tests to turn red every time you split a
table in the database or modify the type of one of the parameters in a stored proce-
dure. The database and your application must be treated as one system.
 This obviously poses an issue. How would you test the work with such a depen-
dency without compromising the feedback speed, the third attribute of a good unit
test? You’ll see this subject covered in depth in the following two chapters. 
5.4.2
Using mocks to verify behavior
Mocks are often said to verify behavior. In the vast majority of cases, they don’t. The
way each individual class interacts with neighboring classes in order to achieve some
goal has nothing to do with observable behavior; it’s an implementation detail.
 Verifying communications between classes is akin to trying to derive a person’s
behavior by measuring the signals that neurons in the brain pass among each other.
Such a level of detail is too granular. What matters is the behavior that can be traced
back to the client goals. The client doesn’t care what neurons in your brain light up
when they ask you to help. The only thing that matters is the help itself—provided by
you in a reliable and professional fashion, of course. Mocks have something to do with
behavior only when they verify interactions that cross the application boundary and
only when the side effects of those interactions are visible to the external world. 
Summary
Test double is an overarching term that describes all kinds of non-production-
ready, fake dependencies in tests. There are five variations of test doubles—
dummy, stub, spy, mock, and fake—that can be grouped in just two types: mocks
and stubs. Spies are functionally the same as mocks; dummies and fakes serve
the same role as stubs.
Mocks help emulate and examine outcoming interactions: calls from the SUT to
its dependencies that change the state of those dependencies. Stubs help


