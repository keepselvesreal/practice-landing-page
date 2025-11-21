# 7.3.1 Example 1: Introducing methods to facilitate assertions (pp.184-186)

---
**Page 184**

184
CHAPTER 7
Designing for testability
depend on what the mocked class offers as a contract. The more complex the class
you are mocking, the harder it is to write the test. When you have ports, adapters, and
the dependency inversion principle in mind, the interface of a port is naturally sim-
ple. The methods that ports offer are usually cohesive and straight to the point.
 In the example, the ShoppingCartRepository class has a List<ShoppingCart>
cartsPaidToday() method. It is clear what this method does: it returns a list of shop-
ping carts that were paid today. Mocking this method is trivial. Its concrete adapter
implementation is probably complicated, full of database-related code and SQL que-
ries. The interface removes all this complexity from testing the PaidShoppingCarts-
Batch class. Therefore, designing the ports in a simple way also makes your code
easier to test. Complex ports and interfaces require more work.
 When things become more complicated, making sure dependencies are always
injected may not be as straightforward as I have made it seem. It is much easier not to do
this. But you must convince yourself that the extra effort will pay off later during testing.
NOTE
This chapter is a quick introduction to the Hexagonal Architecture
and to the Dependency Inversion Priniciple. I suggest you dive into the
related literature, including the books by Martin (2014) and Freeman and
Pryce (2009), for more details. I also recommend Schuchert’s guest post on
dependency inversion in the wild in Fowler’s wiki (2013); he explains the dif-
ference between dependency inversion and dependency injection and gives
lots of examples of how he applied the principle in real-world situations. 
7.3
Making your classes and methods observable
Observability, at the class level, is about how easy it is to assert that the behavior of the
functionality went as expected. My main advice is to ensure that your classes provide
developers with simple and easy ways to assert their state. Does a class produce a list of
objects you need to assert one by one? Create a getListOfSomething in that class,
which the test can use to get the generated list of objects. Does a class make calls to
other classes? Make sure these dependencies can be mocked and your test can assert
their interaction. Does a class make internal changes in its attributes, but the class can-
not or does not offer getters to each of them? Make the class offer a simple isValid
method that returns whether the class is in a valid state.
 It has to be easy for the test code to inspect the class behavior. Whenever it is difficult
to observe whether the program behaves as expected, reflect on how observable the
classes are. Do not be afraid to introduce simple getters or simple solutions to facilitate
your testing. Behavior that is easy to observe will make the test code much easier! Let’s
look at two pragmatic changes I make in my code so it is more observable.
7.3.1
Example 1: Introducing methods to facilitate assertions
Take another look at the processAll() method and its test, in listings 7.2 and 7.5. Most
of what its test asserts is the interaction with the ports. Such assertions are easily done,
and we did not need much more than basic Mockito. Now, let’s look closer at one specific
assertion: verify(someCart).markAsReadyForDelivery(someDate);. The someCart


---
**Page 185**

185
Making your classes and methods observable
instance of ShoppingCart is not a mock but a spy. To ensure that the cart was marked as
ready for delivery, we had to spy on the object. Mockito’s API enables us to spy objects
with a single line of code. However, whenever we need a spy to assert the behavior, we
must ask ourselves why we need a spy. Isn’t there an easier way?
 In this particular case, we need to check whether ShoppingCart is marked as ready
for delivery after processing (listing 7.7). We can increase the observability of the
ShoppingCart class (in other words, we can make it simpler to observe the expected
behavior of the shopping cart) by making it provide a method that indicates whether
it is ready for delivery: isReadyForDelivery.
public class ShoppingCart {
    private boolean readyForDelivery = false;
    // more info about the shopping cart...
    public void markAsReadyForDelivery(Calendar estimatedDayOfDelivery) {
        this.readyForDelivery = true;
        // ...
    }
    public boolean isReadyForDelivery() { 
        return readyForDelivery;
    }
}
Because we can now easily ask ShoppingCart whether it is ready for delivery, our test
no longer requires a spy. A vanilla assertion should do. Here is the new test.
@Test
void theWholeProcessHappens() {
  PaidShoppingCartsBatch batch = new PaidShoppingCartsBatch(db,
    ➥ deliveryCenter, notifier, sap);
  ShoppingCart someCart = new ShoppingCart(); 
  assertThat(someCart.isReadyForDelivery()).isFalse();
  Calendar someDate = Calendar.getInstance();
  when(db.cartsPaidToday()).thenReturn(Arrays.asList(someCart));
  when(deliveryCenter.deliver(someCart)).thenReturn(someDate);
  batch.processAll();
  verify(deliveryCenter).deliver(someCart);
  verify(notifier).sendEstimatedDeliveryNotification(someCart);
  verify(db).persist(someCart);
  verify(sap).cartReadyForDelivery(someCart);
  assertThat(someCart.isReadyForDelivery()).isTrue(); 
}
Listing 7.7
Improving the observability of the ShoppingCart class
Listing 7.8
Avoiding the spy when testing PaidShoppingCartsBatch
The new isReadyForDelivery 
method is here to improve 
the observability of the class.
No need for a spy 
anymore, as it is now easy 
to observe the behavior.
Uses a simple vanilla 
assertion instead of a 
Mockito assertion


---
**Page 186**

186
CHAPTER 7
Designing for testability
I urge you not to take this particular code change (the addition of a getter) as the
solution for all observability issues. Rather, abstract away what we did here: we noticed
that asserting that the shopping cart was marked as ready for delivery was not straight-
forward, as it required a spy. We then re-evaluated our code and looked for a simple
way to let the test know that the shopping cart was marked as ready for delivery. In this
case, a getter was the easy implementation. 
7.3.2
Example 2: Observing the behavior of void methods
When a method returns an object, it is natural to think that assertions will check
whether the returned object is as expected. However, this does not happen naturally
in void methods. If your method does not return anything, what will you assert? It is
even more complicated if what you need to assert stays within the method. As an
example, the following method creates a set of Installments based on a Shopping-
Cart.
public class InstallmentGenerator {
  private InstallmentRepository repository;
  public InstallmentGenerator(InstallmentRepository repository) { 
    this.repository = repository;
  }
  public void generateInstallments(ShoppingCart cart,
    ➥ int numberOfInstallments) {
    LocalDate nextInstallmentDueDate = LocalDate.now(); 
    double amountPerInstallment = cart.getValue() / numberOfInstallments; 
    for(int i = 1; i <= numberOfInstallments; i++) { 
      nextInstallmentDueDate =
        nextInstallmentDueDate.plusMonths(1);   
      Installment newInstallment =
        new Installment(nextInstallmentDueDate, amountPerInstallment);
      repository.persist(newInstallment); 
    }
  }
}
To test this method, we need to check whether the newly created Installments are set
with the right value and date. The question is, how can we get the Installments eas-
ily? The Installment classes are instantiated within the method and sent to the repos-
itory for persistence, and that is it. If you know Mockito well, you know there is a way
to get all the instances passed to a mock: an ArgumentCaptor. The overall idea is that
we ask the mock, “Can you give me all the instances passed to you during the test?” We
Listing 7.9
InstallmentGenerator 
We can inject a stub of
InstallmentRepository.
Creates a variable to store the
last installment date
Calculates the
amount per
installment
Creates a sequence 
of installments, one 
month apart
Adds 1 to
the month
Creates and persists 
the installment


