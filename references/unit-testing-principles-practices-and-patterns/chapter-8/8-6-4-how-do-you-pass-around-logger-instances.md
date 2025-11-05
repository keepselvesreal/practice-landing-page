# 8.6.4 How do you pass around logger instances? (pp.212-213)

---
**Page 212**

212
CHAPTER 8
Why integration testing?
8.6.3
How much logging is enough?
Another important question is about the optimum amount of logging. How much log-
ging is enough? Support logging is out of the question here because it’s a business
requirement. You do have control over diagnostic logging, though.
 It’s important not to overuse diagnostic logging, for the following two reasons:
Excessive logging clutters the code. This is especially true for the domain model.
That’s why I don’t recommend using diagnostic logging in User even though
such a use is fine from a unit testing perspective: it obscures the code.
Logs’ signal-to-noise ratio is key. The more you log, the harder it is to find relevant
information. Maximize the signal; minimize the noise.
Try not to use diagnostic logging in the domain model at all. In most cases, you can
safely move that logging from domain classes to controllers. And even then, resort to
diagnostic logging only temporarily when you need to debug something. Remove it
once you finish debugging. Ideally, you should use diagnostic logging for unhandled
exceptions only. 
8.6.4
How do you pass around logger instances?
Finally, the last question is how to pass logger instances in the code. One way to
resolve these instances is using static methods, as shown in the following listing.
public class User
{
private static readonly ILogger _logger =   
LogManager.GetLogger(typeof(User));     
public void ChangeEmail(string newEmail, Company company)
{
_logger.Info(
$"Changing email for user {UserId} to {newEmail}");
/* ... */
_logger.Info($"Email is changed for user {UserId}");
}
}
Steven van Deursen and Mark Seeman, in their book Dependency Injection Principles,
Practices, Patterns (Manning Publications, 2018), call this type of dependency acquisi-
tion ambient context. This is an anti-pattern. Two of their arguments are that
The dependency is hidden and hard to change.
Testing becomes more difficult.
I fully agree with this analysis. To me, though, the main drawback of ambient con-
text is that it masks potential problems in code. If injecting a logger explicitly into a
Listing 8.8
Storing ILogger in a static field
Resolves ILogger through a 
static method, and stores it 
in a private static field


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


