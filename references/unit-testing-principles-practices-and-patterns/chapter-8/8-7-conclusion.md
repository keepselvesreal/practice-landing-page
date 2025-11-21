# 8.7 Conclusion (pp.213-213)

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


