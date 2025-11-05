# 11.1.1 Private methods and test fragility (pp.260-260)

---
**Page 260**

260
CHAPTER 11
Unit testing anti-patterns
11.1
Unit testing private methods
When it comes to unit testing, one of the most commonly asked questions is how to
test a private method. The short answer is that you shouldn’t do so at all, but there’s
quite a bit of nuance to this topic.
11.1.1 Private methods and test fragility
Exposing methods that you would otherwise keep private just to enable unit testing
violates one of the foundational principles we discussed in chapter 5: testing observ-
able behavior only. Exposing private methods leads to coupling tests to implementa-
tion details and, ultimately, damaging your tests’ resistance to refactoring—the most
important metric of the four. (All four metrics, once again, are protection against
regressions, resistance to refactoring, fast feedback, and maintainability.) Instead of
testing private methods directly, test them indirectly, as part of the overarching observ-
able behavior. 
11.1.2 Private methods and insufficient coverage
Sometimes, the private method is too complex, and testing it as part of the observable
behavior doesn’t provide sufficient coverage. Assuming the observable behavior
already has reasonable test coverage, there can be two issues at play:
This is dead code. If the uncovered code isn’t being used, this is likely some extra-
neous code left after a refactoring. It’s best to delete this code.
There’s a missing abstraction. If the private method is too complex (and thus is
hard to test via the class’s public API), it’s an indication of a missing abstraction
that should be extracted into a separate class.
Let’s illustrate the second issue with an example.
public class Order
{
private Customer _customer;
private List<Product> _products;
public string GenerateDescription()
{
return $"Customer name: {_customer.Name}, " +
$"total number of products: {_products.Count}, " +
$"total price: {GetPrice()}";             
}
private decimal GetPrice()     
{
decimal basePrice = /* Calculate based on _products */;
decimal discounts = /* Calculate based on _customer */;
decimal taxes = /* Calculate based on _products */;
Listing 11.1
A class with a complex private method
The complex private
method is used by a
much simpler public
method.
Complex private 
method


