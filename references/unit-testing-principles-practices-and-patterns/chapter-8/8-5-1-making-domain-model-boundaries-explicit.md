# 8.5.1 Making domain model boundaries explicit (pp.200-200)

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


