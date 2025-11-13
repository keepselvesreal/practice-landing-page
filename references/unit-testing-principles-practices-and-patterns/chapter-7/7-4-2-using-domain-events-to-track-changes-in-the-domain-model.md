# 7.4.2 Using domain events to track changes in the domain model (pp.175-178)

---
**Page 175**

175
Handling conditional logic in controllers
7.4.2
Using domain events to track changes in the domain model
It’s sometimes hard to deduct what steps led the domain model to the current state.
Still, it might be important to know these steps because you need to inform external
systems about what exactly has happened in your application. Putting this responsibil-
ity on the controllers would make them more complicated. To avoid that, you can
track important changes in the domain model and then convert those changes into
calls to out-of-process dependencies after the business operation is complete. Domain
events help you implement such tracking.
DEFINITION
A domain event describes an event in the application that is mean-
ingful to domain experts. The meaningfulness for domain experts is what
differentiates domain events from regular events (such as button clicks).
Domain events are often used to inform external applications about import-
ant changes that have happened in your system.
Our CRM has a tracking requirement, too: it has to notify external systems about
changed user emails by sending messages to the message bus. The current implemen-
tation has a flaw in the notification functionality: it sends messages even when the
email is not changed, as shown in the following listing.
// User
public void ChangeEmail(string newEmail, Company company)
{
Precondition.Requires(CanChangeEmail() == null);
if (Email == newEmail)   
return;
/* the rest of the method */
}
// Controller
public string ChangeEmail(int userId, string newEmail)
{
/* preparations */
user.ChangeEmail(newEmail, company);
_database.SaveCompany(company);
_database.SaveUser(user);
_messageBus.SendEmailChangedMessage(  
userId, newEmail);
  
return "OK";
}
You could resolve this bug by moving the check for email sameness to the controller,
but then again, there are issues with the business logic fragmentation. And you can’t
Listing 7.11
Sends a notification even when the email has not changed
User email may 
not change.
The controller sends 
a message anyway.


---
**Page 176**

176
CHAPTER 7
Refactoring toward valuable unit tests
put this check to CanChangeEmail() because the application shouldn’t return an
error if the new email is the same as the old one.
 Note that this particular check probably doesn’t introduce too much business logic
fragmentation, so I personally wouldn’t consider the controller overcomplicated if it
contained that check. But you may find yourself in a more difficult situation in which
it’s hard to prevent your application from making unnecessary calls to out-of-process
dependencies without passing those dependencies to the domain model, thus over-
complicating that domain model. The only way to prevent such overcomplication is
the use of domain events.
 From an implementation standpoint, a domain event is a class that contains data
needed to notify external systems. In our specific example, it is the user’s ID and
email:
public class EmailChangedEvent
{
public int UserId { get; }
public string NewEmail { get; }
}
NOTE
Domain events should always be named in the past tense because they
represent things that already happened. Domain events are values—they are
immutable and interchangeable.
User will have a collection of such events to which it will add a new element when the
email changes. This is how its ChangeEmail() method looks after the refactoring.
public void ChangeEmail(string newEmail, Company company)
{
Precondition.Requires(CanChangeEmail() == null);
if (Email == newEmail)
return;
UserType newType = company.IsEmailCorporate(newEmail)
? UserType.Employee
: UserType.Customer;
if (Type != newType)
{
int delta = newType == UserType.Employee ? 1 : -1;
company.ChangeNumberOfEmployees(delta);
}
Email = newEmail;
Type = newType;
EmailChangedEvents.Add(
  
new EmailChangedEvent(UserId, newEmail));  
}
Listing 7.12
User adding an event when the email changes
A new event indicates 
the change of email.


---
**Page 177**

177
Handling conditional logic in controllers
The controller then will convert the events into messages on the bus.
public string ChangeEmail(int userId, string newEmail)
{
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
foreach (var ev in user.EmailChangedEvents)  
{
  
_messageBus.SendEmailChangedMessage(
  
ev.UserId, ev.NewEmail);
  
}
  
return "OK";
}
Notice that the Company and User instances are still persisted in the database uncondi-
tionally: the persistence logic doesn’t depend on domain events. This is due to the dif-
ference between changes in the database and messages in the bus.
 Assuming that no application has access to the database other than the CRM, com-
munications with that database are not part of the CRM’s observable behavior—they
are implementation details. As long as the final state of the database is correct, it
doesn’t matter how many calls your application makes to that database. On the other
hand, communications with the message bus are part of the application’s observable
behavior. In order to maintain the contract with external systems, the CRM should put
messages on the bus only when the email changes.
 There are performance implications to persisting data in the database uncondi-
tionally, but they are relatively insignificant. The chances that after all the validations
the new email is the same as the old one are quite small. The use of an ORM can also
help. Most ORMs won’t make a round trip to the database if there are no changes to
the object state.
 You can generalize the solution with domain events: extract a DomainEvent base
class and introduce a base class for all domain classes, which would contain a collec-
tion of such events: List<DomainEvent> events. You can also write a separate event
dispatcher instead of dispatching domain events manually in controllers. Finally, in
larger projects, you might need a mechanism for merging domain events before
Listing 7.13
The controller processing domain events
Domain event 
processing


---
**Page 178**

178
CHAPTER 7
Refactoring toward valuable unit tests
dispatching them. That topic is outside the scope of this book, though. You can read
about it in my article “Merging domain events before dispatching” at http://mng
.bz/YeVe.
 Domain events remove the decision-making responsibility from the controller and
put that responsibility into the domain model, thus simplifying unit testing communi-
cations with external systems. Instead of verifying the controller itself and using mocks
to substitute out-of-process dependencies, you can test the domain event creation
directly in unit tests, as shown next.
[Fact]
public void Changing_email_from_corporate_to_non_corporate()
{
var company = new Company("mycorp.com", 1);
var sut = new User(1, "user@mycorp.com", UserType.Employee, false);
sut.ChangeEmail("new@gmail.com", company);
company.NumberOfEmployees.Should().Be(0);
sut.Email.Should().Be("new@gmail.com");
sut.Type.Should().Be(UserType.Customer);
sut.EmailChangedEvents.Should().Equal(
   
new EmailChangedEvent(1, "new@gmail.com"));  
}
Of course, you’ll still need to test the controller to make sure it does the orchestration
correctly, but doing so requires a much smaller set of tests. That’s the topic of the next
chapter. 
7.5
Conclusion
Notice a theme that has been present throughout this chapter: abstracting away the
application of side effects to external systems. You achieve such abstraction by keeping
those side effects in memory until the very end of the business operation, so that they
can be tested with plain unit tests without involving out-of-process dependencies.
Domain events are abstractions on top of upcoming messages in the bus. Changes in
domain classes are abstractions on top of upcoming modifications in the database.
NOTE
It’s easier to test abstractions than the things they abstract.
Although we were able to successfully contain all the decision-making in the domain
model with the help of domain events and the CanExecute/Execute pattern, you
won’t be able to always do that. There are situations where business logic fragmenta-
tion is inevitable.
 For example, there’s no way to verify email uniqueness outside the controller with-
out introducing out-of-process dependencies in the domain model. Another example
is failures in out-of-process dependencies that should alter the course of the business
Listing 7.14
Testing the creation of a domain event
Simultaneously asserts 
the collection size and the 
element in the collection


