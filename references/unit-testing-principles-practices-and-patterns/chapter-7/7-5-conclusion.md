# 7.5 Conclusion (pp.178-180)

---
**Page 178**

178
CHAPTER 7
Refactoring toward valuable unit tests
dispatching them. That topic is outside the scope of this book, though. You can read
about it in my article “Merging domain events before dispatching” at http://mng
.bz/YeVe.
 Domain events remove the decision-making responsibility from the controller and
put that responsibility into the domain model, thus simplifying unit testing communi-
cations with external systems. Instead of verifying the controller itself and using mocks
to substitute out-of-process dependencies, you can test the domain event creation
directly in unit tests, as shown next.
[Fact]
public void Changing_email_from_corporate_to_non_corporate()
{
var company = new Company("mycorp.com", 1);
var sut = new User(1, "user@mycorp.com", UserType.Employee, false);
sut.ChangeEmail("new@gmail.com", company);
company.NumberOfEmployees.Should().Be(0);
sut.Email.Should().Be("new@gmail.com");
sut.Type.Should().Be(UserType.Customer);
sut.EmailChangedEvents.Should().Equal(
   
new EmailChangedEvent(1, "new@gmail.com"));  
}
Of course, you’ll still need to test the controller to make sure it does the orchestration
correctly, but doing so requires a much smaller set of tests. That’s the topic of the next
chapter. 
7.5
Conclusion
Notice a theme that has been present throughout this chapter: abstracting away the
application of side effects to external systems. You achieve such abstraction by keeping
those side effects in memory until the very end of the business operation, so that they
can be tested with plain unit tests without involving out-of-process dependencies.
Domain events are abstractions on top of upcoming messages in the bus. Changes in
domain classes are abstractions on top of upcoming modifications in the database.
NOTE
It’s easier to test abstractions than the things they abstract.
Although we were able to successfully contain all the decision-making in the domain
model with the help of domain events and the CanExecute/Execute pattern, you
won’t be able to always do that. There are situations where business logic fragmenta-
tion is inevitable.
 For example, there’s no way to verify email uniqueness outside the controller with-
out introducing out-of-process dependencies in the domain model. Another example
is failures in out-of-process dependencies that should alter the course of the business
Listing 7.14
Testing the creation of a domain event
Simultaneously asserts 
the collection size and the 
element in the collection


---
**Page 179**

179
Conclusion
operation. The decision about which way to go can’t reside in the domain layer
because it’s not the domain layer that calls those out-of-process dependencies. You will
have to put this logic into controllers and then cover it with integration tests. Still,
even with the potential fragmentation, there’s a lot of value in separating business
logic from orchestration because this separation drastically simplifies the unit test-
ing process.
 Just as you can’t avoid having some business logic in controllers, you will rarely be
able to remove all collaborators from domain classes. And that’s fine. One, two, or
even three collaborators won’t turn a domain class into overcomplicated code, as long
as these collaborators don’t refer to out-of-process dependencies.
 Don’t use mocks to verify interactions with such collaborators, though. These
interactions have nothing to do with the domain model’s observable behavior. Only
the very first call, which goes from a controller to a domain class, has an immediate
connection to that controller’s goal. All the subsequent calls the domain class
makes to its neighbor domain classes within the same operation are implementa-
tion details.
 Figure 7.13 illustrates this idea. It shows the communications between components
in the CRM and their relationship to observable behavior. As you may remember from
chapter 5, whether a method is part of the class’s observable behavior depends on
whom the client is and what the goals of that client are. To be part of the observable
behavior, the method must meet one of the following two criteria:
Have an immediate connection to one of the client’s goals
Incur a side effect in an out-of-process dependency that is visible to external
applications
The controller’s ChangeEmail() method is part of its observable behavior, and so is
the call it makes to the message bus. The first method is the entry point for the exter-
nal client, thereby meeting the first criterion. The call to the bus sends messages to
external applications, thereby meeting the second criterion. You should verify both of
External client
Application
service
(controller)
Message bus
User
Company
Observable behavior
for external client
Observable behavior
for controller
Observable
behavior for user
Figure 7.13
A map that shows communications among components in the CRM and the 
relationship between these communications and observable behavior


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


