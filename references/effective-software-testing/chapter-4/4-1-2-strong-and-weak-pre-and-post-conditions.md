# 4.1.2 Strong and weak pre- and post-conditions (pp.100-102)

---
**Page 100**

100
CHAPTER 4
Designing contracts
    assert value >= 0 : "Value cannot be negative"; 
    double taxValue = 0;
    // some complex business rule here...
    // final value goes to 'taxValue'
    assert taxValue >= 0 : "Calculated tax value
    ➥ cannot be negative."; 
    return taxValue;
  }
}
Deciding whether to use assert instructions or simple if statements that throw
exceptions is something to discuss with your team members. I’ll give you my opinion
about it later in section 4.5.3.
 The assert instruction can be disabled via a parameter to the JVM, so it does not
have to be executed at all times. If you disable it in production, for example, the pre-
conditions will not be checked while running the system. If you do not have full con-
trol of your production environment, you may want to opt for exceptions so you can
be sure your pre-conditions will be checked.
 An argument against the use of asserts is that they always throw AssertionError,
which is a generic error. Sometimes you may want to throw a more specific exception
that the caller can handle. For simplicity, I make use of assert in the remainder of
this chapter.
 Later in this chapter, we differentiate between pre-conditions and validations. This
may also be taken into account when deciding between asserts and exceptions. 
4.1.2
Strong and weak pre- and post-conditions
When defining pre- and post-conditions, an important decision is how weak or strong
you want them to be. In the previous example, we handle the pre-condition very
strongly: if a negative value comes in, it violates the pre-condition of the method, so
we halt the program.
 One way to avoid halting the program due to negative numbers would be to
weaken the pre-condition. In other words, instead of accepting only values that are
greater than zero, the method could accept any value, positive or negative. We could
do this by removing the if statement, as shown in the following listing (the developer
would have to find a way to take negative numbers into account and handle them).
public double calculateTax(double value) {
  
  // method continues ...
}
Listing 4.4
TaxCalculator with a weaker pre-condition
The same pre-condition, 
now as an assert 
statement
The same post-condition, 
now as an assert 
statement
No pre-conditions 
check; any value 
is valid.


---
**Page 101**

101
Pre-conditions and post-conditions
Weaker pre-conditions make it easier for other classes to invoke the method. After all,
regardless of the value you pass to calculateTax, the program will return something.
This is in contrast to the previous version, where a negative number throws an error.
 There is no single answer for whether to use weaker or stronger pre-conditions. It
depends on the type of system you are developing as well as what you expect from the
consumers of the class you are modeling. I prefer stronger conditions, as I believe they
reduce the range of mistakes that may happen in the code. However, this means I spend
more time encoding these conditions as assertions, so my code becomes more complex.
In some cases, you cannot weaken the pre-condition. For the tax calculation, there is
no way to accept negative values, and the pre-condition should be strong. Pragmati-
cally speaking, another way of handling such a case is to return an error value. For
example, if a negative number comes in, the program can return 0 instead of halting,
as in the following listing.
public double calculateTax(double value) {
  // pre-condition check
  if(value < 0) { 
    return 0;
  }
  // method continues ...
}
While this approach simplifies the clients’ lives, they now have to be aware that if they
receive a 0, it might be because of invalid input. Perhaps the method could return –1
to differentiate from zero taxes. Deciding between a weaker pre-condition or an error
value is another decision to make after considering all the possibilities.
 For those that know the original theory of design-by-contracts: we do not weaken
the pre-condition here to make it easier for clients to handle the outcomes of the
method. We decided to return an error code instead of throwing an exception. In the
remainder of this chapter, you see that my perspective on contracts is more pragmatic
than that in the original design-by-contract paper by Meyer in 1992. What matters to
me is reflecting on what classes and methods can and cannot handle and what they
should do in case a violation happens. 
Can you apply the same reasoning to post-conditions?
You may find a reason to return a value instead of throwing an exception. To be hon-
est, I cannot recall a single time I’ve done that. In the TaxCalculator example, a
negative number would mean there was a bug in the implementation, and you prob-
ably do not want someone to pay zero taxes.
Listing 4.5
TaxCalculator returning an error code instead of an exception
If the pre-condition does not hold, 
the method returns 0. The client of 
this method does not need to worry 
about exceptions.


---
**Page 102**

102
CHAPTER 4
Designing contracts
4.2
Invariants
We have seen that pre-conditions should hold before a method’s execution, and post-
conditions should hold after a method’s execution. Now we move on to conditions
that must always hold before and after a method’s execution. These conditions are
called invariants. An invariant is thus a condition that holds throughout the entire life-
time of an object or a data structure.
 Imagine a Basket class that stores the products the user is buying from an online
shop. The class offers methods such as add(Product p, int quantity), which adds a
product p a quantity number of times, and remove(Product p), which removes the
product completely from the cart. Here is a skeleton of the class.
public class Basket {
  private BigDecimal totalValue = BigDecimal.ZERO; 
  private Map<Product, Integer> basket = new HashMap<>();
  public void add(Product product, int qtyToAdd) { 
    // add the product
    // update the total value
  }
  public void remove(Product product) { 
    // remove the product from the basket
    // update the total value
  }
}
Before we talk about invariants, let’s focus on the method’s pre- and post-conditions.
For the add() method, we can ensure that the product is not null (you cannot add
a null product to the cart) and that the quantity is greater than 0 (you cannot buy a
product 0 or fewer times). In addition, a clear post-condition is that the product is
now in the basket. Listing 4.7 shows the implementation. Note that I am using Java’s
assert method to express the pre-condition, which means I must have assertions
enabled in my JVM when I run the system. You could also use a simple if statement,
as I showed earlier.
public void add(Product product, int qtyToAdd) {
  assert product != null : "Product is required"; 
  assert qtyToAdd > 0 : "Quantity has to be greater than zero"; 
  // ...
  // add the product in the basket
  // update the total value
  // ...
Listing 4.6
The Basket class
Listing 4.7
Basket's add method with its pre-conditions
We use BigDecimal 
instead of double to avoid 
rounding issues in Java.
Adds the product to the 
cart and updates the 
total value of the cart
Removes a product from 
the cart and updates its 
total value
Pre-condition ensuring 
that product is not null
Pre-condition ensuring
that qtyToAdd is
greater than 0


