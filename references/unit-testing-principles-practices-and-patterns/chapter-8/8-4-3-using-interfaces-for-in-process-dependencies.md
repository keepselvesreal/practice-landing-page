# 8.4.3 Using interfaces for in-process dependencies (pp.199-200)

---
**Page 199**

199
Using interfaces to abstract dependencies
8.4.2
Why use interfaces for out-of-process dependencies?
So, why use interfaces for out-of-process dependencies at all, assuming that each of
those interfaces has only one implementation? The real reason is much more practi-
cal and down-to-earth. It’s to enable mocking—as simple as that. Without an interface,
you can’t create a test double and thus can’t verify interactions between the system
under test and the out-of-process dependency.
 Therefore, don’t introduce interfaces for out-of-process dependencies unless you need to mock
out those dependencies. You only mock out unmanaged dependencies, so the guideline
can be boiled down to this: use interfaces for unmanaged dependencies only. Still inject
managed dependencies into the controller explicitly, but use concrete classes for that.
 Note that genuine abstractions (abstractions that have more than one implementa-
tion) can be represented with interfaces regardless of whether you mock them out.
Introducing an interface with a single implementation for reasons other than mock-
ing is a violation of YAGNI, however.
 And you might have noticed in listing 8.2 that UserController now accepts both
the message bus and the database explicitly via the constructor, but only the message
bus has a corresponding interface. The database is a managed dependency and thus
doesn’t require such an interface. Here’s the controller:
public class UserController
{
private readonly Database _database;   
private readonly IMessageBus _messageBus;    
public UserController(Database database, IMessageBus messageBus)
{
_database = database;
_messageBus = messageBus;
}
public string ChangeEmail(int userId, string newEmail)
{
/* the method uses _database and _messageBus */
}
}
NOTE
You can mock out a dependency without resorting to an interface by
making methods in that dependency virtual and using the class itself as a base
for the mock. This approach is inferior to the one with interfaces, though. I
explain more on this topic of interfaces versus base classes in chapter 11. 
8.4.3
Using interfaces for in-process dependencies
You sometimes see code bases where interfaces back not only out-of-process depen-
dencies but in-process dependencies as well. For example:
public interface IUser
{
int UserId { get; set; }
A concrete 
class
The interface


---
**Page 200**

200
CHAPTER 8
Why integration testing?
string Email { get; }
string CanChangeEmail();
void ChangeEmail(string newEmail, Company company);
}
public class User : IUser
{
/* ... */
}
Assuming that IUser has only one implementation (and such specific interfaces always
have only one implementation), this is a huge red flag. Just like with out-of-process
dependencies, the only reason to introduce an interface with a single implementation
for a domain class is to enable mocking. But unlike out-of-process dependencies, you
should never check interactions between domain classes, because doing so results in
brittle tests: tests that couple to implementation details and thus fail on the metric of
resisting to refactoring (see chapter 5 for more details about mocks and test fragility). 
8.5
Integration testing best practices
There are some general guidelines that can help you get the most out of your integra-
tion tests:
Making domain model boundaries explicit
Reducing the number of layers in the application
Eliminating circular dependencies
As usual, best practices that are beneficial for tests also tend to improve the health of
your code base in general.
8.5.1
Making domain model boundaries explicit
Try to always have an explicit, well-known place for the domain model in your code
base. The domain model is the collection of domain knowledge about the problem your
project is meant to solve. Assigning the domain model an explicit boundary helps you
better visualize and reason about that part of your code.
 This practice also helps with testing. As I mentioned earlier in this chapter, unit
tests target the domain model and algorithms, while integration tests target control-
lers. The explicit boundary between domain classes and controllers makes it easier to
tell the difference between unit and integration tests.
 The boundary itself can take the form of a separate assembly or a namespace. The
particulars aren’t that important as long as all of the domain logic is put under a sin-
gle, distinct umbrella and not scattered across the code base. 
8.5.2
Reducing the number of layers
Most programmers naturally gravitate toward abstracting and generalizing the code
by introducing additional layers of indirection. In a typical enterprise-level applica-
tion, you can easily observe several such layers (figure 8.9).


