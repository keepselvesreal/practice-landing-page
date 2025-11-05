# 5.3.2 Intra-system vs. inter-system communications (pp.110-111)

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


---
**Page 111**

111
The relationship between mocks and test fragility
The use of mocks is beneficial when verifying the communication pattern between
your system and external applications. Conversely, using mocks to verify communica-
tions between classes inside your system results in tests that couple to implementation
details and therefore fall short of the resistance-to-refactoring metric.
5.3.3
Intra-system vs. inter-system communications: An example
To illustrate the difference between intra-system and inter-system communications, I’ll
expand on the example with the Customer and Store classes that I used in chapter 2
and earlier in this chapter. Imagine the following business use case:
A customer tries to purchase a product from a store.
If the amount of the product in the store is sufficient, then
– The inventory is removed from the store.
– An email receipt is sent to the customer.
– A confirmation is returned.
Let’s also assume that the application is an API with no user interface.
 In the following listing, the CustomerController class is an application service that
orchestrates the work between domain classes (Customer, Product, Store) and the
external application (EmailGateway, which is a proxy to an SMTP service).
public class CustomerController
{
public bool Purchase(int customerId, int productId, int quantity)
Listing 5.9
Connecting the domain model with external applications
Third-party
system
SMTP service
Implementation detail
Observable behavior (contract)
Observable behavior (contract)
Figure 5.12
Inter-system communications form the observable 
behavior of your application as a whole. Intra-system communications 
are implementation details.


