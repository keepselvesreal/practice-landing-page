# 7.6 Summary (pp.180-185)

---
**Page 180**

180
CHAPTER 7
Refactoring toward valuable unit tests
these method calls (which is the topic of the next chapter). However, the subsequent
call from the controller to User doesn’t have an immediate connection to the goals of
the external client. That client doesn’t care how the controller decides to implement
the change of email as long as the final state of the system is correct and the call to the
message bus is in place. Therefore, you shouldn’t verify calls the controller makes to
User when testing that controller’s behavior.
 When you step one level down the call stack, you get a similar situation. Now it’s
the controller who is the client, and the ChangeEmail method in User has an immedi-
ate connection to that client’s goal of changing the user email and thus should be
tested. But the subsequent calls from User to Company are implementation details
from the controller’s point of view. Therefore, the test that covers the ChangeEmail
method in User shouldn’t verify what methods User calls on Company. The same line
of reasoning applies when you step one more level down and test the two methods in
Company from User’s point of view.
 Think of the observable behavior and implementation details as onion layers. Test
each layer from the outer layer’s point of view, and disregard how that layer talks to
the underlying layers. As you peel these layers one by one, you switch perspective:
what previously was an implementation detail now becomes an observable behavior,
which you then cover with another set of tests. 
Summary
Code complexity is defined by the number of decision-making points in the
code, both explicit (made by the code itself) and implicit (made by the libraries
the code uses).
Domain significance shows how significant the code is for the problem domain
of your project. Complex code often has high domain significance and vice
versa, but not in 100% of all cases.
Complex code and code that has domain significance benefit from unit test-
ing the most because the corresponding tests have greater protection against
regressions.
Unit tests that cover code with a large number of collaborators have high
maintenance costs. Such tests require a lot of space to bring collaborators to
an expected condition and then check their state or interactions with them
afterward.
All production code can be categorized into four types of code by its complexity
or domain significance and the number of collaborators:
– Domain model and algorithms (high complexity or domain significance, few
collaborators) provide the best return on unit testing efforts.
– Trivial code (low complexity and domain significance, few collaborators)
isn’t worth testing at all.


---
**Page 181**

181
Summary
– Controllers (low complexity and domain significance, large number of col-
laborators) should be tested briefly by integration tests.
– Overcomplicated code (high complexity or domain significance, large num-
ber of collaborators) should be split into controllers and complex code.
The more important or complex the code is, the fewer collaborators it should
have.
The Humble Object pattern helps make overcomplicated code testable by
extracting business logic out of that code into a separate class. As a result, the
remaining code becomes a controller—a thin, humble wrapper around the busi-
ness logic.
The hexagonal and functional architectures implement the Humble Object
pattern. Hexagonal architecture advocates for the separation of business logic and
communications with out-of-process dependencies. Functional architecture sepa-
rates business logic from communications with all collaborators, not just out-of-
process ones.
Think of the business logic and orchestration responsibilities in terms of code
depth versus code width. Your code can be either deep (complex or important)
or wide (work with many collaborators), but never both.
Test preconditions if they have a domain significance; don’t test them otherwise.
There are three important attributes when it comes to separating business logic
from orchestration:
– Domain model testability—A function of the number and the type of collabora-
tors in domain classes
– Controller simplicity—Depends on the presence of decision-making points in
the controller
– Performance—Defined by the number of calls to out-of-process dependencies
You can have a maximum of two of these three attributes at any given moment:
– Pushing all external reads and writes to the edges of a business operation—Preserves
controller simplicity and keeps the domain model testability, but concedes
performance
– Injecting out-of-process dependencies into the domain model—Keeps performance
and the controller’s simplicity, but damages domain model testability
– Splitting the decision-making process into more granular steps—Preserves perfor-
mance and domain model testability, but gives up controller simplicity
Splitting the decision-making process into more granular steps—Is a trade-off with the
best set of pros and cons. You can mitigate the growth of controller complexity
using the following two patterns:
– The CanExecute/Execute pattern introduces a CanDo() for each Do() method
and makes its successful execution a precondition for Do(). This pattern
essentially eliminates the controller’s decision-making because there’s no
option not to call CanDo() before Do().


---
**Page 182**

182
CHAPTER 7
Refactoring toward valuable unit tests
– Domain events help track important changes in the domain model, and then
convert those changes to calls to out-of-process dependencies. This pattern
removes the tracking responsibility from the controller.
It’s easier to test abstractions than the things they abstract. Domain events are
abstractions on top of upcoming calls to out-of-process dependencies. Changes
in domain classes are abstractions on top of upcoming modifications in the
data storage.


---
**Page 183**

Part 3
Integration testing
Have you ever been in a situation where all the unit tests pass but the
application still doesn’t work? Validating software components in isolation from
each other is important, but it’s equally important to check how those compo-
nents work in integration with external systems. This is where integration testing
comes into play.
 In chapter 8, we’ll look at integration testing in general and revisit the Test
Pyramid concept. You’ll learn the trade-offs inherent to integration testing and
how to navigate them. Chapters 9 and 10 will then discuss more specific topics.
Chapter 9 will teach you how to get the most out of your mocks. Chapter 10 is a
deep dive into working with relational databases in tests.


---
**Page 184**

 


---
**Page 185**

185
Why integration testing?
You can never be sure your system works as a whole if you rely on unit tests exclu-
sively. Unit tests are great at verifying business logic, but it’s not enough to check
that logic in a vacuum. You have to validate how different parts of it integrate with
each other and external systems: the database, the message bus, and so on.
 In this chapter, you’ll learn the role of integration tests: when you should apply
them and when it’s better to rely on plain old unit tests or even other techniques
such as the Fail Fast principle. You will see which out-of-process dependencies to
use as-is in integration tests and which to replace with mocks. You will also see inte-
gration testing best practices that will help improve the health of your code base in
general: making domain model boundaries explicit, reducing the number of layers
in the application, and eliminating circular dependencies. Finally, you’ll learn why
interfaces with a single implementation should be used sporadically, and how and
when to test logging functionality.
This chapter covers
Understanding the role of integration testing
Diving deeper into the Test Pyramid concept
Writing valuable integration tests


