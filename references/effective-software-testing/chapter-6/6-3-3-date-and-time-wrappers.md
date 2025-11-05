# 6.3.3 Date and time wrappers (pp.164-166)

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


---
**Page 165**

165
Mocks in the real world
method makes explicit, direct calls to LocalDate.now(). The problem is analogous when
InvoiceFilter instantiated the IssuedInvoices class directly: we could not stub it.
 We can then ask a more specific question: how can we stub Java’s Time API? In par-
ticular, how can we do so for the static method call to LocalDate.now()? Mockito
allows developers to mock static methods (http://mng.bz/g48n), so we could use this
Mockito feature.
 Another solution (which is still popular in code bases) is to encapsulate all the date
and time logic into a class. In other words, we create a class called Clock, and this class
handles these operations. The rest of our system only uses this class when it needs
dates and times. This new Clock class is passed as a dependency to all classes that need
it and can therefore be stubbed. The new version of ChristmasDiscount is in the fol-
lowing listing.
public class Clock {
  public LocalDate now() {   
    return LocalDate.now();
  }
  // any other date and time operation here...
}
public class ChristmasDiscount {
  private final Clock clock;               
  public ChristmasDiscount(Clock clock) {  
    this.clock = clock;
  }
  public double applyDiscount(double rawAmount) {
    LocalDate today = clock.now();   
    double discountPercentage = 0;
    boolean isChristmas = today.getMonth() == Month.DECEMBER
        && today.getDayOfMonth() == 25;
    if(isChristmas)
      discountPercentage = 0.15;
    return rawAmount - (rawAmount * discountPercentage);
  }
}
Testing it should be easy, given that we can stub the Clock class (see listing 6.20). We
have two tests: one for when it is Christmas (where we set the clock to December 25 of
any year) and another for when it is not Christmas (where we set the clock to any
other date).
Listing 6.19
The Clock abstraction
Encapsulates the static call. This 
seems too simple, but think of other, 
more complex operations you will 
encapsulate in this class.
Clock is a plain old dependency 
that we store in a field and 
receive via the constructor.
Calls the clock whenever we need, 
for example, the current date


---
**Page 166**

166
CHAPTER 6
Test doubles and mocks
public class ChristmasDiscountTest {
  private final Clock clock = mock(Clock.class);    
  private final ChristmasDiscount cd = new ChristmasDiscount(clock);
  @Test
  public void christmas() {
    LocalDate christmas = LocalDate.of(2015, Month.DECEMBER, 25);
    when(clock.now()).thenReturn(christmas);   
    double finalValue = cd.applyDiscount(100.0);
    assertThat(finalValue).isCloseTo(85.0, offset(0.001));
  }
  @Test
  public void notChristmas() {
    LocalDate notChristmas = LocalDate.of(2015, Month.DECEMBER, 26);
    when(clock.now()).thenReturn(notChristmas);     
    double finalValue = cd.applyDiscount(100.0);
    assertThat(finalValue).isCloseTo(100.0, offset(0.001));
  }
}
As I said, creating an abstraction on top of date and time operations is common. The
idea is that having a class that encapsulates these operations will facilitate the testing
of the other classes in the system, because they are no longer handling date and time
operations. And because these classes now receive this clock abstraction as a depen-
dency, it can be easily stubbed. Martin Fowler’s wiki even has an entry called Clock-
Wrapper, which explains the same thing.
 Is it a problem to use Mockito’s ability to mock static methods? As always, there are
no right and wrong answers. If your system does not have complex date and time
operations, stubbing them using Mockito’s mockStatic() API should be fine. Pragma-
tism always makes sense. 
6.3.4
Mocking types you do not own
Mocking frameworks are powerful. They even allow you to mock classes you do not
own. For example, we could stub the LocalDate class if we wanted to. We can mock
any classes from any library our software system uses. The question is, do we want to?
 When mocking, it is a best practice to avoid mocking types you do not own. Imag-
ine that your software system uses a library. This library is costly, so you decide to mock
it 100% of the time. In the long run, you may face the following complications:
If this library ever changes (for example, a method stops doing what it was sup-
posed to do), you will not have a breaking test. The entire behavior of that
library was mocked. You will only notice it in production. Remember that you
want your tests to break whenever something goes wrong.
Listing 6.20
Testing the new ChristmasDiscount
Clock is a stub.
Stubs the now() 
method to return 
the Christmas date
Stubs the now() 
method. It now 
returns a date that 
is not Christmas.


