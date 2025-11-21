# 7.7 Summary (pp.196-198)

---
**Page 196**

196
CHAPTER 7
Designing for testability
    OrderDao dao = new OrderDao();
    DeliveryStartProcess delivery = new DeliveryStartProcess();
    List<Order> orders = dao.paidButNotDelivered();
    for (Order order : orders) {
      delivery.start(order);
      if (order.isInternational()) {
        order.setDeliveryDate("5 days from now");
      } else {
        order.setDeliveryDate("2 days from now");
      }
    }
  }
}
class OrderDao {
  // accesses a database
}
class DeliveryStartProcess {
  // communicates with a third-party web service
}
7.4
Consider the KingsDayDiscount class below:
public class KingsDayDiscount {
  public double discount(double value) {
    Calendar today = Calendar.getInstance();
    boolean isKingsDay = today.get(MONTH) == Calendar.APRIL
        && today.get(DAY_OF_MONTH) == 27;
    return isKingsDay ? value * 0.15 : 0;
  }
}
What would you do to make this class more testable?
7.5
Think about your current project. Are parts of it hard to test? Can you explain
why? What can you do to make it more testable?
Summary
Writing tests can be easy or hard. Untestable code makes our lives harder. Strive
for code that is easy (or at least easier) to test.
Separate infrastructure from domain code. Infrastructure makes it harder to
write tests. Separating domain from infrastructure enables us to write unit tests
for the domain logic much more cheaply.


---
**Page 197**

197
Summary
Ensure that classes are easily controllable and observable. Controllability is usu-
ally achieved by ensuring that we can control the dependencies of the class
under test. Observability is achieved by ensuring that the class provides easy
ways for the test to assert expected behavior.
While you should not change your code in ways you do not believe in, you
should also be pragmatic. I am all in favor of changing the production code to
facilitate testing.


---
**Page 198**

198
Test-driven development
Software developers are pretty used to the traditional development process. First,
they implement. Then, and only then, they test. But why not do it the other way
around? In other words, why not write a test first and then implement the produc-
tion code?
 In this chapter, we discuss this well-known approach: test-driven development (TDD).
In a nutshell, TDD challenges our traditional way of coding, which has always been
“write some code and then test it.” With TDD, we start by writing a test representing
the next small feature we want to implement. This test naturally fails, as the feature
has not yet been implemented! We then make the test pass by writing some code.
With the test now green, and knowing that the feature has been implemented, we
go back to the code we wrote and refactor it.
 TDD is a popular practice, especially among Agile practitioners. Before I dive
into the advantages of TDD and pragmatic questions about working this way, let’s
look at a small example.
This chapter covers
Understanding test-driven development
Being productive with TDD
When not to use TDD


