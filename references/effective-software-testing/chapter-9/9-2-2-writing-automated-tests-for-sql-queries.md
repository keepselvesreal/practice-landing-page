# 9.2.2 Writing automated tests for SQL queries (pp.231-236)

---
**Page 231**

231
Database and SQL testing
9.2.2
Writing automated tests for SQL queries
We can use JUnit to write SQL tests. All we need to do is (1) establish a connection
with the database, (2) make sure the database is in the right initial state, (3) execute
the SQL query, and (4) check the output.
 Consider the following scenario:
We have an Invoice table composed of a name (varchar, length 100) and a value
(double).
We have an InvoiceDao class that uses an API to communicate with the data-
base. The precise API does not matter.
This DAO performs three actions: save() persists an invoice in the database,
all() returns all invoices in the database, and allWithAtLeast() returns all
invoices with at least a specified value. Specifically,
– save() runs INSERT INTO invoice (name, value) VALUES (?,?).
– all() runs SELECT * FROM invoice.
– allWithAtLeast() runs SELECT * FROM invoice WHERE value >= ?.
A simple JDBC implementation of such a class is shown in listings 9.17, 9.18, and 9.19.
import java.sql.*;
import java.util.ArrayList;
import java.util.List;
public class InvoiceDao {
  private final Connection connection;  
  public InvoiceDao(Connection connection) {
    this.connection = connection;
  }
  public List<Invoice> all() {
    try {
      PreparedStatement ps = connection.prepareStatement(
        ➥ "select * from invoice");   
      ResultSet rs = ps.executeQuery();
      List<Invoice> allInvoices = new ArrayList<>();
      while (rs.next()) {                                 
        allInvoices.add(new Invoice(rs.getString("name"),
        ➥ rs.getInt("value")));
      }
      return allInvoices;
    } catch(Exception e) {   
      throw new RuntimeException(e);
    }
  }
Listing 9.17
Simple JDBC implementation of InvoiceDao, part 1
The DAO holds 
a connection to 
the database.
Prepares and 
executes the 
SQL query
Loops through the 
results, creating a 
new Invoice entity 
for each of them
The JDBC API throws checked 
exceptions. To simplify, we convert 
them to unchecked exceptions.


---
**Page 232**

232
CHAPTER 9
Writing larger tests
public List<Invoice> allWithAtLeast(int value) {  
    try {
      PreparedStatement ps = connection.prepareStatement(
        ➥ "select * from invoice where value >= ?");
      ps.setInt(1, value);
      ResultSet rs = ps.executeQuery();
      List<Invoice> allInvoices = new ArrayList<>();
      while (rs.next()) {
        allInvoices.add(
          new Invoice(rs.getString("name"), rs.getInt("value"))
        );
      }
      return allInvoices;
    } catch (Exception e) {
      throw new RuntimeException(e);
    }
  }
public void save(Invoice inv) {
    try {
      PreparedStatement ps = connection.prepareStatement(
        "insert into invoice (name, value) values (?,?)");  
      ps.setString(1, inv.customer);
      ps.setInt(2, inv.value);
      ps.execute();
      connection.commit();
    } catch(Exception e) {
      throw new RuntimeException(e);
    }
  }
}
NOTE
This implementation is a naive way to access a database. In more com-
plex projects, you should use a professional production-ready database API
such as jOOQ, Hibernate, or Spring Data.
Let’s test the InvoiceDao class. Remember, we want to apply the same ideas we have
seen so far. The difference is that we have a database in the loop. Let’s start with
all(). This method sends a SELECT * FROM invoice to the database and gets back the
result. But for this query to return something, we must first insert some invoices into
the database. The InvoiceDao class also provides the save() method, which sends an
INSERT query. This is enough for our first test.
Listing 9.18
Simple JDBC implementation of InvoiceDao, part 2
Listing 9.19
Simple JDBC implementation of InvoiceDao, part 3
The same thing 
happens here: we 
prepare the SQL 
query, execute it, 
and then create one 
Invoice entity for 
each row.
Prepares 
the INSERT 
statement and 
executes it


---
**Page 233**

233
Database and SQL testing
public class InvoiceDaoIntegrationTest {
  private Connection connection;   
  private InvoiceDao dao;          
  @Test
  void save() {
   Invoice inv1 = new Invoice("Mauricio", 10);   
   Invoice inv2 = new Invoice("Frank", 11);
   dao.save(inv1);   
   List<Invoice> afterSaving = dao.all();    
   assertThat(afterSaving).containsExactlyInAnyOrder(inv1);
   dao.save(inv2);    
   List<Invoice> afterSavingAgain = dao.all();
   assertThat(afterSavingAgain)
     .containsExactlyInAnyOrder(inv1, inv2);
  }
}
This test method creates two invoices (inv1, inv2), persists the first one using the
save() method, retrieves the invoices from the database, and asserts that it returns
one invoice. Then it persists another invoice, retrieves the invoices from the database
again, and asserts that now it returns two invoices. The test method ensures the cor-
rect behavior of both the save() and all() methods. The containsExactlyInAny-
Order assertion from AssertJ ensures that the list contains the precise invoices that we
pass to it, in any order. For that to happen, the Invoice class needs a proper imple-
mentation of the equals() method.
 In terms of testing, our implementation is correct. However, given the database, we
have some extra concerns. First, we should not forget that the database persists the
data permanently. Suppose we start with an empty database. The first time we run the
test, it will persist two invoices in the database. The second time we run the test, it will
persist two new invoices, totaling four invoices. This will make our test fail, as it
expects the database to have one and two invoices, respectively.
 This was never a problem in our previous unit tests: every object we created lived in
memory, and they disappeared after the test method was done. When testing with a
real database, we must ensure a clean state:
Before the test runs, we open the database connection, clean the database, and
(optionally) put it in the state we need it to be in before executing the SQL
query under test.
After the test runs, we close the database connection.
This is a perfect fit for JUnit’s @BeforeEach and @AfterEach, as shown in the following
listing.
Listing 9.20
First step of our SQL test
This test requires a connection to 
the database and an invoice DAO.
Creates a set 
of invoices
Persists the
first one
Gets all invoices from the database 
and ensures that the database only 
contains the invoice we inserted
Inserts another 
invoice and ensures 
that the database 
contains both of 
them


---
**Page 234**

234
CHAPTER 9
Writing larger tests
public class InvoiceDaoIntegrationTest {
  private Connection connection;
  private InvoiceDao dao;
  @BeforeEach
  void openConnectionAndCleanup() throws SQLException {
    connection = DriverManager.getConnection("jdbc:hsqldb:mem:book");   
    PreparedStatement preparedStatement = connection.prepareStatement(
      ➥ "create table if not exists invoice (name varchar(100),
      ➥ value double)");   
    preparedStatement.execute();
    connection.commit();
    connection.prepareStatement("truncate table invoice").execute();  
    dao = new InvoiceDao(connection);  
  }
  @AfterEach
  void close() throws SQLException {
    connection.close();   
  }
  @Test
  void save() {   
    // ...
  }
}
The openConnectionAndCleanup() method is annotated as @BeforeEach, which
means JUnit will run the cleanup before every test method. Right now, its implemen-
tation is simplistic: it sends a truncate table query to the database.
NOTE
In larger systems, you may prefer to use a framework to help you han-
dle the database. I suggest Flyway (https://flywaydb.org) or Liquibase (https://
www.liquibase.org). In addition to supporting you in evolving your database
schema, these frameworks contain helper methods that help clean up the
database and make sure it contains the right schema (that is, all tables, con-
straints, and indexes are there).
We also open the connection to the database manually, using JDBC’s most rudimen-
tary API call, getConnection. (In a real software system, you would probably ask
Hibernate or Spring Data for an active database connection.) Finally, we close the
connection in the close() method (which happens after every test method).
 Let’s now test the other method: allWithAtLeast(). This method is more interest-
ing, as the SQL query contains a predicate, where value >= ?. This means we have
Listing 9.21
Setting up and tearing down the database
Opens a connection to the database.
For simplicity, I am using HSQLDB, an
in-memory database. In real systems,
you may want to connect to the same
type of database you use in
production.
Ensures that the database has the right tables and schema. 
In this example, we create the invoice table. You may need 
something fancier than that in real applications.
Truncates the table to
ensure that no data from
previous tests is in the
database. Again, you may
need something fancier
in more complex
applications.
Creates
the DAO
Closes the connection. You 
may decide to close the 
connection only at the end of 
the entire test suite. In that 
case, you can use JUnit’s 
@BeforeAll and @AfterAll.
The test
we wrote


---
**Page 235**

235
Database and SQL testing
different scenarios to exercise. Here we can use all of our knowledge about boundary
testing and think of on and off points, as we did in chapter 2.
 Figure 9.2 shows the boundary analysis. The on point is the point on the boundary.
In this case, it is whatever concrete number we pass in the SQL query. The off point
is the nearest point to the on point that flips the condition. In this case, that is what-
ever concrete number we pass in the SQL query minus one, since it makes the con-
dition false.
The following listing shows the JUnit test. Note that we add an in point to the test
suite. Although it isn’t needed, it is cheap to do and makes the test more readable:
@Test
void atLeast() {
  int value = 50;
  Invoice inv1 = new Invoice("Mauricio", value - 1);   
  Invoice inv2 = new Invoice("Arie", value);           
  Invoice inv3 = new Invoice("Frank", value + 1);      
  dao.save(inv1);    
  dao.save(inv2);
  dao.save(inv3);
  List<Invoice> afterSaving = dao.allWithAtLeast(value);
  assertThat(afterSaving)
    .containsExactlyInAnyOrder(inv2, inv3);    
}
The strategy we use to derive the test case is very similar to what we have seen previ-
ously. We exercise the on and off points and then ensure that the result is correct.
Given where value >= ?, where we concretely replace ? with 50 (see the value variable
and the inv2 variable), we have 50 as on point and 49 as off point (value - 1 in inv1).
Listing 9.22
Integration test for the atLeast method
where value >= ?
On point:
Oﬀpoint:
?
? – 1
The on point is the number
in the boundary. In this case,
it’s whatever number we
pass in the SQL.
The off point ﬂips the result of the on point. In
this case, it should make the expression false: e.g.,
whatever number we pass in the SQL minus
makes
1
the expression false.
Figure 9.2
On and off points 
for the allWithAtLeast() 
SQL query
The on point of the value 
>= x boundary is x. The off 
point is x - 1. A random in 
point can be x + 1.
Persists them all 
in the database
We expect the method to 
return only inv2 and inv3.


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


