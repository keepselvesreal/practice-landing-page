# 4.2 Invariants (pp.102-105)

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


---
**Page 103**

103
Invariants
  assert basket.containsKey(product) :
   "Product was not inserted in the basket"; 
}
You could model other post-conditions here, such as “the new total value should be
greater than the previous total value.” Java does not provide an easy way to do that, so
we need extra code to keep the old total value, which we use in the post-condition
check (see listing 4.8). Interestingly, in languages like Eiffel, doing so would not
require an extra variable! Those languages provide old and new values of variables to
facilitate the post-condition check.
public void add(Product product, int qtyToAdd) {
  assert product != null : "Product is required";
  assert qtyToAdd > 0 : "Quantity has to be greater than zero";
  BigDecimal oldTotalValue = totalValue; 
  // add the product in the basket
  // update the total value
  assert basket.containsKey(product) :
    "Product was not inserted in the basket";
  assert totalValue.compareTo(oldTotalValue) == 1 :
    "Total value should be greater than
    ➥ previous total value"; 
}
NOTE
We use the BigDecimal class here instead of a simple double. Big-
Decimals are recommended whenever you want to avoid rounding issues that
may happen when you use doubles. Check your programming language for
how to do that. BigDecimal gives us precision, but it is verbose. In listing 4.8,
for example, we have to use the compareTo method to compare two Big-
Decimals, which is more complicated than a > b. Another trick is to represent
money in cents and use integer or long as the types, but that is beyond the
scope of this book.
Now for the pre-conditions of the remove() method. The product should not be null;
moreover, the product to be removed needs to be in the basket. If the product is not
in the basket, how can you remove it? As a post-condition, we can ensure that, after
the removal, the product is no longer in the basket. See the implementation of both
pre- and post-conditions in the following listing.
public void remove(Product product) {
  assert product != null : "product can't be null";                   
  assert basket.containsKey(product) : "Product must already be in the
  ➥ basket";                                                         
Listing 4.8
Another post-condition for Basket's add method
Listing 4.9
Pre- and post-conditions for the remove method
Post-condition ensuring 
that the product was 
added to the cart
For the post-condition to 
happen, we need to save 
the old total value.
The post-condition ensures 
that the total value is 
greater than before.
Pre-conditions: the product cannot be
null, and it must exist in the basket.


---
**Page 104**

104
CHAPTER 4
Designing contracts
  // ...
  // remove the product from the basket
  // update the total value
  // ...
  assert !basket.containsKey(product) : "Product is still in the  
  ➥ basket";                                                     
}
We are finished with the pre- and post-conditions. It is time to model the class invari-
ants. Regardless of products being added to and removed from the basket, the total
value of the basket should never be negative. This is not a pre-condition nor a post-
condition: this is an invariant, and the class is responsible for maintaining it. For the
implementation, you can use assertions or ifs or whatever your programming lan-
guage offers. Whenever a method that manipulates the totalValue field is called, we
ensure that totalValue is still a positive number at the end of the method. See the
implementation of the invariants in the following listing.
public class Basket {
  private BigDecimal totalValue = BigDecimal.ZERO;
  private Map<Product, Integer> basket = new HashMap<>();
  public void add(Product product, int qtyToAdd) {
    assert product != null : "Product is required";
    assert qtyToAdd > 0 : "Quantity has to be greater than zero";
    BigDecimal oldTotalValue = totalValue;
    // add the product in the basket
    // update the total value
    assert basket.containsKey(product) : "Product was not inserted in
    ➥ the basket";
    assert totalValue.compareTo(oldTotalValue) == 1 : "Total value should
    ➥ be greater than previous total value";
    assert totalValue.compareTo(BigDecimal.ZERO) >= 0 :
      "Total value can't be negative." 
  }
  public void remove(Product product) {
    assert product != null : "product can't be null";
    assert basket.containsKey(product) : "Product must already be in the 
basket";
    ➥ 
    // remove the product from the basket
    // update the total value
    assert !basket.containsKey(product) : "Product is still in the basket";
    assert totalValue.compareTo(BigDecimal.ZERO) >= 0 : 
      "Total value can't be negative."
  }
}
Listing 4.10
Invariants of the Basket class
Post-condition: the product
is no longer in the basket.
The invariant ensures that the total 
value is greater than or equal to 0.
The same invariant 
check for the remove


---
**Page 105**

105
Changing contracts, and the Liskov substitution principle
Because the invariant checking may happen at the end of all the methods of a class,
you may want to reduce duplication and create a method for such checks, such as the
invariant() method in listing 4.11. We call invariant() at the end of every public
method: after each method does its business (and changes the object’s state), we want
to ensure that the invariants hold.
public class Basket {
  public void add(Product product, int qtyToAdd) {
    // ... method here ...
    assert invariant() : "Invariant does not hold";
  }
  public void remove(Product product) {
    // ... method here ...
    assert invariant() : "Invariant does not hold";
  }
  private boolean invariant() {
    return totalValue.compareTo(BigDecimal.ZERO) >= 0;
  }
}
Note that invariants may not hold, say, in the middle of the method execution. The
method may break the invariants for a second, as part of its algorithm. However, the
method needs to ensure that, in the end, the invariants hold.
NOTE
You might be curious about the concrete implementation of the Bas-
ket class and how we would test it. We cannot test all possible combinations of
method calls (adds and removes, in any order). How would you tackle this?
We get to property-based testing in chapter 5. 
4.3
Changing contracts, and the Liskov substitution 
principle
What happens if we change the contract of a class or method? Suppose the calculate-
Tax method we discussed earlier needs new pre-conditions. Instead of “value
should be greater than or equal to 0,” they are changed to “value should be greater
than or equal to 100.” What impact would this change have on the system and our
test suites? Or suppose the add method from the previous section, which does not
accept null as product, now accepts it. What is the impact of this decision? Do these
two changes impact the system in the same way, or does one change have less impact
than the other?
 In an ideal world, we would not change the contract of a class or method after we
define it. In the real world, we are sometimes forced to do so. While there may not be
anything we can do to prevent the change, we can understand its impact. If you do not
Listing 4.11
invariant() method for the invariant check


