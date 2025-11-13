# 2.4.9 Test for nulls and exceptional cases, but only when it makes sense (pp.56-57)

---
**Page 56**

56
CHAPTER 2
Specification-based testing
2.4.6
When the number of combinations explodes, be pragmatic
If we had combined all the partitions we derived from the substringsBetween pro-
gram, we would have ended up with 320 tests. This number is even larger for more
complex problems. Combinatorial testing is an entire area of research in software test-
ing; I will not dive into the techniques that have been proposed for such situations,
but I will provide you with two pragmatic suggestions.
 First, reduce the number of combinations as much as possible. Testing exceptional
behavior isolated from other behaviors (as we did in the example) is one way to do so.
You may also be able to leverage your domain knowledge to further reduce the num-
ber of combinations.
 Second, if you are facing many combinations at the method level, consider breaking
the method in two. Two smaller methods have fewer things to test and, therefore, fewer
combinations to test. Such a solution works well if you carefully craft the method con-
tracts and the way they should pass information. You also reduce the chances of bugs
when the two simple methods are combined into a larger, more complex one. 
2.4.7
When in doubt, go for the simplest input
Picking concrete input for test cases is tricky. You want to choose a value that is realis-
tic but, at the same time, simple enough to facilitate debugging if the test fails.
 I recommend that you avoid choosing complex inputs unless you have a good rea-
son to use them. Do not pick a large integer value if you can choose a small integer
value. Do not pick a 100-character string if you can select a 5-character string. Simplic-
ity matters. 
2.4.8
Pick reasonable values for inputs you do not care about
Sometimes, your goal is to exercise a specific part of the functionality, and that part does
not use one of the input values. You can pass any value to that “useless” input variable. In
such scenarios, my recommendation is to pass realistic values for these inputs. 
2.4.9
Test for nulls and exceptional cases, but only when 
it makes sense
Testing nulls and exceptional cases is always important because developers often for-
get to handle such cases in their code. But remember that you do not want to write
tests that never catch a bug. Before writing such tests, you should understand the over-
all picture of the software system (and its architecture). The architecture may ensure
that the pre-conditions of the method are satisfied before calling it.
 If the piece of code you are testing is very close to the UI, exercise more corner
cases such as null, empty strings, uncommon integer values, and so on. If the code is
far from the UI and you are sure the data is sanitized before it reaches the component
under test, you may be able to skip such tests. Context is king. Only write tests that will
eventually catch a bug. 


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


