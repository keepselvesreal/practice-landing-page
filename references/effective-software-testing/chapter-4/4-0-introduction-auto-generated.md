# 4.0 Introduction [auto-generated] (pp.97-98)

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


