# 8.8 Summary (pp.213-216)

---
**Page 213**

213
Summary
domain class becomes so inconvenient that you have to resort to ambient context,
that’s a certain sign of trouble. You either log too much or use too many layers of indi-
rection. In any case, ambient context is not a solution. Instead, tackle the root cause
of the problem.
 The following listing shows one way to explicitly inject the logger: as a method
argument. Another way is through the class constructor.
public void ChangeEmail(
string newEmail,      
Company company,      
ILogger logger)       
{
logger.Info(
$"Changing email for user {UserId} to {newEmail}");
/* ... */
logger.Info($"Email is changed for user {UserId}");
}
8.7
Conclusion
View communications with all out-of-process dependencies through the lens of whether
this communication is part of the application’s observable behavior or an imple-
mentation detail. The log storage isn’t any different in that regard. Mock logging
functionality if the logs are observable by non-programmers; don’t test it otherwise.
In the next chapter, we’ll dive deeper into the topic of mocking and best practices
related to it. 
Summary
An integration test is any test that is not a unit test. Integration tests verify how
your system works in integration with out-of-process dependencies:
– Integration tests cover controllers; unit tests cover algorithms and the domain
model.
– Integration tests provide better protection against regressions and resistance
to refactoring; unit tests have better maintainability and feedback speed.
The bar for integration tests is higher than for unit tests: the score they have in
the metrics of protection against regressions and resistance to refactoring must
be higher than that of a unit test to offset the worse maintainability and feed-
back speed. The Test Pyramid represents this trade-off: the majority of tests
should be fast and cheap unit tests, with a smaller number of slow and more
expensive integration tests that check correctness of the system as a whole:
– Check as many of the business scenario’s edge cases as possible with unit
tests. Use integration tests to cover one happy path, as well as any edge cases
that can’t be covered by unit tests.
Listing 8.9
Injecting the logger explicitly
Method 
injection 


---
**Page 214**

214
CHAPTER 8
Why integration testing?
– The shape of the Test Pyramid depends on the project’s complexity. Simple
projects have little code in the domain model and thus can have an equal
number of unit and integration tests. In the most trivial cases, there might be
no unit tests.
The Fail Fast principle advocates for making bugs manifest themselves quickly
and is a viable alternative to integration testing.
Managed dependencies are out-of-process dependencies that are only accessible
through your application. Interactions with managed dependencies aren’t
observable externally. A typical example is the application database.
Unmanaged dependencies are out-of-process dependencies that other applications
have access to. Interactions with unmanaged dependencies are observable exter-
nally. Typical examples include an SMTP server and a message bus.
Communications with managed dependencies are implementation details; com-
munications with unmanaged dependencies are part of your system’s observ-
able behavior.
Use real instances of managed dependencies in integration tests; replace unman-
aged dependencies with mocks.
Sometimes an out-of-process dependency exhibits attributes of both managed and
unmanaged dependencies. A typical example is a database that other applications
have access to. Treat the observable part of the dependency as an unmanaged
dependency: replace that part with mocks in tests. Treat the rest of the depen-
dency as a managed dependency: verify its final state, not interactions with it.
An integration test must go through all layers that work with a managed depen-
dency. In an example with a database, this means checking the state of that
database independently of the data used as input parameters.
Interfaces with a single implementation are not abstractions and don’t provide
loose coupling any more than the concrete classes that implement those inter-
faces. Trying to anticipate future implementations for such interfaces violates
the YAGNI (you aren’t gonna need it) principle.
The only legitimate reason to use interfaces with a single implementation is to
enable mocking. Use such interfaces only for unmanaged dependencies. Use
concrete classes for managed dependencies.
Interfaces with a single implementation used for in-process dependencies are
a red flag. Such interfaces hint at using mocks to check interactions between
domain classes, which leads to coupling tests to the code’s implementation
details.
Have an explicit and well-known place for the domain model in your code base.
The explicit boundary between domain classes and controllers makes it easier
to tell unit and integration tests apart.
An excessive number of layers of indirection negatively affects your ability to
reason about the code. Have as few layers of indirections as possible. In most


---
**Page 215**

215
Summary
backend systems, you can get away with just three of them: the domain model,
an application services layer (controllers), and an infrastructure layer.
Circular dependencies add cognitive load when you try to understand the code.
A typical example is a callback (when a callee notifies the caller about the result
of its work). Break the cycle by introducing a value object; use that value object
to return the result from the callee to the caller.
Multiple act sections in a test are only justified when that test works with out-of-
process dependencies that are hard to bring into a desirable state. You should
never have multiple acts in a unit test, because unit tests don’t work with out-of-
process dependencies. Multistep tests almost always belong to the category of
end-to-end tests.
Support logging is intended for support staff and system administrators; it’s
part of the application’s observable behavior. Diagnostic logging helps devel-
opers understand what’s going on inside the application: it’s an implementa-
tion detail.
Because support logging is a business requirement, reflect that requirement
explicitly in your code base. Introduce a special DomainLogger class where you
list all the support logging needed for the business.
Treat support logging like any other functionality that works with an out-of-pro-
cess dependency. Use domain events to track changes in the domain model;
convert those domain events into calls to DomainLogger in controllers.
Don’t test diagnostic logging. Unlike support logging, you can do diagnostic
logging directly in the domain model.
Use diagnostic logging sporadically. Excessive diagnostic logging clutters the
code and damages the logs’ signal-to-noise ratio. Ideally, you should only use
diagnostic logging for unhandled exceptions.
Always inject all dependencies explicitly (including loggers), either via the con-
structor or as a method argument.


---
**Page 216**

216
Mocking best practices
As you might remember from chapter 5, a mock is a test double that helps to emu-
late and examine interactions between the system under test and its dependencies.
As you might also remember from chapter 8, mocks should only be applied to
unmanaged dependencies (interactions with such dependencies are observable by
external applications). Using mocks for anything else results in brittle tests (tests that
lack the metric of resistance to refactoring). When it comes to mocks, adhering to
this one guideline will get you about two-thirds of the way to success.
 This chapter shows the remaining guidelines that will help you develop inte-
gration tests that have the greatest possible value by maxing out mocks’ resistance
to refactoring and protection against regressions. I’ll first show a typical use of
mocks, describe its drawbacks, and then demonstrate how you can overcome
those drawbacks.
This chapter covers
Maximizing the value of mocks
Replacing mocks with spies
Mocking best practices


