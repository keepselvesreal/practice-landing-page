# 8.6.3 How much logging is enough? (pp.212-212)

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


