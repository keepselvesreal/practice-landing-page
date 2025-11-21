# 4.5.5 When not to use design-by-contract (pp.113-114)

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


---
**Page 114**

114
CHAPTER 4
Designing contracts
I recommend that you consider using this approach. (Note that I am not discussing
input validation here, which is fundamental and has to be done whether or not you
like design-by-contracts.)
 I also want to highlight that design-by-contract does not replace the need for test-
ing. Why? Because, to the best of my knowledge and experience, you cannot express all
the expected behavior of a piece of code solely with pre-conditions, post-conditions, and
invariants. In practice, I suggest that you design contracts to ensure that classes can
communicate with each other without fear, and test to ensure that the behavior of the
class is correct. 
4.5.6
Should we write tests for pre-conditions, post-conditions, 
and invariants?
In a way, assertions, pre-conditions, post-conditions, and invariant checks test the pro-
duction code from the inside. Do we also need to write (unit) tests for them?
 To answer this question, let me again discuss the difference between validation and
pre-conditions. Validation is what you do to ensure that the data is valid. Pre-conditions
explicitly state under what conditions a method can be invoked.
 I usually write automated tests for validation. We want to ensure that our validation
mechanisms are in place and working as expected. On the other hand, I rarely write
tests for assertions. They are naturally covered by tests that focus on other business
rules. I suggest reading Arie van Deursen’s answer on Stack Overflow about writing
tests for assertions (https://stackoverflow.com/a/6486294/165292).
NOTE
Some code coverage tools do not handle asserts well. JaCoCo, for
example, cannot report full branch coverage in assertions. This is another
great example of why you should not use coverage numbers blindly. 
4.5.7
Tooling support
There is more and more support for pre- and post-condition checks, even in languages
like Java. For instance, IntelliJ, a famous Java IDE, offers the @Nullable and @NotNull
annotations (http://mng.bz/QWMe). You can annotate your methods, attributes, or
return values with them, and IntelliJ will alert you about possible violations. IntelliJ can
even transform those annotations into proper assert checks at compile time.
 In addition, projects such as Bean Validation (https://beanvalidation.org) enable
you to write more complex validations, such as “this string should be an email” or “this
integer should be between 1 and 10.” I appreciate such useful tools that help us
ensure the quality of our products. The more, the merrier. 
Exercises
4.1
Which of the following is a valid reason to use assertions in your code?
A To verify expressions with side effects
B To handle exceptional cases in the program


