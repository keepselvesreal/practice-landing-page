# 8.3.1 What scenarios to test? (pp.194-195)

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


---
**Page 195**

195
Integration testing: An example
8.3.2
Categorizing the database and the message bus
Before writing the integration test, you need to categorize the two out-of-process
dependencies and decide which of them to test directly and which to replace with a
mock. The application database is a managed dependency because no other system
can access it. Therefore, you should use a real instance of it. The integration test will
Insert a user and a company into the database.
Run the change of email scenario on that database.
Verify the database state.
On the other hand, the message bus is an unmanaged dependency—its sole pur-
pose is to enable communication with other systems. The integration test will mock
out the message bus and verify the interactions between the controller and the
mock afterward. 
8.3.3
What about end-to-end testing?
There will be no end-to-end tests in our sample project. An end-to-end test in a sce-
nario with an API would be a test running against a deployed, fully functioning ver-
sion of that API, which means no mocks for any of the out-of-process dependencies
(figure 8.7). On the other hand, integration tests host the application within the same
process and substitute unmanaged dependencies with mocks (figure 8.8).
 As I mentioned in chapter 2, whether to use end-to-end tests is a judgment call. For
the most part, when you include managed dependencies in the integration testing
scope and mock out only unmanaged dependencies, integration tests provide a level
End-to-end test
Application
Message bus
Database
Out-of-process
In-process
Figure 8.7
End-to-end tests emulate the external client and therefore test a 
deployed version of the application with all out-of-process dependencies included 
in the testing scope. End-to-end tests shouldn’t check managed dependencies 
(such as the database) directly, only indirectly through the application.


