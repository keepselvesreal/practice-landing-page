# Writing larger tests (pp.215-258)

---
**Page 215**

215
Writing larger tests
Most of the code we tested in previous chapters could be tested via unit tests. When
that was not possible because, say, the class depended on something else, we used
stubs and mocks to replace the dependency, and we still wrote a unit test. As I said
when we discussed the testing pyramid in chapter 1, I favor unit tests as much as
possible when testing business rules.
 But not everything in our systems can (or should) be tested via unit tests. Writ-
ing unit tests for some pieces of code is a waste of time. Forcing yourself to write
unit tests for them would result in test suites that are not good enough to find bugs,
are hard to write, or are flaky and break when you make small changes in the code.
 This chapter discusses how to identify which parts of the system should be tested
with integration or system tests. Then I will illustrate how I write these tests for three
common situations: (1) components (or sets of classes) that should be exercised
together, because otherwise, the test suite would be too weak; (2) components that
communicate with external infrastructure, such as classes that communicate with
databases and are full of SQL queries; and (3) the entire system, end to end.
This chapter covers
Deciding when to write a larger test
Engineering reliable integration and system tests


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


---
**Page 225**

225
When to use larger tests
class A {
  private B b;
  public void action() {
    new C().method();
  }
}
In listing 9.13, I show a simplified implementation of the CBO metric (you can see the
full code on my GitHub). The implementation looks at any declared or used type in
the class and adds it to a set. Later, it returns the number of types in the set. Note all
the visit methods: they are called by the JDT whenever there is, for example, a
method invocation or a field declaration.
public class CBO implements CKASTVisitor {   
  private Set<String> coupling = new HashSet<String>();  
  @Override
  public void visit(MethodInvocation node) {      
    IMethodBinding binding = node.resolveMethodBinding();
    if(binding!=null)
      coupleTo(binding.getDeclaringClass());
  }
  @Override
  public void visit(FieldDeclaration node) {  
    coupleTo(node.getType());
  }
  // this continues for all the possible places where a type can appear...
  private void coupleTo(Type type) {
    // some complex code here to extract the name of the type.
    String fullyQualifiedName = ...;
    addToSet(fullyQualifiedName);   
  }
  private void addToSet(String name) {
    this.coupling.add(name);
  }
}
How can we write a unit test for the CBO class? The CBO class offers many visit
methods called by the JDT once the JDT builds the AST out of real Java code. We could
Listing 9.12
Fictitious class A that depends on B and C
Listing 9.13
CBO implementation in CK
I created my own interface, instead of using 
JDT’s ASTVisitor, but it is the same thing.
Declares a set 
to keep all the 
unique types 
this class uses
If there is a method 
invocation, gets the 
type of the class of 
the invoked method
If there is a field 
declaration, gets the 
type of the field
Adds the full 
name of the 
type to the set


---
**Page 226**

226
CHAPTER 9
Writing larger tests
try to mock all the types that these visit methods receive, such as MethodInvocation
and FieldDeclaration, and then make a sequence of calls to these methods. But in
my opinion, that would be too far from what will happen when we run JDT for real.
 I do not see a way to unit-test this class without starting up JDT, asking JDT to build
an AST out of a small but real Java class, using CBO to visit the generated AST, and
comparing the result. So, I used real integration testing in this case.
 The test class in listing 9.14 runs CK (which runs JDT) in a specific directory. This
directory contains fake Java classes that I created for the sole purpose of the tests. In
the code, it is the cbo directory. I have one directory per metric. Because running JDT
takes a few seconds, I run it once for the entire test class (see the @BeforeAll
method). The test method then asks for the report of a specific class. In the case of
the countDifferentDependencies test, I am interested in the coupling of the fake
Coupling1 class. I then assert that its coupling is 6.
public class CBOTest extends BaseTest {   
  @BeforeAll
  public void setUp() {
    report = run(fixturesDir() + "/cbo");   
  }
  @Test
  public void countDifferentDependencies() {
    CKClassResult result = report.get("cbo.Coupling1");   
    assertEquals(6, result.getCbo());   
  }
}
To help you better understand why the CBO is 6, listing 9.15 shows the Coupling1
class. This code makes no sense, but it is enough for us to count dependencies. This
class uses classes A, B, C, D, C2, and CouplingHelper: that makes six dependencies.
public class Coupling1 {
  private B b;      
  public D m1() {     
    A a = new A();   
    C[] x = new C[10];   
    CouplingHelper h = new CouplingHelper();    
    C2 c2 = h.m1();   
    return d;
  }
}
Listing 9.14
CBOTest 
Listing 9.15
Coupling1 fixture
The BaseTest class provides 
basic functionality for all 
the test classes.
Runs JDT on all code in the cbo 
directory. This directory contains 
Java code I created solely for 
testing purposes.
CK returns a report, 
which we use to get the 
results of a specific Java 
class we created for this 
test (see listing 9.15).
We expect this class to be
coupled with six classes.
B
D
A
C
CouplingHelper
C2


---
**Page 227**

227
When to use larger tests
The CBOTest class contains many other test methods, each exercising a different case.
For example, it tests whether CK can count a dependency even though the depen-
dency’s code is not available (imagine that class A in the example is not in the direc-
tory). It also tests whether it counts interfaces and inherited classes, types in method
parameters, and so on.
 It was challenging to come up with good test cases here; and it was not easy to
apply specification-based testing, because the input could be virtually any Java class.
You may face similar challenges when implementing classes for a plug-and-play archi-
tecture. This is a good example of a specific context where we need to learn more
about how to test. Testing compilers, which is a related problem, is also a significant
area of research. 
TESTING THE ANDY TOOL
Another example where I could not write isolated unit tests involved a tool my teaching
assistants and I wrote to assess the test suites that our students engineered. The tool,
named Andy (https://github.com/cse1110/andy), compiles the test code provided by a
student, runs all the provided JUnit tests, calculates code coverage, runs some static
analysis, and checks whether the test suite is strong enough to kill mutant versions of the
code under test. Andy then gives a grade and a detailed description of its assessment.
 Each step is implemented in its own class. For example, CompilationStep is
responsible for compiling the student’s code, RunJUnitTestsStep is responsible for
executing all the unit tests in the student’s submission, and RunMetaTestsStep checks
whether the test suite kills all the manually engineered mutants we expect it to kill.
Figure 9.1 illustrates Andy’s overall flow.
 If we were to unit-test everything, we would need a unit test for the compilation
step, another for the step that runs JUnit, and so on. But how could we exercise the
“run JUnit” step without compiling the code first? It is not possible.
Student’s
test
(“submission”)
Program to
test
(“exercise”)
Student
Tests
Engineers
test cases
Submits
Andy
Compiles
the code
Runs tests
Calculates
coverage
Runs meta
tests
Generates a ﬁnal
assessment
Final grade: 78/100
Coverage: 85/100
Meta tests: 2/3
Meta test 1: Killed
Meta test 2: Survived
…
Prints the assessment
Figure 9.1
Simplified flow of Andy


---
**Page 228**

228
CHAPTER 9
Writing larger tests
We decided to use larger tests. For example, the tests that exercise RunMetaTestsStep
run the entire engine we developed. Thus our test provides a real Java file that simulates
the student’s submission and another Java file that contains the class under test. Andy
gets these files, compiles them, runs the JUnit tests, and finally runs the meta tests.
 Listing 9.16 shows one of the tests in the test suite. The run() method, which is
implemented in the IntegrationTestBase test base so all the test classes can use it,
runs the entire Andy engine. The parameters are real Java files: 

NumberUtilsAddLibrary.java, which contains the code of the class under test 

NumberUtilsAddOfficialSolution.java, which contains a possible solution
submitted by the student (in this case, the official solution of this exercise)

NumberUtilsAddConfiguration.java, a configuration class that should be pro-
vided by the teacher
The run() method returns a Result class: an entity containing all the results of each
step. Because this test case focuses on the meta tests, the assertions also focus on them.
In this test method, we expect Andy to run four meta tests—AppliesMultipleCarries-
Wrongly, DoesNotApplyCarryAtAll, DoesNotApplyLastCarry, and DoesNotCheck-
NumbersOutOfRange—and we expect them all to pass.
public class MetaTestsTest extends IntegrationTestBase {
  @Test
  void allMetaTestsPassing() {
    Result result =
      run(         
      "NumberUtilsAddLibrary.java",
      "NumberUtilsAddOfficialSolution.java",
      "NumberUtilsAddConfiguration.java");
    assertThat(result.getMetaTests().getTotalTests())
      .isEqualTo(4);  
    assertThat(result.getMetaTests().getPassedMetaTests())
      .isEqualTo(4);
    assertThat(result.getMetaTests())
      .has(passedMetaTest("AppliesMultipleCarriesWrongly"))
      .has(passedMetaTest("DoesNotApplyCarryAtAll"))
      .has(passedMetaTest("DoesNotApplyLastCarry"))
      .has(passedMetaTest("DoesNotCheckNumbersOutOfRange"));
  }
}
NOTE
You may be curious about the passedMetaTest method in this test
method. AssertJ enables us to extend its set of assertions, and we created one
specifically for meta tests. I will show how to do this in chapter 10.
These two examples illustrate situations where unit-testing a class in isolation does not
make sense. In general, my advice is to use unit testing as much as possible, because—as
Listing 9.16
Integration test for the MetaTests step
Runs the full 
Andy engine
Asserts that
the meta tests
step executed
as expected


---
**Page 229**

229
Database and SQL testing
I have said many times before—unit tests are cheap and easy to write. But do not be
afraid to write larger tests whenever you believe they will give you more confidence. 
9.2
Database and SQL testing
In many of the examples in this book, a Data Access Object (DAO) class is responsible
for retrieving or persisting information in the database. Whenever these classes
appear, we quickly stub or mock them out of our way. However, at some point, you
need to test these classes. These DAOs often perform complex SQL queries, and they
encapsulate a lot of business knowledge, requiring testers to spend some energy mak-
ing sure they produce the expected outcomes. The following sections examine what
to test in a SQL query, how to write automated test cases for such queries, and the
challenges and best practices involved.
9.2.1
What to test in a SQL query
SQL is a robust language and contains many different functions we can use. Let’s sim-
plify and look at queries as a composition of predicates. Here are some examples:

SELECT * FROM INVOICE WHERE VALUE < 50

SELECT * FROM INVOICE I JOIN CUSTOMER C ON I.CUSTOMER_ID = C.ID WHERE
C.COUNTRY = 'NL'

SELECT * FROM INVOICE WHERE VALUE > 50 AND VALUE < 200
In these examples, value < 50, i.customer_id = c.id, c.country = 'NL', and value >
50 and value < 200 are the predicates that compose the different queries. As a tester, a
possible criterion is to exercise the predicates and check whether the SQL query
returns the expected results when predicates are evaluated to different results.
 Virtually all the testing techniques we have discussed in this book can be applied
here:
Specification-based testing—SQL queries emerge out of a requirement. A tester can
analyze the requirements and derive equivalent partitions that need to be tested.
Boundary analysis—Such programs have boundaries. Because we expect bound-
aries to be places with a high bug probability, exercising them is important.
Structural testing—SQL queries contain predicates, and a tester can use the
SQL’s structure to derive test cases.
Here, we focus on structural testing. If we look at the third SQL example and try to
make an analogy with what we have discussed about structural testing, we see that the
SQL query contains a single branch composed of two predicates (value > 50 and
value < 200). This means there are four possible combinations of results in these two
predicates: (true, true), (true, false), (false, true), and (false, false). We
can aim at either of the following:
Branch coverage—In this case, two tests (one that makes the overall decision eval-
uate to true and one that makes it evaluate to false) would be enough to
achieve 100% branch coverage.


---
**Page 230**

230
CHAPTER 9
Writing larger tests
Condition + branch coverage—In this case, three tests would be enough to achieve
100% condition + branch coverage: for example, T1 = 150, T2 = 40, T3 = 250.
In “A practical guide to SQL white-box testing,” a 2006 paper by Tuya, Suárez-Cabal,
and De La Riva, the authors suggest five guidelines for designing SQL tests:
Adopting modified condition/decision coverage (MC/DC) for SQL conditions—Deci-
sions happen at three places in a SQL query: join, where, and having condi-
tions. We can use criteria like MC/DC to fully exercise the query’s predicates. If
you do not remember how MC/DC coverage works, revisit chapter 3.
Adapting MC/DC for tackling nulls—Because databases have a special way of han-
dling/returning nulls, any (coverage) criteria should be adapted to three-valued
logic (true, false, null). In other words, consider the possibility of values being
null in your query.
Category-partitioning selected data—SQL can be considered a declarative specifica-
tion for which we can define partitions to be tested. Directly from Tuya et al.’s
paper, we define the following:
– Rows that are retrieved—We include a test state to force the query to not select
any row.
– Rows that are merged—The presence of unwanted duplicate rows in the output
is a common failure in some queries. We include a test state in which identi-
cal rows are selected.
– Rows that are grouped—For each of the group-by columns, we design test states
to obtain at least two different groups at the output, such that the value used
for the grouping is the same and all the others are different.
– Rows that are selected in a subquery—For each subquery, we include test states
that return zero or more rows, with at least one null and two different values
in the selected column.
– Values that participate in aggregate functions—For each aggregate function
(excluding count), we include at least one test state in which the function
computes two equal values and another that is different.
– Other expressions—We also design test states for expressions involving the like
predicate, date management, string management, data type conversions, or
other functions using category partitioning and boundary checking.
Checking the outputs—We should check not only the input domain but also the
output domain. SQL queries may return null or empty values in specific col-
umns, which may make the rest of the program break.
Checking the database constraints—Databases have constraints. We should make
sure the database enforces these constraints.
As you can see, many things can go wrong in a SQL query. It is part of the tester’s job
to make sure that does not happen. 


---
**Page 231**

231
Database and SQL testing
9.2.2
Writing automated tests for SQL queries
We can use JUnit to write SQL tests. All we need to do is (1) establish a connection
with the database, (2) make sure the database is in the right initial state, (3) execute
the SQL query, and (4) check the output.
 Consider the following scenario:
We have an Invoice table composed of a name (varchar, length 100) and a value
(double).
We have an InvoiceDao class that uses an API to communicate with the data-
base. The precise API does not matter.
This DAO performs three actions: save() persists an invoice in the database,
all() returns all invoices in the database, and allWithAtLeast() returns all
invoices with at least a specified value. Specifically,
– save() runs INSERT INTO invoice (name, value) VALUES (?,?).
– all() runs SELECT * FROM invoice.
– allWithAtLeast() runs SELECT * FROM invoice WHERE value >= ?.
A simple JDBC implementation of such a class is shown in listings 9.17, 9.18, and 9.19.
import java.sql.*;
import java.util.ArrayList;
import java.util.List;
public class InvoiceDao {
  private final Connection connection;  
  public InvoiceDao(Connection connection) {
    this.connection = connection;
  }
  public List<Invoice> all() {
    try {
      PreparedStatement ps = connection.prepareStatement(
        ➥ "select * from invoice");   
      ResultSet rs = ps.executeQuery();
      List<Invoice> allInvoices = new ArrayList<>();
      while (rs.next()) {                                 
        allInvoices.add(new Invoice(rs.getString("name"),
        ➥ rs.getInt("value")));
      }
      return allInvoices;
    } catch(Exception e) {   
      throw new RuntimeException(e);
    }
  }
Listing 9.17
Simple JDBC implementation of InvoiceDao, part 1
The DAO holds 
a connection to 
the database.
Prepares and 
executes the 
SQL query
Loops through the 
results, creating a 
new Invoice entity 
for each of them
The JDBC API throws checked 
exceptions. To simplify, we convert 
them to unchecked exceptions.


---
**Page 232**

232
CHAPTER 9
Writing larger tests
public List<Invoice> allWithAtLeast(int value) {  
    try {
      PreparedStatement ps = connection.prepareStatement(
        ➥ "select * from invoice where value >= ?");
      ps.setInt(1, value);
      ResultSet rs = ps.executeQuery();
      List<Invoice> allInvoices = new ArrayList<>();
      while (rs.next()) {
        allInvoices.add(
          new Invoice(rs.getString("name"), rs.getInt("value"))
        );
      }
      return allInvoices;
    } catch (Exception e) {
      throw new RuntimeException(e);
    }
  }
public void save(Invoice inv) {
    try {
      PreparedStatement ps = connection.prepareStatement(
        "insert into invoice (name, value) values (?,?)");  
      ps.setString(1, inv.customer);
      ps.setInt(2, inv.value);
      ps.execute();
      connection.commit();
    } catch(Exception e) {
      throw new RuntimeException(e);
    }
  }
}
NOTE
This implementation is a naive way to access a database. In more com-
plex projects, you should use a professional production-ready database API
such as jOOQ, Hibernate, or Spring Data.
Let’s test the InvoiceDao class. Remember, we want to apply the same ideas we have
seen so far. The difference is that we have a database in the loop. Let’s start with
all(). This method sends a SELECT * FROM invoice to the database and gets back the
result. But for this query to return something, we must first insert some invoices into
the database. The InvoiceDao class also provides the save() method, which sends an
INSERT query. This is enough for our first test.
Listing 9.18
Simple JDBC implementation of InvoiceDao, part 2
Listing 9.19
Simple JDBC implementation of InvoiceDao, part 3
The same thing 
happens here: we 
prepare the SQL 
query, execute it, 
and then create one 
Invoice entity for 
each row.
Prepares 
the INSERT 
statement and 
executes it


---
**Page 233**

233
Database and SQL testing
public class InvoiceDaoIntegrationTest {
  private Connection connection;   
  private InvoiceDao dao;          
  @Test
  void save() {
   Invoice inv1 = new Invoice("Mauricio", 10);   
   Invoice inv2 = new Invoice("Frank", 11);
   dao.save(inv1);   
   List<Invoice> afterSaving = dao.all();    
   assertThat(afterSaving).containsExactlyInAnyOrder(inv1);
   dao.save(inv2);    
   List<Invoice> afterSavingAgain = dao.all();
   assertThat(afterSavingAgain)
     .containsExactlyInAnyOrder(inv1, inv2);
  }
}
This test method creates two invoices (inv1, inv2), persists the first one using the
save() method, retrieves the invoices from the database, and asserts that it returns
one invoice. Then it persists another invoice, retrieves the invoices from the database
again, and asserts that now it returns two invoices. The test method ensures the cor-
rect behavior of both the save() and all() methods. The containsExactlyInAny-
Order assertion from AssertJ ensures that the list contains the precise invoices that we
pass to it, in any order. For that to happen, the Invoice class needs a proper imple-
mentation of the equals() method.
 In terms of testing, our implementation is correct. However, given the database, we
have some extra concerns. First, we should not forget that the database persists the
data permanently. Suppose we start with an empty database. The first time we run the
test, it will persist two invoices in the database. The second time we run the test, it will
persist two new invoices, totaling four invoices. This will make our test fail, as it
expects the database to have one and two invoices, respectively.
 This was never a problem in our previous unit tests: every object we created lived in
memory, and they disappeared after the test method was done. When testing with a
real database, we must ensure a clean state:
Before the test runs, we open the database connection, clean the database, and
(optionally) put it in the state we need it to be in before executing the SQL
query under test.
After the test runs, we close the database connection.
This is a perfect fit for JUnit’s @BeforeEach and @AfterEach, as shown in the following
listing.
Listing 9.20
First step of our SQL test
This test requires a connection to 
the database and an invoice DAO.
Creates a set 
of invoices
Persists the
first one
Gets all invoices from the database 
and ensures that the database only 
contains the invoice we inserted
Inserts another 
invoice and ensures 
that the database 
contains both of 
them


---
**Page 234**

234
CHAPTER 9
Writing larger tests
public class InvoiceDaoIntegrationTest {
  private Connection connection;
  private InvoiceDao dao;
  @BeforeEach
  void openConnectionAndCleanup() throws SQLException {
    connection = DriverManager.getConnection("jdbc:hsqldb:mem:book");   
    PreparedStatement preparedStatement = connection.prepareStatement(
      ➥ "create table if not exists invoice (name varchar(100),
      ➥ value double)");   
    preparedStatement.execute();
    connection.commit();
    connection.prepareStatement("truncate table invoice").execute();  
    dao = new InvoiceDao(connection);  
  }
  @AfterEach
  void close() throws SQLException {
    connection.close();   
  }
  @Test
  void save() {   
    // ...
  }
}
The openConnectionAndCleanup() method is annotated as @BeforeEach, which
means JUnit will run the cleanup before every test method. Right now, its implemen-
tation is simplistic: it sends a truncate table query to the database.
NOTE
In larger systems, you may prefer to use a framework to help you han-
dle the database. I suggest Flyway (https://flywaydb.org) or Liquibase (https://
www.liquibase.org). In addition to supporting you in evolving your database
schema, these frameworks contain helper methods that help clean up the
database and make sure it contains the right schema (that is, all tables, con-
straints, and indexes are there).
We also open the connection to the database manually, using JDBC’s most rudimen-
tary API call, getConnection. (In a real software system, you would probably ask
Hibernate or Spring Data for an active database connection.) Finally, we close the
connection in the close() method (which happens after every test method).
 Let’s now test the other method: allWithAtLeast(). This method is more interest-
ing, as the SQL query contains a predicate, where value >= ?. This means we have
Listing 9.21
Setting up and tearing down the database
Opens a connection to the database.
For simplicity, I am using HSQLDB, an
in-memory database. In real systems,
you may want to connect to the same
type of database you use in
production.
Ensures that the database has the right tables and schema. 
In this example, we create the invoice table. You may need 
something fancier than that in real applications.
Truncates the table to
ensure that no data from
previous tests is in the
database. Again, you may
need something fancier
in more complex
applications.
Creates
the DAO
Closes the connection. You 
may decide to close the 
connection only at the end of 
the entire test suite. In that 
case, you can use JUnit’s 
@BeforeAll and @AfterAll.
The test
we wrote


---
**Page 235**

235
Database and SQL testing
different scenarios to exercise. Here we can use all of our knowledge about boundary
testing and think of on and off points, as we did in chapter 2.
 Figure 9.2 shows the boundary analysis. The on point is the point on the boundary.
In this case, it is whatever concrete number we pass in the SQL query. The off point
is the nearest point to the on point that flips the condition. In this case, that is what-
ever concrete number we pass in the SQL query minus one, since it makes the con-
dition false.
The following listing shows the JUnit test. Note that we add an in point to the test
suite. Although it isn’t needed, it is cheap to do and makes the test more readable:
@Test
void atLeast() {
  int value = 50;
  Invoice inv1 = new Invoice("Mauricio", value - 1);   
  Invoice inv2 = new Invoice("Arie", value);           
  Invoice inv3 = new Invoice("Frank", value + 1);      
  dao.save(inv1);    
  dao.save(inv2);
  dao.save(inv3);
  List<Invoice> afterSaving = dao.allWithAtLeast(value);
  assertThat(afterSaving)
    .containsExactlyInAnyOrder(inv2, inv3);    
}
The strategy we use to derive the test case is very similar to what we have seen previ-
ously. We exercise the on and off points and then ensure that the result is correct.
Given where value >= ?, where we concretely replace ? with 50 (see the value variable
and the inv2 variable), we have 50 as on point and 49 as off point (value - 1 in inv1).
Listing 9.22
Integration test for the atLeast method
where value >= ?
On point:
Oﬀpoint:
?
? – 1
The on point is the number
in the boundary. In this case,
it’s whatever number we
pass in the SQL.
The off point ﬂips the result of the on point. In
this case, it should make the expression false: e.g.,
whatever number we pass in the SQL minus
makes
1
the expression false.
Figure 9.2
On and off points 
for the allWithAtLeast() 
SQL query
The on point of the value 
>= x boundary is x. The off 
point is x - 1. A random in 
point can be x + 1.
Persists them all 
in the database
We expect the method to 
return only inv2 and inv3.


---
**Page 236**

236
CHAPTER 9
Writing larger tests
In addition, we test a single in point. While doing so is not necessary, as we discussed
in the boundary testing section in chapter 2, one more test case is cheap and makes
the test strategy more comprehensible.
NOTE
Your tests should run against a test database—a database set up exclu-
sively for your tests. Needless to say, you do not want to run your tests against
the production database. 
9.2.3
Setting up infrastructure for SQL tests
In our example, it was simple to open a connection, reset the database state, and so
on, but that may become more complicated (or lengthy) when your database schema
is complicated. Invest in test infrastructure to facilitate your SQL testing and make
sure that when a developer wants to write an integration test, they do not need to set
up connections manually or handle transactions. This should be a given from the test
suite class.
 A strategy I often apply is to create a base class for my integration tests: say, SQL-
IntegrationTestBase. This base class handles all the magic, such as creating a con-
nection, cleaning up the database, and closing the connection. Then the test class,
such as InvoiceDaoTest, which would extend SQLIntegrationTestBase, focuses only
on testing the SQL queries. JUnit allows you to put BeforeEach and AfterEach in base
classes, and those are executed as if they were in the child test class.
 Another advantage of having all the database logic in the test base class is that
future changes will only need to be made in one place. Listing 9.23 shows an imple-
mentation example. Note how the InvoiceDaoIntegrationTest code focuses primar-
ily on tests.
public class SqlIntegrationTestBase {
  private Connection connection;
  protected InvoiceDao dao;     
  @BeforeEach   
  void openConnectionAndCleanup() throws SQLException {
    // ...
  }
  @AfterEach    
  void close() throws SQLException {
    // ...
  }
}
public class InvoiceDaoIntegrationTest extends SqlIntegrationTestBase {  
Listing 9.23
Base class that handles the database-related logic
Makes the InvoiceDao 
protected so we can access 
it from the child classes
The methods
are the same
as before.
InvoiceDaoTest now extends
SqlIntegrationTestBase.


---
**Page 237**

237
Database and SQL testing
  @Test
  void save() {      
    // ...
  }
  @Test
  void atLeast() {   
    // ...
  }
}
I will not provide a complete code example, because it changes from project to proj-
ect. Instead, the following sections list what I do in such an integration test base class.
OPENING THE DATABASE CONNECTION
This means opening a JDBC connection, a Hibernate connection, or the connection
of whatever persistence framework you use. In some cases, you may be able to open a
single connection per test suite instead of one per test method. In this case, you may
want to declare it as static and use JUnit’s BeforeAll to open and AfterAll to close it. 
OPENING AND COMMITTING THE TRANSACTION
In more complex database operations, it is common to make them all happen
within a transaction scope. In some systems, your framework handles this automati-
cally (think of Spring and its @Transactional annotations). In other systems, devel-
opers do it by hand, calling something that begins the transaction and later something
that commits it.
 You should decide on how to handle transactions in your test. A common approach
is to open the transaction and, at the end of the test method, commit the transaction.
Some people never commit the transaction, but roll it back once the test is over.
Because this is an integration test, I suggest committing the transaction for each test
method (and not for the entire test class, as we did for the connection). 
RESETTING THE STATE OF THE DATABASE
You want all your tests to start with a clean database state. This means ensuring the
correct database schema and having no unexpected data in the tables. The simplest
way to do this is to truncate every table at the beginning of each test method. If you
have many tables, you truncate them all. You can do this by hand (and manually add
one truncate instruction per table in the code) or use a smarter framework that does
it automatically.
 Some developers prefer to truncate the tables before the test method, and others
after. In the former case, you are sure the database is clean before running the test. In
the latter, you ensure that everything is clean afterward, which helps ensure that it will
be clean the next time you run it. I prefer to avoid confusion and truncate before the
test method. 
The test class focuses on 
the tests themselves, as the 
database infrastructure is 
handled by the base class.


---
**Page 238**

238
CHAPTER 9
Writing larger tests
HELPER METHODS THAT REDUCE THE AMOUNT OF CODE IN THE TESTS
SQL integration test methods can be long. You may need to create many entities
and perform more complex assertions. If code can be reused by many other tests, I
extract it to a method and move it to the base class. The test classes now all inherit
this utility method and can use it. Object builders, frequent assertions, and specific
database operations that are often reused are good candidates to become methods
in the base class. 
9.2.4
Best practices
Let’s close this section with some final tips on writing tests for SQL queries.
USE TEST DATA BUILDERS
Creating invoices in our earlier example was a simple task. The entity was small and
contained only two properties. However, entities in real-world systems are much more
complex and may require more work to be instantiated. You do not want to write 15
lines of code and pass 20 parameters to create a simple invoice object. Instead, use
helper classes that instantiate test objects for you. These test data builders, as they are
known, help you quickly build the data structures you need. I will show how to imple-
ment test data builders in chapter 10. 
USE GOOD AND REUSABLE ASSERTION APIS
Asserting was easy in the example, thanks to AssertJ. However, many SQL queries
return lists of objects, and AssertJ provides several methods to assert them in many dif-
ferent ways. If a specific assertion is required by many test methods, do not be afraid
to create a utility method that encapsulates this complex assertion. As I discussed, put-
ting it in the base test class is my usual way to go. 
MINIMIZE THE REQUIRED DATA
Make sure the input data is minimized. You do not want to have to load hundreds of
thousands of elements to exercise your SQL query. If your test only requires data in
two tables, only insert data in these two tables. If your test requires no more than 10
rows in that table, only insert 10 rows. 
TAKE THE SCHEMA EVOLUTION INTO CONSIDERATION
In real software systems, database schemas evolve quickly. Make sure your test suite is
resilient toward these changes. In other words, database evolution should not break
the existing test suite. Of course, you cannot (and you probably do not want to)
decouple your code completely from the database. But if you are writing a test and
notice that a future change may break it, consider reducing the number of points that
will require change. Also, if the database changes, you must propagate the change to
the test database. If you are using a framework to help you with migration (like Flyway
or Liquibase), you can ask the framework to perform the migrations. 


---
**Page 239**

239
System tests
CONSIDER (OR DON’T) AN IN-MEMORY DATABASE
You should decide whether your tests will communicate with a real database (the same
type of database as in your production environment) or a simpler database (such as
an in-memory database). As always, both sides have advantages and disadvantages.
Using the same database as in production makes your tests more realistic: your tests
will exercise the same SQL engine that will be exercised in production. On the other
hand, running full-blown MySQL is much more expensive, computationally speaking,
than a simple in-memory database. All in all, I favor using real databases when I am
writing SQL integration tests. 
9.3
System tests
At some point, your classes, business rules, persistence layers, and so on are combined
to form, for example, a web application. Let’s think about how a web application tradi-
tionally works. Users visit a web page (that is, their browser makes a request to the
server, and the server processes the request and returns a response that the browser
shows) and interact with the elements on the page. These interactions often trigger
other requests and responses. Considering a pet clinic application: a user goes to the
web page that lists all the scheduled appointments for today, clicks the New Appoint-
ment button, fills out the name of their pet and its owner, and selects an available time
slot. The web page then takes the user back to the Appointments page, which now
shows the newly added appointment.
 If this pet clinic web application was developed using test-driven approaches and
everything we discussed in the previous chapters of this book, the developer already
wrote (systematic) unit tests for each unit in the software. For example, the Appointment
class already has unit tests of its own.
 In this section, we discuss what to test in a web application and what tools we can
use to automatically open the browser and interact with the web page. We also discuss
some best practices for writing system tests.
NOTE
Although I use a web application as an example of how to write a sys-
tem test, the ideas in this section apply to any other type of software system.
9.3.1
An introduction to Selenium
Before diving into the best practices, let’s get familiar with the mechanics of writing such
tests. For that, we will rely on Selenium. The Selenium framework (www.selenium.dev)
is a well-known tool that supports developers in testing web applications. Selenium
can connect to any browser and control it. Then, through the Selenium API, we can
give commands such as “open this URL,” “find this HTML element in the page and
get its inner text,” and “click that button.” We will use commands like these to test our
web applications.
 We use the Spring PetClinic web application (https://projects.spring.io/spring
-petclinic) as an example throughout this section. If you are a Java web developer,
you are probably familiar with Spring Boot. For those who are not, Spring Boot is


---
**Page 240**

240
CHAPTER 9
Writing larger tests
the state-of-the-art framework for web development in Java. Spring PetClinic is a sim-
ple web application that illustrates how powerful and easy to use Spring Boot is. Its
code base contains the two lines required for you to download (via Git) and run (via
Maven) the web application. Once you do, you should be able to visit your local-
host:8080 and see the web application, shown in figures 9.3 and 9.4.
Figure 9.3
First screenshot of the Spring PetClinic application
Figure 9.4
Second screenshot of the Spring PetClinic application


---
**Page 241**

241
System tests
Before discussing testing techniques and best practices, let’s get started with Sele-
nium. The Selenium API is intuitive and easy to use. The following listing shows our
first test.
public class FirstSeleniumTest {
  @Test
  void firstSeleniumTest() {
    WebDriver browser = new SafariDriver();   
    browser.get("http:/ /localhost:8080");   
    WebElement welcomeHeader = browser.findElement(By.tagName("h2"));   
    assertThat(welcomeHeader.getText())
      .isEqualTo("Welcome");  
    browser.close();   
  }
}
Let’s go line by line:
1
The first line, WebDriver browser = new SafariDriver(), instantiates a Safari
browser. WebDriver is the abstraction that all other browsers implement. If you
would like to try a different browser, you can use new FirefoxBrowser() or new
ChromeBrowser() instead. I am using Safari for two reasons:
a
I am a Mac user, and Safari is often my browser of choice.
b
Other browsers, such as Chrome, may require you to download an external
application that enables Safari to communicate with it. In the case of Chrome,
you need to download ChromeDriver (https://chromedriver.chromium.org/
downloads).
2
With an instantiated browser, we visit a URL by means of browser.get("url");.
Whatever URL we pass, the browser will visit. Remember that Selenium is not
simulating the browser: it is using the real browser.
3
The test visits the home page of the Spring PetClinic web app (figure 9.3). This
website is very simple and shows a brief message (“Welcome”) and a cute pic-
ture of a dog and a cat. To ensure that we can extract data from the page we are
visiting, let’s ensure that the “Welcome” message is on the screen. To do that,
we first must locate the element that contains the message. Knowledge of
HTML and DOM is required here.
If you inspect the HTML of the Spring PetClinic, you see that the message is
within an h2 tag. Later, we discuss the best ways to locate elements on the page;
but for now, we locate the only h2 element. To do so, we use Selenium’s find-
Element() function, which receives a strategy that Selenium will use to find the
Listing 9.24
Our first Selenium test
Selects a driver. The 
driver indicates which 
browser to use.
Visits a page at 
the given URL
Finds an HTML
element in the page
Asserts that the 
page contains 
what we want
Closes the browser and 
the selenium session


---
**Page 242**

242
CHAPTER 9
Writing larger tests
element. We can find elements by their names, IDs, CSS classes, and tag name.
By.tagName("h2") returns a WebElement, an abstraction representing an ele-
ment on the web page.
4
We extract some properties of this element: in particular, the text inside the h2
tag. For that, we call the getText() method. Because we expect it to return
“Welcome”, we write an assertion the same way we are used to. Remember, this
is an automated test. If the web element does not contain “Welcome”, the test
will fail.
5
We close the browser. This is an important step, as it disconnects Selenium
from the browser. It is always a good practice to close any resources you use in
your tests.
If you run the test, you should see Safari (or your browser of choice) open, be auto-
matically controlled by Selenium, and then close. This will get more exciting when we
start to fill out forms. 
9.3.2
Designing page objects
For web applications and system testing, we do not want to exercise just one unit of
the system but the entire system. We want to do what we called system testing in chap-
ter 1. What should we test in a web application, with all the components working
together and an infinite number of different paths to test?
 Following what we discussed in the testing pyramid, all the units of the web appli-
cation are at this point (we hope) already tested at the unit or integration level. The
entities in the Spring PetClinic, such as Owner or Pet, have been unit-tested, and all
the queries that may exist in DAOs have also been tested via integration tests similar to
what we just did.
 But if everything has already been tested, what is left for us to test? We can test the
different user journeys via web testing. Here is Fowler’s definition of a user journey test
(2003): “User-journey tests are a form of business-facing test, designed to simulate a
typical user’s journey through the system. Such a test will typically cover a user’s entire
interaction with the system to achieve some goal. They act as one path in a use case.”
 Think of possible user journeys in the Spring PetClinic application. One possible
journey is the user trying to find owners. Other possible journeys include the user
adding a new owner, adding a pet to the owner, or adding a log entry of the pet after
the pet visits the veterinarian.
 Let’s test one journey: the find owners journey. We will code this test using a Page
Object pattern. Page objects (POs) help us write more maintainable and readable web
tests. The idea of the Page Object pattern is to define a class that encapsulates all the
(Selenium) logic involved in manipulating one page.
 For example, if the application has a List of Owners page that shows all the owners,
we will create a ListOfOwnersPage class that will know how to handle it (such as
extracting the names of the owners from the HTML). If the application has an Add
Owner page, we will create an AddOwnerPage class that will know how to handle it


---
**Page 243**

243
System tests
(such as filling out the form with the name of the new owner and clicking the button
that saves it). Later, we will put all these POs together in a JUnit test, simulate the
whole journey, and assert that it went as expected.
 When I write Selenium web tests, I prefer to start by designing my POs. Let’s begin
by modeling the first page of this journey: the Find Owners page. This page is shown
in figure 9.5, and the page can be accessed by clicking the Find Owners link in the menu.
This page primarily contains one interesting thing to be modeled: the “find owners”
functionality. For that to work, we need to fill in the Last Name input field and click
the Find Owners button. Let’s start with that.
public class FindOwnersPage extends PetClinicPageObject {
  public FindOwnersPage(WebDriver driver) {  
    super(driver);
  }
  public ListOfOwnersPage findOwners(String ownerLastName) {   
    driver.findElement(By.id("lastName")).sendKeys(ownerLastName);   
    WebElement findOwnerButton = driver
      .findElement(By.id("search-owner-form"))
      .findElement(By.tagName("button"));
    findOwnerButton.click();   
    ListOfOwnersPage listOfOwnersPage = new ListOfOwnersPage(driver);  
    listOfOwnersPage.isReady();   
    return listOfOwnersPage;
  }
}
Listing 9.25
FindOwners page object
We need to type the name of the owner in
this HTML ﬁeld and press the Find Owner
button for the search to happen.
Figure 9.5
The Find Owners page
The constructor of all our POs receives the Selenium 
driver. The PO needs it to manipulate the web page.
This method is
responsible for
finding an owner
on this page based
on their last name.
Finds the HTML element
whose ID is lastName and
types the last name of the
owner we are looking for.
Clicks the
Find Owner
button. We
find it on
the page by
its ID.
Takes us to another page.
To represent that, we
make the PO return the
new page, also as a PO.
Waits for the 
page to be 
ready before 
returning it


---
**Page 244**

244
CHAPTER 9
Writing larger tests
Let’s look at this code line by line:
1
The newly created class FindOwnersPage represents the Find Owners page. It
inherits from another class, PetClinicPageObject, which will serve as a com-
mon abstraction for our POs. I show its source code later.
2
Our POs always have a constructor that receives a WebDriver. Everything we do
with Selenium starts with the WebDriver class, which we will instantiate later
from a JUnit test method.
3
Methods in this PO represent actions we can take with the page we are model-
ing. The first action we modeled is findOwners(), which fills the Last Name
input with the value passed to the ownerLastName string parameter.
4
The implementation of the method is straightforward. We first locate the
HTML input element. By inspecting the Spring PetClinic web page, we see that
the field has an ID. Elements with IDs are usually easy to find, as IDs are unique
in the page. With the element in hand, we use the sendKeys() function to fill in
the input with ownerLastName. Selenium’s API is fluent, so we can chain the
method calls: findElement(…).sendKeys(…).
5
We search for the Find Owner button. When inspecting the page, we see that
this button does not have a specific ID. This means we need to find another way
to locate it on the HTML page. My first instinct is to see if this button’s HTML
form has an ID. It does: search-owner-form. We can locate the form and then
locate a button inside it (as this form has one button).
Note how we chain calls for the findElement method. Remember that
HTML elements may have other HTML elements inside them. Therefore, the
first findElement() returns the form, and the second findElement searches
only the elements inside the element returned by the first findElement. With
the button available to us, we call the click() method, which clicks the button.
The form is now submitted.
6
The website takes us to another page that shows the list of owners with the
searched last name. This is no longer the Find Owners page, so we should now
use another PO to represent the current page. That is why we make the find-
Owners() method return a ListOfOwnersPage: one page takes you to another
page.
7
Before we return the newly instantiated ListOfOwnersPage, we call an isReady()
method. This method waits for the Owners page to be ready. Remember that
this is a web application, so requests and responses may take some time. If we
try to look for an element from the page, but the element is not there yet, the
test will fail. Selenium has a set of APIs that enable us to wait for such things,
which we will see soon.
We still have more POs to model before writing the test for the entire journey. Let’s
model the Owners page, shown in figure 9.6. This page contains a table in which each
row represents one owner.


---
**Page 245**

245
System tests
Our ListOfOwnersPage PO models a single action that will be very important for our
test later: getting the list of owners in this table. The following listing shows the source
code.
public class ListOfOwnersPage extends PetClinicPageObject {
  public ListOfOwnersPage(WebDriver driver) {    
    super(driver);
  }
  @Override
  public void isReady() {   
    WebDriverWait wait = new WebDriverWait (driver, Duration.ofSeconds(3));
    wait.until(
      ExpectedConditions.visibilityOfElementLocated(
      By.id("owners")));    
  }
  public List<OwnerInfo> all() {
    List<OwnerInfo> owners = new ArrayList<>();    
    WebElement table = driver.findElement(By.id("owners"));   
    List<WebElement> rows = table.findElement(By.tagName(
      ➥ "tbody")).findElements(By.tagName("tr"));
    for (WebElement row : rows) {    
      List<WebElement> columns = row.findElements(By.tagName("td"));  
      String name = columns.get(0).getText().trim();   
      String address = columns.get(1).getText().trim();
      String city = columns.get(2).getText().trim();
      String telephone = columns.get(3).getText().trim();
      String pets = columns.get(4).getText().trim();
Listing 9.26
ListOfOwners PO
We need to get the list of
owners from this HTML table.
Figure 9.6
The Owners page
As we know, all POs receive the 
WebDriver in the constructor.
The isReady method lets us know whether the 
page is ready in the browser so we can start 
manipulating it. This is important, as some 
pages take more time than others to load.
The Owners page is considered ready when the list of 
owners is loaded. We find the table with owners by its 
ID. We wait up to three seconds for that to happen.
Creates
a list to
hold all the
owners. For
that, we
create an
OwnerInfo
class.
Gets the HTML table 
and all its rows. The 
table’s ID is owners, 
which makes it easy 
to find.
For each row in 
the table …
… gets the 
HTML row
Gets the value of each 
HTML cell. The first 
column contains the 
name, the second the 
address, and so on.


---
**Page 246**

246
CHAPTER 9
Writing larger tests
      OwnerInfo ownerInfo = new OwnerInfo(
        ➥ name, address, city, telephone, pets);    
      owners.add(ownerInfo);
    }
    return owners;   
  }
}
Let’s walk through this code:
1
Our class is a PO, so it extends from PetClinicPageObject, which forces the
class to have a constructor that receives a WebDriver. We still have not seen the
PetClinicPageObject code, but we will soon.
2
The isReady() method (which you can see by the @Override annotation is also
defined in the base class) knows when this page is loaded. How do we do this?
The simplest way is to wait a few seconds for a specific element to appear on the
page. In this case, we wait for the element with ID “owners” (the table with all
the owners) to be on the page. We tell WebDriverWait to wait up to three sec-
onds for the owners element to be visible. If the element is not there after three
seconds, the method throws an exception. Why three seconds? That was a
guess; in practice, you have to find the number that best fits your test.
3
We return to our main action: the all() method. The objective is to extract the
names of all the owners. Because this is an HTML table, we know that each row
is in a tr element. The table has a header, which we want to ignore. So, we
locate #owners > tbody > tr or, in other words, all trs inside tbody that are
inside the owners element. We do this using nested findElement() and find-
Elements() calls. Note the difference between the two methods: one returns a
single element, the other multiple elements (useful in this case, as we know
there are many trs to be returned).
4
With the list of rows ready, we iterate over each element. We know that trs are
composed of tds. We find all tds inside the current tr and extract the text
inside each td, one by one. We know the first cell contains the name, the sec-
ond cell contains the address, and so on. We then build an object to hold this
information: the OwnerInfo class. This is a simple class with getters only. We also
trim() the string to get rid of any whitespaces in the HTML.
5
We return the list of owners in the table.
Now, searching for an owner with their surname takes us to the next page, where we
can extract the list of owners. Figure 9.7 illustrates the two POs we have implemented
so far and which pages of the web application they model.
 We are only missing two things. First and foremost, to search for an owner, the
owner must be in the application. How do we add a new owner? We use the Add
Owner page. So, we need to model one more PO. Second we need a way to visit these
pages for the first time.
Once all the information 
is collected from the 
HTML, we build an 
OwnerInfo class.
Returns a list of 
OwnerInfos. This object 
knows nothing about 
the HTML page.


---
**Page 247**

247
System tests
NOTE
Much more work is required to write a test for a single journey than we
are used to when doing unit tests. System tests are naturally more expensive
to create. But I also want you to recognize that adding a new test becomes eas-
ier once you have an initial structure with POs. The high cost comes now,
when building this initial infrastructure.
Let’s start with adding an owner. The next listing shows the AddOwnerPage PO.
public class AddOwnerPage extends PetClinicPageObject {
  public AddOwnerPage(WebDriver driver) {   
    super(driver);
  }
  @Override
  public void isReady() {
    WebDriverWait wait = new WebDriverWait (driver, Duration.ofSeconds(3));
    wait.until(
      ExpectedConditions.visibilityOfElementLocated(
      By.id("add-owner-form")));     
  }
  public OwnerInformationPage add(AddOwnerInfo ownerToBeAdded) {
    driver.findElement(By.id("firstName"))
      .sendKeys(ownerToBeAdded.getFirstName());   
    driver.findElement(By.id("lastName"))
      .sendKeys(ownerToBeAdded.getLastName());
    driver.findElement(By.id("address"))
      .sendKeys(ownerToBeAdded.getAddress());
    driver.findElement(By.id("city"))
      .sendKeys(ownerToBeAdded.getCity());
    driver.findElement(By.id("telephone"))
      .sendKeys(ownerToBeAdded.getTelephone());
Listing 9.27
.AddOwnerPage page object
/findOwners
owners?lastName=x
FindOwnersPage
(Java object)
ow er
n
s()
…
ListOfOwnersPage
(Java object)
all()
…
Web pages
Page objects
Each page object represents one web page. It contains elegant
methods that know how to manipulate the page. Test methods
use these page objects to test the web application.
Figure 9.7
An illustration 
of web pages and their 
respective POs
Again, the PO 
receives the 
WebDriver.
The HTML page is 
ready when the 
form appears on 
the screen.
Fills out all the HTML form 
elements with the data 
provided in AddOwnerInfo, 
a class created for that 
purpose. We find the form 
elements by their IDs.


---
**Page 248**

248
CHAPTER 9
Writing larger tests
    driver.findElement(By.id("add-owner-form"))
        .findElement(By.tagName("button"))
        .click();     
    OwnerInformationPage ownerInformationPage =
      new OwnerInformationPage(driver);  
    ownerInformationPage.isReady();
    return ownerInformationPage;
  }
}
The implementation should not be a surprise. The isReady() method waits for the
form to be ready. The add() method, which is the relevant method here, finds the
input elements (which all have specific IDs, making our lives much easier), fills them
in, finds the Add Owner button, and returns the PO that represents the page we go to
after adding an owner: OwnerInformationPage. I do not show its code, to save space,
but it is a PO much like the others we have seen.
 Finally, all we need is a way to visit the pages. I usually have a visit() method in
my POs to take me directly to that page. Let’s add a visit() method to the POs we
need to visit: the Find Owner page and the Add Owner page.
// FindOwnersPage
public void visit() {
  visit("/owners/find");
}
// AddOwnersPage
public void visit() {
  visit("/owners/new");
}
Note that these visit() methods call another visit method in the superclass.
 Now it is time to show the PO base class. This is where we put common behavior
that all our POs have. Base classes like these support and simplify the development of
our tests.
public abstract class PetClinicPageObject {
  protected final WebDriver driver;   
  public PetClinicPageObject(WebDriver driver) {
    this.driver = driver;
  }
  public void visit() {     
    throw new RuntimeException("This page does not have a visit link");
  }
Listing 9.28
Adding visit() methods to all the POs
Listing 9.29
Initial code of the PO base class
Clicks the 
Add button
When an owner is added, the web 
application redirects us to the Owner 
Information page. The method then 
returns the PO of the class we are 
redirected to.
The base class keeps 
the reference to the 
WebDriver.
The visit method 
should be overridden 
by the child classes.


---
**Page 249**

249
System tests
  protected void visit(String url) {       
    driver.get("http:/ /localhost:8080" + url);  
    isReady();
  }
  public abstract void isReady();    
}
You can make this PO base class as complex as you need. In more involved apps, the
base class is more complex and full of helper methods. For now, we have a constructor
that receives WebDriver (forcing all POs to have the same constructor), a visit()
method that can be overridden by child POs, a helper visit() method that com-
pletes the URL with the localhost URL, and an abstract isReady() method that forces
all POs to implement this functionality.
 We now have enough POs to model our first journey. The following listing shows a
JUnit test.
public class FindOwnersFlowTest {
  protected static WebDriver driver = new SafariDriver();   
  private FindOwnersPage page = new FindOwnersPage(driver);   
  @AfterAll
  static void close() {   
    driver.close();
  }
  @Test
  void findOwnersBasedOnTheirLastNames() {
    AddOwnerInfo owner1 = new AddOwnerInfo(
      ➥ "John", "Doe", "some address", "some city", "11111");   
    AddOwnerInfo owner2 = new AddOwnerInfo(
      ➥ "Jane", "Doe", "some address", "some city", "11111");
    AddOwnerInfo owner3 = new AddOwnerInfo(
      ➥ "Sally", "Smith", "some address", "some city", "11111");
    addOwners(owner1, owner2, owner3);
    page.visit();   
    ListOfOwnersPage listPage = page.findOwners("Doe");  
    List<OwnerInfo> all = listPage.all();
    assertThat(all).hasSize(2).
        containsExactlyInAnyOrder(
        owner1.toOwnerInfo(), owner2.toOwnerInfo());  
  }
Listing 9.30
Our first journey: find owners
Provides a helper 
method for the base 
classes to help them 
visit the page
The hard-coded URL can come 
from a configuration file.
All POs are forced to implement an isReady 
method. Making methods abstract is a nice 
way to force all POs to implement their 
minimum required behavior.
Creates a concrete WebDriver, the SafariDriver.
Later, we will make this more flexible so our
tests can run in multiple browsers.
Creates the 
FindOwners PO, 
where the test 
should start
When the test suite is done, we 
close the Selenium driver. This 
method is also a good candidate 
to move to a base class.
Creates a bunch of owners to
be added. We need owners
before testing the listing page.
Visits the Find 
Owners page
Looks for all 
owners with Doe 
as their surname
Asserts that we find 
John and Jane from 
the Doe family


---
**Page 250**

250
CHAPTER 9
Writing larger tests
  private void addOwners(AddOwnerInfo... owners) {   
    AddOwnerPage addOwnerPage = new AddOwnerPage(driver);
    for (AddOwnerInfo owner : owners) {
      addOwnerPage.visit();
      addOwnerPage.add(owner);
    }
  }
}
Let’s walk through this code:
1
At the top of the class, we create a static instance of SafariDriver, which we
enclose in the @AfterAll method. To save some time (opening and closing the
browser for every test), we only need one instance of WebDriver for all the tests
in this class. For now, this means our test has the Safari browser hard-coded.
Later we will discuss how to make it more flexible so you can run your test suite
in multiple browsers.
2
The findOwnersBasedOnTheirLastNames() method contains our journey. We
create two fake AddOwnerInfos: two owners that will be added to the applica-
tion. For each owner, we visit the Add Owner page, fill in the information, and
save. (I created an addOwners() private helper method to increase the readabil-
ity of the main test method.)
3
We visit the Owners page and get all the owners in the list. We expect both
newly added owners to be there, so we assert that the list contains two items and
they are the two owners we created.
4
AddOwnerInfo, the data structure used by AddOwnerPage, is different from Owner-
Info, the data structure returned by the ListOfOwnersPage page. In one, a
name is the first name and last name together, and in the other, the first name
and last name are separate. We could use a single data structure for both or
design them separately. I chose to design them separately, so I needed to con-
vert from one to another. So, I implemented toOwnerInfo() in the AddOwner-
Info class. It is a simple method, as you see in the next listing.
public OwnerInfo toOwnerInfo() {
  return new OwnerInfo(firstName + " " + lastName, address, city, telephone, "");
}
Now, when we run the test, it looks almost like magic: the browser opens, the names of
the owners are typed in the page, buttons are clicked, pages change, the browser
closes, and JUnit shows us that the test passed. We are finished with our first web Sele-
nium test.
NOTE
A good exercise for you is to write tests for other application journeys.
This will require the development of more POs!
Listing 9.31
toOwnerInfo converter method
The addOwners 
helper method 
adds an owner 
via the Add 
Owner page.


---
**Page 251**

251
System tests
If you run the test again, it will fail. The list of owners will return four people instead
of two, as the test expects—we are running our entire web application, and data is per-
sisted in the database. We need to make sure we can reset the web application when-
ever we run a test, and we discuss that in the next section. 
9.3.3
Patterns and best practices
You probably noticed that the amount of code required to get our first system test
working was much greater than in previous chapters. In this section, I introduce some
patterns and best practices that will help you write maintainable web tests. These pat-
terns come from my own experience after writing many such tests. Together with
Guerra and Gerosa, I proposed some of these patterns at the PLoP conference in
2014.
PROVIDE A WAY TO SET THE SYSTEM TO THE STATE THAT THE WEB TEST REQUIRES
To ensure that the Find Owners journey worked properly, we needed some owners in
the database. We added them by repeatedly navigating to the Add Owner page, filling
in the form, and saving it. This strategy works fine in simple cases. However, imagine a
more complicated scenario where your test requires 10 different entities in the data-
base. Visiting 10 different web pages in a specific order is too much work (and also
slow, since the test would take a considerable amount of time to visit all the pages).
 In such cases, I suggest creating all the required data before running the test. But
how do you do that if the web application runs standalone and has its own database?
You can provide web services (say, REST web services) that are easily accessible by the
test. This way, whenever you need some data in the application, you can get it through
simple requests. Imagine that instead of visiting the pages, we call the API. From the
test side, we implement classes that abstract away all the complexity of calling a
remote web service. The following listing shows how the previous test would look if it
consumed a web service.
@Test
void findOwnersBasedOnTheirLastNames() {
  AddOwnerInfo owner1 = new AddOwnerInfo(
    ➥ "John", "Doe", "some address", "some city", "11111");
  AddOwnerInfo owner2 = new AddOwnerInfo(
    ➥ "Jane", "Doe", "some address", "some city", "11111");
  AddOwnerInfo owner3 = new AddOwnerInfo(
    ➥ "Sally", "Smith", "some address", "some city", "11111");
  OwnersAPI api = new OwnersAPI();  
  api.add(owner1);
  api.add(owner2);
  api.add(owner3);
  page.visit();
  ListOfOwnersPage listPage = page.findOwners("Doe");
  List<OwnerInfo> all = listPage.all();
Listing 9.32
Our test if we had a web service to add owners
Calls the API. We no longer need to visit 
the Add Owner page. The OwnersAPI 
class hides the complexity of calling 
a web service.


---
**Page 252**

252
CHAPTER 9
Writing larger tests
  assertThat(all).hasSize(2).
      containsExactlyInAnyOrder(owner1.toOwnerInfo(), owner2.toOwnerInfo());
}
Creating simple REST web services is easy today, given the full support of the web
frameworks. In Spring MVC (or Ruby, or Django, or Asp.Net Core), you can write one
in a couple of lines. The same thing happens from the client side. Calling a REST web
service is simple, and you don’t have to write much code.
 You may be thinking of security issues. What if you do not want the web services in
production? If they are only for testing purposes, your software should hide the API
when in production and allow the API only in the testing environment.
 Moreover, do not be afraid to write different functionalities for these APIs, if doing
so makes the testing process easier. If your web page needs a combination of Products,
Invoices, Baskets, and Items, perhaps you can devise a web service solely to help the
test build up complex data. 
MAKE SURE EACH TEST ALWAYS RUNS IN A CLEAN ENVIRONMENT
Similar to what we did earlier when testing SQL queries, we must make sure our tests
always run in a clean version of the web application. Otherwise, the test may fail for
reasons other than a bug. This means databases (and any other dependencies) must
only contain the bare minimum amount of data for the test to start.
 We can reset the web application the same way we provide data to it: via web ser-
vices. The application could provide an easy backdoor that resets it. It goes without
saying that such a web service should never be deployed in production.
 Resetting the web application often means resetting the database. You can imple-
ment that in many different ways, such as truncating all the tables or dropping and re-
creating them.
WARNING
Be very careful. The reset backdoor is nice for tests, but if it is
deployed into production, chaos may result. If you use this solution, make
sure it is only available in the test environment!
GIVE MEANINGFUL NAMES TO YOUR HTML ELEMENTS
Locating elements is a vital part of a web test, and we do that by, for example,
searching for their name, class, tag, or XPath. In one of our examples, we first
searched for the form the element was in and then found the element by its tag. But
user interfaces change frequently during the life of a website. That is why web test
suites are often highly unstable. We do not want a change in the presentation of a
web page (such as moving a button from the left menu to the right menu) to break
the test.
 Therefore, I suggest assigning proper (unique) names and IDs to elements that
will play a role in the test. Even if the element does not need an ID, giving it one will
simplify the test and make sure the test will not break if the presentation of the ele-
ment changes.


---
**Page 253**

253
System tests
 If for some reason an element has a very unstable ID (perhaps it is dynamically
generated), we need to create any specific property for the testing. HTML5 allows us
to create extra attributes on HTML tags, like the following example.
<input type="text"
id="customer_\${i}"
name="customer"
data-selenium="customer-name" />    
If you think this extra property may be a problem in the production environment,
remove it during deployment. There are many tools that manipulate HTML pages
before deploying them (minification is an example).
NOTE
Before applying this pattern to the project, you may want to talk to
your team’s frontend lead. 
VISIT EVERY STEP OF A JOURNEY ONLY WHEN THAT JOURNEY IS UNDER TEST
Unlike unit testing, building up scenarios on a system test can be complicated. We saw
that some journeys may require the test to navigate through many different pages
before getting to the page it wants to test.
 Imagine a specific page A that requires the test to visit pages B, C, D, E, and F
before it can finally get to A and test it. A test for that page is shown here.
@Test
void longest() {
  BPage b = new BPage();    
  b.action1(..);
  b.action2(..);
  CPage c = new CPage();   
  c.action1(..);
  DPage d = new DPage();   
  d.action1(..);
  d.action2(..);
  EPage e = new EPage();
  e.action1(..);
  FPage e = new FPage();
  f.action1(..);
  // finally!!
  APage a = new APage();
  a.action1();
  assertThat(a.confirmationAppears()).isTrue();
}
Listing 9.33
HTML element with a property that makes it easy to find
Listing 9.34
A very long test that calls many POs
It is easy to find the HTML element 
that has a data-selenium attribute 
with customer-name as its value.
Calls the 
first PO
Calls a 
second PO
Calls a third 
PO, and so on


---
**Page 254**

254
CHAPTER 9
Writing larger tests
Note how long and complex the test is. We discussed a similar problem, and our
solution was to provide a web service that enabled us to skip many of the page visits.
But if visiting all these pages is part of the journey under test, the test should visit
each one. If one or two of these steps are not part of the journey, you can use the
web services. 
ASSERTIONS SHOULD USE DATA THAT COMES FROM THE POS
In the Find Owners test, our assertions focused on checking whether all the owners
were on the list. In the code, the FindOwnersPage PO provided an all() method that
returned the owners. The test code was only responsible for the assertion. This is a
good practice. Whenever your tests require information from the page for the asser-
tion, the PO provides this information. Your JUnit test should not locate HTML ele-
ments by itself. However, the assertions stay in the JUnit test code. 
PASS IMPORTANT CONFIGURATIONS TO THE TEST SUITE
The example test suite has some hard-coded details, such as the local URL of the
application (right now, it is localhost:8080) and the browser to run the tests (currently
Safari). However, you may need to change these configurations dynamically. For
example, your continuous integration may need to run the web app on a different
port, or you may want to run your test suite on Chrome.
 There are many different ways to pass configuration to Java tests, but I usually opt
for the simplest approach: everything that is a configuration is provided by a method
in  my PageObject base class. For example, a String baseUrl() method returns the
base URL of the application, and a WebDriver browser() method returns the con-
crete instance of WebDriver. These methods then read from a configuration file or an
environment variable, as those are easy to pass via build scripts. 
RUN YOUR TESTS IN MULTIPLE BROWSERS
You should run your tests in multiple browsers to be sure everything works every-
where. But I don’t do this on my machine, because it takes too much time. Instead, my
continuous integration (CI) tool has a multiple-stage process that runs the web test
suite multiple times, each time passing a different browser. If configuring such a CI is
an issue, consider using a service such as SauceLabs (https://saucelabs.com), which
automates this process for you. 
9.4
Final notes on larger tests
I close this chapter with some points I have not yet mentioned regarding larger tests.
9.4.1
How do all the testing techniques fit?
In the early chapters of this book, our goal was to explore techniques that would help
you engineer test cases systematically. In this chapter, we discuss a more orthogonal
topic: how large should our tests be? I have shown you examples of larger component
tests, integration tests, and system tests. But regardless of the test level, engineering
good test cases should still be the focus.


---
**Page 255**

255
Final notes on larger tests
 When you write a larger test, use the requirement and its boundaries, the structure
of the code, and the properties it should uphold to engineer good test cases. The chal-
lenge is that an entire component has a much larger requirement and a much larger
code base, which means many more tests to engineer.
 I follow this rule of thumb: exercise everything at the unit level (you can easily
cover entire requirements and structures at the unit level), and exercise the most
important behavior in larger tests (so you have more confidence that the program will
work when the pieces are put together). It may help to reread about the testing pyra-
mid in section 1.4 in chapter 1.
9.4.2
Perform cost/benefit analysis
One of the testing mantras is that a good test is cheap to write but can capture import-
ant bugs. Unit tests are cheap to write, so we do not have to think much about cost.
 Larger tests may not be cheap to write, run, or maintain. I have seen integration
test suites that take hours to run—and cases where developers spend hours writing a
single integration test.
 Therefore, it is fundamental to perform a simple cost/benefit analysis. Questions
like “How much will it cost me to write this test?” “How much will it cost to run?”
“What is the benefit of this test? What bugs will it catch?” and “Is this functionality
already covered by unit tests? If so, do I need to cover it via integration tests, too?” may
help you understand whether this is a fundamental test.
 The answer will be “yes” in many cases. The benefits outweigh the costs, so you
should write the test. If the cost is too high, consider simplifying your test. Can you
stub parts of the test without losing too much? Can you write a more focused test that
exercises a smaller part of the system? As always, there is no single good answer or
golden rule to follow. 
9.4.3
Be careful with methods that are covered but not tested
Larger tests exercise more classes, methods, and behaviors together. In addition to all
the trade-offs discussed in this chapter, with larger tests, the chances of covering a
method but not testing it are much higher.
 Vera-Pérez and colleagues (2019) coined the term pseudo-tested methods. These
methods are tested, but if we replace their entire implementation with a simple
return null, tests still pass. And believe it or not, Vera-Pérez and colleagues show that
pseudo-tested methods happen in the wild, even in important open source projects.
This is another reason I defend both unit tests and larger tests, used together to
ensure that everything works. 
9.4.4
Proper code infrastructure is key
Integration and system tests both require a decent infrastructure behind the scenes.
Without it, we may spend too much time setting up the environment or asserting that
behavior was as expected. My key advice here is to invest in test infrastructure. Your


---
**Page 256**

256
CHAPTER 9
Writing larger tests
infrastructure should help developers set up the environment, clean up the environ-
ment, retrieve complex data, assert complex data, and perform whatever other com-
plex tasks are required to write tests. 
9.4.5
DSLs and tools for stakeholders to write tests
In this chapter, we wrote the system tests ourselves with lots of Java code. At this level,
it is also common to see more automation. Some tools, such as the Robot framework
(https://robotframework.org) and Cucumber (https://cucumber.io), even allow you
to write tests in language that is almost completely natural. These tools make a lot of
sense if you want others to write tests, too, such as (non-technical) stakeholders. 
9.4.6
Testing other types of web systems
The higher we go in levels of testing, such as web testing, the more we start to think
about the frameworks and environment our application runs in. Our web application
is responsive; how do we test for that? If we use Angular or React, how do we test it?
Or, if we use a non-relational database like Mongo, how do we test it?
 Testing these specific technologies is far beyond the scope of this book. My sugges-
tion is that you visit those communities and explore their state-of-the-art tools and
bodies of knowledge. All the test case engineering techniques you learn in this book
will apply to your software, regardless of the technology.
SYSTEM TESTS IN SOFTWARE OTHER THAN WEB APPLICATIONS
I used web applications to exemplify system tests because I have a lot of experience
with them. But the idea of system testing can be applied to any type of software you
develop. If your software is a library or framework, your system tests will exercise the
entire library as the clients would. If your software is a mobile application, your system
tests will exercise the mobile app as the clients would.
 The best practices I discussed still apply. Engineering system tests will be harder
than engineering unit tests, and you may need some infrastructure code (like the POs
we created) to make you more productive. There are probably also specific best prac-
tices for your type of software—be sure to do some research. 
Exercises
9.1
Which of the following recommendations should you follow to keep a web
application testable? Select all that apply.
A Use TypeScript instead of JavaScript.
B Make sure the HTML elements can be found easily from the tests.
C Make sure requests to web servers are performed asynchronously.
D Avoid inline JavaScript in an HTML page.
9.2
Which of the following statements is true about end-to-end/system testing?
A End-to-end testing cannot be automated for web applications and there-
fore has to be performed manually.


---
**Page 257**

257
Summary
B In web testing, end-to-end testing is more important than unit testing.
C End-to-end testing can be used to verify whether the frontend and back-
end work together well.
D End-to-end tests are, like unit tests, not very realistic.
9.3
Which of the following is true about page objects?
A POs abstract the HTML page to facilitate the engineering of end-to-end
tests.
B POs cannot be used in highly complex web applications.
C By introducing a PO, we no longer need libraries like Selenium.
D POs usually make the test code more complex.
9.4
Which of the following are important recommendations for developers who are
engineering integration and system test suites? Choose all that apply.
A What can be tested via unit testing should be tested via unit testing. Use
integration and system tests for bugs that can only be caught at that level.
B It is fundamental for developers to have a solid infrastructure to write
such tests, as otherwise, they would feel unproductive.
C If something is already covered via unit testing, you should not cover it
(again) via integration testing.
D Too many integration tests may mean your application is badly designed.
Focus on unit tests.
9.5
Which of the following can cause web tests to be flaky (that is, sometimes pass,
sometimes fail)? Choose all that apply.
A AJAX requests that take longer than expected
B The use of LESS and SASS instead of pure CSS
C The database of the web app under test is not being cleaned up after every
test run
D Some components of the web app were unavailable at the time
Summary
Developers benefit from writing larger tests, ranging from testing entire compo-
nents together, to integrating with external parties, to entire systems.
Engineering larger tests is more challenging than writing unit tests, because the
component under test is probably much bigger and more complex than a sin-
gle unit of the system.
All the test case engineering techniques we have discussed—specification-based
testing, boundary testing, structural testing, and property-based testing—apply
to larger tests.
Investing in a good test infrastructure for large tests is a requirement. Without
it, you will spend too much time writing a single test case.


---
**Page 258**

258
Test code quality
You have probably noticed that once test infected, the number of JUnit tests a soft-
ware development team writes and maintains can become significant. In practice,
test code bases grow quickly. Moreover, we have observed that Lehman’s law of evo-
lution, “Code tends to rot, unless one actively works against it” (1980), also applies
to test code. A 2018 literature review by Garousi and Küçük shows that our body of
knowledge about things that can go wrong with test code is already comprehensive.
 As with production code, we must put extra effort into writing high-quality test code
bases so they can be maintained and developed sustainably. In this chapter, I discuss two
opposite perspectives of writing test code. First, we examine what constitutes good
and maintainable test code, and best practices that can help you keep complexity
under control. Then we look at what constitutes problematic test code. We focus on
key test smells that hinder test code comprehension and evolution.
 I have discussed some of this material informally in previous chapters. This
chapter consolidates that knowledge.
This chapter covers
Principles and best practices of good and 
maintainable test code
Avoiding test smells that hinder the 
comprehension and evolution of test code


