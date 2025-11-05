# 7.3.1 Testing the domain layer and utility code (pp.167-168)

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


---
**Page 168**

168
CHAPTER 7
Refactoring toward valuable unit tests
[Fact]
public void Changing_email_from_non_corporate_to_corporate()
{
var company = new Company("mycorp.com", 1);
var sut = new User(1, "user@gmail.com", UserType.Customer);
sut.ChangeEmail("new@mycorp.com", company);
Assert.Equal(2, company.NumberOfEmployees);
Assert.Equal("new@mycorp.com", sut.Email);
Assert.Equal(UserType.Employee, sut.Type);
}
To achieve full coverage, you’d need another three such tests:
public void Changing_email_from_corporate_to_non_corporate()
public void Changing_email_without_changing_user_type()
public void Changing_email_to_the_same_one()
Tests for the other three classes would be even shorter, and you could use parameter-
ized tests to group several test cases together:
[InlineData("mycorp.com", "email@mycorp.com", true)]
[InlineData("mycorp.com", "email@gmail.com", false)]
[Theory]
public void Differentiates_a_corporate_email_from_non_corporate(
string domain, string email, bool expectedResult)
{
var sut = new Company(domain, 0);
bool isEmailCorporate = sut.IsEmailCorporate(email);
Assert.Equal(expectedResult, isEmailCorporate);
}
7.3.2
Testing the code from the other three quadrants
Code with low complexity and few collaborators (bottom-left quadrant in table 7.1) is
represented by the constructors in User and Company, such as
public User(int userId, string email, UserType type)
{
UserId = userId;
Email = email;
Type = type;
}
These constructors are trivial and aren’t worth the effort. The resulting tests wouldn’t
provide great enough protection against regressions.
 The refactoring has eliminated all code with high complexity and a large number
of collaborators (top-right quadrant in table 7.1), so we have nothing to test there,
either. As for the controllers quadrant (bottom-right in table 7.1), we’ll discuss testing
it in the next chapter. 


