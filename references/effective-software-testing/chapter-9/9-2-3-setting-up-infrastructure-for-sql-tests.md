# 9.2.3 Setting up infrastructure for SQL tests (pp.236-238)

---
**Page 236**

236
CHAPTER 9
Writing larger tests
In addition, we test a single in point. While doing so is not necessary, as we discussed
in the boundary testing section in chapter 2, one more test case is cheap and makes
the test strategy more comprehensible.
NOTE
Your tests should run against a test database—a database set up exclu-
sively for your tests. Needless to say, you do not want to run your tests against
the production database. 
9.2.3
Setting up infrastructure for SQL tests
In our example, it was simple to open a connection, reset the database state, and so
on, but that may become more complicated (or lengthy) when your database schema
is complicated. Invest in test infrastructure to facilitate your SQL testing and make
sure that when a developer wants to write an integration test, they do not need to set
up connections manually or handle transactions. This should be a given from the test
suite class.
 A strategy I often apply is to create a base class for my integration tests: say, SQL-
IntegrationTestBase. This base class handles all the magic, such as creating a con-
nection, cleaning up the database, and closing the connection. Then the test class,
such as InvoiceDaoTest, which would extend SQLIntegrationTestBase, focuses only
on testing the SQL queries. JUnit allows you to put BeforeEach and AfterEach in base
classes, and those are executed as if they were in the child test class.
 Another advantage of having all the database logic in the test base class is that
future changes will only need to be made in one place. Listing 9.23 shows an imple-
mentation example. Note how the InvoiceDaoIntegrationTest code focuses primar-
ily on tests.
public class SqlIntegrationTestBase {
  private Connection connection;
  protected InvoiceDao dao;     
  @BeforeEach   
  void openConnectionAndCleanup() throws SQLException {
    // ...
  }
  @AfterEach    
  void close() throws SQLException {
    // ...
  }
}
public class InvoiceDaoIntegrationTest extends SqlIntegrationTestBase {  
Listing 9.23
Base class that handles the database-related logic
Makes the InvoiceDao 
protected so we can access 
it from the child classes
The methods
are the same
as before.
InvoiceDaoTest now extends
SqlIntegrationTestBase.


---
**Page 237**

237
Database and SQL testing
  @Test
  void save() {      
    // ...
  }
  @Test
  void atLeast() {   
    // ...
  }
}
I will not provide a complete code example, because it changes from project to proj-
ect. Instead, the following sections list what I do in such an integration test base class.
OPENING THE DATABASE CONNECTION
This means opening a JDBC connection, a Hibernate connection, or the connection
of whatever persistence framework you use. In some cases, you may be able to open a
single connection per test suite instead of one per test method. In this case, you may
want to declare it as static and use JUnit’s BeforeAll to open and AfterAll to close it. 
OPENING AND COMMITTING THE TRANSACTION
In more complex database operations, it is common to make them all happen
within a transaction scope. In some systems, your framework handles this automati-
cally (think of Spring and its @Transactional annotations). In other systems, devel-
opers do it by hand, calling something that begins the transaction and later something
that commits it.
 You should decide on how to handle transactions in your test. A common approach
is to open the transaction and, at the end of the test method, commit the transaction.
Some people never commit the transaction, but roll it back once the test is over.
Because this is an integration test, I suggest committing the transaction for each test
method (and not for the entire test class, as we did for the connection). 
RESETTING THE STATE OF THE DATABASE
You want all your tests to start with a clean database state. This means ensuring the
correct database schema and having no unexpected data in the tables. The simplest
way to do this is to truncate every table at the beginning of each test method. If you
have many tables, you truncate them all. You can do this by hand (and manually add
one truncate instruction per table in the code) or use a smarter framework that does
it automatically.
 Some developers prefer to truncate the tables before the test method, and others
after. In the former case, you are sure the database is clean before running the test. In
the latter, you ensure that everything is clean afterward, which helps ensure that it will
be clean the next time you run it. I prefer to avoid confusion and truncate before the
test method. 
The test class focuses on 
the tests themselves, as the 
database infrastructure is 
handled by the base class.


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


