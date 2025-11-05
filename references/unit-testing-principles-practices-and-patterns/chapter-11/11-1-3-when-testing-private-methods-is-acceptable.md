# 11.1.3 When testing private methods is acceptable (pp.261-263)

---
**Page 261**

261
Unit testing private methods
return basePrice - discounts + taxes;
}
}
The GenerateDescription() method is quite simple: it returns a generic description
of the order. But it uses the private GetPrice() method, which is much more com-
plex: it contains important business logic and needs to be thoroughly tested. That
logic is a missing abstraction. Instead of exposing the GetPrice method, make this
abstraction explicit by extracting it into a separate class, as shown in the next listing.
public class Order
{
private Customer _customer;
private List<Product> _products;
public string GenerateDescription()
{
var calc = new PriceCalculator();
return $"Customer name: {_customer.Name}, " +
$"total number of products: {_products.Count}, " +
$"total price: {calc.Calculate(_customer, _products)}";
}
}
public class PriceCalculator
{
public decimal Calculate(Customer customer, List<Product> products)
{
decimal basePrice = /* Calculate based on products */;
decimal discounts = /* Calculate based on customer */;
decimal taxes = /* Calculate based on products */;
return basePrice - discounts + taxes;
}
}
Now you can test PriceCalculator independently of Order. You can also use the
output-based (functional) style of unit testing, because PriceCalculator doesn’t
have any hidden inputs or outputs. See chapter 6 for more information about styles
of unit testing. 
11.1.3 When testing private methods is acceptable
There are exceptions to the rule of never testing private methods. To understand
those exceptions, we need to revisit the relationship between the code’s publicity and
purpose from chapter 5. Table 11.1 sums up that relationship (you already saw this
table in chapter 5; I’m copying it here for convenience).
Listing 11.2
Extracting the complex private method


---
**Page 262**

262
CHAPTER 11
Unit testing anti-patterns
As you might remember from chapter 5, making the observable behavior public and
implementation details private results in a well-designed API. On the other hand,
leaking implementation details damages the code’s encapsulation. The intersection of
observable behavior and private methods is marked N/A in the table because for a
method to become part of observable behavior, it has to be used by the client code,
which is impossible if that method is private.
 Note that testing private methods isn’t bad in and of itself. It’s only bad because
those private methods are a proxy for implementation details. Testing implementa-
tion details is what ultimately leads to test brittleness. Having that said, there are rare
cases where a method is both private and part of observable behavior (and thus the
N/A marking in table 11.1 isn’t entirely correct).
 Let’s take a system that manages credit inquiries as an example. New inquiries are
bulk-loaded directly into the database once a day. Administrators then review those
inquiries one by one and decide whether to approve them. Here’s how the Inquiry
class might look in that system.
public class Inquiry
{
public bool IsApproved { get; private set; }
public DateTime? TimeApproved { get; private set; }
private Inquiry(
  
bool isApproved, DateTime? timeApproved)  
{
if (isApproved && !timeApproved.HasValue)
throw new Exception();
IsApproved = isApproved;
TimeApproved = timeApproved;
}
public void Approve(DateTime now)
{
if (IsApproved)
return;
IsApproved = true;
TimeApproved = now;
}
}
Table 11.1
The relationship between the code’s publicity and purpose
Observable behavior
Implementation detail
Public
Good
Bad
Private
N/A
Good
Listing 11.3
A class with a private constructor
Private 
constructor


---
**Page 263**

263
Exposing private state
The private constructor is private because the class is restored from the database by an
object-relational mapping (ORM) library. That ORM doesn’t need a public construc-
tor; it may well work with a private one. At the same time, our system doesn’t need a
constructor, either, because it’s not responsible for the creation of those inquiries.
 How do you test the Inquiry class given that you can’t instantiate its objects? On
the one hand, the approval logic is clearly important and thus should be unit tested.
But on the other, making the constructor public would violate the rule of not expos-
ing private methods.
 Inquiry’s constructor is an example of a method that is both private and part of
the observable behavior. This constructor fulfills the contract with the ORM, and the
fact that it’s private doesn’t make that contract less important: the ORM wouldn’t be
able to restore inquiries from the database without it.
 And so, making Inquiry’s constructor public won’t lead to test brittleness in this par-
ticular case. In fact, it will arguably bring the class’s API closer to being well-designed.
Just make sure the constructor contains all the preconditions required to maintain its
encapsulation. In listing 11.3, such a precondition is the requirement to have the
approval time in all approved inquiries.
 Alternatively, if you prefer to keep the class’s public API surface as small as possi-
ble, you can instantiate Inquiry via reflection in tests. Although this looks like a hack,
you are just following the ORM, which also uses reflection behind the scenes. 
11.2
Exposing private state
Another common anti-pattern is exposing private state for the sole purpose of unit
testing. The guideline here is the same as with private methods: don’t expose state
that you would otherwise keep private—test observable behavior only. Let’s take a
look at the following listing.
public class Customer
{
private CustomerStatus _status =   
CustomerStatus.Regular;
   
public void Promote()
{
_status = CustomerStatus.Preferred;
}
public decimal GetDiscount()
{
return _status == CustomerStatus.Preferred ? 0.05m : 0m;
}
}
public enum CustomerStatus
{
Listing 11.4
A class with private state
Private 
state


