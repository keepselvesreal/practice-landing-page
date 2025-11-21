# 4.3.1 Inheritance and contracts (pp.107-109)

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


