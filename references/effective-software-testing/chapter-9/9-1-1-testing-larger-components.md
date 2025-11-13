# 9.1.1 Testing larger components (pp.216-224)

---
**Page 216**

216
CHAPTER 9
Writing larger tests
9.1
When to use larger tests
I see two situations where you should use a larger test:
You have exercised each class individually, but the overall behavior is composed
of many classes, and you want to see them work together. Think of a set of
classes that calculates the final cost of a shopping cart. You have unit-tested the
class responsible for business rule 1 and the class responsible for business rule 2.
But you still want to see the final cost of the shopping cart after all the rules
have been applied to it.
The class you want to test is a component in a larger plug-and-play architecture.
One of the main advantages of object-oriented design is that we can encapsu-
late and abstract repetitive complexity, so the user only has to implement what
matters. Think of a plugin for your favorite IDE (in my case, IntelliJ). You can
develop the logic of the plugin, but many actions will only happen when IntelliJ
calls the plugin and passes parameters to it.
The following sections show examples of both cases and will help you generalize
them.
9.1.1
Testing larger components
As always, let’s use a concrete example. Suppose we have the following requirement:
Given a shopping cart with items, quantities, and respective unit prices, the
final price of the cart is calculated as follows:
The final price of each item is calculated by multiplying its unit price by
the quantity.
The delivery costs are the following. For shopping carts with
– 1 to 3 elements (inclusive), we charge 5 dollars extra.
– 4 to 10 elements (inclusive), we charge 12.5 dollars extra.
– More than 10 elements, we charge 20 dollars extra.
If there is an electronic item in the cart, we charge 7.5 dollars extra.
NOTE
The business rule related to delivery costs is not realistic. As a devel-
oper, when you notice such inconsistencies, you should talk to the stake-
holder, product owner, or whomever is sponsoring that feature. I am keeping
this business rule simple for the sake of the example.
Before I begin coding, I think about how to approach the problem. I see how the
final price is calculated and that a list of rules is applied to the shopping cart. My
experience with software design and design for testability tells me that each rule
should be in its own class—putting everything in a single class would result in a large
class, which would require lots of tests. We prefer small classes that require only a
handful of tests.


---
**Page 217**

217
When to use larger tests
 Suppose the ShoppingCart and Item classes already exist in our code base. They are
simple entities. ShoppingCart holds a list of Items. An Item is composed of a name, a
quantity, a price per unit, and a type indicating whether this item is a piece of electronics.
 Let’s define the contract that all the prices have in common. Listing 9.1 shows the
PriceRule interface that all the price rules will follow. It receives a ShoppingCart and
returns the value that should be aggregated to the final price of the shopping cart.
Aggregating all the price rules will be the responsibility of another class, which we will
code later.
public interface PriceRule {
    double priceToAggregate(ShoppingCart cart);
}
We begin with the DeliveryPrice price rule. It is straightforward, as its value depends
solely on the number of items in the cart.
public class DeliveryPrice implements PriceRule {
  @Override
  public double priceToAggregate(ShoppingCart cart) {
    int totalItems = cart.numberOfItems();      
    if(totalItems == 0)   
      return 0;
    if(totalItems >= 1 && totalItems <= 3)
      return 5;
    if(totalItems >= 4 && totalItems <= 10)
      return 12.5;
    return 20.0;
  }
}
NOTE
I am using double to represent prices for illustration purposes, but as
discussed before, that would be a poor choice in real life. You may prefer to
use BigDecimal or represent prices using integers or longs.
With the implementation ready, let’s test it as we have learned: with unit testing. The
class is so small and localized that it makes sense to exercise it via unit testing. We will
apply specification-based and, more importantly, boundary testing (discussed in chap-
ter 2). The requirements contain clear boundaries, and these boundaries are continu-
ous (1 to 3 items, 4 to 10 items, more than 10 items). This means we can test each
rule’s on and off points:
0 items
1 item
Listing 9.1
PriceRule interface
Listing 9.2
Implementation of DeliveryPrice
Gets the number of items 
in the cart. The delivery 
price is based on this.
These if statements based 
on the requirements are 
enough to return the 
price.


---
**Page 218**

218
CHAPTER 9
Writing larger tests
3 items
4 items
10 items
More than 10 items (with 11 being the off point)
NOTE
Notice the “0 items” handler: the requirements do not mention that
case. But I was thinking of the class’s pre-conditions and decided that if the
cart has no items, the price should return 0. This corner case deserves a test.
We use a parameterized test and comma-separated values (CSV) source to implement
the JUnit test.
public class DeliveryPriceTest {
  @ParameterizedTest
  @CsvSource({    
    "0,0",
    "1,5",
    "3,5",
    "4,12.5",
    "10,12.5",
    "11,20"})
  void deliveryIsAccordingToTheNumberOfItems(int noOfItems,
    ➥ double expectedDeliveryPrice) {
    ShoppingCart cart = new ShoppingCart();   
    for(int i = 0; i < noOfItems; i++) {
      cart.add(new Item(ItemType.OTHER, "ANY", 1, 1));
    }
    double price = new DeliveryPrice().priceToAggregate(cart);  
    assertThat(price).isEqualTo(expectedDeliveryPrice);  
  }
}
Listing 9.3
Tests for DeliveryPrice
Refactoring to achieve 100% code coverage
This example illustrates why you cannot blindly use code coverage. If you generate
the report, you will see that the tool does not report 100% branch coverage! In fact,
only three of the five conditions are fully exercised: totalItems >= 1 and total-
Items >= 4 are not.
Why? Let’s take the first case as an example. We have lots of tests where the num-
ber of items is greater than 1, so the true branch of this condition is exercised. But
how can we exercise the false branch? We would need a number of items less than
1. We have a test where the number of items is zero, but the test never reaches that
Exercises the six boundaries. 
The first value is the number 
of items in the cart; the 
second is the expected 
delivery price.
Creates a shopping cart and 
adds the specified number 
of items to it. The type, 
name, quantity, and unit 
price do not matter.
Calls the
DeliveryPrice
rule …
… and asserts 
its output.


---
**Page 219**

219
When to use larger tests
Next, we implement ExtraChargeForElectronics. The implementation is also
straightforward, as all we need to do is check whether the cart contains any electron-
ics. If so, we add the extra charge.
public class ExtraChargeForElectronics implements PriceRule {
  @Override
  public double priceToAggregate(ShoppingCart cart) {
    List<Item> items = cart.getItems();
    boolean hasAnElectronicDevice = items
      .stream()
      .anyMatch(it -> it.getType() == ItemType.ELECTRONIC);   
    if(hasAnElectronicDevice)   
      return 7.50;
    return 0;   
  }
}
We have three cases to exercise: no electronics in the cart, one or more electronics in
the cart, and an empty cart. Let’s implement them in three test methods. First, the fol-
lowing test exercises the “one or more electronics” case. We can use parameterized
tests to try this.
 
 
condition because an early return happens in totalItems == 0. Pragmatically
speaking, we have covered all the branches, but the tool cannot see it.
One idea is to rewrite the code so this is not a problem. In the following code, the
implementation is basically the same, but the sequence of if statements is written
such that the tool can report 100% branch coverage:
public double priceToAggregate(ShoppingCart cart) {
  int totalItems = cart.numberOfItems();
  if(totalItems == 0)
    return 0;
  if(totalItems <= 3)   
    return 5;
  if(totalItems <= 10)   
    return 12.5;
  return 20.0;
}
Listing 9.4
ExtraChargeForElectronics implementation
We do not need to check totalItems >= 1, 
as that is the only thing that can happen if 
we reach this if statement.
Same here: no 
need to check 
totalItems >= 4
Looks for any item
whose type is equal to
ELECTRONIC
If there is at least one 
such item, we return 
the extra charge.
Otherwise, we do not 
add an extra charge.


---
**Page 220**

220
CHAPTER 9
Writing larger tests
public class ExtraChargeForElectronicsTest {
  @ParameterizedTest
  @CsvSource({"1", "2"})    
  void chargeTheExtraPriceIfThereIsAnyElectronicInTheCart(
    ➥ int numberOfElectronics) {
    ShoppingCart cart = new ShoppingCart();
    for(int i = 0; i < numberOfElectronics; i++) {      
      cart.add(new Item(ItemType.ELECTRONIC, "ANY ELECTRONIC", 1, 1));
    }
    double price = new ExtraChargeForElectronics().priceToAggregate(cart);
    assertThat(price).isEqualTo(7.50);  
  }
}
We then test that no extra charges are added when there are no electronics in the cart
(see listing 9.6).
NOTE
If you read chapter 5, you may wonder if we should write a property-
based test in this case. The implementation is straightforward, and the num-
ber of electronic items does not significantly affect how the algorithm works,
so I am fine with example-based testing here.
@Test
void noExtraChargesIfNoElectronics() {
  ShoppingCart cart = new ShoppingCart();  
  cart.add(new Item(ItemType.OTHER, "BOOK", 1, 1));
  cart.add(new Item(ItemType.OTHER, "CD", 1, 1));
  cart.add(new Item(ItemType.OTHER, "BABY TOY", 1, 1));
  double price = new ExtraChargeForElectronics().priceToAggregate(cart);
  assertThat(price).isEqualTo(0);    
}
Finally, we test the case where there are no items in the shopping cart.
@Test
void noItems() {
  ShoppingCart cart = new ShoppingCart();
Listing 9.5
Testing the extra charge for electronics
Listing 9.6
Testing for no extra charge for electronics
Listing 9.7
No items in the shopping cart, so no electronics charge
The parameterized test will run a test with one electronic item in the cart and 
another test with two electronic items in the cart. We want to ensure that having 
multiple electronics in the cart does not incur incorrect extra charges.
A simple loop that adds 
the specified number of 
electronics. We could 
also have added a non-
electronic item. Would 
that make the test 
stronger?
Asserts that the extra 
electronics price is charged
Creates a cart with 
random items, all 
non-electronic
Asserts that nothing 
is charged


---
**Page 221**

221
When to use larger tests
  double price = new ExtraChargeForElectronics().priceToAggregate(cart);
  assertThat(price).isEqualTo(0);     
}
The final rule to implement is PriceOfItems, which navigates the list of items and cal-
culates the unit price times the quantity of each item. I do not show the code and the
test, to save space; they are available in the book’s code repository.
 Let’s go to the class that aggregates all the price rules and calculates the final price.
The FinalPriceCalculator class receives a list of PriceRules in its constructor. Its
calculate method receives a ShoppingCart, passes it to all the price rules, and
returns the aggregated price.
public class FinalPriceCalculator {
  private final List<PriceRule> rules;
  public FinalPriceCalculator(List<PriceRule> rules) {  
    this.rules = rules;
  }
  public double calculate(ShoppingCart cart) {
    double finalPrice = 0;
    for (PriceRule rule : rules) {   
      finalPrice += rule.priceToAggregate(cart);
    }
    return finalPrice;     
  }
}
We can easily unit-test this class: all we need to do is stub a set of PriceRules. Listing 9.9
creates three price rule stubs. Each returns a different value, including 0, as 0 may
happen. We then create a very simple shopping cart—its items do not matter, because
we are mocking the price rules.
public class FinalPriceCalculatorTest {
  @Test
  void callAllPriceRules() {
    PriceRule rule1 = mock(PriceRule.class);      
    PriceRule rule2 = mock(PriceRule.class);
    PriceRule rule3 = mock(PriceRule.class);
    ShoppingCart cart = new ShoppingCart();   
    cart.add(new Item(ItemType.OTHER, "ITEM", 1, 1));
Listing 9.8
FinalPriceCalculator that runs all the PriceRules
Listing 9.9
Testing FinalPriceCalculator
The shopping cart is empty, 
so nothing is charged.
Receives a list of 
price rules in the 
constructor. This 
class is flexible and 
can receive any 
combination of 
price rules.
For each price rule, 
gets the price to add 
to the final price
Returns the final 
aggregated price
Creates three 
different stubs 
of price rules
Creates a 
simple cart


---
**Page 222**

222
CHAPTER 9
Writing larger tests
    when(rule1.priceToAggregate(cart)).thenReturn(1.0);   
    when(rule2.priceToAggregate(cart)).thenReturn(0.0);
    when(rule3.priceToAggregate(cart)).thenReturn(2.0);
    List<PriceRule> rules = Arrays.asList(rule1, rule2, rule3);   
    FinalPriceCalculator calculator = new FinalPriceCalculator(rules);
    double price = calculator.calculate(cart);
    assertThat(price).isEqualTo(3);  
  }
}
If this is what you envisioned when I posed the requirements, you understand my way
of thinking about design and testing. But you may be thinking that even though we
tested each of the price rules individually, and we tested the price calculator with
stubbed rules, we don’t know if these pieces will work when we plug them together.
 This is a valid skeptical thought. Why not write more tests? Because our tests
already cover all the requirements. Structurally, we have covered everything. In these
cases, I suggest writing a larger test that exercises all the classes together. In this case,
the larger test will exercise FinalPriceCalculator together with all the PriceRules.
First, let’s create a factory class in the production code that is responsible for instanti-
ating the calculator with all its dependencies.
public class FinalPriceCalculatorFactory {
  public FinalPriceCalculator build() {
    List<PriceRule> priceRules = Arrays.asList(   
        new PriceOfItems(),
        new ExtraChargeForElectronics(),
        new DeliveryPrice());
    return new FinalPriceCalculator(priceRules);
  }
}
Now all we need to do is to use the factory to build up a real FinalPriceCalculator
and then give it some inputs. To get started, let’s write a test with a shopping cart that
has four items (the delivery price is 12.5) and an electronic item (the final price will
include the extra charge).
public class FinalPriceCalculatorLargerTest {
  private final FinalPriceCalculator calculator =
  ➥  new FinalPriceCalculatorFactory().build();   
Listing 9.10
FinalPriceCalculatorFactory 
Listing 9.11
A larger test for FinalPriceCalculator
Makes the stubs 
return different values, 
given the cart
Passes the
stubs to the
calculator
and runs it
Given the values we set for 
the stubs, we expect a 
final value of 3.
Passes the list of 
PriceRules manually. 
You can use dependency 
injection frameworks to 
do this.
Uses a real 
FinalPriceCalculator with 
all the real PriceRules


---
**Page 223**

223
When to use larger tests
  @Test
  void appliesAllRules() {
    ShoppingCart cart = new ShoppingCart();  
    cart.add(new Item(ItemType.ELECTRONIC, "PS5", 1, 299));
    cart.add(new Item(ItemType.OTHER, "BOOK", 1, 29));
    cart.add(new Item(ItemType.OTHER, "CD", 2, 12));
    cart.add(new Item(ItemType.OTHER, "CHOCOLATE", 3, 1.50));
    double price = calculator.calculate(cart);
    double expectedPrice =
        299 + 29 + 12 * 2 + 1.50 * 3 +   
        7.50 +   
        12.5;  
    assertThat(price)
      .isEqualTo(expectedPrice);  
  }
}
In terms of test code, this is no different from writing a unit test. In fact, based on the
definition I gave in chapter 1, I do not consider this an integration test, as it does not
go beyond the system’s boundaries. This is a larger test that exercises many units.
 From a testing perspective, we can apply specification-based, boundary, and struc-
tural testing the same way. The difference is that the granularity may be coarser. When
testing the DeliveryPrice unit, we only had to think about the rules related to deliv-
ery. Now that we are testing all the behavior together (the calculator plus the price
rules), the number of combinations is larger.
Specification-based testing in larger tests
Let’s look at how I would apply specification-based testing here. I would consider
each price rule a category to exercise individually, analogous to the input values of
the methods we test in isolation. Therefore, my categories would be price per item,
delivery, and electronics extra charge, each with its own partitions. The item itself can
also vary. The categories and partitions are as follows:
Shopping cart:
a
Empty cart
b
1 element
c
Many elements
Each individual item:
a
Single quantity
b
More than one
c
Unit price times quantity, rounded
d
Unit price times quantity, not rounded
Builds up a 
shopping cart
The prices of 
the items
Includes an 
electronic
Delivery
price
Asserts that the 
final value matches 
the shopping cart


---
**Page 224**

224
CHAPTER 9
Writing larger tests
This example shows how much more work it is to test sets of classes together. I use this
approach when I see value in it, such as for debugging a problem that happens in pro-
duction. However, I use these tests in addition to unit tests. I also do not re-test every-
thing. I prefer to use these large component tests as an excuse to try the component
with real-world inputs. 
9.1.2
Testing larger components that go beyond our code base
In the previous example, the large test gives us confidence about the overall behavior
of the component, but we could still test each unit individually. In some cases, how-
ever, we cannot write tests for units in isolation. Or rather, we can write tests, but doing
so would not make sense. Let’s look at examples of two small open source projects I
coded.
TESTING THE CK TOOL
The first example is a project called CK (https://github.com/mauricioaniche/ck),
available on my GitHub page. CK is a tool that calculates code metrics for Java code.
To do so, it relies on Eclipse JDT (www.eclipse.org/jdt/), a library that is part of the
Eclipse IDE. Among its many functionalities, JDT enables us to build abstract syntax
trees (ASTs) of Java code. CK builds ASTs using JDT and then visits these trees and cal-
culates the different metrics.
 As you can imagine, CK is highly dependent on how JDT does things. Given an
AST, JDT offers clients a way to visit the tree. Clients need to create a class that inherits
from ASTVisitor. (Visitor is a popular design pattern for navigating complex data
structures.) CK then implements many of these AST visitors, one for each metric.
 One of the metrics that CK implements is coupling between objects (CBO). The
metric counts the number of other classes the class under analysis depends on.
Imagine the fictitious class A in the following listing. This class declares a field of
type B and instantiates class C. CK detects the dependency on B and C and returns 2
as the CBO.
 
(continued)
Delivery price:
a
1 to 3 items
b
4 to 10 items
c
More than 10 items
Electronics:
a
Has an electronic item
b
No electronic items
I would then combine the partitions that make sense, engineer the different test
cases, and write them as automated JUnit tests. I will leave that as an exercise for
you.


