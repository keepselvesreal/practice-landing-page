# 7.1.2 Using the Humble Object pattern to split overcomplicated code (pp.155-158)

---
**Page 155**

155
Identifying the code to refactor
NOTE
Remember that it’s better to not write a test at all than to write a
bad test.
Of course, getting rid of overcomplicated code is easier said than done. Still, there are
techniques that can help you do that. I’ll first explain the theory behind those tech-
niques and then demonstrate them using a close-to-real-world example. 
7.1.2
Using the Humble Object pattern to split overcomplicated code
To split overcomplicated code, you need to use the Humble Object design pattern.
This pattern was introduced by Gerard Meszaros in his book xUnit Test Patterns: Refac-
toring Test Code (Addison-Wesley, 2007) as one of the ways to battle code coupling, but
it has a much broader application. You’ll see why shortly.
 We often find that code is hard to test because it’s coupled to a framework depen-
dency (see figure 7.3). Examples include asynchronous or multi-threaded execution,
user interfaces, communication with out-of-process dependencies, and so on.
To bring the logic of this code under test, you need to extract a testable part out of it.
As a result, the code becomes a thin, humble wrapper around that testable part: it glues
Complexity,
domain
signiﬁcance
Domain model,
algorithms
Overcomplicated
code
Trivial code
Number of
collaborators
Controllers
Figure 7.2
Refactor overcomplicated 
code by splitting it into algorithms and 
controllers. Ideally, you should have no 
code in the top-right quadrant.
Overcomplicated code
Hard-to-test
dependency
Logic
Test
Figure 7.3
It’s hard to test 
code that couples to a difficult 
dependency. Tests have to deal 
with that dependency, too, which 
increases their maintenance cost.


---
**Page 156**

156
CHAPTER 7
Refactoring toward valuable unit tests
the hard-to-test dependency and the newly extracted component together, but itself
contains little or no logic and thus doesn’t need to be tested (figure 7.4).
 If this approach looks familiar, it’s because you already saw it in this book. In fact,
both hexagonal and functional architectures implement this exact pattern. As you
may remember from previous chapters, hexagonal architecture advocates for the sep-
aration of business logic and communications with out-of-process dependencies. This
is what the domain and application services layers are responsible for, respectively.
 Functional architecture goes even further and separates business logic from com-
munications with all collaborators, not just out-of-process ones. This is what makes
functional architecture so testable: its functional core has no collaborators. All depen-
dencies in a functional core are immutable, which brings it very close to the vertical
axis on the types-of-code diagram (figure 7.5).
Humble object
Hard-to-test
dependency
Test
Logic
Figure 7.4
The Humble Object 
pattern extracts the logic out of the 
overcomplicated code, making that 
code so humble that it doesn’t need to 
be tested. The extracted logic is 
moved into another class, decoupled 
from the hard-to-test dependency.
Complexity,
domain
signiﬁcance
Number of
collaborators
Domain model,
algorithms
Overcomplicated
code
Trivial code
Controllers
Domain layer
Mutable shell and
application services layer
Functional core
Figure 7.5
The functional core in a functional architecture and the domain layer in 
a hexagonal architecture reside in the top-left quadrant: they have few collaborators 
and exhibit high complexity and domain significance. The functional core is closer 
to the vertical axis because it has no collaborators. The mutable shell (functional 
architecture) and the application services layer (hexagonal architecture) belong 
to the controllers’ quadrant.


---
**Page 157**

157
Identifying the code to refactor
Another way to view the Humble Object pattern is as a means to adhere to the Single
Responsibility principle, which states that each class should have only a single respon-
sibility.1 One such responsibility is always business logic; the pattern can be applied to
segregate that logic from pretty much anything.
 In our particular situation, we are interested in the separation of business logic
and orchestration. You can think of these two responsibilities in terms of code depth
versus code width. Your code can be either deep (complex or important) or wide (work
with many collaborators), but never both (figure 7.6).
I can’t stress enough how important this separation is. In fact, many well-known princi-
ples and patterns can be described as a form of the Humble Object pattern: they are
designed specifically to segregate complex code from the code that does orchestration.
 You already saw the relationship between this pattern and hexagonal and func-
tional architectures. Other examples include the Model-View-Presenter (MVP) and
the Model-View-Controller (MVC) patterns. These two patterns help you decouple
business logic (the Model part), UI concerns (the View), and the coordination between
them (Presenter or Controller). The Presenter and Controller components are humble
objects: they glue the view and the model together.
 Another example is the Aggregate pattern from Domain-Driven Design.2 One of its
goals is to reduce connectivity between classes by grouping them into clusters—
aggregates. The classes are highly connected inside those clusters, but the clusters them-
selves are loosely coupled. Such a structure decreases the total number of communica-
tions in the code base. The reduced connectivity, in turn, improves testability.
1 See Agile Principles, Patterns, and Practices in C# by Robert C. Martin and Micah Martin (Prentice Hall, 2006).
2 See Domain-Driven Design: Tackling Complexity in the Heart of Software by Eric Evans (Addison-Wesley, 2003).
Controllers
Domain layer,
algorithms
Figure 7.6
Code depth versus code width is 
a useful metaphor to apply when you think of 
the separation between the business logic 
and orchestration responsibilities. Controllers 
orchestrate many dependencies (represented as 
arrows in the figure) but aren’t complex on their 
own (complexity is represented as block height). 
Domain classes are the opposite of that.


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


