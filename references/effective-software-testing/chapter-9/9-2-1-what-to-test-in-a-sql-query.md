# 9.2.1 What to test in a SQL query (pp.229-231)

---
**Page 229**

229
Database and SQL testing
I have said many times before—unit tests are cheap and easy to write. But do not be
afraid to write larger tests whenever you believe they will give you more confidence. 
9.2
Database and SQL testing
In many of the examples in this book, a Data Access Object (DAO) class is responsible
for retrieving or persisting information in the database. Whenever these classes
appear, we quickly stub or mock them out of our way. However, at some point, you
need to test these classes. These DAOs often perform complex SQL queries, and they
encapsulate a lot of business knowledge, requiring testers to spend some energy mak-
ing sure they produce the expected outcomes. The following sections examine what
to test in a SQL query, how to write automated test cases for such queries, and the
challenges and best practices involved.
9.2.1
What to test in a SQL query
SQL is a robust language and contains many different functions we can use. Let’s sim-
plify and look at queries as a composition of predicates. Here are some examples:

SELECT * FROM INVOICE WHERE VALUE < 50

SELECT * FROM INVOICE I JOIN CUSTOMER C ON I.CUSTOMER_ID = C.ID WHERE
C.COUNTRY = 'NL'

SELECT * FROM INVOICE WHERE VALUE > 50 AND VALUE < 200
In these examples, value < 50, i.customer_id = c.id, c.country = 'NL', and value >
50 and value < 200 are the predicates that compose the different queries. As a tester, a
possible criterion is to exercise the predicates and check whether the SQL query
returns the expected results when predicates are evaluated to different results.
 Virtually all the testing techniques we have discussed in this book can be applied
here:
Specification-based testing—SQL queries emerge out of a requirement. A tester can
analyze the requirements and derive equivalent partitions that need to be tested.
Boundary analysis—Such programs have boundaries. Because we expect bound-
aries to be places with a high bug probability, exercising them is important.
Structural testing—SQL queries contain predicates, and a tester can use the
SQL’s structure to derive test cases.
Here, we focus on structural testing. If we look at the third SQL example and try to
make an analogy with what we have discussed about structural testing, we see that the
SQL query contains a single branch composed of two predicates (value > 50 and
value < 200). This means there are four possible combinations of results in these two
predicates: (true, true), (true, false), (false, true), and (false, false). We
can aim at either of the following:
Branch coverage—In this case, two tests (one that makes the overall decision eval-
uate to true and one that makes it evaluate to false) would be enough to
achieve 100% branch coverage.


---
**Page 230**

230
CHAPTER 9
Writing larger tests
Condition + branch coverage—In this case, three tests would be enough to achieve
100% condition + branch coverage: for example, T1 = 150, T2 = 40, T3 = 250.
In “A practical guide to SQL white-box testing,” a 2006 paper by Tuya, Suárez-Cabal,
and De La Riva, the authors suggest five guidelines for designing SQL tests:
Adopting modified condition/decision coverage (MC/DC) for SQL conditions—Deci-
sions happen at three places in a SQL query: join, where, and having condi-
tions. We can use criteria like MC/DC to fully exercise the query’s predicates. If
you do not remember how MC/DC coverage works, revisit chapter 3.
Adapting MC/DC for tackling nulls—Because databases have a special way of han-
dling/returning nulls, any (coverage) criteria should be adapted to three-valued
logic (true, false, null). In other words, consider the possibility of values being
null in your query.
Category-partitioning selected data—SQL can be considered a declarative specifica-
tion for which we can define partitions to be tested. Directly from Tuya et al.’s
paper, we define the following:
– Rows that are retrieved—We include a test state to force the query to not select
any row.
– Rows that are merged—The presence of unwanted duplicate rows in the output
is a common failure in some queries. We include a test state in which identi-
cal rows are selected.
– Rows that are grouped—For each of the group-by columns, we design test states
to obtain at least two different groups at the output, such that the value used
for the grouping is the same and all the others are different.
– Rows that are selected in a subquery—For each subquery, we include test states
that return zero or more rows, with at least one null and two different values
in the selected column.
– Values that participate in aggregate functions—For each aggregate function
(excluding count), we include at least one test state in which the function
computes two equal values and another that is different.
– Other expressions—We also design test states for expressions involving the like
predicate, date management, string management, data type conversions, or
other functions using category partitioning and boundary checking.
Checking the outputs—We should check not only the input domain but also the
output domain. SQL queries may return null or empty values in specific col-
umns, which may make the rest of the program break.
Checking the database constraints—Databases have constraints. We should make
sure the database enforces these constraints.
As you can see, many things can go wrong in a SQL query. It is part of the tester’s job
to make sure that does not happen. 


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


