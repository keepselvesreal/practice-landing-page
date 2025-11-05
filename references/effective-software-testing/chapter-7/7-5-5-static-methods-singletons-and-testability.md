# 7.5.5 Static methods, singletons, and testability (pp.194-194)

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
 
 


