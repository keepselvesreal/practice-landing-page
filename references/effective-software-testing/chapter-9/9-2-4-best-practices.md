# 9.2.4 Best practices (pp.238-239)

---
**Page 238**

238
CHAPTER 9
Writing larger tests
HELPER METHODS THAT REDUCE THE AMOUNT OF CODE IN THE TESTS
SQL integration test methods can be long. You may need to create many entities
and perform more complex assertions. If code can be reused by many other tests, I
extract it to a method and move it to the base class. The test classes now all inherit
this utility method and can use it. Object builders, frequent assertions, and specific
database operations that are often reused are good candidates to become methods
in the base class. 
9.2.4
Best practices
Let’s close this section with some final tips on writing tests for SQL queries.
USE TEST DATA BUILDERS
Creating invoices in our earlier example was a simple task. The entity was small and
contained only two properties. However, entities in real-world systems are much more
complex and may require more work to be instantiated. You do not want to write 15
lines of code and pass 20 parameters to create a simple invoice object. Instead, use
helper classes that instantiate test objects for you. These test data builders, as they are
known, help you quickly build the data structures you need. I will show how to imple-
ment test data builders in chapter 10. 
USE GOOD AND REUSABLE ASSERTION APIS
Asserting was easy in the example, thanks to AssertJ. However, many SQL queries
return lists of objects, and AssertJ provides several methods to assert them in many dif-
ferent ways. If a specific assertion is required by many test methods, do not be afraid
to create a utility method that encapsulates this complex assertion. As I discussed, put-
ting it in the base test class is my usual way to go. 
MINIMIZE THE REQUIRED DATA
Make sure the input data is minimized. You do not want to have to load hundreds of
thousands of elements to exercise your SQL query. If your test only requires data in
two tables, only insert data in these two tables. If your test requires no more than 10
rows in that table, only insert 10 rows. 
TAKE THE SCHEMA EVOLUTION INTO CONSIDERATION
In real software systems, database schemas evolve quickly. Make sure your test suite is
resilient toward these changes. In other words, database evolution should not break
the existing test suite. Of course, you cannot (and you probably do not want to)
decouple your code completely from the database. But if you are writing a test and
notice that a future change may break it, consider reducing the number of points that
will require change. Also, if the database changes, you must propagate the change to
the test database. If you are using a framework to help you with migration (like Flyway
or Liquibase), you can ask the framework to perform the migrations. 


---
**Page 239**

239
System tests
CONSIDER (OR DON’T) AN IN-MEMORY DATABASE
You should decide whether your tests will communicate with a real database (the same
type of database as in your production environment) or a simpler database (such as
an in-memory database). As always, both sides have advantages and disadvantages.
Using the same database as in production makes your tests more realistic: your tests
will exercise the same SQL engine that will be exercised in production. On the other
hand, running full-blown MySQL is much more expensive, computationally speaking,
than a simple in-memory database. All in all, I favor using real databases when I am
writing SQL integration tests. 
9.3
System tests
At some point, your classes, business rules, persistence layers, and so on are combined
to form, for example, a web application. Let’s think about how a web application tradi-
tionally works. Users visit a web page (that is, their browser makes a request to the
server, and the server processes the request and returns a response that the browser
shows) and interact with the elements on the page. These interactions often trigger
other requests and responses. Considering a pet clinic application: a user goes to the
web page that lists all the scheduled appointments for today, clicks the New Appoint-
ment button, fills out the name of their pet and its owner, and selects an available time
slot. The web page then takes the user back to the Appointments page, which now
shows the newly added appointment.
 If this pet clinic web application was developed using test-driven approaches and
everything we discussed in the previous chapters of this book, the developer already
wrote (systematic) unit tests for each unit in the software. For example, the Appointment
class already has unit tests of its own.
 In this section, we discuss what to test in a web application and what tools we can
use to automatically open the browser and interact with the web page. We also discuss
some best practices for writing system tests.
NOTE
Although I use a web application as an example of how to write a sys-
tem test, the ideas in this section apply to any other type of software system.
9.3.1
An introduction to Selenium
Before diving into the best practices, let’s get familiar with the mechanics of writing such
tests. For that, we will rely on Selenium. The Selenium framework (www.selenium.dev)
is a well-known tool that supports developers in testing web applications. Selenium
can connect to any browser and control it. Then, through the Selenium API, we can
give commands such as “open this URL,” “find this HTML element in the page and
get its inner text,” and “click that button.” We will use commands like these to test our
web applications.
 We use the Spring PetClinic web application (https://projects.spring.io/spring
-petclinic) as an example throughout this section. If you are a Java web developer,
you are probably familiar with Spring Boot. For those who are not, Spring Boot is


