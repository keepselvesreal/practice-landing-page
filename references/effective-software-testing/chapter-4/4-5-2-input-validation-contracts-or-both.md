# 4.5.2 Input validation, contracts, or both? (pp.110-112)

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


