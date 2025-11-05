# 7.5.6 The Hexagonal Architecture and mocks as a design technique (pp.194-195)

---
**Page 194**

194
CHAPTER 7
Designing for testability
7.5.5
Static methods, singletons, and testability
As we have seen, static methods adversely affect testability. Therefore, a good rule of
thumb is to avoid creating static methods whenever possible. Exceptions to this rule are
utility methods, which are often not mocked. If your system has to depend on a specific
static method, perhaps because it comes with the framework your software depends on,
adding an abstraction on top of it—similar to what we did with the LocalDate class in
the previous chapter—may be a good decision to facilitate testability.
 The same recommendation applies when your system needs code from others or
external dependencies. Again, creating layers and classes that abstract away the
dependency may help you increase testability. Don’t be afraid to create these extra lay-
ers: although it may seem that they will increase the overall complexity of the design,
the increased testability pays off.
 Using the Singleton design pattern also harms testability. This approach ensures
that there is only one instance of a class throughout the entire system. Whenever you
need an instance of that class, you ask the singleton, and the singleton returns the
same one. A singleton makes testing difficult because it is like having a global variable
that is persistent throughout the program’s life cycle. When testing software systems
that use singletons, we often have to write extra code in the test suite to reset or
replace the singleton in the different test cases. Singletons also bring other disadvan-
tages to maintainability in general. If you are not familiar with this pattern, I suggest
reading about it. 
7.5.6
The Hexagonal Architecture and mocks as a design technique
Now that you know about the Hexagonal Architecture and the idea of ports and
adapters, we can talk about mocks as a design technique. In a nutshell, whenever
mockists develop a feature (or a domain object) and notice that they need something
from another place, they let a port emerge. As we saw, the port is an interface that
allows the mockist to develop the remainder of the feature without being bothered by
the concrete implementation of the adapter. The mockist takes this as a design activ-
ity: they reflect on the contract that the port should offer to the core of the applica-
tion and model the best interface possible.
 Whenever I am coding a class (or set of classes) and notice that I need something
else, I let an interface emerge that represents this “something else.” I reflect on what the
class under development needs from it, model the best interface, and continue develop-
ing the class. Only later do I implement the concrete adapter. I enjoy this approach as it
lets me focus on the class I am implementing by giving me a way to abstract things that I
do not care about right now, like the implementation of adapters. 
 
 


---
**Page 195**

195
Exercises
7.5.7
Further reading about designing for testability
Entire books can be written about this topic. In fact, entire books have been written
about it:
Michael Feathers’s Working Effectively with Legacy Code (2004) is about working
with legacy systems, but a huge part of it is about untestable code (common in
legacy) and how to make it testable. Feathers also has a nice talk on YouTube
about the “deep synergy between well-designed production code and testabil-
ity,” as he calls it (2013).
Steve Freeman and Nat Pryce’s book Growing-Object Oriented Systems Guided by
Tests (2009) is also a primer for writing classes that are easy to test.
Robert Martin’s Clean Architecture ideas (2018) align with the ideas discussed here. 
Exercises
7.1
Observability and controllability are two important concepts of software testing.
Three developers could benefit from improving either the observability or the
controllability of the system/class they are testing, but each developer encoun-
ters a problem.
State whether each of the problems relates to observability or controllability.
A Developer 1: “I can’t assert whether the method under test worked well.”
B Developer 2: “I need to make sure this class starts with a boolean set to
false, but I can’t do it.”
C Developer 3: “I instantiated the mock object, but there’s no way to inject it
into the class.”
7.2
Sarah has joined a mobile app team that has been trying to write automated
tests for a while. The team wants to write unit tests for part of their code, but
they tell Sarah, “It’s hard.” After some code review, the developers list the fol-
lowing problems in their code base:
A Many classes mix infrastructure and business rules.
B The database has large tables and no indexes.
C There are lots of calls to libraries and external APIs.
D Some classes have too many attributes/fields.
To increase testability, the team has a budget to work on two of these four
issues. Which items should Sarah recommend that they tackle first?
Note: All four issues should be fixed, but try to prioritize the two most
important ones. Which influences testability the most?
7.3
How can you improve the testability of the following OrderDeliveryBatch class?
public class OrderDeliveryBatch {
  public void runBatch() {


