# 8.5.3 Eliminating circular dependencies (pp.202-204)

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


---
**Page 203**

203
Integration testing best practices
/* other code */
}
}
public class ReportGenerationService
{
public void GenerateReport(
int orderId,
CheckOutService checkOutService)
{
/* calls checkOutService when generation is completed */
}
}
Here, CheckOutService creates an instance of ReportGenerationService and passes
itself to that instance as an argument. ReportGenerationService calls CheckOut-
Service back to notify it about the result of the report generation.
 Just like an excessive number of abstraction layers, circular dependencies add tre-
mendous cognitive load when you try to read and understand the code. The reason is
that circular dependencies don’t give you a clear starting point from which you can
begin exploring the solution. To understand just one class, you have to read and
understand the whole graph of its siblings all at once. Even a small set of interdepen-
dent classes can quickly become too hard to grasp.
 Circular dependencies also interfere with testing. You often have to resort to inter-
faces and mocking in order to split the class graph and isolate a single unit of behav-
ior, which, again, is a no-go when it comes to testing the domain model (more on that
in chapter 5).
 Note that the use of interfaces only masks the problem of circular dependencies. If
you introduce an interface for CheckOutService and make ReportGenerationService
depend on that interface instead of the concrete class, you remove the circular depen-
dency at compile time (figure 8.11), but the cycle still persists at runtime. Even
though the compiler no longer regards this class composition as a circular reference,
the cognitive load required to understand the code doesn’t become any smaller. If
anything, it increases due to the additional interface.
CheckOutService
ICheckOutService
ReportGenerationService
Figure 8.11
With an interface, you remove the circular dependency 
at compile time, but not at runtime. The cognitive load required to 
understand the code doesn’t become any smaller.


---
**Page 204**

204
CHAPTER 8
Why integration testing?
A better approach to handle circular dependencies is to get rid of them. Refactor
ReportGenerationService such that it depends on neither CheckOutService nor the
ICheckOutService interface, and make ReportGenerationService return the result
of its work as a plain value instead of calling CheckOutService:
public class CheckOutService
{
public void CheckOut(int orderId)
{
var service = new ReportGenerationService();
Report report = service.GenerateReport(orderId);
/* other work */
}
}
public class ReportGenerationService
{
public Report GenerateReport(int orderId)
{
/* ... */
}
}
It’s rarely possible to eliminate all circular dependencies in your code base. But even
then, you can minimize the damage by making the remaining graphs of interdepen-
dent classes as small as possible. 
8.5.4
Using multiple act sections in a test
As you might remember from chapter 3, having more than one arrange, act, or assert
section in a test is a code smell. It’s a sign that this test checks multiple units of behav-
ior, which, in turn, hinders the test’s maintainability. For example, if you have two
related use cases—say, user registration and user deletion—it might be tempting to
check both of these use cases in a single integration test. Such a test could have the
following structure:
Arrange—Prepare data with which to register a user.
Act—Call UserController.RegisterUser().
Assert—Query the database to see if the registration is completed successfully.
Act—Call UserController.DeleteUser().
Assert—Query the database to make sure the user is deleted.
This approach is compelling because the user states naturally flow from one another,
and the first act (registering a user) can simultaneously serve as an arrange phase for
the subsequent act (user deletion). The problem is that such tests lose focus and can
quickly become too bloated.
 It’s best to split the test by extracting each act into a test of its own. It may seem like
unnecessary work (after all, why create two tests where one would suffice?), but this


