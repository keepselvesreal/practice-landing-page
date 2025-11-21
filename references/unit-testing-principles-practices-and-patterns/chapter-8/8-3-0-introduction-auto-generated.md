# 8.3.0 Introduction [auto-generated] (pp.193-194)

---
**Page 193**

193
Integration testing: An example
tests no longer provide as good protection against regressions. And if the database is
the only out-of-process dependency in your project, the resulting integration tests
would deliver no additional protection compared to the existing set of unit tests (assum-
ing these unit tests follow the guidelines from chapter 7).
 The only thing such integration tests would do, in addition to unit tests, is check
what repository methods the controller calls. In other words, you wouldn’t really gain
confidence about anything other than those three lines of code in your controller
being correct, while still having to do a lot of plumbing.
 If you can’t test the database as-is, don’t write integration tests at all, and instead,
focus exclusively on unit testing of the domain model. Remember to always put all
your tests under close scrutiny. Tests that don’t provide a high enough value should
have no place in your test suite. 
8.3
Integration testing: An example
Let’s get back to the sample CRM system from chapter 7 and see how it can be cov-
ered with integration tests. As you may recall, this system implements one feature:
changing the user’s email. It retrieves the user and the company from the database,
delegates the decision-making to the domain model, and then saves the results back
to the database and puts a message on the bus if needed (figure 8.6).
The following listing shows how the controller currently looks.
public class UserController
{
private readonly Database _database = new Database();
private readonly MessageBus _messageBus = new MessageBus();
public string ChangeEmail(int userId, string newEmail)
{
Listing 8.1
The user controller 
Application
service
(controller)
Business logic
(domain model)
Database
Message bus
GetUserById
CanChangeEmail
SaveCompany
GetCompany
ChangeEmail
SaveUser
SendMessage
Figure 8.6
The use case of changing the user’s email. The controller orchestrates the work between 
the database, the message bus, and the domain model.


---
**Page 194**

194
CHAPTER 8
Why integration testing?
object[] userData = _database.GetUserById(userId);
User user = UserFactory.Create(userData);
string error = user.CanChangeEmail();
if (error != null)
return error;
object[] companyData = _database.GetCompany();
Company company = CompanyFactory.Create(companyData);
user.ChangeEmail(newEmail, company);
_database.SaveCompany(company);
_database.SaveUser(user);
foreach (EmailChangedEvent ev in user.EmailChangedEvents)
{
_messageBus.SendEmailChangedMessage(ev.UserId, ev.NewEmail);
}
return "OK";
}
}
In the following section, I’ll first outline scenarios to verify using integration tests.
Then I’ll show you how to work with the database and the message bus in tests.
8.3.1
What scenarios to test?
As I mentioned earlier, the general guideline for integration testing is to cover the
longest happy path and any edge cases that can’t be exercised by unit tests. The longest
happy path is the one that goes through all out-of-process dependencies.
 In the CRM project, the longest happy path is a change from a corporate to a non-
corporate email. Such a change leads to the maximum number of side effects:
In the database, both the user and the company are updated: the user changes
its type (from corporate to non-corporate) and email, and the company changes
its number of employees.
A message is sent to the message bus.
As for the edge cases that aren’t tested by unit tests, there’s only one such edge case:
the scenario where the email can’t be changed. There’s no need to test this scenario,
though, because the application will fail fast if this check isn’t present in the control-
ler. That leaves us with a single integration test:
public void Changing_email_from_corporate_to_non_corporate()


