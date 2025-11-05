# 8.1.3 Integration testing vs. failing fast (pp.188-190)

---
**Page 188**

188
CHAPTER 8
Why integration testing?
8.1.3
Integration testing vs. failing fast
This section elaborates on the guideline of using integration tests to cover one happy
path per business scenario and any edge cases that can’t be covered by unit tests. 
 For an integration test, select the longest happy path in order to verify interactions
with all out-of-process dependencies. If there’s no one path that goes through all such
interactions, write additional integration tests—as many as needed to capture commu-
nications with every external system.
 As with the edge cases that can’t be covered by unit tests, there are exceptions to
this part of the guideline, too. There’s no need to test an edge case if an incorrect
execution of that edge case immediately fails the entire application. For example, you
saw in chapter 7 how User from the sample CRM system implemented a CanChange-
Email method and made its successful execution a precondition for ChangeEmail():
End-
to-end
Integration
tests
Unit tests
Test count
Protection against
regressions,
resistance to
refactoring
Fast feedback,
maintainability
Figure 8.2
The Test Pyramid represents a trade-off that works best for most 
applications. Fast, cheap unit tests cover the majority of edge cases, while a 
smaller number of slow, more expensive integration tests ensure the correctness 
of the system as a whole.
Figure 8.3
The Test Pyramid of a simple project. 
Little complexity requires a smaller number of unit 
tests compared to a normal pyramid.
Unit tests
Integration tests


---
**Page 189**

189
What is an integration test?
public void ChangeEmail(string newEmail, Company company)
{
Precondition.Requires(CanChangeEmail() == null);
/* the rest of the method */
}
The controller invokes CanChangeEmail() and interrupts the operation if that
method returns an error:
// UserController
public string ChangeEmail(int userId, string newEmail)
{
object[] userData = _database.GetUserById(userId);
User user = UserFactory.Create(userData);
string error = user.CanChangeEmail();
if (error != null)                    
return error;                     
/* the rest of the method */
}
This example shows the edge case you could theoretically cover with an integration
test. Such a test doesn’t provide a significant enough value, though. If the controller
tries to change the email without consulting with CanChangeEmail() first, the applica-
tion crashes. This bug reveals itself with the first execution and thus is easy to notice
and fix. It also doesn’t lead to data corruption.
TIP
It’s better to not write a test at all than to write a bad test. A test that
doesn’t provide significant value is a bad test.
Unlike the call from the controller to CanChangeEmail(), the presence of the precon-
dition in User should be tested. But that is better done with a unit test; there’s no need
for an integration test.
 Making bugs manifest themselves quickly is called the Fail Fast principle, and it’s a
viable alternative to integration testing.
The Fail Fast principle 
The Fail Fast principle stands for stopping the current operation as soon as any unex-
pected error occurs. This principle makes your application more stable by
Shortening the feedback loop—The sooner you detect a bug, the easier it is
to fix. A bug that is already in production is orders of magnitude more expen-
sive to fix compared to a bug found during development.
Protecting the persistence state—Bugs lead to corruption of the application’s
state. Once that state penetrates into the database, it becomes much harder
to fix. Failing fast helps you prevent the corruption from spreading.
Edge case


---
**Page 190**

190
CHAPTER 8
Why integration testing?
8.2
Which out-of-process dependencies to test directly
As I mentioned earlier, integration tests verify how your system integrates with out-of-
process dependencies. There are two ways to implement such verification: use the real
out-of-process dependency, or replace that dependency with a mock. This section
shows when to apply each of the two approaches.
8.2.1
The two types of out-of-process dependencies
All out-of-process dependencies fall into two categories:
Managed dependencies (out-of-process dependencies you have full control over)—These
dependencies are only accessible through your application; interactions with
them aren’t visible to the external world. A typical example is a database. Exter-
nal systems normally don’t access your database directly; they do that through
the API your application provides.
Unmanaged dependencies (out-of-process dependencies you don’t have full control over)—
Interactions with such dependencies are observable externally. Examples include
an SMTP server and a message bus: both produce side effects visible to other
applications.
I mentioned in chapter 5 that communications with managed dependencies are
implementation details. Conversely, communications with unmanaged dependencies
are part of your system’s observable behavior (figure 8.4). This distinction leads to the
difference in treatment of out-of-process dependencies in integration tests.
IMPORTANT
Use real instances of managed dependencies; replace unman-
aged dependencies with mocks.
As discussed in chapter 5, the requirement to preserve the communication pattern
with unmanaged dependencies stems from the necessity to maintain backward com-
patibility with those dependencies. Mocks are perfect for this task. With mocks, you
can ensure communication pattern permanence in light of any possible refactorings.
(continued)
Stopping the current operation is normally done by throwing exceptions, because
exceptions have semantics that are perfectly suited for the Fail Fast principle: they
interrupt the program flow and pop up to the highest level of the execution stack,
where you can log them and shut down or restart the operation.
Preconditions are one example of the Fail Fast principle in action. A failing precondi-
tion signifies an incorrect assumption made about the application state, which is
always a bug. Another example is reading data from a configuration file. You can
arrange the reading logic such that it will throw an exception if the data in the config-
uration file is incomplete or incorrect. You can also put this logic close to the appli-
cation startup, so that the application doesn’t launch if there’s a problem with its
configuration. 


