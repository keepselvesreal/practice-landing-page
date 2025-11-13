# 4.5.4 Exception or soft return values? (pp.113-113)

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


