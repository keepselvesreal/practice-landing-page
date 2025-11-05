# 8.4.1 Interfaces and loose coupling (pp.198-199)

---
**Page 198**

198
CHAPTER 8
Why integration testing?
8.4.1
Interfaces and loose coupling
Many developers introduce interfaces for out-of-process dependencies, such as the
database or the message bus, even when these interfaces have only one implementation.
This practice has become so widespread nowadays that hardly anyone questions it.
You’ll often see class-interface pairs similar to the following:
public interface IMessageBus
public class MessageBus : IMessageBus
public interface IUserRepository
public class UserRepository : IUserRepository
The common reasoning behind the use of such interfaces is that they help to
Abstract out-of-process dependencies, thus achieving loose coupling
Add new functionality without changing the existing code, thus adhering to the
Open-Closed principle (OCP)
Both of these reasons are misconceptions. Interfaces with a single implementation are
not abstractions and don’t provide loose coupling any more than concrete classes that
implement those interfaces. Genuine abstractions are discovered, not invented. The dis-
covery, by definition, takes place post factum, when the abstraction already exists but
is not yet clearly defined in the code. Thus, for an interface to be a genuine abstrac-
tion, it must have at least two implementations.
 The second reason (the ability to add new functionality without changing the exist-
ing code) is a misconception because it violates a more foundational principle:
YAGNI. YAGNI stands for “You aren’t gonna need it” and advocates against investing
time in functionality that’s not needed right now. You shouldn’t develop this function-
ality, nor should you modify your existing code to account for the appearance of such
functionality in the future. The two major reasons are as follows:
Opportunity cost—If you spend time on a feature that business people don’t need
at the moment, you steer that time away from features they do need right now.
Moreover, when the business people finally come to require the developed func-
tionality, their view on it will most likely have evolved, and you will still need to
adjust the already-written code. Such activity is wasteful. It’s more beneficial to
implement the functionality from scratch when the actual need for it emerges.
The less code in the project, the better. Introducing code just in case without an imme-
diate need unnecessarily increases your code base’s cost of ownership. It’s bet-
ter to postpone introducing new functionality until as late a stage of your
project as possible.
TIP
Writing code is an expensive way to solve problems. The less code the
solution requires and the simpler that code is, the better.
There are exceptional cases where YAGNI doesn’t apply, but these are few and far
between. For those cases, see my article “OCP vs YAGNI,” at https://enterprise-
craftsmanship.com/posts/ocp-vs-yagni. 


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


