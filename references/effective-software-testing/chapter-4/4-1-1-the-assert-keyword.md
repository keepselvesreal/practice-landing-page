# 4.1.1 The assert keyword (pp.99-100)

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


