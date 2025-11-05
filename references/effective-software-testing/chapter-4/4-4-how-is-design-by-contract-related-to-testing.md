# 4.4 How is design-by-contract related to testing? (pp.109-110)

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


