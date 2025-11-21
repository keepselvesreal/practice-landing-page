# 7.2.4 Take 3: Removing complexity from the application service (pp.163-164)

---
**Page 163**

163
Refactoring toward valuable unit tests
7.2.4
Take 3: Removing complexity from the application service
To put UserController firmly into the controllers quadrant, we need to extract the
reconstruction logic from it. If you use an object-relational mapping (ORM) library
to map the database into the domain model, that would be a good place to which to
attribute the reconstruction logic. Each ORM library has a dedicated place where you
can specify how your database tables should be mapped to domain classes, such as
attributes on top of those domain classes, XML files, or files with fluent mappings.
 If you don’t want to or can’t use an ORM, create a factory in the domain model
that will instantiate the domain classes using raw database data. This factory can be a
separate class or, for simpler cases, a static method in the existing domain classes. The
reconstruction logic in our sample application is not too complicated, but it’s good to
keep such things separated, so I’m putting it in a separate UserFactory class as shown
in the following listing.
public class UserFactory
{
public static User Create(object[] data)
{
Precondition.Requires(data.Length >= 3);
int id = (int)data[0];
string email = (string)data[1];
UserType type = (UserType)data[2];
return new User(id, email, type);
}
}
This code is now fully isolated from all collaborators and therefore easily testable.
Notice that I’ve put a safeguard in this method: a requirement to have at least three
elements in the data array. Precondition is a simple custom class that throws an
exception if the Boolean argument is false. The reason for this class is the more
succinct code and the condition inversion: affirmative statements are more read-
able than negative ones. In our example, the data.Length >= 3 requirement reads
better than
if (data.Length < 3)
throw new Exception();
Note that while this reconstruction logic is somewhat complex, it doesn’t have domain
significance: it isn’t directly related to the client’s goal of changing the user email. It’s
an example of the utility code I refer to in previous chapters.
 
Listing 7.3
User factory


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


