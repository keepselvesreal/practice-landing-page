# 7.4.0 Introduction [auto-generated] (pp.169-172)

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


---
**Page 170**

170
CHAPTER 7
Refactoring toward valuable unit tests
There are a lot of situations where these stages aren’t as clearcut, though. As we discussed
in chapter 6, you might need to query additional data from an out-of-process depen-
dency based on an intermediate result of the decision-making process (figure 7.11). Writ-
ing to the out-of-process dependency often depends on that result, too.
As also discussed in the previous chapter, you have three options in such a situation:
Push all external reads and writes to the edges anyway. This approach preserves the
read-decide-act structure but concedes performance: the controller will call
out-of-process dependencies even when there’s no need for that.
Inject the out-of-process dependencies into the domain model and allow the business
logic to directly decide when to call those dependencies.
Split the decision-making process into more granular steps and have the controller act
on each of those steps separately.
Read
Invoke
Write
Out-of-process
dependencies:
ﬁlesystem,
database, etc.
Application
service
(controller)
Business logic
(domain
model)
Figure 7.10
Hexagonal and functional architectures work best when all 
references to out-of-process dependencies can be pushed to the edges of 
business operations.
Read
Read
Invoke 1
Write
Out-of-process
dependencies:
ﬁlesystem,
database, etc.
Application
service
(controller)
Business logic
(domain
model)
Invoke 2
Figure 7.11
A hexagonal architecture doesn’t work as well when you need to refer to 
out-of-process dependencies in the middle of the business operation.


---
**Page 171**

171
Handling conditional logic in controllers
The challenge is to balance the following three attributes:
Domain model testability, which is a function of the number and type of collabora-
tors in domain classes
Controller simplicity, which depends on the presence of decision-making (branch-
ing) points in the controller
Performance, as defined by the number of calls to out-of-process dependencies
Each option only gives you two out of the three attributes (figure 7.12):
Pushing all external reads and writes to the edges of a business operation—Preserves
controller simplicity and keeps the domain model isolated from out-of-process
dependencies (thus allowing it to remain testable) but concedes performance.
Injecting out-of-process dependencies into the domain model—Keeps performance and
the controller’s simplicity intact but damages domain model testability.
Splitting the decision-making process into more granular steps—Helps with both per-
formance and domain model testability but concedes controller simplicity.
You’ll need to introduce decision-making points in the controller in order to
manage these granular steps.
In most software projects, performance is important, so the first approach (pushing
external reads and writes to the edges of a business operation) is out of the question.
The second option (injecting out-of-process dependencies into the domain model)
brings most of your code into the overcomplicated quadrant on the types-of-code dia-
gram. This is exactly what we refactored the initial CRM implementation away from. I
recommend that you avoid this approach: such code no longer preserves the separation
Domain model
testability
Performance
Pushing all external reads
and writes to the edges of
the business operation
Injecting out-of-process
dependencies into the
domain model
Splitting the decision-making
process into more granular steps
Controller simplicity
Figure 7.12
There’s no single solution that satisfies all three attributes: controller simplicity, 
domain model testability, and performance. You have to choose two out of the three.


---
**Page 172**

172
CHAPTER 7
Refactoring toward valuable unit tests
between business logic and communication with out-of-process dependencies and
thus becomes much harder to test and maintain.
 That leaves you with the third option: splitting the decision-making process into
smaller steps. With this approach, you will have to make your controllers more com-
plex, which will also push them closer to the overcomplicated quadrant. But there are
ways to mitigate this problem. Although you will rarely be able to factor all the com-
plexity out of controllers as we did previously in the sample project, you can keep that
complexity manageable.
7.4.1
Using the CanExecute/Execute pattern
The first way to mitigate the growth of the controllers’ complexity is to use the Can-
Execute/Execute pattern, which helps avoid leaking of business logic from the
domain model to controllers. This pattern is best explained with an example, so let’s
expand on our sample project.
 Let’s say that a user can change their email only until they confirm it. If a user tries
to change the email after the confirmation, they should be shown an error message.
To accommodate this new requirement, we’ll add a new property to the User class.
public class User
{
public int UserId { get; private set; }
public string Email { get; private set; }
public UserType Type { get; private set; }
public bool IsEmailConfirmed               
{ get; private set; }
               
/* ChangeEmail(newEmail, company) method */
}
There are two options for where to put this check. First, you could put it in User’s
ChangeEmail method:
public string ChangeEmail(string newEmail, Company company)
{
if (IsEmailConfirmed)
return "Can't change a confirmed email";
/* the rest of the method */
}
Then you could make the controller either return an error or incur all necessary side
effects, depending on this method’s output.
public string ChangeEmail(int userId, string newEmail)
{
Listing 7.7
User with a new property
Listing 7.8
The controller, still stripped of all decision-making
New property


