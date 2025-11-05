# 5.2.4 Leaking implementation details: An example with state (pp.104-106)

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


---
**Page 105**

105
Observable behavior vs. implementation details
new FooterRenderer()
};
}
public string Render(Message message)
{
return SubRenderers
.Select(x => x.Render(message))
.Aggregate("", (str1, str2) => str1 + str2);
}
}
The sub-renderers collection is public. But is it part of observable behavior? Assuming
that the client’s goal is to render an HTML message, the answer is no. The only class
member such a client would need is the Render method itself. Thus SubRenderers is
also a leaking implementation detail.
 I bring up this example again for a reason. As you may remember, I used it to illus-
trate a brittle test. That test was brittle precisely because it was tied to this implementa-
tion detail—it checked to see the collection’s composition. The brittleness was fixed by
re-targeting the test at the Render method. The new version of the test verified the result-
ing message—the only output the client code cared about, the observable behavior.
 As you can see, there’s an intrinsic connection between good unit tests and a well-
designed API. By making all implementation details private, you leave your tests no
choice other than to verify the code’s observable behavior, which automatically
improves their resistance to refactoring.
TIP
Making the API well-designed automatically improves unit tests.
Another guideline flows from the definition of a well-designed API: you should expose
the absolute minimum number of operations and state. Only code that directly helps
clients achieve their goals should be made public. Everything else is implementation
details and thus must be hidden behind the private API.
 Note that there’s no such problem as leaking observable behavior, which would be
symmetric to the problem of leaking implementation details. While you can expose an
implementation detail (a method or a class that is not supposed to be used by the cli-
ent), you can’t hide an observable behavior. Such a method or class would no longer
have an immediate connection to the client goals, because the client wouldn’t be able
to directly use it anymore. Thus, by definition, this code would cease to be part of
observable behavior. Table 5.1 sums it all up.
Table 5.1
The relationship between the code’s publicity and purpose. Avoid making implementation
details public.
Observable behavior
Implementation detail
Public
Good
Bad
Private
N/A
Good 


---
**Page 106**

106
CHAPTER 5
Mocks and test fragility
5.3
The relationship between mocks and test fragility
The previous sections defined a mock and showed the difference between observable
behavior and an implementation detail. In this section, you will learn about hexago-
nal architecture, the difference between internal and external communications, and
(finally!) the relationship between mocks and test fragility.
5.3.1
Defining hexagonal architecture
A typical application consists of two layers, domain and application services, as
shown in figure 5.8. The domain layer resides in the middle of the diagram because
it’s the central part of your application. It contains the business logic: the essential
functionality your application is built for. The domain layer and its business logic
differentiate this application from others and provide a competitive advantage for
the organization.
The application services layer sits on top of the domain layer and orchestrates com-
munication between that layer and the external world. For example, if your applica-
tion is a RESTful API, all requests to this API hit the application services layer first.
This layer then coordinates the work between domain classes and out-of-process
dependencies. Here’s an example of such coordination for the application service. It
does the following:
Queries the database and uses the data to materialize a domain class instance
Invokes an operation on that instance
Saves the results back to the database
The combination of the application services layer and the domain layer forms a hexa-
gon, which itself represents your application. It can interact with other applications,
which are represented with their own hexagons (see figure 5.9). These other applica-
tions could be an SMTP service, a third-party system, a message bus, and so on. A set
of interacting hexagons makes up a hexagonal architecture.
 
Domain
(business logic)
Application
services
Figure 5.8
A typical application consists of a 
domain layer and an application services layer. 
The domain layer contains the application’s 
business logic; application services tie that 
logic to business use cases.


