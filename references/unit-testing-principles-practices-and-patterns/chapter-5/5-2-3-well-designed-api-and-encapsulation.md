# 5.2.3 Well-designed API and encapsulation (pp.103-104)

---
**Page 103**

103
Observable behavior vs. implementation details
NOTE
Strictly speaking, Name’s getter should also be made private, because
it’s not used by UserController. In reality, though, you almost always want to
read back changes you make. Therefore, in a real project, there will certainly be
another use case that requires seeing users’ current names via Name’s getter.
There’s a good rule of thumb that can help you determine whether a class leaks its
implementation details. If the number of operations the client has to invoke on the
class to achieve a single goal is greater than one, then that class is likely leaking imple-
mentation details. Ideally, any individual goal should be achieved with a single operation. In
listing 5.5, for example, UserController has to use two operations from User:
string normalizedName = user.NormalizeName(newName);
user.Name = normalizedName;
After the refactoring, the number of operations has been reduced to one:
user.Name = newName;
In my experience, this rule of thumb holds true for the vast majority of cases where
business logic is involved. There could very well be exceptions, though. Still, be sure
to examine each situation where your code violates this rule for a potential leak of
implementation details. 
5.2.3
Well-designed API and encapsulation
Maintaining a well-designed API relates to the notion of encapsulation. As you might
recall from chapter 3, encapsulation is the act of protecting your code against inconsis-
tencies, also known as invariant violations. An invariant is a condition that should be
held true at all times. The User class from the previous example had one such invari-
ant: no user could have a name that exceeded 50 characters.
 Exposing implementation details goes hand in hand with invariant violations—the
former often leads to the latter. Not only did the original version of User leak its
implementation details, but it also didn’t maintain proper encapsulation. It allowed
the client to bypass the invariant and assign a new name to a user without normalizing
that name first.
Observable behavior
Public API
Normalize
name
Name
Private API
Implementation detail
Figure 5.7
User with a well-designed API. 
Only the observable behavior is public; the 
implementation details are now private.


---
**Page 104**

104
CHAPTER 5
Mocks and test fragility
 Encapsulation is crucial for code base maintainability in the long run. The reason
why is complexity. Code complexity is one of the biggest challenges you’ll face in soft-
ware development. The more complex the code base becomes, the harder it is to work
with, which, in turn, results in slowing down development speed and increasing the
number of bugs.
 Without encapsulation, you have no practical way to cope with ever-increasing
code complexity. When the code’s API doesn’t guide you through what is and what
isn’t allowed to be done with that code, you have to keep a lot of information in mind
to make sure you don’t introduce inconsistencies with new code changes. This brings
an additional mental burden to the process of programming. Remove as much of that
burden from yourself as possible. You cannot trust yourself to do the right thing all the
time—so, eliminate the very possibility of doing the wrong thing. The best way to do so is to
maintain proper encapsulation so that your code base doesn’t even provide an option
for you to do anything incorrectly. Encapsulation ultimately serves the same goal as
unit testing: it enables sustainable growth of your software project.
 There’s a similar principle: tell-don’t-ask. It was coined by Martin Fowler (https://
martinfowler.com/bliki/TellDontAsk.html) and stands for bundling data with the
functions that operate on that data. You can view this principle as a corollary to the
practice of encapsulation. Code encapsulation is a goal, whereas bundling data and
functions together, as well as hiding implementation details, are the means to achieve
that goal:
Hiding implementation details helps you remove the class’s internals from the eyes
of its clients, so there’s less risk of corrupting those internals.
Bundling data and operations helps to make sure these operations don’t violate
the class’s invariants. 
5.2.4
Leaking implementation details: An example with state
The example shown in listing 5.5 demonstrated an operation (the NormalizeName
method) that was an implementation detail leaking to the public API. Let’s also look
at an example with state. The following listing contains the MessageRenderer class you
saw in chapter 4. It uses a collection of sub-renderers to generate an HTML represen-
tation of a message containing a header, a body, and a footer.
public class MessageRenderer : IRenderer
{
public IReadOnlyList<IRenderer> SubRenderers { get; }
public MessageRenderer()
{
SubRenderers = new List<IRenderer>
{
new HeaderRenderer(),
new BodyRenderer(),
Listing 5.7
State as an implementation detail 


