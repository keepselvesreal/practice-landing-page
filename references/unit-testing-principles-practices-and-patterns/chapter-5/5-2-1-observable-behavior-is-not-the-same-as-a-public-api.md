# 5.2.1 Observable behavior is not the same as a public API (pp.99-100)

---
**Page 99**

99
Observable behavior vs. implementation details
5.2
Observable behavior vs. implementation details
Section 5.1 showed what a mock is. The next step on the way to explaining the con-
nection between mocks and test fragility is diving into what causes such fragility.
 As you might remember from chapter 4, test fragility corresponds to the second
attribute of a good unit test: resistance to refactoring. (As a reminder, the four attri-
butes are protection against regressions, resistance to refactoring, fast feedback, and
maintainability.) The metric of resistance to refactoring is the most important
because whether a unit test possesses this metric is mostly a binary choice. Thus, it’s
good to max out this metric to the extent that the test still remains in the realm of unit
testing and doesn’t transition to the category of end-to-end testing. The latter, despite
being the best at resistance to refactoring, is generally much harder to maintain.
 In chapter 4, you also saw that the main reason tests deliver false positives (and thus
fail at resistance to refactoring) is because they couple to the code’s implementation
details. The only way to avoid such coupling is to verify the end result the code produces
(its observable behavior) and distance tests from implementation details as much as pos-
sible. In other words, tests must focus on the whats, not the hows. So, what exactly is an
implementation detail, and how is it different from an observable behavior?
5.2.1
Observable behavior is not the same as a public API
All production code can be categorized along two dimensions:
Public API vs. private API (where API means application programming interface)
Observable behavior vs. implementation details 
The categories in these dimensions don’t overlap. A method can’t belong to both a pub-
lic and a private API; it’s either one or the other. Similarly, the code is either an internal
implementation detail or part of the system’s observable behavior, but not both.
 Most programming languages provide a simple mechanism to differentiate between
the code base’s public and private APIs. For example, in C#, you can mark any mem-
ber in a class with the private keyword, and that member will be hidden from the cli-
ent code, becoming part of the class’s private API. The same is true for classes: you can
easily make them private by using the private or internal keyword.
 The distinction between observable behavior and internal implementation details
is more nuanced. For a piece of code to be part of the system’s observable behavior, it
has to do one of the following things:
Expose an operation that helps the client achieve one of its goals. An operation is
a method that performs a calculation or incurs a side effect or both.
Expose a state that helps the client achieve one of its goals. State is the current
condition of the system.
Any code that does neither of these two things is an implementation detail.
 Notice that whether the code is observable behavior depends on who its client is
and what the goals of that client are. In order to be a part of observable behavior, the


---
**Page 100**

100
CHAPTER 5
Mocks and test fragility
code needs to have an immediate connection to at least one such goal. The word client
can refer to different things depending on where the code resides. The common
examples are client code from the same code base, an external application, or the
user interface.
 Ideally, the system’s public API surface should coincide with its observable behav-
ior, and all its implementation details should be hidden from the eyes of the clients.
Such a system has a well-designed API (figure 5.4).
Often, though, the system’s public API extends beyond its observable behavior and
starts exposing implementation details. Such a system’s implementation details leak to
its public API surface (figure 5.5). 
5.2.2
Leaking implementation details: An example with an operation
Let’s take a look at examples of code whose implementation details leak to the public
API. Listing 5.5 shows a User class with a public API that consists of two members: a
Name property and a NormalizeName() method. The class also has an invariant: users’
names must not exceed 50 characters and should be truncated otherwise.
public class User
{
public string Name { get; set; }
Listing 5.5
User class with leaking implementation details
Observable behavior
Public API
Private API
Implementation detail
Figure 5.4
In a well-designed API, the 
observable behavior coincides with the public 
API, while all implementation details are 
hidden behind the private API.
Observable behavior
Public API
Private API
Leaking implementation detail
Figure 5.5
A system leaks implementation 
details when its public API extends beyond 
the observable behavior.


