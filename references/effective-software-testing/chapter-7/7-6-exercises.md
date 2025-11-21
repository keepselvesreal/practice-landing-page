# 7.6 Exercises (pp.195-196)

---
**Page 195**

195
Exercises
7.5.7
Further reading about designing for testability
Entire books can be written about this topic. In fact, entire books have been written
about it:
Michael Feathers’s Working Effectively with Legacy Code (2004) is about working
with legacy systems, but a huge part of it is about untestable code (common in
legacy) and how to make it testable. Feathers also has a nice talk on YouTube
about the “deep synergy between well-designed production code and testabil-
ity,” as he calls it (2013).
Steve Freeman and Nat Pryce’s book Growing-Object Oriented Systems Guided by
Tests (2009) is also a primer for writing classes that are easy to test.
Robert Martin’s Clean Architecture ideas (2018) align with the ideas discussed here. 
Exercises
7.1
Observability and controllability are two important concepts of software testing.
Three developers could benefit from improving either the observability or the
controllability of the system/class they are testing, but each developer encoun-
ters a problem.
State whether each of the problems relates to observability or controllability.
A Developer 1: “I can’t assert whether the method under test worked well.”
B Developer 2: “I need to make sure this class starts with a boolean set to
false, but I can’t do it.”
C Developer 3: “I instantiated the mock object, but there’s no way to inject it
into the class.”
7.2
Sarah has joined a mobile app team that has been trying to write automated
tests for a while. The team wants to write unit tests for part of their code, but
they tell Sarah, “It’s hard.” After some code review, the developers list the fol-
lowing problems in their code base:
A Many classes mix infrastructure and business rules.
B The database has large tables and no indexes.
C There are lots of calls to libraries and external APIs.
D Some classes have too many attributes/fields.
To increase testability, the team has a budget to work on two of these four
issues. Which items should Sarah recommend that they tackle first?
Note: All four issues should be fixed, but try to prioritize the two most
important ones. Which influences testability the most?
7.3
How can you improve the testability of the following OrderDeliveryBatch class?
public class OrderDeliveryBatch {
  public void runBatch() {


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


