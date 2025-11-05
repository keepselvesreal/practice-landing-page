# 5.6.1 Example-based testing vs. property-based testing (pp.137-138)

---
**Page 137**

137
Property-based testing in the real world
public class BookTest {
  @Property
  void differentBooks(@ForAll("books") Book book) {
    // different books!
    System.out.println(book);
    // write your test here!
  }
  @Provide
  Arbitrary<Book> books() {
    Arbitrary<String> titles = Arbitraries.strings().withCharRange(
      ➥ 'a', 'z')
        .ofMinLength(10).ofMaxLength(100); 
    Arbitrary<String> authors = Arbitraries.strings().withCharRange(
      ➥ 'a', 'z')
        .ofMinLength(5).ofMaxLength(21);   
    Arbitrary<Integer> qtyOfPages = Arbitraries.integers().between(
      ➥ 0, 450); 
    return Combinators.combine(titles, authors, qtyOfPages)
        .as((title, author, pages) -> new Book(title, author, pages)); 
  }
}
The Combinators API lets us combine different generators to build a more complex
object. All we have to do is to build specific Arbitrarys for each of the attributes of the
complex class we want to build: in this case, one Arbitrary<String> for the title,
another Arbitrary<String> for the author, and one Arbitrary<Integer> for the num-
ber of pages. After that, we use the Combinators.combine() method, which receives a
series of Arbitrarys and returns an Arbitrary of the complex object. The magic hap-
pens in the as() method, which gives us the values we use to instantiate the object.
 Note how flexible jqwik is. You can build virtually any object you want. Moreover,
nothing prevents you from building even more realistic input values: for example,
instead of building random author names, we could develop something that returns
real people’s names. Try implementing such an arbitrary yourself. 
5.6
Property-based testing in the real world
Let me give you some tips on writing property-based tests.
5.6.1
Example-based testing vs. property-based testing
Property-based testing seems much fancier than example-based testing. It also explores
the input domain much better. Should we only use property-based testing from now on?
 In practice, I mix example-based testing and property-based testing. In the testing
workflow I propose, I use example-based testing when doing specification-based and
structural testing. Example-based tests are naturally simpler than property-based tests,
Listing 5.22
Using the Combinators API to generate complex objects
Instantiates
one arbitrary
for each of the
Book’s fields
Combines them
to generate an
instance of Book


---
**Page 138**

138
CHAPTER 5
Property-based testing
and they require less creativity to automate. I like that: their simplicity allows me to
focus on understanding the requirements and engineer better test cases. When I am
done with both testing techniques and have a much better grasp of the program
under test, I evaluate which test cases would be better as property-based tests.
 Do I always write property-based tests for my programs? Honestly, no. In many of the
problems I work on, I feel pretty confident with example-based testing. I use property-
based testing when I do not feel entirely secure that my example-based tests were
enough. 
5.6.2
Common issues in property-based tests
I see three common issues in the property-based tests my students write when they
learn this technique. The first is requiring jqwik to generate data that is very expensive
or even impossible. If you ask jqwik to, say, generate an array of 100 elements in which
the numbers have to be unique and multiples of 2, 3, 5, and 15, such an array can be
difficult to find, given jqwik’s random approach. Or if you want an array with 10
unique elements, but you give jqwik a range of 2 to 8, the array is impossible to gener-
ate. In general, if jqwik is taking too long to generate the data for you, maybe you can
find a better way to generate the data or write the test.
 Second, we saw in previous chapters that boundaries are a perfect place for bugs.
So, we want to exercise those boundaries when writing property-based tests. Ensure
that you are expressing the boundaries of the property correctly. When we wrote the
tests for the passing-grade problem (section 5.1), we wrote arbitraries like Arbitraries
.floats().lessThan(1f) and Arbitraries.floats().greaterThan(10f). Jqwik will
do its best to generate boundary values: for example, the closest possible number to
1f or the smallest possible float. The default configuration for jqwik is to mix edge
cases with random data points. Again, all of this will work well only if you express the
properties and boundaries correctly.
 The third caveat is ensuring that the input data you pass to the method under test
is fairly distributed among all the possible options. Jqwik does its best to generate well-
distributed inputs. For example, if you ask for an integer between 0 and 10, all the
numbers in the interval will have the same probability of being generated. But I have
seen tests that manipulate the generated data and then harm this property. For exam-
ple, imagine testing a method that receives three integers, a, b, and c, and returns a
boolean indicating whether these three sides can form a triangle. The implementa-
tion of this method is simple, as shown in the following listing.
public class Triangle {
  public static boolean isTriangle(int a, int b, int c) {
    boolean hasABadSide = a >= (b + c) || c >= (b + a) || b >= (a + c);
    return !hasABadSide;
  }
}
Listing 5.23
Implementation of the isTriangle method


