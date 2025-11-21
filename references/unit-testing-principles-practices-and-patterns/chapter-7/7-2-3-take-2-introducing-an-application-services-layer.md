# 7.2.3 Take 2: Introducing an application services layer (pp.160-163)

---
**Page 160**

160
CHAPTER 7
Refactoring toward valuable unit tests
often fails to scale as the code base grows. The reason is precisely this lack of separa-
tion between these two responsibilities: business logic and communication with out-of-
process dependencies. 
7.2.2
Take 1: Making implicit dependencies explicit
The usual approach to improve testability is to make implicit dependencies explicit:
that is, introduce interfaces for Database and MessageBus, inject those interfaces into
User, and then mock them in tests. This approach does help, and that’s exactly what
we did in the previous chapter when we introduced the implementation with mocks
for the audit system. However, it’s not enough.
 From the perspective of the types-of-code diagram, it doesn’t matter if the domain
model refers to out-of-process dependencies directly or via an interface. Such depen-
dencies are still out-of-process; they are proxies to data that is not yet in memory. You
still need to maintain complicated mock machinery in order to test such classes,
which increases the tests’ maintenance costs. Moreover, using mocks for the database
dependency would lead to test fragility (we’ll discuss this in the next chapter).
 Overall, it’s much cleaner for the domain model not to depend on out-of-process
collaborators at all, directly or indirectly (via an interface). That’s what the hexagonal
architecture advocates as well—the domain model shouldn’t be responsible for com-
munications with external systems. 
7.2.3
Take 2: Introducing an application services layer
To overcome the problem of the domain model directly communicating with external
systems, we need to shift this responsibility to another class, a humble controller (an
application service, in the hexagonal architecture taxonomy). As a general rule, domain
classes should only depend on in-process dependencies, such as other domain classes,
or plain values. Here’s what the first version of that application service looks like.
Domain model,
algorithms
Overcomplicated
code
Trivial code
Controllers
Complexity,
domain
signiﬁcance
Number of
collaborators
User class
Figure 7.7
The initial 
implementation of the User 
class scores highly on both 
dimensions and thus falls 
into the category of 
overcomplicated code.


---
**Page 161**

161
Refactoring toward valuable unit tests
public class UserController
{
private readonly Database _database = new Database();
private readonly MessageBus _messageBus = new MessageBus();
public void ChangeEmail(int userId, string newEmail)
{
object[] data = _database.GetUserById(userId);
string email = (string)data[1];
UserType type = (UserType)data[2];
var user = new User(userId, email, type);
object[] companyData = _database.GetCompany();
string companyDomainName = (string)companyData[0];
int numberOfEmployees = (int)companyData[1];
int newNumberOfEmployees = user.ChangeEmail(
newEmail, companyDomainName, numberOfEmployees);
_database.SaveCompany(newNumberOfEmployees);
_database.SaveUser(user);
_messageBus.SendEmailChangedMessage(userId, newEmail);
}
}
This is a good first try; the application service helped offload the work with out-of-
process dependencies from the User class. But there are some issues with this imple-
mentation:
The out-of-process dependencies (Database and MessageBus) are instantiated
directly, not injected. That’s going to be a problem for the integration tests we’ll
be writing for this class.
The controller reconstructs a User instance from the raw data it receives from
the database. This is complex logic and thus shouldn’t belong to the applica-
tion service, whose sole role is orchestration, not logic of any complexity or
domain significance.
The same is true for the company’s data. The other problem with that data is
that User now returns an updated number of employees, which doesn’t look
right. The number of company employees has nothing to do with a specific
user. This responsibility should belong elsewhere.
The controller persists modified data and sends notifications to the message
bus unconditionally, regardless of whether the new email is different than the
previous one.
The User class has become quite easy to test because it no longer has to communicate
with out-of-process dependencies. In fact, it has no collaborators whatsoever—out-of-
process or not. Here’s the new version of User’s ChangeEmail method:
Listing 7.2
Application service, version 1


---
**Page 162**

162
CHAPTER 7
Refactoring toward valuable unit tests
public int ChangeEmail(string newEmail,
string companyDomainName, int numberOfEmployees)
{
if (Email == newEmail)
return numberOfEmployees;
string emailDomain = newEmail.Split('@')[1];
bool isEmailCorporate = emailDomain == companyDomainName;
UserType newType = isEmailCorporate
? UserType.Employee
: UserType.Customer;
if (Type != newType)
{
int delta = newType == UserType.Employee ? 1 : -1;
int newNumber = numberOfEmployees + delta;
numberOfEmployees = newNumber;
}
Email = newEmail;
Type = newType;
return numberOfEmployees;
}
Figure 7.8 shows where User and UserController currently stand in our diagram.
User has moved to the domain model quadrant, close to the vertical axis, because it
no longer has to deal with collaborators. UserController is more problematic.
Although I’ve put it into the controllers quadrant, it almost crosses the boundary into
overcomplicated code because it contains logic that is quite complex. 
Domain model,
algorithms
Overcomplicated
code
Trivial code
Controllers
Complexity,
domain
signiﬁcance
Number of
collaborators
UserController
User
Figure 7.8
Take 2 puts User in the domain model quadrant, close to the vertical 
axis. UserController almost crosses the boundary with the overcomplicated 
quadrant because it contains complex logic.


---
**Page 163**

163
Refactoring toward valuable unit tests
7.2.4
Take 3: Removing complexity from the application service
To put UserController firmly into the controllers quadrant, we need to extract the
reconstruction logic from it. If you use an object-relational mapping (ORM) library
to map the database into the domain model, that would be a good place to which to
attribute the reconstruction logic. Each ORM library has a dedicated place where you
can specify how your database tables should be mapped to domain classes, such as
attributes on top of those domain classes, XML files, or files with fluent mappings.
 If you don’t want to or can’t use an ORM, create a factory in the domain model
that will instantiate the domain classes using raw database data. This factory can be a
separate class or, for simpler cases, a static method in the existing domain classes. The
reconstruction logic in our sample application is not too complicated, but it’s good to
keep such things separated, so I’m putting it in a separate UserFactory class as shown
in the following listing.
public class UserFactory
{
public static User Create(object[] data)
{
Precondition.Requires(data.Length >= 3);
int id = (int)data[0];
string email = (string)data[1];
UserType type = (UserType)data[2];
return new User(id, email, type);
}
}
This code is now fully isolated from all collaborators and therefore easily testable.
Notice that I’ve put a safeguard in this method: a requirement to have at least three
elements in the data array. Precondition is a simple custom class that throws an
exception if the Boolean argument is false. The reason for this class is the more
succinct code and the condition inversion: affirmative statements are more read-
able than negative ones. In our example, the data.Length >= 3 requirement reads
better than
if (data.Length < 3)
throw new Exception();
Note that while this reconstruction logic is somewhat complex, it doesn’t have domain
significance: it isn’t directly related to the client’s goal of changing the user email. It’s
an example of the utility code I refer to in previous chapters.
 
Listing 7.3
User factory


