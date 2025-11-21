# 7.3.2 Example 2: Observing the behavior of void methods (pp.186-189)

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


---
**Page 187**

187
Making your classes and methods observable
then make assertions about them. In this case, we can ask the repository mock
whether all the Installments were passed to the persist method.
 The test in listing 7.10 creates a shopping cart with value 100 and asks the genera-
tor for 10 installments. Therefore, it should create 10 installments of 10.0 each. That is
what we want to assert. After the method under test is executed, we collect all the install-
ments using an ArgumentCaptor. See the calls for capture() and getAllValues(). With
the list available, we use traditional AssertJ assertions.
public class InstallmentGeneratorTest {
    @Mock private InstallmentRepository repository; 
    @Test
    void checkInstallments() {
      InstallmentGenerator generator =
        new InstallmentGenerator(repository); 
      ShoppingCart cart = new ShoppingCart(100.0);
      generator.generateInstallments(cart, 10); 
      ArgumentCaptor<Installment> captor =
        ArgumentCaptor.forClass(Installment.class); 
      verify(repository,times(10)).persist(captor.capture());     
      List<Installment> allInstallments = captor.getAllValues();  
      assertThat(allInstallments)
          .hasSize(10)
          .allMatch(i -> i.getValue() == 10); 
      for(int month = 1; month <= 10; month++) { 
        final LocalDate dueDate = LocalDate.now().plusMonths(month);
        assertThat(allInstallments)
            .anyMatch(i -> i.getDate().equals(dueDate));
      }
    }
}
The ArgumentCaptor makes writing the test possible. ArgumentCaptors are handy
whenever we test methods that return void.
 If we apply the idea of simplicity, you may wonder if there is a way to avoid the
ArgumentCaptor. It would be much simpler if there were a “get all generated install-
ments” method. If we make the generateInstallments method return the list of all
newly generated Installments, the test becomes even simpler. The change required
in InstallmentGenerator is small: as all we need to do is keep track of the install-
ments in a list. The following listing shows the new implementation.
Listing 7.10
Tests for InstallmentGenerator using ArgumentCaptor
Creates a mock of 
the repository
Instantiates the class
under test, passing the
mock as a dependency
Calls the method 
under test. Note that 
the method returns 
void, so we need 
something smarter to 
assert its behavior.
Creates an
ArgumentCaptor
Using the captor, we
get all the installments
passed to the repository.
Asserts that the installments 
are correct. All of them should 
have a value of 10.0.
Also asserts that
the installments
should be one
month apart


---
**Page 188**

188
CHAPTER 7
Designing for testability
public List<Installment> generateInstallments(ShoppingCart cart,
  ➥ int numberOfInstallments) {
  List<Installment> generatedInstallments = new ArrayList<Installment>(); 
  LocalDate nextInstallmentDueDate = LocalDate.now();
  double amountPerInstallment = cart.getValue() / numberOfInstallments;
  for(int i = 1; i <= numberOfInstallments; i++) {
    nextInstallmentDueDate = nextInstallmentDueDate.plusMonths(1);
    Installment newInstallment =
      new Installment(nextInstallmentDueDate, amountPerInstallment);
    repository.persist(newInstallment);
    generatedInstallments.add(newInstallment); 
  }
  return generatedInstallments; 
}
Now we can avoid the ArgumentCaptor completely in the test code.
public class InstallmentGeneratorTest {
    @Mock
    private InstallmentRepository repository;
    @Test
    void checkInstallments() {
      ShoppingCart cart = new ShoppingCart(100.0);
      InstallmentGenerator generator =
        new InstallmentGenerator(repository);
      List<Installment> allInstallments =
        generator.generateInstallments(cart, 10); 
      assertThat(allInstallments)
          .hasSize(10)
          .allMatch(i -> i.getValue() == 10); 
      for(int month = 1; month <= 10; month++) {
        final LocalDate dueDate = LocalDate.now().plusMonths(month);
        assertThat(allInstallments)
            .anyMatch(i -> i.getDate().equals(dueDate));
      }
    }
}
Listing 7.11
InstallmentGenerator returning the list of installments
Listing 7.12
InstallmentGeneratorTest without the ArgumentCaptor
Creates a
list that will
keep track
of all the
generated
installments
Stores each of 
the generated 
installments
Returns the list 
of installments
The method under 
test returns the list of 
installments. No need 
for ArgumentCaptor.
Same assertions 
as before


---
**Page 189**

189
Dependency via class constructor or value via method parameter?
Again, do not take this example literally. Just remember that small design changes
that improve your testability are fine. Sometimes it can be hard to tell whether a
change will make the code design bad. Try it, and if you don’t like it, discard it. Prag-
matism is key. 
7.4
Dependency via class constructor or value via 
method parameter?
A very common design decision is whether to pass a dependency to the class via con-
structor (so the class uses the dependency to get a required value) or pass that value
directly to the method. As always, there is no right or wrong way. However, there is a
trade-off you must understand to make the best decision.
 Let’s use the ChristmasDiscount example, as it fits this discussion perfectly. The
following listing shows the code again.
public class ChristmasDiscount {
  private final Clock clock;
  public ChristmasDiscount(Clock clock) { 
    this.clock = clock;
  }
  public double applyDiscount(double rawAmount) {
    LocalDate today = clock.now(); 
    double discountPercentage = 0;
    boolean isChristmas = today.getMonth()== Month.DECEMBER
                && today.getDayOfMonth()==25;
    if(isChristmas)
      discountPercentage = 0.15;
    return rawAmount - (rawAmount * discountPercentage);
  }
}
The ChristmasDiscount class needs the current date so it knows whether it is
Christmas and whether to apply the Christmas discount. To get the date, the class
uses another dependency, which knows how to get the current date: the Clock
class. Testing ChristmasDiscount is easy because we can stub Clock and simulate
any date we want.
 But having to stub one class is more complex than not having to stub one class.
Another way to model this class and its expected behavior is to avoid the dependency
on Clock and receive the data as a parameter of the method. This other implementa-
tion is shown in listing 7.14. Now the applyDiscount() method receives two parame-
ters: rawAmount and today, which is today’s date.
Listing 7.13
ChristmasDiscount class, one more time
We can inject a stubbed 
version of Clock here.
Calls the now() method 
to get the current date


