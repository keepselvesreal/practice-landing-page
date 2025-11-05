# 2.4.12 How does this work with classes and state? (pp.57-59)

---
**Page 57**

57
Specification-based testing in the real world
2.4.10 Go for parameterized tests when tests have the same skeleton
A little duplication is never a problem, but a lot of duplication is. We created 21 differ-
ent tests for the substringsBetween program. The test code was lean because we
grouped some of the test cases into single test methods. Imagine writing 21 almost-
identical test cases. If each method took 5 lines of code, we would have a test class with
21 methods and 105 lines. This is much longer than the test suite with the parameter-
ized test that we wrote.
 Some developers argue that parameterized tests are confusing. Deciding whether
to use JUnit test cases or parameterized tests is, most of all, a matter of taste. I use
parameterized tests when the amount of duplication in my test suite is too large. In
this chapter, I leaned more toward JUnit test cases: lots of test cases logically grouped
in a small set of test methods. We discuss test code quality further in chapter 10. 
2.4.11 Requirements can be of any granularity
The seven-step approach I propose in this chapter works for requirements of any
granularity. Here, we applied it in a specification that could be implemented by a sin-
gle method. However, nothing prevents you from using it with larger requirements
that involve many classes. Traditionally, specification-based testing techniques focus
on black-box testing: that is, testing an entire program or feature, rather than unit-
testing specific components. I argue that these ideas also make sense at the unit level.
 When we discuss larger tests (integration testing), we will also look at how to devise
test cases for sets of classes or components. The approach is the same: reflect on the
inputs and their expected outputs, divide the domain space, and create test cases. You
can generalize the technique discussed here to tests at any level. 
2.4.12 How does this work with classes and state?
The two methods we tested in this chapter have no state, so all we had to do was think
of inputs and outputs. In object-oriented systems, classes have state. Imagine a Shop-
pingCart class and a behavior totalPrice() that requires some CartItems to be
inserted before the method can do its job. How do we apply specification-based test-
ing in this case? See the following listing.
public class ShoppingCart {
  private List<CartItem> items = new ArrayList<CartItem>();
  public void add(CartItem item) {   
    this.items.add(item);
  }
  public double totalPrice() {   
    double totalPrice = 0;
    for (CartItem item : items) {
Listing 2.14
ShoppingCart and CartItem classes
Adds items 
to the cart
Loops through all the items 
and sums up the final price


---
**Page 58**

58
CHAPTER 2
Specification-based testing
      totalPrice += item.getUnitPrice() * item.getQuantity();
    }
    return totalPrice;
  }
}
public class CartItem {   
  private final String product;
  private final int quantity;
  private final double unitPrice;
  public CartItem(String product, int quantity,
   double unitPrice) {
    this.product = product;
    this.quantity = quantity;
    this.unitPrice = unitPrice;
  }
  // getters
}
Nothing changes in the way we approach specification-based testing. The only differ-
ence is that when we reflect about the method under test, we must consider not only
the possible input parameters, but also the state the class should be in. For this spe-
cific example, looking at the expected behavior of the totalPrice method, I can
imagine tests exercising the behavior of the method when the cart has zero items, a
single item, multiple items, and various quantities (plus corner cases such as nulls).
All we do differently is to set up the class’s state (by adding multiple items to the cart)
before calling the method we want to test, as in the following listing.
import org.junit.jupiter.api.Test;
import static org.assertj.core.api.Assertions.assertThat;
public class ShoppingCartTest {
  private final ShoppingCart cart = new ShoppingCart();   
  @Test
  void noItems() {
    assertThat(cart.totalPrice())   
      .isEqualTo(0);
  }
  @Test
  void itemsInTheCart() {
    cart.add(new CartItem("TV", 1, 120));
    assertThat(cart.totalPrice())   
      .isEqualTo(120);
Listing 2.15
Tests for the ShoppingCart class
A simple class that 
represents an item 
in the cart
Having the cart as a 
field means we don’t 
have to instantiate it 
for every test. This is 
a common technique 
to improve legibility.
Asserts that 
an empty cart 
returns 0
Asserts that it 
works for a single 
item in the cart …


---
**Page 59**

59
Exercises
    cart.add(new CartItem("Chocolate", 2, 2.5));
    assertThat(cart.totalPrice())   
      .isEqualTo(120 + 2.5*2);
  }
}
Again, the mechanics are the same. We just have to take more into consideration when
engineering the test cases. 
2.4.13 The role of experience and creativity
If two testers performed the specification-based testing technique I described earlier
in the same program, would they develop the same set of tests? Ideally, but possibly
not. In the substringsBetween() example, I would expect most developers to come
up with similar test cases. But it is not uncommon for developers to approach a prob-
lem from completely different yet correct angles.
 I am trying to reduce the role of experience and creativity by giving developers a
process that everybody can follow, but in practice, experience and creativity make a
difference in testing. We observed that in a small controlled experiment (Yu, Treude,
and Aniche, 2019).
 In the substringsBetween() example, experienced testers may see more compli-
cated test cases, but a novice tester may have difficulty spotting those. A more experi-
enced tester may realize that spaces in the string play no role and skip this test,
whereas a novice developer may be in doubt and write an extra “useless” test. This is
why I like the specification-based testing systematic approach I described in this
chapter: it will help you remember what to think about. But it is still up to you to do
the thinking!
Exercises
2.1
Which statement is false about applying the specification-based testing method
on the following Java method?
/**
 * Puts the supplied value into the Map,
 * mapped by the supplied key.
 * If the key is already in the map, its
 * value will be replaced by the new value.
 *
 * NOTE: Nulls are not accepted as keys;
 *  a RuntimeException is thrown when key is null.
 *
 * @param key the key used to locate the value
 * @param value the value to be stored in the HashMap
 * @return the prior mapping of the key,
 *  or null if there was none.
*/
public V put(K key, V value) {
  // implementation here
}
… as well as for 
many items in 
the cart.


