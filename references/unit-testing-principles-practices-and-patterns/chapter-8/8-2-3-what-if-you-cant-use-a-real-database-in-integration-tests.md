# 8.2.3 What if you can’t use a real database in integration tests? (pp.192-193)

---
**Page 192**

192
CHAPTER 8
Why integration testing?
other applications as an unmanaged dependency. Such tables in effect act as a mes-
sage bus, with their rows playing the role of messages. Use mocks to make sure the
communication pattern with these tables remains unchanged. At the same time, treat
the rest of your database as a managed dependency and verify its final state, not the
interactions with it (figure 8.5).
It’s important to differentiate these two parts of your database because, again, the
shared tables are observable externally, and you need to be careful about how your
application communicates with them. Don’t change the way your system interacts with
those tables unless absolutely necessary! You never know how other applications will
react to such a change. 
8.2.3
What if you can’t use a real database in integration tests?
Sometimes, for reasons outside of your control, you just can’t use a real version of a
managed dependency in integration tests. An example would be a legacy database
that you can’t deploy to a test automation environment, not to mention a developer
machine, because of some IT security policy, or because the cost of setting up and
maintaining a test database instance is prohibitive.
 What should you do in such a situation? Should you mock out the database anyway,
despite it being a managed dependency? No, because mocking out a managed depen-
dency compromises the integration tests’ resistance to refactoring. Furthermore, such
External applications
Table
Table
Table
Table
Managed part
Table
Table
Unmanaged part
Test directly
Replace with mocks
Database
Your application
Figure 8.5
Treat the part of the database that is visible to external 
applications as an unmanaged dependency. Replace it with mocks in 
integration tests. Treat the rest of the database as a managed dependency. 
Verify its final state, not interactions with it.


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


