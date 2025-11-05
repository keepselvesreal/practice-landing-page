# 4.6 Exercises (pp.114-116)

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


---
**Page 115**

115
Exercises
C To conduct user input validation
D To make debugging easier
4.2
Consider the following squareAt method:
public Square squareAt(int x, int y){
   assert x >= 0;
   assert x < board.length;
   assert y >= 0;
   assert y < board[x].length;
   assert board != null;
   Square result = board[x][y];
   assert result != null;
   return result;
}
Suppose we remove the last assertion (assert result != null), which states
that the result can never be null. Are the existing pre-conditions of the
squareAt method enough to ensure the property of the removed assertion?
What can we add to the class (other than the just-removed post-condition) to
guarantee this property?
4.3
See the squareAt method in exercise 4.3. Which assertion(s), if any, can be
turned into class invariants? Choose all that apply.
A
x >= 0 and x < board.length
B
board != null
C
result != null
D
y >= 0 and y < board[x].length
4.4
You run your application with assertion checking enabled. Unfortunately, it
reports an assertion failure, signaling a class invariant violation in one of the
libraries your application uses. Assume that your application is following all the
pre-conditions established by the library.
Which of the following statements best characterizes the situation and corre-
sponding action to take?
A Since you assume that the contract is correct, the safe action is to run the
server with assertion checking disabled.
B This indicates an integration fault and requires a redesign that involves
the interface that is offered by the library and used by your application.
C This indicates a problem in the implementation of that library and
requires a fix in the library’s code.
D This indicates that you invoked one of the methods of the library in the
wrong way and requires a fix in your application.
4.5
Can static methods have invariants? Explain your answer.


---
**Page 116**

116
CHAPTER 4
Designing contracts
4.6
A method M belongs to a class C and has a pre-condition P and a post-condition
Q. Suppose that a developer creates a class C' that extends C and creates a method
M' that overrides M.
Which one of the following statements correctly explains the relative strength
of the pre- (P') and post-conditions (Q') of the overridden method M'?
A
P' should be equal to or weaker than P, and Q' should be equal to or
stronger than Q.
B
P' should be equal to or stronger than P, and Q' should be equal to or
stronger than Q.
C
P' should be equal to or weaker than P, and Q' should be equal to or
weaker than Q.
D
P' should be equal to or stronger than P, and Q' should be equal to or
weaker than Q.
Summary
Contracts ensure that classes can safely communicate with each other without
surprises.
In practice, designing contracts boils down to explicitly defining the pre-
conditions, post-conditions, and invariants of our classes and methods.
Deciding to go for a weaker or a stronger contract is a contextual decision. Both
have advantages and disadvantages.
Design-by-contract does not remove the need for validation. Validation and con-
tract checking are different things with different objectives. Both should be done.
Whenever changing a contract, we need to reflect on the impact of the change.
Some contract changes might be breaking changes.


