# 8.6.1 Should you test logging? (pp.205-207)

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


---
**Page 206**

206
CHAPTER 8
Why integration testing?
if (Type != newType)
{
int delta = newType == UserType.Employee ? 1 : -1;
company.ChangeNumberOfEmployees(delta);
_logger.Info(
   
$"User {UserId} changed type " +
   
$"from {Type} to {newType}");
   
}
Email = newEmail;
Type = newType;
EmailChangedEvents.Add(new EmailChangedEvent(UserId, newEmail));
_logger.Info(
    
$"Email is changed for user {UserId}");
}
}
The User class records in a log file each beginning and ending of the ChangeEmail
method, as well as the change of the user type. Should you test this functionality?
 On the one hand, logging generates important information about the applica-
tion’s behavior. But on the other hand, logging can be so ubiquitous that it’s not obvi-
ous whether this functionality is worth the additional, quite significant, testing effort.
The answer to the question of whether you should test logging comes down to this: Is
logging part of the application’s observable behavior, or is it an implementation detail?
 In that sense, it isn’t different from any other functionality. Logging ultimately
results in side effects in an out-of-process dependency such as a text file or a database.
If these side effects are meant to be observed by your customer, the application’s cli-
ents, or anyone else other than the developers themselves, then logging is an observ-
able behavior and thus must be tested. If the only audience is the developers, then it’s
an implementation detail that can be freely modified without anyone noticing, in
which case it shouldn’t be tested.
 For example, if you write a logging library, then the logs this library produces are
the most important (and the only) part of its observable behavior. Another example is
when business people insist on logging key application workflows. In this case, logs
also become a business requirement and thus have to be covered by tests. However, in
the latter example, you might also have separate logging just for developers.
 Steve Freeman and Nat Pryce, in their book Growing Object-Oriented Software, Guided
by Tests (Addison-Wesley Professional, 2009), call these two types of logging support
logging and diagnostic logging:
Support logging produces messages that are intended to be tracked by support
staff or system administrators.
Diagnostic logging helps developers understand what’s going on inside the
application. 
Changes the 
user type
End of the
method


---
**Page 207**

207
How to test logging functionality
8.6.2
How should you test logging?
Because logging involves out-of-process dependencies, when it comes to testing it, the
same rules apply as with any other functionality that touches out-of-process dependen-
cies. You need to use mocks to verify interactions between your application and the
log storage.
INTRODUCING A WRAPPER ON TOP OF ILOGGER
But don’t just mock out the ILogger interface. Because support logging is a business
requirement, reflect that requirement explicitly in your code base. Create a special
DomainLogger class where you explicitly list all the support logging needed for the
business; verify interactions with that class instead of the raw ILogger.
 For example, let’s say that business people require you to log all changes of the
users’ types, but the logging at the beginning and the end of the method is there just
for debugging purposes. The next listing shows the User class after introducing a
DomainLogger class.
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
if (Type != newType)
{
int delta = newType == UserType.Employee ? 1 : -1;
company.ChangeNumberOfEmployees(delta);
_domainLogger.UserTypeHasChanged(         
UserId, Type, newType);
         
}
Email = newEmail;
Type = newType;
EmailChangedEvents.Add(new EmailChangedEvent(UserId, newEmail));
_logger.Info(
   
$"Email is changed for user {UserId}");
}
The diagnostic logging still uses the old logger (which is of type ILogger), but the
support logging now uses the new domainLogger instance of type IDomainLogger. The
following listing shows the implementation of IDomainLogger.
Listing 8.4
Extracting support logging into the DomainLogger class
Diagnostic
logging
Support 
logging
Diagnostic
logging


