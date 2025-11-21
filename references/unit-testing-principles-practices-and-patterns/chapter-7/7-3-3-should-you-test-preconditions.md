# 7.3.3 Should you test preconditions? (pp.169-169)

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


