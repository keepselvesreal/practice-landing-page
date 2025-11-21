# 5.3.1 Defining hexagonal architecture (pp.106-110)

---
**Page 106**

106
CHAPTER 5
Mocks and test fragility
5.3
The relationship between mocks and test fragility
The previous sections defined a mock and showed the difference between observable
behavior and an implementation detail. In this section, you will learn about hexago-
nal architecture, the difference between internal and external communications, and
(finally!) the relationship between mocks and test fragility.
5.3.1
Defining hexagonal architecture
A typical application consists of two layers, domain and application services, as
shown in figure 5.8. The domain layer resides in the middle of the diagram because
it’s the central part of your application. It contains the business logic: the essential
functionality your application is built for. The domain layer and its business logic
differentiate this application from others and provide a competitive advantage for
the organization.
The application services layer sits on top of the domain layer and orchestrates com-
munication between that layer and the external world. For example, if your applica-
tion is a RESTful API, all requests to this API hit the application services layer first.
This layer then coordinates the work between domain classes and out-of-process
dependencies. Here’s an example of such coordination for the application service. It
does the following:
Queries the database and uses the data to materialize a domain class instance
Invokes an operation on that instance
Saves the results back to the database
The combination of the application services layer and the domain layer forms a hexa-
gon, which itself represents your application. It can interact with other applications,
which are represented with their own hexagons (see figure 5.9). These other applica-
tions could be an SMTP service, a third-party system, a message bus, and so on. A set
of interacting hexagons makes up a hexagonal architecture.
 
Domain
(business logic)
Application
services
Figure 5.8
A typical application consists of a 
domain layer and an application services layer. 
The domain layer contains the application’s 
business logic; application services tie that 
logic to business use cases.


---
**Page 107**

107
The relationship between mocks and test fragility
The term hexagonal architecture was introduced by Alistair Cockburn. Its purpose is to
emphasize three important guidelines:
The separation of concerns between the domain and application services layers—Business
logic is the most important part of the application. Therefore, the domain layer
should be accountable only for that business logic and exempted from all other
responsibilities. Those responsibilities, such as communicating with external
applications and retrieving data from the database, must be attributed to appli-
cation services. Conversely, the application services shouldn’t contain any busi-
ness logic. Their responsibility is to adapt the domain layer by translating the
incoming requests into operations on domain classes and then persisting the
results or returning them back to the caller. You can view the domain layer as a
collection of the application’s domain knowledge (how-to’s) and the application
services layer as a set of business use cases (what-to’s).
Communications inside your application—Hexagonal architecture prescribes a
one-way flow of dependencies: from the application services layer to the domain
layer. Classes inside the domain layer should only depend on each other; they
should not depend on classes from the application services layer. This guideline
flows from the previous one. The separation of concerns between the applica-
tion services layer and the domain layer means that the former knows about the
latter, but the opposite is not true. The domain layer should be fully isolated
from the external world.
Communications between applications—External applications connect to your
application through a common interface maintained by the application services
layer. No one has a direct access to the domain layer. Each side in a hexagon
represents a connection into or out of the application. Note that although a
Domain
(business logic)
Application
services
Third-party
system
Message
bus
SMTP
service
Figure 5.9
A hexagonal 
architecture is a set of 
interacting applications—
hexagons.


---
**Page 108**

108
CHAPTER 5
Mocks and test fragility
hexagon has six sides, it doesn’t mean your application can only connect to six
other applications. The number of connections is arbitrary. The point is that
there can be many such connections.
Each layer of your application exhibits observable behavior and contains its own set of
implementation details. For example, observable behavior of the domain layer is the
sum of this layer’s operations and state that helps the application service layer achieve
at least one of its goals. The principles of a well-designed API have a fractal nature:
they apply equally to as much as a whole layer or as little as a single class.
 When you make each layer’s API well-designed (that is, hide its implementation
details), your tests also start to have a fractal structure; they verify behavior that helps
achieve the same goals but at different levels. A test covering an application service
checks to see how this service attains an overarching, coarse-grained goal posed by the
external client. At the same time, a test working with a domain class verifies a subgoal
that is part of that greater goal (figure 5.10).
You might remember from previous chapters how I mentioned that you should be
able to trace any test back to a particular business requirement. Each test should tell a
story that is meaningful to a domain expert, and if it doesn’t, that’s a strong indication
that the test couples to implementation details and therefore is brittle. I hope now you
can see why.
 Observable behavior flows inward from outer layers to the center. The overarching
goal posed by the external client gets translated into subgoals achieved by individual
Goal
(use case)
Subgoal
Subgoal
Test 1
Test 2
Test 3
External client
Application service
Domain class 1
Domain class 2
Figure 5.10
Tests working with different layers have a fractal nature: they verify the 
same behavior at different levels. A test of an application service checks to see how 
the overall business use case is executed. A test working with a domain class verifies 
an intermediate subgoal on the way to use-case completion.


---
**Page 109**

109
The relationship between mocks and test fragility
domain classes. Each piece of observable behavior in the domain layer therefore pre-
serves the connection to a particular business use case. You can trace this connection
recursively from the innermost (domain) layer outward to the application services
layer and then to the needs of the external client. This traceability follows from the
definition of observable behavior. For a piece of code to be part of observable behav-
ior, it needs to help the client achieve one of its goals. For a domain class, the client is
an application service; for the application service, it’s the external client itself.
 Tests that verify a code base with a well-designed API also have a connection to
business requirements because those tests tie to the observable behavior only. A good
example is the User and UserController classes from listing 5.6 (I’m repeating the
code here for convenience).
public class User
{
private string _name;
public string Name
{
get => _name;
set => _name = NormalizeName(value);
}
private string NormalizeName(string name)
{
/* Trim name down to 50 characters */
}
}
public class UserController
{
public void RenameUser(int userId, string newName)
{
User user = GetUserFromDatabase(userId);
user.Name = newName;
SaveUserToDatabase(user);
}
}
UserController in this example is an application service. Assuming that the exter-
nal client doesn’t have a specific goal of normalizing user names, and all names are
normalized solely due to restrictions from the application itself, the NormalizeName
method in the User class can’t be traced to the client’s needs. Therefore, it’s an
implementation detail and should be made private (we already did that earlier in
this chapter). Moreover, tests shouldn’t check this method directly. They should ver-
ify it only as part of the class’s observable behavior—the Name property’s setter in
this example.
 This guideline of always tracing the code base’s public API to business require-
ments applies to the vast majority of domain classes and application services but less
Listing 5.8
A domain class with an application service


---
**Page 110**

110
CHAPTER 5
Mocks and test fragility
so to utility and infrastructure code. The individual problems such code solves are
often too low-level and fine-grained and can’t be traced to a specific business use case. 
5.3.2
Intra-system vs. inter-system communications
There are two types of communications in a typical application: intra-system and inter-
system. Intra-system communications are communications between classes inside your
application. Inter-system communications are when your application talks to other appli-
cations (figure 5.11).
NOTE
Intra-system communications are implementation details; inter-system
communications are not.
Intra-system communications are implementation details because the collaborations
your domain classes go through in order to perform an operation are not part of their
observable behavior. These collaborations don’t have an immediate connection to the
client’s goal. Thus, coupling to such collaborations leads to fragile tests.
 Inter-system communications are a different matter. Unlike collaborations between
classes inside your application, the way your system talks to the external world forms
the observable behavior of that system as a whole. It’s part of the contract your appli-
cation must hold at all times (figure 5.12).
 This attribute of inter-system communications stems from the way separate applica-
tions evolve together. One of the main principles of such an evolution is maintaining
backward compatibility. Regardless of the refactorings you perform inside your sys-
tem, the communication pattern it uses to talk to external applications should always
stay in place, so that external applications can understand it. For example, messages
your application emits on a bus should preserve their structure, the calls issued to an
SMTP service should have the same number and type of parameters, and so on.
Third-party
system
SMTP service
Intra-system
Inter-system
Inter-system
Figure 5.11
There are two types 
of communications: intra-system 
(between classes inside the 
application) and inter-system 
(between applications).


