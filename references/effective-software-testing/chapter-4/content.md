# Designing contracts (pp.97-117)

---
**Page 97**

97
Designing contracts
Imagine a piece of software that handles a very complex financial process. For that
big routine to happen, the software system chains calls to several subroutines (or
classes) in a complex flow of information: that is, the results of one class are passed
to the next class, whose results are again passed to the next class, and so on. As
usual, the data comes from different sources, such as databases, external web ser-
vices, and users. At some point in the routine, the class TaxCalculator (which han-
dles calculating a specific tax) is called. From the requirements of this class, the
calculation only makes sense for positive numbers.
 We need to think about how we want to model such a restriction. I see three
options when facing such a restriction:
Ensure that classes never call other classes with invalid inputs. In our exam-
ple, any other classes called TaxCalculator will ensure that they will never
pass a negative number. While this simplifies the code of the class under
This chapter covers
Designing pre-conditions, post-conditions, and 
invariants
Understanding the differences between contracts 
and validation


---
**Page 98**

98
CHAPTER 4
Designing contracts
development, since it does not need to deal with the special cases, it adds com-
plexity to the caller classes that need to be sure they never make a bad call.
Program in a more defensive manner, ensuring that if an invalid input happens,
the system halts and returns an error message to the user. This adds a little com-
plexity to every class in the system, as they all have to know how to handle
invalid inputs. At the same time, it makes the system more resilient. However,
coding defensively in an ad hoc manner is not productive. You may end up add-
ing unnecessary code, such as restrictions that were already checked.
My favorite approach, and the goal of this chapter, is to define clear contracts for
each class we develop. These contracts clearly establish what the class requires as
pre-conditions, what the class provides as post-conditions, and what invariants
always hold for the class. This is a major modeling activity for which the design-by-
contract idea will inspire us (originally proposed by Bertrand Meyer).
Such contract decisions happen while the developer is implementing the functional-
ity. That is why design-by-contract appears on the “testing to guide development” side
of the development flow I propose (see figure 1.4).
4.1
Pre-conditions and post-conditions
Going back to the tax calculation example, we need to reflect on pre-conditions that the
method needs to function properly, as well as its post-conditions: what the method guar-
antees as outcomes. We already mentioned a pre-condition: the method does not
accept negative numbers. A possible post-condition of this method is that it also does
not return negative numbers.
 Once the method’s pre- and post-conditions are established, it is time to add
them to the source code. Doing so can be as simple as an if instruction, as shown in
the following listing.
public class TaxCalculator {
  public double calculateTax(double value) {
    if(value < 0) { 
      throw new RuntimeException("Value cannot be negative.");
    }
    double taxValue = 0;
    // some complex business rule here...
    // final value goes to 'taxValue'
    if(taxValue < 0) { 
      throw new RuntimeException("Calculated tax value
      ➥ cannot be negative.");
    }
Listing 4.1
TaxCalculator with pre- and post-conditions
The pre-condition: a 
simple if ensuring that 
no invalid values pass
The post-condition is also 
implemented as a simple if. If 
something goes wrong, we throw an 
exception, alerting the consumer that 
the post-condition does not hold.


---
**Page 99**

99
Pre-conditions and post-conditions
    return taxValue;
  }
}
NOTE
You may be wondering what value, the input parameter of the
calculateTax method, represents. Also, how is the tax rate set? In real life, the
requirements and implementation of a tax calculator would be much more
complex—this simple code lets you focus on the technique. Bear with me!
Note that the pre- and post-conditions ensure different things. Pre-conditions (in this
case, a single pre-condition) ensure that the input values received by a method adhere
to what it requires. Post-conditions ensure that the method returns what it promises to
other methods.
 You may be wondering, “How can I have a value that breaks the post-condition if I
am coding the implementation of this method?” In this example, you hope that your
implementation will never return a negative number. But in very complex implemen-
tations, a bug may slip in! If bugs did not exist, there would be no reason for this
book. The post-condition check ensures that if there is a bug in the implementation,
the method will throw an exception instead of returning an invalid value. An excep-
tion will make your program halt—and halting is often much better than continuing
with an incorrect value.
 Making your pre- and post-conditions clear in the documentation is also funda-
mental and very much recommended. Let’s do that in the next listing.
/**
 * Calculates the tax according to (some
 * explanation here...)
 *
 * @param value the base value for tax calculation. Value has
 *              to be a positive number.
 * @return the calculated tax. The tax is always a positive number.
 */
public double calculateTax(double value) { ... }
4.1.1
The assert keyword
The Java language offers the keyword assert, which is a native way of writing asser-
tions. In the previous example, instead of throwing an exception, we could write
assert value >= 0 : "Value cannot be negative.". If value is not greater than or
equal to 0, the Java Virtual Machine (JVM) will throw an AssertionError. In the fol-
lowing listing, I show a version of the TaxCalculator using asserts.
public class TaxCalculator {
  public double calculateTax(double value) {
Listing 4.2
Javadoc of the calculateTax method describing its contract
Listing 4.3
TaxCalculator with pre- and post-conditions implemented via asserts


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


---
**Page 106**

106
CHAPTER 4
Designing contracts
understand the impact of the change, your system may behave unexpectedly—and
this is how contract changes are related to testing and quality.
 The easiest way to understand the impact of a change is not to look at the change
itself or at the class in which the change is happening, but at all the other classes (or
dependencies) that may use the changing class. Figure 4.1 shows the calculateTax()
method and  three other (imaginary) classes that use it. When these classes were cre-
ated, they knew the pre-conditions of the calculateTax() at that point: “value has to
be greater than or equal to 0.” They knew calculateTax() would throw an exception
if they passed a negative number. So, these client classes currently ensure that they
never pass a negative number to calculateTax().
Notice that m1() passes 50 as value, m2() passes 150, and m3 passes a value from a
database (after ensuring that the value is greater than 0). Now, suppose we change the
pre-condition to value > 100. What will happen to these three dependencies? Nothing
will happen to m2(): by pure luck, the new pre-condition holds for the value of 150.
However, we cannot say the same for the other two methods: m1() will crash, and m3()
will have erratic behavior, as some values from the database may be greater than 100,
while others may be smaller than 100. What do we learn here? If we change our pre-
conditions to something stronger and more restrictive, such as accepting a smaller set
of values (100 to infinity instead of 0 to infinity), we may have a problem with classes
that depend on the previously defined contract.
 Now, suppose calculateTax() changes its pre-condition to accept negative num-
bers as inputs. In this case, the three existing dependencies would not break. The new
pre-condition is more relaxed than the previous one: it accepts a larger set of inputs.
What do we learn? If we change our pre-conditions to something weaker and less
restrictive, we do not break the contracts with the clients of the changing class.
Ta
tor
xCalcula
calculateTax(value),
value >= 0
The
method is used by many other classes in the
calculateTax()
system. The
class doesn’t know about them.
TaxCalculator
Dependency 1
m1() {
calculateTax(50);
}
Dependency 2
m2() {
calculateTax(150);
}
Dependency 3
m3() {
t = getFromDB()
ensur      0
e t >
c
teTax(t);
alcula
}
Figure 4.1
The calculateTax() method and all the classes that possibly depend on it


---
**Page 107**

107
Changing contracts, and the Liskov substitution principle
 The same type of reasoning can be applied to the post-conditions. There, we
observe the inverse relation. The clients know that calculateTax never returns nega-
tive numbers. Although this would make no business sense, let’s suppose the method
now also returns negative numbers. This is a breaking change: the clients of this class
do not expect negative numbers to come back and probably are not ready to handle
them. The system may behave erratically, depending on whether the returned tax is
negative. We learn that if we change our post-condition to something weaker and less
restrictive, our clients may break.
 On the other hand, if the post-condition changes to “the returned value is always
greater than 100,” the clients will not break. They were already prepared for the
returning value to be between 0 and infinity, and the range from 100 to infinity is a
subset of the previous domain. We learn that changing post-conditions to something
stronger and more restrictive prevents breaking changes in the dependencies.
4.3.1
Inheritance and contracts
We mostly use Java for the examples in this book, and Java is an object-oriented lan-
guage, so I must discuss what happens when we use inheritance. Figure 4.2 shows that
the TaxCalculator class has many children (TaxCalculatorBrazil which calculates
taxes in Brazil, TaxCalculatorNL, which calculates taxes in the Netherlands, and so
on). These child classes all override calculateTax() and change the pre- or post-
conditions one way or another. Are these contract changes breaking changes?
 We can apply the same reasoning as when we discussed changing contracts. Let’s
start by focusing on the client class rather than the child classes. Suppose the client
Ta
tor
xCalcula
c
teTax(value)
alcula
v l
returns
0
a ue >= 0,         >=
Client
Dep
on
ends
Note how all children changed either the pre- or the post-condition,
in comparison to the base class. Are these breaking changes or not?
Ta
torBrazil
xCalcula
c
eTax(value)
alculat
v           returns
,inf]
alue >= 0,         [-inf
Ta
torUS
xCalcula
c
teTax(value)
alcula
v
ue >= 100
r       >= 0
al         ,  eturns
TaxCalculatorNL
c
teTax(value)
alcula
val       f,inf], returns >= 0
ue [-in
Figure 4.2
A base class and its child classes. The client depends on the base class, which means any of its 
children may be used at run time.


---
**Page 108**

108
CHAPTER 4
Designing contracts
class receives a TaxCalculator in its constructor and later uses it in its methods. Due
to polymorphism, we know that any of the child classes can also be passed to the cli-
ent: for example, we can pass a TaxCalculatorBrazil or a TaxCalculatorUS, and it
will be accepted because they are all children of the base class.
 Since the client class does not know which tax calculator was given to it, it can only
assume that whatever class it received will respect the pre- and post-conditions of the
base class (the only class the client knows). In this case, value must be greater than or
equal to 0 and should return a value greater than or equal to 0. Let’s explore what will
happen if each of the child classes is given to the client class:

TaxCalculatorBrazil has the same pre-conditions as the base class. This means
there is no way the client class will observe strange behavior regarding the pre-
conditions if it is given TaxCalculatorBrazil. On the other hand, the Tax-
CalculatorBrazil class has a post-condition that the returned value is any num-
ber. This is bad. The client class expects only values that are greater than or equal
to zero; it does not expect negative numbers. So if TaxCalculatorBrazil returns
a negative number to the client, this may surprise the client and lead to a failure.

TaxCalculatorUS has the following pre-condition: “value greater than or equal
to 100.” This pre-condition is stronger than the pre-condition of the base class
(value >= 0), and the client class does not know that. Thus the client may call
the tax calculator with a value that is acceptable for the base class but not
acceptable for TaxCalculatorUS. We can expect a failure to happen. The post-
condition of TaxCalculatorUS is the same as that of the base class, so we do not
expect problems there.

TaxCalculatorNL has a different pre-condition from the base class: it accepts
any value. In other words, the pre-condition is weaker than that of the base
class. So although the client is not aware of this pre-condition, we do not expect
failures, as TaxCalculatorNL can handle all of the client’s inputs.
If we generalize what we observe in this example, we arrive at the following rules
whenever a subclass S (for example, TaxCalculatorBrazil) inherits from a base class
B (for example, TaxCalculator):
1
The pre-conditions of subclass S should be the same as or weaker (accept more
values) than the pre-conditions of base class B.
2
The post-conditions of subclass S should be the same as or stronger (return
fewer values) than the post-conditions of base class B.
This idea that a subclass may be used as a substitution for a base class without
breaking the expected behavior of the system is known as the Liskov substitution
principle (LSP). This principle was introduced by Barbara Liskov in a 1987 keynote
and later refined by her and Jeannette Wing in the famous “A behavioral notion of
subtyping” paper (1994). The LSP became even more popular among software
developers when Robert Martin popularized the SOLID principles, where the “L”
stands for LSP.


---
**Page 109**

109
How is design-by-contract related to testing?
NOTE
A well-known best practice is to avoid inheritance whenever possible
(see Effective Java’s item 16, “favor compostion over inheritance”). If you avoid
inheritance, you naturally avoid all the problems just discussed. But it is not the
goal of this book to discuss best practices in object-oriented design. If you ever
need to use inheritance, you now know what to pay attention to. 
4.4
How is design-by-contract related to testing?
Defining clear pre-conditions, post-conditions, and invariants (and automating them
in your code via, for example, assertions) helps developers in many ways. First, asser-
tions ensure that bugs are detected early in the production environment. As soon as a
contract is violated, the program halts instead of continuing its execution, which is
usually a good idea. The error you get from an assertion violation is very specific, and
you know precisely what to debug for. This may not be the case without assertions.
Imagine a program that performs calculations. The method that does the heavy calcu-
lation does not work well with negative numbers. However, instead of defining such a
restriction as an explicit pre-condition, the method returns an invalid output if a neg-
ative number comes in. This invalid number is then passed to other parts of the sys-
tem, which may incur other unexpected behavior. Given that the program does not
crash per se, it may be hard for the developer to know that the root cause of the prob-
lem was a violation of the pre-condition.
 Second, pre-conditions, post-conditions, and invariants provide developers with
ideas about what to test. As soon as we see the qty > 0 pre-condition, we know this is
something to exercise via unit, integration, or system tests. Therefore, contracts do
not replace (unit) testing: they complement it. In chapter 5, you will see how to use
such contracts and write test cases that automatically generate random input data,
looking for possible violations.
 Third, such explicit contracts make the lives of consumers much easier. The class
(or server, if you think of it as a client-server application) does its job as long as its meth-
ods are used properly by the consumer (or client). If the client uses the server’s meth-
ods so that their pre-conditions hold, the server guarantees that the post-conditions will
hold after the method call. In other words, the server makes sure the method delivers
what it promises. Suppose a method expects only positive numbers (as a pre-condition)
and promises to return only positive numbers (as a post-condition). As a client, if you
pass a positive number, you are sure the server will return a positive number and never
a negative number. The client, therefore, does not need to check if the return is nega-
tive, simplifying its code.
 I do not see design-by-contract as a testing practice per se. I see it as more of a
design technique. That is also why I include it in the development part of the devel-
oper testing workflow (figure 1.4).
NOTE
Another benefit of assertions is that they serve as oracles during fuzz-
ing or other intelligent testing. These tools reason about the pre-conditions,
post-conditions, and invariants that are clearly expressed in the code and


---
**Page 110**

110
CHAPTER 4
Designing contracts
look for ways to break them. If you want to read more about fuzzing, I suggest
The Fuzzing Book (https://fuzzingbook.org). 
4.5
Design-by-contract in the real world
Let me close this chapter with some pragmatic tips on how to use design-by-contract
in practice.
4.5.1
Weak or strong pre-conditions?
A very important design decision when modeling contracts is whether to use strong or
weak contracts. This is a matter of trade-offs.
 Consider a method with a weak pre-condition. For example, the method accepts
any input value, including null. This method is easy for clients to use for the clients:
any call to it will work, and the method will never throw an exception related to a pre-
condition being violated (as there are no pre-conditions to be violated). However, this
puts an extra burden on the method, as it has to handle any invalid inputs.
 On the other hand, consider a strong contract: the method only accepts positive
numbers and does not accept null values. The extra burden is now on the side of the
client. The client must make sure it does not violate the pre-conditions of the method.
This may require extra code.
 There is no clear way to go, and the decision should be made considering the
whole context. For example, many methods of the Apache Commons library have
weak pre-conditions, making it much easier for clients to use the API. Library develop-
ers often prefer to design weaker pre-conditions and simplify the clients’ lives. 
4.5.2
Input validation, contracts, or both?
Developers are aware of how important input validation is. A mistake in the validation
may lead to security vulnerabilities. Therefore, developers often handle input valida-
tion whenever data comes from the end user.
 Consider a web application that stores products for an online store. To add a new
product, a user must pass a name, a description, and a value. Before saving the new
product to the database, the developer performs checks to ensure that the input val-
ues are as expected. Here is the greatly simplified pseudo-code.
class ProductController {
  // more code here ...
  public void add(String productName, String productDescription,
   double price) { 
    String sanitizedProductName = sanitize(productName); 
    String sanitizedProductDescription = sanitize(productDescription); 
Listing 4.12
Pseudo-code for input validation
These parameters come directly from the 
end user, and they need to be validated 
before being used.
We use the made-up sanitize()
method to sanitize (remove invalid
characters from) the inputs.


---
**Page 111**

111
Design-by-contract in the real world
    if(!isValidProductName(sanitizedProductName)) { 
       errorMessages.add("Invalid product name");
    }
    if(!isValidProductDescription(sanitizedProductDescription)) { 
       errorMessages.add("Invalid product description");
    }
    if(!isValidPriceRange(price)) { 
       errorMessages.add("Invalid price");
    }
    if(errorMessages.empty()) { 
      Product newProduct = new Product(sanitizedProductName,
        ➥ productDescription, price);
      database.save(newProduct);
      redirectTo("productPage", newProduct.getId());
    } else { 
      redirectTo("addProduct", errorMessages.getErrors());
    }
  }
}
Given all this validation before the objects are even created, you may be thinking, “Do
I need to model pre-conditions and post-conditions in the classes and methods? I
already know the values are valid!” Let me give you a pragmatic perspective.
 First, let’s focus on the difference between validation and contracts. Validation
ensures that bad or invalid data that may come from users does not infiltrate our sys-
tems. For example, if the user types a string in the Quantity field on the Add Product
page, we should return a friendly message saying “Quantity should be a numeric
value.” This is what validation is about: it validates that the data coming from the user
is correct and, if not, returns a message.
 On the other hand, contracts ensure that communication between classes happens
without a problem. We do not expect problems to occur—the data is already vali-
dated. However, if a violation occurs, the program halts, since something unexpected
happened. The application also returns an error message to the user. Figure 4.3 illus-
trates the difference between validation and code contracts.
 Both validation and contracts should happen, as they are different. The question is
how to avoid repetition. Maybe the validation and pre-condition are the same, which
means either there is code repetition or the check is happening twice.
 I tend to be pragmatic. As a rule of thumb, I prefer to avoid repetition. If the input
validation already checked for, say, the length of the product description being
greater than 10 characters, I don’t re-check it as a pre-condition in the constructor of
the Product class. This implies that no instances of Product are instantiated without
input validation first. Your architecture must ensure that some zones of the code are
safe and that data has been already cleaned up.
 On the other hand, if a contract is very important and should never be broken
(the impact could be significant), I do not mind using a little repetition and extra
Ensures that
values are
within the
expected
format,
range, and
so on
Only when the parameters are 
valid do we create objects. 
Is this a replacement for 
design-by-contract?
Otherwise, we return 
to the Add Product 
page and display the 
error messages.


---
**Page 112**

112
CHAPTER 4
Designing contracts
computational power to check it at both input-validation time and contract-checking
time. Again, consider the context to decide what works best for each situation.
NOTE
Arie van Deursen offers a clear answer on Stack Overflow about the
differences between design-by-contract and validation, and I strongly recom-
mend that you check it out: https://stackoverflow.com/a/5452329. 
4.5.3
Asserts and exceptions: When to use one or the other
Java does not offer a clear mechanism for expressing code contracts. Only a few
popular programming languages do, such as F#. The assert keyword in Java is okay,
but if you forget to enable it in the runtime, the contracts may not be checked in
production. That is why many developers prefer to use (checked or unchecked)
exceptions.
 Here is my rule of thumb:
If I am modeling the contracts of a library or utility class, I favor exceptions, fol-
lowing the wisdom of the most popular libraries.
If I am modeling business classes and their interactions and I know that the
data was cleaned up in previous layers (say, in the controller of a Model-View-
Controller [MVC] architecture), I favor assertions. The data was already vali-
dated, and I am sure they start their work with valid data. I do not expect pre-
conditions or post-conditions to be violated, so I prefer to use the assert
instruction. It will throw an AssertionError, which will halt execution. I also
ensure that my final user does not see an exception stack trace but instead is
shown a more elegant error page.
If I am modeling business classes but I am not sure whether the data was already
cleaned up, I go for exceptions.
Input validation
Input
data
User
Bad input values that come from the
user do not get to the main classes.
Instead, a message is displayed, and
the user tries again.
If a class makes a bad call to another class, e.g., a pre-condition violation,
the program halts, as this should not happen. The user may also be informed
about the problem, although commonly with a more generic message.
Class B
Class A
Class C
Figure 4.3
The difference between validation and code contracts. Each 
circle represents one input coming to the system.


---
**Page 113**

113
Design-by-contract in the real world
When it comes to validation, I tend not to use either assertions or exceptions. I prefer
to model validations in more elegant ways. First, you rarely want to stop the validation
when the first check fails. Instead, it is more common to show a complete list of errors
to the user. Therefore, you need a structure that allows you to build the error message
as you go. Second, you may want to model complex validations, which may require
lots of code. Having all the validations in a single class or method may lead to code
that is very long, highly complex, and hard to reuse.
 If you are curious, I suggest the Specification pattern proposed by Eric Evans in his
seminal book, Domain-Driven Design (2004). Another nice resource is the article “Use
of Assertions” by John Regehr (2014); it discusses the pros and cons of assertions, mis-
conceptions, and limitations in a very pragmatic way.
 Finally, in this chapter, I used native Java exceptions, such as RuntimeException. In
practice, you may prefer to throw more specialized and semantic exceptions, such as
NegativeValueException. That helps clients treat business exceptions differently
from real one-in-a-million exceptional behavior.
NOTE
Formal semantics scholars do not favor the use of assertions over
exceptions. I should not use the term design-by-contract for the snippets where I
use an if statement and throw an exception—that is defensive programming.
But, as I said before, I am using the term design-by-contract for the idea of
reflecting about contracts and somehow making them explicit in the code. 
4.5.4
Exception or soft return values?
We saw that a possible way to simplify clients’ lives is to make your method return a
“soft value” instead of throwing an exception. Go back to listing 4.5 for an example.
 My rule of thumb is the following:
If it is behavior that should not happen, and clients would not know what to do
with it, I throw an exception. That would be the case with the calculateTax
method. If a negative value comes in, that is unexpected behavior, and we
should halt the program rather than let it make bad calculations. The monitor-
ing systems will catch the exception, and we will debug the case.
On the other hand, if I can see a soft return for the client method that would allow
the client to keep working, I go for it. Imagine a utility method that trims a string.
A pre-condition of this method could be that it does not accept null strings. But
returning an empty string in case of a null is a soft return that clients can deal with. 
4.5.5
When not to use design-by-contract
Understanding when not to use a practice is as important as knowing when to use it.
In this case, I may disappoint you, as I cannot see a single good reason not to use the
design-by-contract ideas presented in this chapter. The development of object-oriented
systems is all about ensuring that objects can communicate and collaborate properly.
Experience shows me that making the pre-conditions, post-conditions, and invari-
ants explicit in the code is not expensive and does not take a lot of time. Therefore,


---
**Page 114**

114
CHAPTER 4
Designing contracts
I recommend that you consider using this approach. (Note that I am not discussing
input validation here, which is fundamental and has to be done whether or not you
like design-by-contracts.)
 I also want to highlight that design-by-contract does not replace the need for test-
ing. Why? Because, to the best of my knowledge and experience, you cannot express all
the expected behavior of a piece of code solely with pre-conditions, post-conditions, and
invariants. In practice, I suggest that you design contracts to ensure that classes can
communicate with each other without fear, and test to ensure that the behavior of the
class is correct. 
4.5.6
Should we write tests for pre-conditions, post-conditions, 
and invariants?
In a way, assertions, pre-conditions, post-conditions, and invariant checks test the pro-
duction code from the inside. Do we also need to write (unit) tests for them?
 To answer this question, let me again discuss the difference between validation and
pre-conditions. Validation is what you do to ensure that the data is valid. Pre-conditions
explicitly state under what conditions a method can be invoked.
 I usually write automated tests for validation. We want to ensure that our validation
mechanisms are in place and working as expected. On the other hand, I rarely write
tests for assertions. They are naturally covered by tests that focus on other business
rules. I suggest reading Arie van Deursen’s answer on Stack Overflow about writing
tests for assertions (https://stackoverflow.com/a/6486294/165292).
NOTE
Some code coverage tools do not handle asserts well. JaCoCo, for
example, cannot report full branch coverage in assertions. This is another
great example of why you should not use coverage numbers blindly. 
4.5.7
Tooling support
There is more and more support for pre- and post-condition checks, even in languages
like Java. For instance, IntelliJ, a famous Java IDE, offers the @Nullable and @NotNull
annotations (http://mng.bz/QWMe). You can annotate your methods, attributes, or
return values with them, and IntelliJ will alert you about possible violations. IntelliJ can
even transform those annotations into proper assert checks at compile time.
 In addition, projects such as Bean Validation (https://beanvalidation.org) enable
you to write more complex validations, such as “this string should be an email” or “this
integer should be between 1 and 10.” I appreciate such useful tools that help us
ensure the quality of our products. The more, the merrier. 
Exercises
4.1
Which of the following is a valid reason to use assertions in your code?
A To verify expressions with side effects
B To handle exceptional cases in the program


---
**Page 115**

115
Exercises
C To conduct user input validation
D To make debugging easier
4.2
Consider the following squareAt method:
public Square squareAt(int x, int y){
   assert x >= 0;
   assert x < board.length;
   assert y >= 0;
   assert y < board[x].length;
   assert board != null;
   Square result = board[x][y];
   assert result != null;
   return result;
}
Suppose we remove the last assertion (assert result != null), which states
that the result can never be null. Are the existing pre-conditions of the
squareAt method enough to ensure the property of the removed assertion?
What can we add to the class (other than the just-removed post-condition) to
guarantee this property?
4.3
See the squareAt method in exercise 4.3. Which assertion(s), if any, can be
turned into class invariants? Choose all that apply.
A
x >= 0 and x < board.length
B
board != null
C
result != null
D
y >= 0 and y < board[x].length
4.4
You run your application with assertion checking enabled. Unfortunately, it
reports an assertion failure, signaling a class invariant violation in one of the
libraries your application uses. Assume that your application is following all the
pre-conditions established by the library.
Which of the following statements best characterizes the situation and corre-
sponding action to take?
A Since you assume that the contract is correct, the safe action is to run the
server with assertion checking disabled.
B This indicates an integration fault and requires a redesign that involves
the interface that is offered by the library and used by your application.
C This indicates a problem in the implementation of that library and
requires a fix in the library’s code.
D This indicates that you invoked one of the methods of the library in the
wrong way and requires a fix in your application.
4.5
Can static methods have invariants? Explain your answer.


---
**Page 116**

116
CHAPTER 4
Designing contracts
4.6
A method M belongs to a class C and has a pre-condition P and a post-condition
Q. Suppose that a developer creates a class C' that extends C and creates a method
M' that overrides M.
Which one of the following statements correctly explains the relative strength
of the pre- (P') and post-conditions (Q') of the overridden method M'?
A
P' should be equal to or weaker than P, and Q' should be equal to or
stronger than Q.
B
P' should be equal to or stronger than P, and Q' should be equal to or
stronger than Q.
C
P' should be equal to or weaker than P, and Q' should be equal to or
weaker than Q.
D
P' should be equal to or stronger than P, and Q' should be equal to or
weaker than Q.
Summary
Contracts ensure that classes can safely communicate with each other without
surprises.
In practice, designing contracts boils down to explicitly defining the pre-
conditions, post-conditions, and invariants of our classes and methods.
Deciding to go for a weaker or a stronger contract is a contextual decision. Both
have advantages and disadvantages.
Design-by-contract does not remove the need for validation. Validation and con-
tract checking are different things with different objectives. Both should be done.
Whenever changing a contract, we need to reflect on the impact of the change.
Some contract changes might be breaking changes.


---
**Page 117**

117
Property-based testing
So far, we have been doing example-based testing. We judiciously divide the input
space of a program (into partitions), pick one concrete example from all the possi-
ble ones, and write the test case. What if we did not have to pick one concrete
example out of many? What if we could express the property we are trying to exercise
and let the test framework choose several concrete examples for us? Our tests
would be less dependent on a concrete example, and the test framework would be
able to call the method under test multiple times with different input parameters—
usually with zero effort from us.
 This is what property-based testing is about. We do not pick a concrete example;
rather, we define a property (or a set of properties) that the program should
adhere to, and the test framework tries to find a counterexample that causes the
program to break with these properties.
 I have learned that the best way to teach how to write property-based tests is with
multiple examples. So, this chapter presents five different examples with varying
levels of complexity. I want you to focus on my way of thinking and notice how
much creativity is required to write such tests.
This chapter covers
Writing property-based tests
Understanding when to write property-based tests 
or example-based tests


