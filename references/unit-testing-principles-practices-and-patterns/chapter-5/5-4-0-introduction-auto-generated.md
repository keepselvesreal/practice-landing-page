# 5.4.0 Introduction [auto-generated] (pp.114-115)

---
**Page 114**

114
CHAPTER 5
Mocks and test fragility
Unlike the communication between CustomerController and the SMTP service, the
RemoveInventory() method call from Customer to Store doesn’t cross the applica-
tion boundary: both the caller and the recipient reside inside the application. Also,
this method is neither an operation nor a state that helps the client achieve its goals.
The client of these two domain classes is CustomerController with the goal of making
a purchase. The only two members that have an immediate connection to this goal are
customer.Purchase() and store.GetInventory(). The Purchase() method initiates
the purchase, and GetInventory() shows the state of the system after the purchase is
completed. The RemoveInventory() method call is an intermediate step on the way to
the client’s goal—an implementation detail. 
5.4
The classical vs. London schools of unit testing, 
revisited
As a reminder from chapter 2 (table 2.1), table 5.2 sums up the differences between
the classical and London schools of unit testing.
In chapter 2, I mentioned that I prefer the classical school of unit testing over the
London school. I hope now you can see why. The London school encourages the use
of mocks for all but immutable dependencies and doesn’t differentiate between intra-
system and inter-system communications. As a result, tests check communications
between classes just as much as they check communications between your application
and external systems.
 This indiscriminate use of mocks is why following the London school often results
in tests that couple to implementation details and thus lack resistance to refactoring.
As you may remember from chapter 4, the metric of resistance to refactoring (unlike
the other three) is mostly a binary choice: a test either has resistance to refactoring or
it doesn’t. Compromising on this metric renders the test nearly worthless.
 The classical school is much better at this issue because it advocates for substitut-
ing only dependencies that are shared between tests, which almost always translates
into out-of-process dependencies such as an SMTP service, a message bus, and so on.
But the classical school is not ideal in its treatment of inter-system communications,
either. This school also encourages excessive use of mocks, albeit not as much as the
London school.
Table 5.2
The differences between the London and classical schools of unit testing
Isolation of
A unit is
Uses test doubles for
London school
Units
A class
All but immutable dependencies
Classical school
Unit tests
A class or a set of classes
Shared dependencies


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


