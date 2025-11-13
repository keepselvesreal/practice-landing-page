# 8.4.2 Why use interfaces for out-of-process dependencies? (pp.199-199)

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


