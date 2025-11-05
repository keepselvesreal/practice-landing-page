# 9.3 Summary (pp.227-229)

---
**Page 227**

227
Summary
9.2.4
Only mock types that you own
The last guideline I’d like to talk about is mocking only types that you own. It was first
introduced by Steve Freeman and Nat Pryce.1 The guideline states that you should
always write your own adapters on top of third-party libraries and mock those adapters
instead of the underlying types. A few of their arguments are as follows:
You often don’t have a deep understanding of how the third-party code works.
Even if that code already provides built-in interfaces, it’s risky to mock those
interfaces, because you have to be sure the behavior you mock matches what
the external library actually does.
Adapters abstract non-essential technical details of the third-party code and
define the relationship with the library in your application’s terms.
I fully agree with this analysis. Adapters, in effect, act as an anti-corruption layer
between your code and the external world.2 These help you to
Abstract the underlying library’s complexity
Only expose features you need from the library
Do that using your project’s domain language
The IBus interface in our sample CRM project serves exactly that purpose. Even if the
underlying message bus’s library provides as nice and clean an interface as IBus, you
are still better off introducing your own wrapper on top of it. You never know how the
third-party code will change when you upgrade the library. Such an upgrade could
cause a ripple effect across the whole code base! The additional abstraction layer
restricts that ripple effect to just one class: the adapter itself.
 Note that the “mock your own types” guideline doesn’t apply to in-process depen-
dencies. As I explained previously, mocks are for unmanaged dependencies only.
Thus, there’s no need to abstract in-memory or managed dependencies. For instance,
if a library provides a date and time API, you can use that API as-is, because it doesn’t
reach out to unmanaged dependencies. Similarly, there’s no need to abstract an ORM
as long as it’s used for accessing a database that isn’t visible to external applications.
Of course, you can introduce your own wrapper on top of any library, but it’s rarely
worth the effort for anything other than unmanaged dependencies. 
Summary
Verify interactions with an unmanaged dependency at the very edges of your
system. Mock the last type in the chain of types between the controller and the
unmanaged dependency. This helps you increase both protection against
regressions (due to more code being validated by the integration test) and
1 See page 69 in Growing Object-Oriented Software, Guided by Tests by Steve Freeman and Nat Pryce (Addison-Wesley
Professional, 2009).
2 See Domain-Driven Design: Tackling Complexity in the Heart of Software by Eric Evans (Addison-Wesley, 2003).


---
**Page 228**

228
CHAPTER 9
Mocking best practices
resistance to refactoring (due to detaching the mock from the code’s imple-
mentation details).
Spies are handwritten mocks. When it comes to classes residing at the system’s
edges, spies are superior to mocks. They help you reuse code in the assertion
phase, thereby reducing the test’s size and improving readability.
Don’t rely on production code when making assertions. Use a separate set of lit-
erals and constants in tests. Duplicate those literals and constants from the pro-
duction code if necessary. Tests should provide a checkpoint independent of
the production code. Otherwise, you risk producing tautology tests (tests that
don’t verify anything and contain semantically meaningless assertions).
Not all unmanaged dependencies require the same level of backward compati-
bility. If the exact structure of the message isn’t important, and you only want to
verify the existence of that message and the information it carries, you can
ignore the guideline of verifying interactions with unmanaged dependencies at
the very edges of your system. The typical example is logging.
Because mocks are for unmanaged dependencies only, and because controllers
are the only code working with such dependencies, you should only apply mock-
ing when testing controllers—in integration tests. Don’t use mocks in unit tests.
The number of mocks used in a test is irrelevant. That number depends solely
on the number of unmanaged dependencies participating in the operation.
Ensure both the existence of expected calls and the absence of unexpected calls
to mocks.
Only mock types that you own. Write your own adapters on top of third-party
libraries that provide access to unmanaged dependencies. Mock those adapters
instead of the underlying types.


---
**Page 229**

229
Testing the database
The last piece of the puzzle in integration testing is managed out-of-process depen-
dencies. The most common example of a managed dependency is an application
database—a database no other application has access to.
 Running tests against a real database provides bulletproof protection against
regressions, but those tests aren’t easy to set up. This chapter shows the preliminary
steps you need to take before you can start testing your database: it covers keeping
track of the database schema, explains the difference between the state-based and
migration-based database delivery approaches, and demonstrates why you should
choose the latter over the former.
 After learning the basics, you’ll see how to manage transactions during the test,
clean up leftover data, and keep tests small by eliminating insignificant parts and
amplifying the essentials. This chapter focuses on relational databases, but many of
This chapter covers
Prerequisites for testing the database
Database testing best practices
Test data life cycle
Managing database transactions in tests


