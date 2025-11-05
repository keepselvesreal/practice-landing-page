# 4.1.0 Introduction [auto-generated] (pp.98-99)

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


