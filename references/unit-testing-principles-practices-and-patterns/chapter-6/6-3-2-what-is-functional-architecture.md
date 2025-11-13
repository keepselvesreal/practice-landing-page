# 6.3.2 What is functional architecture? (pp.132-133)

---
**Page 132**

132
CHAPTER 6
Styles of unit testing
6.3.2
What is functional architecture?
You can’t create an application that doesn’t incur any side effects whatsoever, of
course. Such an application would be impractical. After all, side effects are what you
create all applications for: updating the user’s information, adding a new order line to
the shopping cart, and so on.
 The goal of functional programming is not to eliminate side effects altogether but
rather to introduce a separation between code that handles business logic and code
that incurs side effects. These two responsibilities are complex enough on their own;
mixing them together multiplies the complexity and hinders code maintainability in
the long run. This is where functional architecture comes into play. It separates busi-
ness logic from side effects by pushing those side effects to the edges of a business operation.
DEFINITION
Functional architecture maximizes the amount of code written in a
purely functional (immutable) way, while minimizing code that deals with
side effects. Immutable means unchangeable: once an object is created, its
state can’t be modified. This is in contrast to a mutable object (changeable
object), which can be modified after it is created.
The separation between business logic and side effects is done by segregating two
types of code:
Code that makes a decision—This code doesn’t require side effects and thus can
be written using mathematical functions.
Code that acts upon that decision—This code converts all the decisions made by
the mathematical functions into visible bits, such as changes in the database or
messages sent to a bus.
The code that makes decisions is often referred to as a functional core (also known as an
immutable core). The code that acts upon those decisions is a mutable shell (figure 6.9).
Input
Decisions
Functional core
Mutable shell
Figure 6.9
In functional architecture, 
the functional core is implemented using 
mathematical functions and makes all 
decisions in the application. The mutable 
shell provides the functional core with 
input data and interprets its decisions by 
applying side effects to out-of-process 
dependencies such as a database.


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


