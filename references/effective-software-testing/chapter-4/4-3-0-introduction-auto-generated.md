# 4.3.0 Introduction [auto-generated] (pp.105-107)

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


