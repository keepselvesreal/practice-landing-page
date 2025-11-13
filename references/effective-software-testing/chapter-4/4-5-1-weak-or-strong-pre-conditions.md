# 4.5.1 Weak or strong pre-conditions? (pp.110-110)

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


