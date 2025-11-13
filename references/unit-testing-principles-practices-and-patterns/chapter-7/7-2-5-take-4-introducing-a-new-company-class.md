# 7.2.5 Take 4: Introducing a new Company class (pp.164-167)

---
**Page 164**

164
CHAPTER 7
Refactoring toward valuable unit tests
7.2.5
Take 4: Introducing a new Company class
Look at this code in the controller once again:
object[] companyData = _database.GetCompany();
string companyDomainName = (string)companyData[0];
int numberOfEmployees = (int)companyData[1];
int newNumberOfEmployees = user.ChangeEmail(
newEmail, companyDomainName, numberOfEmployees);
The awkwardness of returning an updated number of employees from User is a sign
of a misplaced responsibility, which itself is a sign of a missing abstraction. To fix this,
we need to introduce another domain class, Company, that bundles the company-
related logic and data together, as shown in the following listing.
public class Company
{
public string DomainName { get; private set; }
public int NumberOfEmployees { get; private set; }
public void ChangeNumberOfEmployees(int delta)
{
Precondition.Requires(NumberOfEmployees + delta >= 0);
NumberOfEmployees += delta;
}
public bool IsEmailCorporate(string email)
{
string emailDomain = email.Split('@')[1];
return emailDomain == DomainName;
}
}
How is the reconstruction logic complex?
How is the reconstruction logic complex, given that there’s only a single branching
point in the UserFactory.Create() method? As I mentioned in chapter 1, there
could be a lot of hidden branching points in the underlying libraries used by the code
and thus a lot of potential for something to go wrong. This is exactly the case for the
UserFactory.Create() method.
Referring to an array element by index (data[0]) entails an internal decision made
by the .NET Framework as to what data element to access. The same is true for the
conversion from object to int or string. Internally, the .NET Framework decides
whether to throw a cast exception or allow the conversion to proceed. All these hid-
den branches make the reconstruction logic test-worthy, despite the lack of decision
points in it. 
Listing 7.4
The new class in the domain layer


---
**Page 165**

165
Refactoring toward valuable unit tests
There are two methods in this class: ChangeNumberOfEmployees() and IsEmail-
Corporate(). These methods help adhere to the tell-don’t-ask principle I mentioned
in chapter 5. This principle advocates for bundling together data and operations on
that data. A User instance will tell the company to change its number of employees or
figure out whether a particular email is corporate; it won’t ask for the raw data and do
everything on its own.
 There’s also a new CompanyFactory class, which is responsible for the reconstruc-
tion of Company objects, similar to UserFactory. This is how the controller now looks.
public class UserController
{
private readonly Database _database = new Database();
private readonly MessageBus _messageBus = new MessageBus();
public void ChangeEmail(int userId, string newEmail)
{
object[] userData = _database.GetUserById(userId);
User user = UserFactory.Create(userData);
object[] companyData = _database.GetCompany();
Company company = CompanyFactory.Create(companyData);
user.ChangeEmail(newEmail, company);
_database.SaveCompany(company);
_database.SaveUser(user);
_messageBus.SendEmailChangedMessage(userId, newEmail);
}
}
And here’s the User class.
public class User
{
public int UserId { get; private set; }
public string Email { get; private set; }
public UserType Type { get; private set; }
public void ChangeEmail(string newEmail, Company company)
{
if (Email == newEmail)
return;
UserType newType = company.IsEmailCorporate(newEmail)
? UserType.Employee
: UserType.Customer;
Listing 7.5
Controller after refactoring 
Listing 7.6
User after refactoring 


---
**Page 166**

166
CHAPTER 7
Refactoring toward valuable unit tests
if (Type != newType)
{
int delta = newType == UserType.Employee ? 1 : -1;
company.ChangeNumberOfEmployees(delta);
}
Email = newEmail;
Type = newType;
}
}
Notice how the removal of the misplaced responsibility made User much cleaner.
Instead of operating on company data, it accepts a Company instance and delegates
two important pieces of work to that instance: determining whether an email is corpo-
rate and changing the number of employees in the company.
 Figure 7.9 shows where each class stands in the diagram. The factories and both
domain classes reside in the domain model and algorithms quadrant. User has moved
to the right because it now has one collaborator, Company, whereas previously it had
none. That has made User less testable, but not much.
UserController now firmly stands in the controllers quadrant because all of its com-
plexity has moved to the factories. The only thing this class is responsible for is gluing
together all the collaborating parties.
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
UserController
User
Company,
UserFactory,
CompanyFactory
Figure 7.9
User has shifted to the right because it now has the Company 
collaborator. UserController firmly stands in the controllers quadrant; all 
its complexity has moved to the factories.


---
**Page 167**

167
Analysis of optimal unit test coverage
 Note the similarities between this implementation and the functional architecture
from the previous chapter. Neither the functional core in the audit system nor the
domain layer in this CRM (the User and Company classes) communicates with out-of-
process dependencies. In both implementations, the application services layer is
responsible for such communication: it gets the raw data from the filesystem or from
the database, passes that data to stateless algorithms or the domain model, and then
persists the results back to the data storage.
 The difference between the two implementations is in their treatment of side
effects. The functional core doesn’t incur any side effects whatsoever. The CRM’s
domain model does, but all those side effects remain inside the domain model in the
form of the changed user email and the number of employees. The side effects only
cross the domain model’s boundary when the controller persists the User and Company
objects in the database.
 The fact that all side effects are contained in memory until the very last moment
improves testability a lot. Your tests don’t need to examine out-of-process dependen-
cies, nor do they need to resort to communication-based testing. All the verification
can be done using output-based and state-based testing of objects in memory. 
7.3
Analysis of optimal unit test coverage
Now that we’ve completed the refactoring with the help of the Humble Object pat-
tern, let’s analyze which parts of the project fall into which code category and how
those parts should be tested. Table 7.1 shows all the code from the sample project
grouped by position in the types-of-code diagram.
With the full separation of business logic and orchestration at hand, it’s easy to decide
which parts of the code base to unit test.
7.3.1
Testing the domain layer and utility code
Testing methods in the top-left quadrant in table 7.1 provides the best results in cost-
benefit terms. The code’s high complexity or domain significance guarantees great
protection against regressions, while having few collaborators ensures the lowest mainte-
nance costs. This is an example of how User could be tested:
Table 7.1
Types of code in the sample project after refactoring using the Humble Object pattern
Few collaborators
Many collaborators
High complexity or 
domain significance
ChangeEmail(newEmail, company) in User;
ChangeNumberOfEmployees(delta) and 
IsEmailCorporate(email) in Company; 
and Create(data) in UserFactory and 
CompanyFactory
Low complexity and 
domain significance
Constructors in User and Company
ChangeEmail(userId, 
newEmail) in 
UserController


