# 2.1 A Web of Objects (pp.13-13)

---
**Page 13**

Chapter 2
Test-Driven Development with
Objects
Music is the space between the notes.
—Claude Debussy
A Web of Objects
Object-oriented design focuses more on the communication between objects than
on the objects themselves. As Alan Kay [Kay98] wrote:
The big idea is “messaging” […] The key in making great and growable systems is
much more to design how its modules communicate rather than what their internal
properties and behaviors should be.
An object communicates by messages: It receives messages from other objects
and reacts by sending messages to other objects as well as, perhaps, returning a
value or exception to the original sender. An object has a method of handling
every type of message that it understands and, in most cases, encapsulates some
internal state that it uses to coordinate its communication with other objects.
An object-oriented system is a web of collaborating objects. A system is built
by creating objects and plugging them together so that they can send messages
to one another. The behavior of the system is an emergent property of the
composition of the objects—the choice of objects and how they are connected
(Figure 2.1).
This lets us change the behavior of the system by changing the composition of
its objects—adding and removing instances, plugging different combinations
together—rather than writing procedural code. The code we write to manage
this composition is a declarative deﬁnition of the how the web of objects will
behave. It’s easier to change the system’s behavior because we can focus on what
we want it to do, not how.
Values and Objects
When designing a system, it’s important to distinguish between values that
model unchanging quantities or measurements, and objects that have an identity,
might change state over time, and model computational processes. In the
13


