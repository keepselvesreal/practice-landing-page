# 7.4.1 Using the CanExecute/Execute pattern (pp.172-175)

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


---
**Page 173**

173
Handling conditional logic in controllers
object[] userData = _database.GetUserById(userId);
  
User user = UserFactory.Create(userData);
  
object[] companyData = _database.GetCompany();
  
Company company = CompanyFactory.Create(companyData);   
string error = user.ChangeEmail(newEmail, company);
     
if (error != null)
    
return error;
     
_database.SaveCompany(company);
      
_database.SaveUser(user);
 
_messageBus.SendEmailChangedMessage(userId, newEmail); 
return "OK";
 
}
This implementation keeps the controller free of decision-making, but it does so at
the expense of a performance drawback. The Company instance is retrieved from the
database unconditionally, even when the email is confirmed and thus can’t be changed.
This is an example of pushing all external reads and writes to the edges of a business
operation.
NOTE
I don’t consider the new if statement analyzing the error string an
increase in complexity because it belongs to the acting phase; it’s not part of
the decision-making process. All the decisions are made by the User class, and
the controller merely acts on those decisions.
The second option is to move the check for IsEmailConfirmed from User to the
controller.
public string ChangeEmail(int userId, string newEmail)
{
object[] userData = _database.GetUserById(userId);
User user = UserFactory.Create(userData);
if (user.IsEmailConfirmed)
   
return "Can't change a confirmed email";  
object[] companyData = _database.GetCompany();
Company company = CompanyFactory.Create(companyData);
user.ChangeEmail(newEmail, company);
_database.SaveCompany(company);
_database.SaveUser(user);
_messageBus.SendEmailChangedMessage(userId, newEmail);
return "OK";
}
Listing 7.9
Controller deciding whether to change the user’s email
Prepares 
the data
Makes a
decision
Acts on the 
decision
Decision-making 
moved here from User.


---
**Page 174**

174
CHAPTER 7
Refactoring toward valuable unit tests
With this implementation, the performance stays intact: the Company instance is
retrieved from the database only after it is certain that the email can be changed. But
now the decision-making process is split into two parts:
Whether to proceed with the change of email (performed by the controller)
What to do during that change (performed by User)
Now it’s also possible to change the email without verifying the IsEmailConfirmed
flag first, which diminishes the domain model’s encapsulation. Such fragmentation
hinders the separation between business logic and orchestration and moves the con-
troller closer to the overcomplicated danger zone.
 To prevent this fragmentation, you can introduce a new method in User, CanChange-
Email(), and make its successful execution a precondition for changing an email. The
modified version in the following listing follows the CanExecute/Execute pattern.
public string CanChangeEmail()
{
if (IsEmailConfirmed)
return "Can't change a confirmed email";
return null;
}
public void ChangeEmail(string newEmail, Company company)
{
Precondition.Requires(CanChangeEmail() == null);
/* the rest of the method */
}
This approach provides two important benefits:
The controller no longer needs to know anything about the process of chang-
ing emails. All it needs to do is call the CanChangeEmail() method to see if the
operation can be done. Notice that this method can contain multiple valida-
tions, all encapsulated away from the controller.
The additional precondition in ChangeEmail() guarantees that the email won’t
ever be changed without checking for the confirmation first.
This pattern helps you to consolidate all decisions in the domain layer. The controller
no longer has an option not to check for the email confirmation, which essentially
eliminates the new decision-making point from that controller. Thus, although the
controller still contains the if statement calling CanChangeEmail(), you don’t need to
test that if statement. Unit testing the precondition in the User class itself is enough.
NOTE
For simplicity’s sake, I’m using a string to denote an error. In a real-
world project, you may want to introduce a custom Result class to indicate
the success or failure of an operation. 
Listing 7.10
Changing an email using the CanExecute/Execute pattern


---
**Page 175**

175
Handling conditional logic in controllers
7.4.2
Using domain events to track changes in the domain model
It’s sometimes hard to deduct what steps led the domain model to the current state.
Still, it might be important to know these steps because you need to inform external
systems about what exactly has happened in your application. Putting this responsibil-
ity on the controllers would make them more complicated. To avoid that, you can
track important changes in the domain model and then convert those changes into
calls to out-of-process dependencies after the business operation is complete. Domain
events help you implement such tracking.
DEFINITION
A domain event describes an event in the application that is mean-
ingful to domain experts. The meaningfulness for domain experts is what
differentiates domain events from regular events (such as button clicks).
Domain events are often used to inform external applications about import-
ant changes that have happened in your system.
Our CRM has a tracking requirement, too: it has to notify external systems about
changed user emails by sending messages to the message bus. The current implemen-
tation has a flaw in the notification functionality: it sends messages even when the
email is not changed, as shown in the following listing.
// User
public void ChangeEmail(string newEmail, Company company)
{
Precondition.Requires(CanChangeEmail() == null);
if (Email == newEmail)   
return;
/* the rest of the method */
}
// Controller
public string ChangeEmail(int userId, string newEmail)
{
/* preparations */
user.ChangeEmail(newEmail, company);
_database.SaveCompany(company);
_database.SaveUser(user);
_messageBus.SendEmailChangedMessage(  
userId, newEmail);
  
return "OK";
}
You could resolve this bug by moving the check for email sameness to the controller,
but then again, there are issues with the business logic fragmentation. And you can’t
Listing 7.11
Sends a notification even when the email has not changed
User email may 
not change.
The controller sends 
a message anyway.


