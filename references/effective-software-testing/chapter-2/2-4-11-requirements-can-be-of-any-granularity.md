# 2.4.11 Requirements can be of any granularity (pp.57-57)

---
**Page 57**

57
Specification-based testing in the real world
2.4.10 Go for parameterized tests when tests have the same skeleton
A little duplication is never a problem, but a lot of duplication is. We created 21 differ-
ent tests for the substringsBetween program. The test code was lean because we
grouped some of the test cases into single test methods. Imagine writing 21 almost-
identical test cases. If each method took 5 lines of code, we would have a test class with
21 methods and 105 lines. This is much longer than the test suite with the parameter-
ized test that we wrote.
 Some developers argue that parameterized tests are confusing. Deciding whether
to use JUnit test cases or parameterized tests is, most of all, a matter of taste. I use
parameterized tests when the amount of duplication in my test suite is too large. In
this chapter, I leaned more toward JUnit test cases: lots of test cases logically grouped
in a small set of test methods. We discuss test code quality further in chapter 10. 
2.4.11 Requirements can be of any granularity
The seven-step approach I propose in this chapter works for requirements of any
granularity. Here, we applied it in a specification that could be implemented by a sin-
gle method. However, nothing prevents you from using it with larger requirements
that involve many classes. Traditionally, specification-based testing techniques focus
on black-box testing: that is, testing an entire program or feature, rather than unit-
testing specific components. I argue that these ideas also make sense at the unit level.
 When we discuss larger tests (integration testing), we will also look at how to devise
test cases for sets of classes or components. The approach is the same: reflect on the
inputs and their expected outputs, divide the domain space, and create test cases. You
can generalize the technique discussed here to tests at any level. 
2.4.12 How does this work with classes and state?
The two methods we tested in this chapter have no state, so all we had to do was think
of inputs and outputs. In object-oriented systems, classes have state. Imagine a Shop-
pingCart class and a behavior totalPrice() that requires some CartItems to be
inserted before the method can do its job. How do we apply specification-based test-
ing in this case? See the following listing.
public class ShoppingCart {
  private List<CartItem> items = new ArrayList<CartItem>();
  public void add(CartItem item) {   
    this.items.add(item);
  }
  public double totalPrice() {   
    double totalPrice = 0;
    for (CartItem item : items) {
Listing 2.14
ShoppingCart and CartItem classes
Adds items 
to the cart
Loops through all the items 
and sums up the final price


