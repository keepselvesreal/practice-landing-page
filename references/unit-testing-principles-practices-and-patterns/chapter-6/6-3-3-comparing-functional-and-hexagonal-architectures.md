# 6.3.3 Comparing functional and hexagonal architectures (pp.133-135)

---
**Page 133**

133
Understanding functional architecture
The functional core and the mutable shell cooperate in the following way:
The mutable shell gathers all the inputs.
The functional core generates decisions.
The shell converts the decisions into side effects.
To maintain a proper separation between these two layers, you need to make sure the
classes representing the decisions contain enough information for the mutable shell
to act upon them without additional decision-making. In other words, the mutable
shell should be as dumb as possible. The goal is to cover the functional core exten-
sively with output-based tests and leave the mutable shell to a much smaller number of
integration tests.
6.3.3
Comparing functional and hexagonal architectures
There are a lot of similarities between functional and hexagonal architectures. Both
of them are built around the idea of separation of concerns. The details of that sepa-
ration vary, though.
 As you may remember from chapter 5, the hexagonal architecture differentiates
the domain layer and the application services layer (figure 6.10). The domain layer is
accountable for business logic while the application services layer, for communication with
Encapsulation and immutability
Like encapsulation, functional architecture (in general) and immutability (in particular)
serve the same goal as unit testing: enabling sustainable growth of your software
project. In fact, there’s a deep connection between the concepts of encapsulation
and immutability.
As you may remember from chapter 5, encapsulation is the act of protecting your
code against inconsistencies. Encapsulation safeguards the class’s internals from
corruption by
Reducing the API surface area that allows for data modification
Putting the remaining APIs under scrutiny
Immutability tackles this issue of preserving invariants from another angle. With
immutable classes, you don’t need to worry about state corruption because it’s impos-
sible to corrupt something that cannot be changed in the first place. As a conse-
quence, there’s no need for encapsulation in functional programming. You only need
to validate the class’s state once, when you create an instance of it. After that, you
can freely pass this instance around. When all your data is immutable, the whole set
of issues related to the lack of encapsulation simply vanishes.
There’s a great quote from Michael Feathers in that regard:
Object-oriented programming makes code understandable by encapsulating mov-
ing parts. Functional programming makes code understandable by minimizing
moving parts.


---
**Page 134**

134
CHAPTER 6
Styles of unit testing
external applications such as a database or an SMTP service. This is very similar to func-
tional architecture, where you introduce the separation of decisions and actions.
 Another similarity is the one-way flow of dependencies. In the hexagonal architec-
ture, classes inside the domain layer should only depend on each other; they should
not depend on classes from the application services layer. Likewise, the immutable
core in functional architecture doesn’t depend on the mutable shell. It’s self-sufficient
and can work in isolation from the outer layers. This is what makes functional archi-
tecture so testable: you can strip the immutable core from the mutable shell entirely
and simulate the inputs that the shell provides using simple values.
 The difference between the two is in their treatment of side effects. Functional
architecture pushes all side effects out of the immutable core to the edges of a busi-
ness operation. These edges are handled by the mutable shell. On the other hand, the
hexagonal architecture is fine with side effects made by the domain layer, as long as
they are limited to that domain layer only. All modifications in hexagonal architecture
should be contained within the domain layer and not cross that layer’s boundary. For
example, a domain class instance can’t persist something to the database directly, but
it can change its own state. An application service will then pick up this change and
apply it to the database.
NOTE
Functional architecture is a subset of the hexagonal architecture. You
can view functional architecture as the hexagonal architecture taken to an
extreme. 
Domain
(business logic)
Application
services
Third-party
system
Message
bus
SMTP
service
Figure 6.10
Hexagonal architecture is a set of interacting 
applications—hexagons. Your application consists of a domain 
layer and an application services layer, which correspond to a 
functional core and a mutable shell in functional architecture.


---
**Page 135**

135
Transitioning to functional architecture and output-based testing
6.4
Transitioning to functional architecture and output-
based testing
In this section, we’ll take a sample application and refactor it toward functional archi-
tecture. You’ll see two refactoring stages:
Moving from using an out-of-process dependency to using mocks
Moving from using mocks to using functional architecture
The transition affects test code, too! We’ll refactor state-based and communication-
based tests to the output-based style of unit testing. Before starting the refactoring,
let’s review the sample project and tests covering it.
6.4.1
Introducing an audit system
The sample project is an audit system that keeps track of all visitors in an organization.
It uses flat text files as underlying storage with the structure shown in figure 6.11. The
system appends the visitor’s name and the time of their visit to the end of the most
recent file. When the maximum number of entries per file is reached, a new file with
an incremented index is created.
The following listing shows the initial version of the system.
public class AuditManager
{
private readonly int _maxEntriesPerFile;
private readonly string _directoryName;
public AuditManager(int maxEntriesPerFile, string directoryName)
{
_maxEntriesPerFile = maxEntriesPerFile;
_directoryName = directoryName;
}
Listing 6.8
Initial implementation of the audit system
Jane;
Jack;
Peter; 2019-04-06T16:30:00
2019-04-06T16:40:00
2019-04-06T17:00:00
Mary;
2019-04-06T17:30:00
New Person; Time of visit
audit_01.txt
audit_02.txt
Figure 6.11
The audit system stores information 
about visitors in text files with a specific format. 
When the maximum number of entries per file is 
reached, the system creates a new file.


