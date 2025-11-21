# 6.3.2 What to mock and what not to mock (pp.160-164)

---
**Page 160**

160
CHAPTER 6
Test doubles and mocks
change the production code. Spadini and colleagues, including me, observed this
through empirical studies in open source systems (2019). Can you avoid such coupling?
Not really, but at least now you are aware of it.
 Interestingly, developers consider this coupling a major drawback of mocks. But I
appreciate that my tests break when I change how a class interacts with other classes.
The broken tests make me reflect on the changes I am making. Of course, my tests do
not break as a result of every minor change I make in my production code. I also do
not use mocks in every situation. I believe that when mocks are properly used, the
coupling with the production code is not a big deal.
6.3.2
What to mock and what not to mock
Mocks and stubs are useful tools for simplifying the process of writing unit tests.
However, mocking too much might also be a problem. A test that uses the real depen-
dencies is more real than a test that uses doubles and, consequently, is more prone
to find real bugs. Therefore, we do not want to mock a dependency that should not
be mocked. Imagine you are testing class A, which depends on class B. How do we
know whether we should mock or stub B or whether it is better to use the real, con-
crete implementation?
 Pragmatically, developers often mock or stub the following types of dependencies:
Dependencies that are too slow—If the dependency is too slow for any reason, it
might be a good idea to simulate it. We do not want slow test suites. Therefore,
I mock classes that deal with databases or web services. Note that I still do inte-
gration tests to ensure that these classes work properly, but I use mocks for all
the other classes that depend on these slow classes.
Dependencies that communicate with external infrastructure—If the dependency talks
to (external) infrastructure, it may be too slow or too complex to set up the
required infrastructure. So, I apply the same principle: whenever testing a class
that depends on a class that handles external infrastructure, I mock the depen-
dency (as we mocked the IssuedInvoices class when testing the Invoice-
Filter class). I then write integration tests for these classes.
Mocking as a design technique
Whenever I say that mocks increase coupling with production code, I am talking about
using mocks from a testing perspective: not using mocks as a way to design the code,
but in the sense of “This is the code we have: let’s test it.” In this case, mocks are
naturally coupled with the code under test, and changes in the code will impact
the mocks.
If you are using mocks as a design technique (as explained in Freeman and Pryce’s
2009 book), you should look at it from a different angle. You want your mocks to be
coupled with the code under test because you care about how the code does its job.
If the code changes, you want your mocks to change. 


---
**Page 161**

161
Mocks in the real world
Cases that are hard to simulate—If we want to force the dependency to behave in a
hard-to-simulate way, mocks or stubs can help. A common example is when we
would like the dependency to throw an exception. Forcing an exception might
be tricky when using the real dependency but is easy to do with a stub.
On the other hand, developers tend not to mock or stub the following dependencies:
Entities—Entities are classes that represent business concepts. They consist pri-
marily of data and methods that manipulate this data. Think of the Invoice
class in this chapter or the ShoppingCart class from previous chapters. In busi-
ness systems, entities commonly depend on other entities. This means, when-
ever testing an entity, we need to instantiate other entities.
For example, to test a ShoppingCart, we may need to instantiate Products
and Items. One possibility would be to mock the Product class when the focus is
to test the ShoppingCart. However, this is not something I recommend. Entities
are classes that are simple to manipulate. Mocking them may require more
work. Therefore, I prefer to never mock them. If my test needs three entities, I
instantiate them.
I make exceptions for heavy entities. Some entities require dozens of other
entities. Think of a complex Invoice class that depends on 10 other entities: Cus-
tomer, Product, and so on. Mocking this complex Invoice class may be easier.
Native libraries and utility methods—It is also not common to mock or stub librar-
ies that come with our programming language and utility methods. For exam-
ple, why would we mock ArrayList or a call to String.format? Unless you have
a very good reason, avoid mocking them.
Things that are simple enough—Simple classes may not be worth mocking. If you
feel a class is too simple to be mocked, it probably is.
Interestingly, I always followed those rules, because they made sense to me. In 2018–
2019, Spadini, myself, and colleagues performed a study to see how developers mock
in the wild. Our findings were surprisingly similar to this list.
 Let me illustrate with a code example. Consider a BookStore class with the follow-
ing requirement:
Given a list of books and their respective quantities, the program should
return the total price of the cart.
If the bookstore does not have all the requested copies of the book, it
includes all the copies it has in stock in the final cart and lets the user know
about the missing ones.
The implementation (listing 6.16) uses a BookRepository class to check whether the
book is available in the store. If not enough copies are available, it keeps track of the
unavailable ones in the Overview class. For the available books, the store notifies Buy-
BookProcess. In the end, it returns the Overview class containing the total amount to
be paid and the list of unavailable copies.


---
**Page 162**

162
CHAPTER 6
Test doubles and mocks
class BookStore {
  private BookRepository bookRepository;
  private BuyBookProcess process;
  public BookStore(BookRepository bookRepository, BuyBookProcess process)  
  {
    this.bookRepository = bookRepository;
    this.process = process;
  }
  private void retrieveBook(String ISBN, int amount, Overview overview) {
    Book book = bookRepository.findByISBN(ISBN);   
    if (book.getAmount() < amount) {   
      overview.addUnavailable(book, amount - book.getAmount());
      amount = book.getAmount();
    }
    overview.addToTotalPrice(amount * book.getPrice());   
    process.buyBook(book, amount);     
  }
  public Overview getPriceForCart(Map<String, Integer> order) {
    if(order==null)
      return null;
    Overview overview = new Overview();
    for (String ISBN : order.keySet()) {     
      retrieveBook(ISBN, order.get(ISBN), overview);
    }
    return overview;
  }
}
Let’s discuss the main dependencies of the BookStore class:
The BookRepository class is responsible for, among other things, searching for
books in the database. This means the concrete implementation of this class
sends SQL queries to a database, parses the result, and transforms it into Book
classes. Using the concrete BookRepository implementation in the test might
be too painful: we would need to set up the database, ensure that it had the
books we wanted persisted, clean the database afterward, and so on. This is a
good dependency to mock.
The BuyBookProcess class is responsible for the process of someone buying a
book. We do not know exactly what it does, but it sounds complex. BuyBook-
Process deserves its own test suite, and we do not want to mix that with the
BookStore tests. This is another good dependency to mock.
Listing 6.16
Implementation of BookStore
We know we must mock
and stub things, so we
inject the dependencies.
Searches
for the
book using
its ISBN
If the number 
of copies in 
stock is less 
than the 
number of 
copies the user 
wants, we keep 
track of the 
missing ones.
Adds the
available
copies to
the final
price
Notifies the
buy book
process
Processes each 
book in the order


---
**Page 163**

163
Mocks in the real world
The Book class represents a book. The implementation of BookStore gets the
books that are returned by BookRepository and uses that information to
know the book’s price and how many copies the bookstore has in stock. This
is a simple class, and there is no need to mock it since it is easy to instantiate a
concrete Book.
The Overview class is also a simple, plain old Java object that stores the total
price of the cart and the list of unavailable books. Again, there is no need to
mock it.
The Map<String, Integer> that the getPriceForCart receives as an input is a
Map object. Map and its concrete implementation HashMap are part of the Java
language. They are simple data structures that also do not need to be mocked.
Now that we have decided what should be mocked and what should not be mocked,
we write the tests. The following test exercises the behavior of the program with a
more complex order.
@Test
void moreComplexOrder() {
  BookRepository bookRepo = mock(BookRepository.class);   
  BuyBookProcess process = mock(BuyBookProcess.class);    
  Map<String, Integer> orderMap = new HashMap<>();  
  orderMap.put("PRODUCT-ENOUGH-QTY", 5);    
  orderMap.put("PRODUCT-PRECISE-QTY", 10);
  orderMap.put("PRODUCT-NOT-ENOUGH", 22);
  Book book1 = new Book("PRODUCT-ENOUGH-QTY", 20, 11); // 11 > 5
  when(bookRepo.findByISBN("PRODUCT-ENOUGH-QTY"))
    .thenReturn(book1);                
  Book book2 = new Book("PRODUCT-PRECISE-QTY", 25, 10); // 10 == 10
  when(bookRepo.findByISBN("PRODUCT-PRECISE-QTY"))
    .thenReturn(book2);                
  Book book3 = new Book("PRODUCT-NOT-ENOUGH", 37, 21); // 21 < 22
  when(bookRepo.findByISBN("PRODUCT-NOT-ENOUGH"))
    .thenReturn(book3);                
  BookStore bookStore = new BookStore(bookRepo, process);   
  Overview overview = bookStore.getPriceForCart(orderMap);
  int expectedPrice =        
      5*20 + // from the first product
          10*25 + // from the second product
          21*37; // from the third product
  assertThat(overview.getTotalPrice()).isEqualTo(expectedPrice);
Listing 6.17
Test for BookStore, only mocking what needs to be mocked
As agreed, 
BookRepository 
and BuyBookProcess 
should be mocked.
No need
to mock
HashMap
The order has three books: one 
where there is enough quantity, 
one where the available quantity 
is precisely what is requested in 
the order, and one where there is 
not enough quantity.
Stubs the
BookRepository
to return the
three books
Injects the 
mocks and 
stubs into 
BookStore
Ensures that 
the total price 
is correct


---
**Page 164**

164
CHAPTER 6
Test doubles and mocks
  verify(process).buyBook(book1, 5);    
  verify(process).buyBook(book2, 10);   
  verify(process).buyBook(book3, 21);   
  assertThat(overview.getUnavailable())
      .containsExactly(entry(book3, 1));  
}
Could we mock everything? Yes, we could—but doing so would not make sense. You
should only stub and mock what is needed. But whenever you mock, you reduce the
reality of the test. It is up to you to understand this trade-off. 
6.3.3
Date and time wrappers
Software systems often use date and time information. For example, you might need
the current date to add a special discount to the customer’s shopping cart, or you
might need the current time to start a batch processing job. To fully exercise some
pieces of code, our tests need to provide different dates and times as input.
 Given that date and time operations are common, a best practice is to wrap them
into a dedicated class (often called Clock). Let’s show that using an example:
The program should give a 15% discount on the total amount of an order if
the current date is Christmas. There is no discount on other dates.
A possible implementation for this requirement is shown next.
public class ChristmasDiscount {
  public double applyDiscount(double amount) {
    LocalDate today = LocalDate.now();  
    double discountPercentage = 0;
    boolean isChristmas = today.getMonth() == Month.DECEMBER
      && today.getDayOfMonth() == 25;
    if(isChristmas)   
      discountPercentage = 0.15;
    return amount - (amount * discountPercentage);
  }
}
The implementation is straightforward; given the characteristics of the class, unit testing
seems to be a perfect fit. The question is, how can we write unit tests for it? To test both
cases (Christmas/not Christmas), we need to be able to control/stub the LocalDate
class, so it returns the dates we want. Right now, this is not easy to do, given that the
Listing 6.18
ChristmasDiscount implementation
Ensures that BuyBookProcess 
was called for three books 
with the right amounts
Ensures that the list of 
unavailable books contains 
the one missing book
Gets the current 
date. Note the 
static call.
If it is Christmas, we 
apply the discount.


