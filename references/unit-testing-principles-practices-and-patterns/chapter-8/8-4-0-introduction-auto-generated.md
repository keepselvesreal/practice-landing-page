# 8.4.0 Introduction [auto-generated] (pp.197-198)

---
**Page 197**

197
Using interfaces to abstract dependencies
// Assert
Assert.Equal("OK", result);
object[] userData = db.GetUserById(user.UserId);   
User userFromDb = UserFactory.Create(userData);    
Assert.Equal("new@gmail.com", userFromDb.Email);   
Assert.Equal(UserType.Customer, userFromDb.Type);  
object[] companyData = db.GetCompany();
   
Company companyFromDb = CompanyFactory
   
.Create(companyData);
   
Assert.Equal(0, companyFromDb.NumberOfEmployees);  
messageBusMock.Verify(
    
x => x.SendEmailChangedMessage(
    
user.UserId, "new@gmail.com"),    
Times.Once);
     
}
TIP
Notice that in the arrange section, the test doesn’t insert the user and
the company into the database on its own but instead calls the CreateUser
and CreateCompany helper methods. These methods can be reused across
multiple integration tests.
It’s important to check the state of the database independently of the data used as
input parameters. To do that, the integration test queries the user and company data
separately in the assert section, creates new userFromDb and companyFromDb instances,
and only then asserts their state. This approach ensures that the test exercises both
writes to and reads from the database and thus provides the maximum protection
against regressions. The reading itself must be implemented using the same code the
controller uses internally: in this example, using the Database, UserFactory, and
CompanyFactory classes.
 This integration test, while it gets the job done, can still benefit from some
improvement. For instance, you could use helper methods in the assertion section, too,
in order to reduce this section’s size. Also, messageBusMock doesn’t provide as good
protection against regressions as it potentially could. We’ll talk about these improve-
ments in the subsequent two chapters where we discuss mocking and database testing
best practices. 
8.4
Using interfaces to abstract dependencies
One of the most misunderstood subjects in the sphere of unit testing is the use of
interfaces. Developers often ascribe invalid reasons to why they introduce interfaces
and, as a result, tend to overuse them. In this section, I’ll expand on those invalid
reasons and show in what circumstances the use of interfaces is and isn’t preferable.
 
Asserts the 
user’s state
Asserts the 
company’s 
state
Checks the 
interactions 
with the mock


---
**Page 198**

198
CHAPTER 8
Why integration testing?
8.4.1
Interfaces and loose coupling
Many developers introduce interfaces for out-of-process dependencies, such as the
database or the message bus, even when these interfaces have only one implementation.
This practice has become so widespread nowadays that hardly anyone questions it.
You’ll often see class-interface pairs similar to the following:
public interface IMessageBus
public class MessageBus : IMessageBus
public interface IUserRepository
public class UserRepository : IUserRepository
The common reasoning behind the use of such interfaces is that they help to
Abstract out-of-process dependencies, thus achieving loose coupling
Add new functionality without changing the existing code, thus adhering to the
Open-Closed principle (OCP)
Both of these reasons are misconceptions. Interfaces with a single implementation are
not abstractions and don’t provide loose coupling any more than concrete classes that
implement those interfaces. Genuine abstractions are discovered, not invented. The dis-
covery, by definition, takes place post factum, when the abstraction already exists but
is not yet clearly defined in the code. Thus, for an interface to be a genuine abstrac-
tion, it must have at least two implementations.
 The second reason (the ability to add new functionality without changing the exist-
ing code) is a misconception because it violates a more foundational principle:
YAGNI. YAGNI stands for “You aren’t gonna need it” and advocates against investing
time in functionality that’s not needed right now. You shouldn’t develop this function-
ality, nor should you modify your existing code to account for the appearance of such
functionality in the future. The two major reasons are as follows:
Opportunity cost—If you spend time on a feature that business people don’t need
at the moment, you steer that time away from features they do need right now.
Moreover, when the business people finally come to require the developed func-
tionality, their view on it will most likely have evolved, and you will still need to
adjust the already-written code. Such activity is wasteful. It’s more beneficial to
implement the functionality from scratch when the actual need for it emerges.
The less code in the project, the better. Introducing code just in case without an imme-
diate need unnecessarily increases your code base’s cost of ownership. It’s bet-
ter to postpone introducing new functionality until as late a stage of your
project as possible.
TIP
Writing code is an expensive way to solve problems. The less code the
solution requires and the simpler that code is, the better.
There are exceptional cases where YAGNI doesn’t apply, but these are few and far
between. For those cases, see my article “OCP vs YAGNI,” at https://enterprise-
craftsmanship.com/posts/ocp-vs-yagni. 


