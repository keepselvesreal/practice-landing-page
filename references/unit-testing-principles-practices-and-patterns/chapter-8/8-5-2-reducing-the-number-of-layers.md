# 8.5.2 Reducing the number of layers (pp.200-202)

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


---
**Page 201**

201
Integration testing best practices
In extreme cases, an application gets so many abstraction layers that it becomes too
hard to navigate the code base and understand the logic behind even the simplest
operations. At some point, you just want to get to the specific solution of the problem
at hand, not some generalization of that solution in a vacuum.
All problems in computer science can be solved by another layer of indirection, except for
the problem of too many layers of indirection.
                                                                   
—David J. Wheeler
Layers of indirection negatively affect your ability to reason about the code. When
every feature has a representation in each of those layers, you have to expend signifi-
cant effort assembling all the pieces into a cohesive picture. This creates an additional
mental burden that handicaps the entire development process.
 An excessive number of abstractions doesn’t help unit or integration testing,
either. Code bases with many layers of indirections tend not to have a clear boundary
between controllers and the domain model (which, as you might remember from
chapter 7, is a precondition for effective tests). There’s also a much stronger tendency
to verify each layer separately. This tendency results in a lot of low-value integration
tests, each of which exercises only the code from a specific layer and mocks out layers
Application
services layer
Business logic
implementation layer
Abstractions layer
Persistence layer
Order checkout
Changing user email
Resetting password
Figure 8.9
Various application concerns are often addressed by 
separate layers of indirection. A typical feature takes up a small 
portion of each layer.


---
**Page 202**

202
CHAPTER 8
Why integration testing?
underneath. The end result is always the same: insufficient protection against regres-
sions combined with low resistance to refactoring.
 Try to have as few layers of indirection as possible. In most backend systems, you
can get away with just three: the domain model, application services layer (control-
lers), and infrastructure layer. The infrastructure layer typically consists of algorithms
that don’t belong to the domain model, as well as code that enables access to out-of-
process dependencies (figure 8.10). 
8.5.3
Eliminating circular dependencies
Another practice that can drastically improve the maintainability of your code base
and make testing easier is eliminating circular dependencies.
DEFINITION
A circular dependency (also known as cyclic dependency) is two or
more classes that directly or indirectly depend on each other to function
properly.
A typical example of a circular dependency is a callback:
public class CheckOutService
{
public void CheckOut(int orderId)
{
var service = new ReportGenerationService();
service.GenerateReport(orderId, this);
Application
services layer
Domain layer
Infrastructure layer
Order checkout
Changing user email
Resetting password
Figure 8.10
You can get away with just three layers: the domain layer (contains 
domain logic), application services layers (provides an entry point for the external 
client, and coordinates the work between domain classes and out-of-process 
dependencies), and infrastructure layer (works with out-of-process dependencies; 
database repositories, ORM mappings, and SMTP gateways reside in this layer).


