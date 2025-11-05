# 7.0 Introduction [auto-generated] (pp.172-173)

---
**Page 172**

172
Designing for testability
I usually say that every software system can be tested. However, some systems are more
testable than others. Imagine that for a single test case, we need to set up three differ-
ent web services, create five different files in different folders, and put the database
in a specific state. After all that, we exercise the feature under test and, to assert the
correct behavior, again need to see if the three web services were invoked, the five
files were consumed correctly, and the database is now in a different state. All those
steps are doable. But couldn’t this process be simpler?
 Software systems are sometimes not ready for or designed to be tested. In this
chapter, we discuss some of the main ideas behind systems that have high testability.
Testability is how easy it is to write automated tests for the system, class, or method
under test. In chapter 6, we saw that by allowing dependencies to be injected, we
This chapter covers
Designing testable code at the architectural, 
design, and implementation levels
Understanding the Hexagonal Architecture, 
dependency injection, observability, and 
controllability
Avoiding testability pitfalls


---
**Page 173**

173
Separating infrastructure code from domain code
could stub the dependency. This chapter is about other strategies you can use to make
testing easier.
 The topic of design for testability deserves an entire book. In this chapter, I cover
several design principles that solve most of the problems I face. When presenting
these principles, I will discuss the underlying ideas so you can apply them even if the
code changes you must make differ from my examples.
 Design for testability is fundamental if our goal is to achieve systematic testing—if
your code is hard to test, you probably won’t test it. When do I design for testability?
What is the right moment to think about testability? All the time. Much of it happens
while I am implementing a feature.
 You should design for testability from the very beginning, which is why I put it in the
“testing to guide development” part of the flow back in chapter 1, figure 1.4. Sometimes
I cannot see the untestable part during the implementation phase, and it haunts me
during the test phase. When that happens, I go back to my code and refactor it.
 Some developers argue that designing for testability is harder and costs too many
extra lines of code. This may be true. Writing spaghetti code is easier than develop-
ing cohesive classes that collaborate and are easily tested. One of the goals of this
chapter is to convince you that the extra effort of designing for testability will pay
off. Good, testable code costs more than bad code, but it is the only way to ensure
quality.
7.1
Separating infrastructure code from domain code
I could spend pages discussing architectural patterns that enable testability. Instead,
I will focus on what I consider the most important advice: separate infrastructure code
from domain code.
 The domain is where the core of the system lies: that is, where all the business rules,
logic, entities, services, and similar elements reside. Entities like Invoice and services
such as ChristmasDiscount are examples of domain classes. Infrastructure relates to all
code that handles an external dependency: for example, pieces of code that handle
database queries (in this case, the database is an external dependency) or web service
calls or file reads and writes. In our previous examples, all of our data access objects
(DAOs) are part of the infrastructure code.
 In practice, when domain code and infrastructure code are mixed, the system
becomes harder to test. You should separate them as much as possible so the infra-
structure does not get in the way of testing. Let’s start with InvoiceFilter example,
now containing the SQL logic instead of depending on a DAO.
public class InvoiceFilter {
  private List<Invoice> all() { 
    try {
      Connection connection =
Listing 7.1
InvoiceFilter that mixes domain and infrastructure
This method gets all the invoices 
directly from the database. Note that it 
resides in the InvoiceFilter class, unlike 
in previous examples.


