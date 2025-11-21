# 11.2 Exposing private state (pp.263-264)

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


---
**Page 264**

264
CHAPTER 11
Unit testing anti-patterns
Regular,
Preferred
}
This example shows a Customer class. Each customer is created in the Regular status
and then can be promoted to Preferred, at which point they get a 5% discount on
everything.
 How would you test the Promote() method? This method’s side effect is a change
of the _status field, but the field itself is private and thus not available in tests. A
tempting solution would be to make this field public. After all, isn’t the change of sta-
tus the ultimate goal of calling Promote()?
 That would be an anti-pattern, however. Remember, your tests should interact with the
system under test (SUT) exactly the same way as the production code and shouldn’t have any spe-
cial privileges. In listing 11.4, the _status field is hidden from the production code and
thus is not part of the SUT’s observable behavior. Exposing that field would result in
coupling tests to implementation details. How to test Promote(), then?
 What you should do, instead, is look at how the production code uses this class. In
this particular example, the production code doesn’t care about the customer’s status;
otherwise, that field would be public. The only information the production code does
care about is the discount the customer gets after the promotion. And so that’s what
you need to verify in tests. You need to check that
A newly created customer has no discount.
Once the customer is promoted, the discount becomes 5%.
Later, if the production code starts using the customer status field, you’d be able to
couple to that field in tests too, because it would officially become part of the SUT’s
observable behavior.
NOTE
Widening the public API surface for the sake of testability is a bad practice. 
11.3
Leaking domain knowledge to tests
Leaking domain knowledge to tests is another quite common anti-pattern. It usually
takes place in tests that cover complex algorithms. Let’s take the following (admit-
tedly, not that complex) calculation algorithm as an example:
public static class Calculator
{
public static int Add(int value1, int value2)
{
return value1 + value2;
}
}
This listing shows an incorrect way to test it.


