# 4.5.7 Tooling support (pp.114-114)

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


