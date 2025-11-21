# 4.5.3 Asserts and exceptions: When to use one or the other (pp.112-113)

---
**Page 112**

112
CHAPTER 4
Designing contracts
computational power to check it at both input-validation time and contract-checking
time. Again, consider the context to decide what works best for each situation.
NOTE
Arie van Deursen offers a clear answer on Stack Overflow about the
differences between design-by-contract and validation, and I strongly recom-
mend that you check it out: https://stackoverflow.com/a/5452329. 
4.5.3
Asserts and exceptions: When to use one or the other
Java does not offer a clear mechanism for expressing code contracts. Only a few
popular programming languages do, such as F#. The assert keyword in Java is okay,
but if you forget to enable it in the runtime, the contracts may not be checked in
production. That is why many developers prefer to use (checked or unchecked)
exceptions.
 Here is my rule of thumb:
If I am modeling the contracts of a library or utility class, I favor exceptions, fol-
lowing the wisdom of the most popular libraries.
If I am modeling business classes and their interactions and I know that the
data was cleaned up in previous layers (say, in the controller of a Model-View-
Controller [MVC] architecture), I favor assertions. The data was already vali-
dated, and I am sure they start their work with valid data. I do not expect pre-
conditions or post-conditions to be violated, so I prefer to use the assert
instruction. It will throw an AssertionError, which will halt execution. I also
ensure that my final user does not see an exception stack trace but instead is
shown a more elegant error page.
If I am modeling business classes but I am not sure whether the data was already
cleaned up, I go for exceptions.
Input validation
Input
data
User
Bad input values that come from the
user do not get to the main classes.
Instead, a message is displayed, and
the user tries again.
If a class makes a bad call to another class, e.g., a pre-condition violation,
the program halts, as this should not happen. The user may also be informed
about the problem, although commonly with a more generic message.
Class B
Class A
Class C
Figure 4.3
The difference between validation and code contracts. Each 
circle represents one input coming to the system.


---
**Page 113**

113
Design-by-contract in the real world
When it comes to validation, I tend not to use either assertions or exceptions. I prefer
to model validations in more elegant ways. First, you rarely want to stop the validation
when the first check fails. Instead, it is more common to show a complete list of errors
to the user. Therefore, you need a structure that allows you to build the error message
as you go. Second, you may want to model complex validations, which may require
lots of code. Having all the validations in a single class or method may lead to code
that is very long, highly complex, and hard to reuse.
 If you are curious, I suggest the Specification pattern proposed by Eric Evans in his
seminal book, Domain-Driven Design (2004). Another nice resource is the article “Use
of Assertions” by John Regehr (2014); it discusses the pros and cons of assertions, mis-
conceptions, and limitations in a very pragmatic way.
 Finally, in this chapter, I used native Java exceptions, such as RuntimeException. In
practice, you may prefer to throw more specialized and semantic exceptions, such as
NegativeValueException. That helps clients treat business exceptions differently
from real one-in-a-million exceptional behavior.
NOTE
Formal semantics scholars do not favor the use of assertions over
exceptions. I should not use the term design-by-contract for the snippets where I
use an if statement and throw an exception—that is defensive programming.
But, as I said before, I am using the term design-by-contract for the idea of
reflecting about contracts and somehow making them explicit in the code. 
4.5.4
Exception or soft return values?
We saw that a possible way to simplify clients’ lives is to make your method return a
“soft value” instead of throwing an exception. Go back to listing 4.5 for an example.
 My rule of thumb is the following:
If it is behavior that should not happen, and clients would not know what to do
with it, I throw an exception. That would be the case with the calculateTax
method. If a negative value comes in, that is unexpected behavior, and we
should halt the program rather than let it make bad calculations. The monitor-
ing systems will catch the exception, and we will debug the case.
On the other hand, if I can see a soft return for the client method that would allow
the client to keep working, I go for it. Imagine a utility method that trims a string.
A pre-condition of this method could be that it does not accept null strings. But
returning an empty string in case of a null is a soft return that clients can deal with. 
4.5.5
When not to use design-by-contract
Understanding when not to use a practice is as important as knowing when to use it.
In this case, I may disappoint you, as I cannot see a single good reason not to use the
design-by-contract ideas presented in this chapter. The development of object-oriented
systems is all about ensuring that objects can communicate and collaborate properly.
Experience shows me that making the pre-conditions, post-conditions, and invari-
ants explicit in the code is not expensive and does not take a lot of time. Therefore,


