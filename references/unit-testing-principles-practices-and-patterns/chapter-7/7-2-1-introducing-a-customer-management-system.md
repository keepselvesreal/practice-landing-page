# 7.2.1 Introducing a customer management system (pp.158-160)

---
**Page 158**

158
CHAPTER 7
Refactoring toward valuable unit tests
 Note that improved testability is not the only reason to maintain the separation
between business logic and orchestration. Such a separation also helps tackle code
complexity, which is crucial for project growth, too, especially in the long run. I per-
sonally always find it fascinating how a testable design is not only testable but also easy
to maintain. 
7.2
Refactoring toward valuable unit tests
In this section, I’ll show a comprehensive example of splitting overcomplicated code
into algorithms and controllers. You saw a similar example in the previous chapter,
where we talked about output-based testing and functional architecture. This time, I’ll
generalize this approach to all enterprise-level applications, with the help of the Hum-
ble Object pattern. I’ll use this project not only in this chapter but also in the subse-
quent chapters of part 3.
7.2.1
Introducing a customer management system
The sample project is a customer management system (CRM) that handles user
registrations. All users are stored in a database. The system currently supports only
one use case: changing a user’s email. There are three business rules involved in this
operation:
If the user’s email belongs to the company’s domain, that user is marked as an
employee. Otherwise, they are treated as a customer.
The system must track the number of employees in the company. If the user’s
type changes from employee to customer, or vice versa, this number must
change, too.
When the email changes, the system must notify external systems by sending a
message to a message bus.
The following listing shows the initial implementation of the CRM system.
public class User
{
public int UserId { get; private set; }
public string Email { get; private set; }
public UserType Type { get; private set; }
public void ChangeEmail(int userId, string newEmail)
{
object[] data = Database.GetUserById(userId);    
UserId = userId;
Email = (string)data[1];
Type = (UserType)data[2];
if (Email == newEmail)
return;
Listing 7.1
Initial implementation of the CRM system
Retrieves the user’s 
current email and 
type from the 
database


---
**Page 159**

159
Refactoring toward valuable unit tests
object[] companyData = Database.GetCompany();       
string companyDomainName = (string)companyData[0];
int numberOfEmployees = (int)companyData[1];
string emailDomain = newEmail.Split('@')[1];
bool isEmailCorporate = emailDomain == companyDomainName;
UserType newType = isEmailCorporate                       
? UserType.Employee
                       
: UserType.Customer;
                       
if (Type != newType)
{
int delta = newType == UserType.Employee ? 1 : -1;
int newNumber = numberOfEmployees + delta;
Database.SaveCompany(newNumber);        
}
Email = newEmail;
Type = newType;
Database.SaveUser(this);              
MessageBus.SendEmailChangedMessage(UserId, newEmail);       
}
}
public enum UserType
{
Customer = 1,
Employee = 2
}
The User class changes a user email. Note that, for brevity, I omitted simple valida-
tions such as checks for email correctness and user existence in the database. Let’s
analyze this implementation from the perspective of the types-of-code diagram.
 The code’s complexity is not too high. The ChangeEmail method contains only a
couple of explicit decision-making points: whether to identify the user as an employee
or a customer, and how to update the company’s number of employees. Despite being
simple, these decisions are important: they are the application’s core business logic.
Hence, the class scores highly on the complexity and domain significance dimension.
 On the other hand, the User class has four dependencies, two of which are explicit
and the other two of which are implicit. The explicit dependencies are the userId
and newEmail arguments. These are values, though, and thus don’t count toward the
class’s number of collaborators. The implicit ones are Database and MessageBus.
These two are out-of-process collaborators. As I mentioned earlier, out-of-process col-
laborators are a no-go for code with high domain significance. Hence, the User class
scores highly on the collaborators dimension, which puts this class into the overcom-
plicated category (figure 7.7).
 This approach—when a domain class retrieves and persists itself to the database—
is called the Active Record pattern. It works fine in simple or short-lived projects but
Retrieves the organization’s 
domain name and the 
number of employees 
from the database
Sets the user type 
depending on the new 
email’s domain name
Updates the number 
of employees in the 
organization, if needed
Persists the user 
in the database
Sends a notification
to the message bus


---
**Page 160**

160
CHAPTER 7
Refactoring toward valuable unit tests
often fails to scale as the code base grows. The reason is precisely this lack of separa-
tion between these two responsibilities: business logic and communication with out-of-
process dependencies. 
7.2.2
Take 1: Making implicit dependencies explicit
The usual approach to improve testability is to make implicit dependencies explicit:
that is, introduce interfaces for Database and MessageBus, inject those interfaces into
User, and then mock them in tests. This approach does help, and that’s exactly what
we did in the previous chapter when we introduced the implementation with mocks
for the audit system. However, it’s not enough.
 From the perspective of the types-of-code diagram, it doesn’t matter if the domain
model refers to out-of-process dependencies directly or via an interface. Such depen-
dencies are still out-of-process; they are proxies to data that is not yet in memory. You
still need to maintain complicated mock machinery in order to test such classes,
which increases the tests’ maintenance costs. Moreover, using mocks for the database
dependency would lead to test fragility (we’ll discuss this in the next chapter).
 Overall, it’s much cleaner for the domain model not to depend on out-of-process
collaborators at all, directly or indirectly (via an interface). That’s what the hexagonal
architecture advocates as well—the domain model shouldn’t be responsible for com-
munications with external systems. 
7.2.3
Take 2: Introducing an application services layer
To overcome the problem of the domain model directly communicating with external
systems, we need to shift this responsibility to another class, a humble controller (an
application service, in the hexagonal architecture taxonomy). As a general rule, domain
classes should only depend on in-process dependencies, such as other domain classes,
or plain values. Here’s what the first version of that application service looks like.
Domain model,
algorithms
Overcomplicated
code
Trivial code
Controllers
Complexity,
domain
signiﬁcance
Number of
collaborators
User class
Figure 7.7
The initial 
implementation of the User 
class scores highly on both 
dimensions and thus falls 
into the category of 
overcomplicated code.


