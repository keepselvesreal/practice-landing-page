# 8.6.2 How should you test logging? (pp.207-212)

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


---
**Page 208**

208
CHAPTER 8
Why integration testing?
public class DomainLogger : IDomainLogger
{
private readonly ILogger _logger;
public DomainLogger(ILogger logger)
{
_logger = logger;
}
public void UserTypeHasChanged(
int userId, UserType oldType, UserType newType)
{
_logger.Info(
$"User {userId} changed type " +
$"from {oldType} to {newType}");
}
}
DomainLogger works on top of ILogger: it uses the domain language to declare spe-
cific log entries required by the business, thus making support logging easier to
understand and maintain. In fact, this implementation is very similar to the concept
of structured logging, which enables great flexibility when it comes to log file post-
processing and analysis. 
UNDERSTANDING STRUCTURED LOGGING
Structured logging is a logging technique where capturing log data is decoupled from
the rendering of that data. Traditional logging works with simple text. A call like
logger.Info("User Id is " + 12);
first forms a string and then writes that string to a log storage. The problem with this
approach is that the resulting log files are hard to analyze due to the lack of structure.
For example, it’s not easy to see how many messages of a particular type there are and
how many of those relate to a specific user ID. You’d need to use (or even write your
own) special tooling for that.
 On the other hand, structured logging introduces structure to your log storage.
The use of a structured logging library looks similar on the surface:
logger.Info("User Id is {UserId}", 12);
But its underlying behavior differs significantly. Behind the scenes, this method com-
putes a hash of the message template (the message itself is stored in a lookup storage
for space efficiency) and combines that hash with the input parameters to form a set
of captured data. The next step is the rendering of that data. You can still have a flat log
file, as with traditional logging, but that’s just one possible rendering. You could also
configure the logging library to render the captured data as a JSON or a CSV file,
where it would be easier to analyze (figure 8.12).
Listing 8.5
DomainLogger as a wrapper on top of ILogger


---
**Page 209**

209
How to test logging functionality
DomainLogger in listing 8.5 isn’t a structured logger per se, but it operates in the same
spirit. Look at this method once again:
public void UserTypeHasChanged(
int userId, UserType oldType, UserType newType)
{
_logger.Info(
$"User {userId} changed type " +
$"from {oldType} to {newType}");
}
You can view UserTypeHasChanged() as the message template’s hash. Together with
the userId, oldType, and newType parameters, that hash forms the log data. The
method’s implementation renders the log data into a flat log file. And you can easily
create additional renderings by also writing the log data into a JSON or a CSV file. 
WRITING TESTS FOR SUPPORT AND DIAGNOSTIC LOGGING
As I mentioned earlier, DomainLogger represents an out-of-process dependency—the
log storage. This poses a problem: User now interacts with that dependency and thus
violates the separation between business logic and communication with out-of-process
dependencies. The use of DomainLogger has transitioned User to the category of
Log data
logger.Info("User Id is {UserId}", 12)
MessageTemplate
UserId
User Id is {UserId}
12
User Id is 12
Flat log ﬁle
{ “MessageTemplate”: “…”,
“UserId” : 12 }
MessageTemplate,UserId
User Id is {UserId},12
JSON ﬁle
CSV ﬁle
Rendering
Figure 8.12
Structured logging decouples log data from renderings of that data. You can set up 
multiple renderings, such as a flat log file, JSON, or CSV file.


---
**Page 210**

210
CHAPTER 8
Why integration testing?
overcomplicated code, making it harder to test and maintain (refer to chapter 7 for
more details about code categories).
 This problem can be solved the same way we implemented the notification of
external systems about changed user emails: with the help of domain events (again,
see chapter 7 for details). You can introduce a separate domain event to track changes
in the user type. The controller will then convert those changes into calls to Domain-
Logger, as shown in the following listing.
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
AddDomainEvent(
        
new UserTypeChangedEvent(
        
UserId, Type, newType));        
}
Email = newEmail;
Type = newType;
AddDomainEvent(new EmailChangedEvent(UserId, newEmail));
_logger.Info($"Email is changed for user {UserId}");
}
Notice that there are now two domain events: UserTypeChangedEvent and Email-
ChangedEvent. Both of them implement the same interface (IDomainEvent) and thus
can be stored in the same collection.
 And here is how the controller looks.
public string ChangeEmail(int userId, string newEmail)
{
object[] userData = _database.GetUserById(userId);
User user = UserFactory.Create(userData);
Listing 8.6
Replacing DomainLogger in User with a domain event
Listing 8.7
Latest version of UserController
Uses a domain 
event instead of 
DomainLogger


---
**Page 211**

211
How to test logging functionality
string error = user.CanChangeEmail();
if (error != null)
return error;
object[] companyData = _database.GetCompany();
Company company = CompanyFactory.Create(companyData);
user.ChangeEmail(newEmail, company);
_database.SaveCompany(company);
_database.SaveUser(user);
_eventDispatcher.Dispatch(user.DomainEvents);   
return "OK";
}
EventDispatcher is a new class that converts domain events into calls to out-of-process
dependencies:

EmailChangedEvent translates into _messageBus.SendEmailChangedMessage().

UserTypeChangedEvent translates into _domainLogger.UserTypeHasChanged().
The use of UserTypeChangedEvent has restored the separation between the two
responsibilities: domain logic and communication with out-of-process dependencies.
Testing support logging now isn’t any different from testing the other unmanaged
dependency, the message bus:
Unit tests should check an instance of UserTypeChangedEvent in the User
under test.
The single integration test should use a mock to ensure the interaction with
DomainLogger is in place.
Note that if you need to do support logging in the controller and not one of the
domain classes, there’s no need to use domain events. As you may remember from
chapter 7, controllers orchestrate the collaboration between the domain model and
out-of-process dependencies. DomainLogger is one of such dependencies, and thus
UserController can use that logger directly.
 Also notice that I didn’t change the way the User class does diagnostic logging.
User still uses the logger instance directly in the beginning and at the end of its Chan-
geEmail method. This is by design. Diagnostic logging is for developers only; you
don’t need to unit test this functionality and thus don’t have to keep it out of the
domain model.
 Still, refrain from the use of diagnostic logging in User or other domain classes
when possible. I explain why in the next section. 
Dispatches user 
domain events


---
**Page 212**

212
CHAPTER 8
Why integration testing?
8.6.3
How much logging is enough?
Another important question is about the optimum amount of logging. How much log-
ging is enough? Support logging is out of the question here because it’s a business
requirement. You do have control over diagnostic logging, though.
 It’s important not to overuse diagnostic logging, for the following two reasons:
Excessive logging clutters the code. This is especially true for the domain model.
That’s why I don’t recommend using diagnostic logging in User even though
such a use is fine from a unit testing perspective: it obscures the code.
Logs’ signal-to-noise ratio is key. The more you log, the harder it is to find relevant
information. Maximize the signal; minimize the noise.
Try not to use diagnostic logging in the domain model at all. In most cases, you can
safely move that logging from domain classes to controllers. And even then, resort to
diagnostic logging only temporarily when you need to debug something. Remove it
once you finish debugging. Ideally, you should use diagnostic logging for unhandled
exceptions only. 
8.6.4
How do you pass around logger instances?
Finally, the last question is how to pass logger instances in the code. One way to
resolve these instances is using static methods, as shown in the following listing.
public class User
{
private static readonly ILogger _logger =   
LogManager.GetLogger(typeof(User));     
public void ChangeEmail(string newEmail, Company company)
{
_logger.Info(
$"Changing email for user {UserId} to {newEmail}");
/* ... */
_logger.Info($"Email is changed for user {UserId}");
}
}
Steven van Deursen and Mark Seeman, in their book Dependency Injection Principles,
Practices, Patterns (Manning Publications, 2018), call this type of dependency acquisi-
tion ambient context. This is an anti-pattern. Two of their arguments are that
The dependency is hidden and hard to change.
Testing becomes more difficult.
I fully agree with this analysis. To me, though, the main drawback of ambient con-
text is that it masks potential problems in code. If injecting a logger explicitly into a
Listing 8.8
Storing ILogger in a static field
Resolves ILogger through a 
static method, and stores it 
in a private static field


