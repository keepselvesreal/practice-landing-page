# 7.3.2 Testing the code from the other three quadrants (pp.168-169)

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


---
**Page 169**

169
Handling conditional logic in controllers
7.3.3
Should you test preconditions?
Let’s take a look at a special kind of branching points—preconditions—and see whether
you should test them. For example, look at this method from Company once again:
public void ChangeNumberOfEmployees(int delta)
{
Precondition.Requires(NumberOfEmployees + delta >= 0);
NumberOfEmployees += delta;
}
It has a precondition stating that the number of employees in the company should
never become negative. This precondition is a safeguard that’s activated only in
exceptional cases. Such exceptional cases are usually the result of bugs. The only pos-
sible reason for the number of employees to go below zero is if there’s an error in
code. The safeguard provides a mechanism for your software to fail fast and to prevent
the error from spreading and being persisted in the database, where it would be much
harder to deal with. Should you test such preconditions? In other words, would such
tests be valuable enough to have in the test suite?
 There’s no hard rule here, but the general guideline I recommend is to test all pre-
conditions that have domain significance. The requirement for the non-negative
number of employees is such a precondition. It’s part of the Company class’s invariants:
conditions that should be held true at all times. But don’t spend time testing precon-
ditions that don’t have domain significance. For example, UserFactory has the follow-
ing safeguard in its Create method:
public static User Create(object[] data)
{
Precondition.Requires(data.Length >= 3);
/* Extract id, email, and type out of data */
}
There’s no domain meaning to this precondition and therefore not much value in
testing it. 
7.4
Handling conditional logic in controllers
Handling conditional logic and simultaneously maintaining the domain layer free of
out-of-process collaborators is often tricky and involves trade-offs. In this section, I’ll
show what those trade-offs are and how to decide which of them to choose in your
own project.
 The separation between business logic and orchestration works best when a busi-
ness operation has three distinct stages:
Retrieving data from storage
Executing business logic
Persisting data back to the storage (figure 7.10)


