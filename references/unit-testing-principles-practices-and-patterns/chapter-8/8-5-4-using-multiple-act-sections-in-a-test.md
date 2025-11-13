# 8.5.4 Using multiple act sections in a test (pp.204-205)

---
**Page 204**

204
CHAPTER 8
Why integration testing?
A better approach to handle circular dependencies is to get rid of them. Refactor
ReportGenerationService such that it depends on neither CheckOutService nor the
ICheckOutService interface, and make ReportGenerationService return the result
of its work as a plain value instead of calling CheckOutService:
public class CheckOutService
{
public void CheckOut(int orderId)
{
var service = new ReportGenerationService();
Report report = service.GenerateReport(orderId);
/* other work */
}
}
public class ReportGenerationService
{
public Report GenerateReport(int orderId)
{
/* ... */
}
}
It’s rarely possible to eliminate all circular dependencies in your code base. But even
then, you can minimize the damage by making the remaining graphs of interdepen-
dent classes as small as possible. 
8.5.4
Using multiple act sections in a test
As you might remember from chapter 3, having more than one arrange, act, or assert
section in a test is a code smell. It’s a sign that this test checks multiple units of behav-
ior, which, in turn, hinders the test’s maintainability. For example, if you have two
related use cases—say, user registration and user deletion—it might be tempting to
check both of these use cases in a single integration test. Such a test could have the
following structure:
Arrange—Prepare data with which to register a user.
Act—Call UserController.RegisterUser().
Assert—Query the database to see if the registration is completed successfully.
Act—Call UserController.DeleteUser().
Assert—Query the database to make sure the user is deleted.
This approach is compelling because the user states naturally flow from one another,
and the first act (registering a user) can simultaneously serve as an arrange phase for
the subsequent act (user deletion). The problem is that such tests lose focus and can
quickly become too bloated.
 It’s best to split the test by extracting each act into a test of its own. It may seem like
unnecessary work (after all, why create two tests where one would suffice?), but this


---
**Page 205**

205
How to test logging functionality
work pays off in the long run. Having each test focus on a single unit of behavior
makes those tests easier to understand and modify when necessary.
 The exception to this guideline is tests working with out-of-process dependencies
that are hard to bring to a desirable state. Let’s say for example that registering a user
results in creating a bank account in an external banking system. The bank has provi-
sioned a sandbox for your organization, and you want to use that sandbox in an end-
to-end test. The problem is that the sandbox is too slow, or maybe the bank limits the
number of calls you can make to that sandbox. In such a scenario, it becomes benefi-
cial to combine multiple acts into a single test and thus reduce the number of interac-
tions with the problematic out-of-process dependency.
 Hard-to-manage out-of-process dependencies are the only legitimate reason to
write a test with more than one act section. This is why you should never have multiple
acts in a unit test—unit tests don’t work with out-of-process dependencies. Even inte-
gration tests should rarely have several acts. In practice, multistep tests almost always
belong to the category of end-to-end tests. 
8.6
How to test logging functionality
Logging is a gray area, and it isn’t obvious what to do with it when it comes to testing.
This is a complex topic that I’ll split into the following questions:
Should you test logging at all?
If so, how should you test it?
How much logging is enough?
How do you pass around logger instances?
We’ll use our sample CRM project as an example.
8.6.1
Should you test logging?
Logging is a cross-cutting functionality, which you can require in any part of your code
base. Here’s an example of logging in the User class.
public class User
{
public void ChangeEmail(string newEmail, Company company)
{
_logger.Info(    
$"Changing email for user {UserId} to {newEmail}");
Precondition.Requires(CanChangeEmail() == null);
if (Email == newEmail)
return;
UserType newType = company.IsEmailCorporate(newEmail)
? UserType.Employee
: UserType.Customer;
Listing 8.3
An example of logging in User
Start of the
method


