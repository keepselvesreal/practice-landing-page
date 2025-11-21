# 9.1.2 Testing larger components that go beyond our code base (pp.224-229)

---
**Page 224**

224
CHAPTER 9
Writing larger tests
This example shows how much more work it is to test sets of classes together. I use this
approach when I see value in it, such as for debugging a problem that happens in pro-
duction. However, I use these tests in addition to unit tests. I also do not re-test every-
thing. I prefer to use these large component tests as an excuse to try the component
with real-world inputs. 
9.1.2
Testing larger components that go beyond our code base
In the previous example, the large test gives us confidence about the overall behavior
of the component, but we could still test each unit individually. In some cases, how-
ever, we cannot write tests for units in isolation. Or rather, we can write tests, but doing
so would not make sense. Let’s look at examples of two small open source projects I
coded.
TESTING THE CK TOOL
The first example is a project called CK (https://github.com/mauricioaniche/ck),
available on my GitHub page. CK is a tool that calculates code metrics for Java code.
To do so, it relies on Eclipse JDT (www.eclipse.org/jdt/), a library that is part of the
Eclipse IDE. Among its many functionalities, JDT enables us to build abstract syntax
trees (ASTs) of Java code. CK builds ASTs using JDT and then visits these trees and cal-
culates the different metrics.
 As you can imagine, CK is highly dependent on how JDT does things. Given an
AST, JDT offers clients a way to visit the tree. Clients need to create a class that inherits
from ASTVisitor. (Visitor is a popular design pattern for navigating complex data
structures.) CK then implements many of these AST visitors, one for each metric.
 One of the metrics that CK implements is coupling between objects (CBO). The
metric counts the number of other classes the class under analysis depends on.
Imagine the fictitious class A in the following listing. This class declares a field of
type B and instantiates class C. CK detects the dependency on B and C and returns 2
as the CBO.
 
(continued)
Delivery price:
a
1 to 3 items
b
4 to 10 items
c
More than 10 items
Electronics:
a
Has an electronic item
b
No electronic items
I would then combine the partitions that make sense, engineer the different test
cases, and write them as automated JUnit tests. I will leave that as an exercise for
you.


---
**Page 225**

225
When to use larger tests
class A {
  private B b;
  public void action() {
    new C().method();
  }
}
In listing 9.13, I show a simplified implementation of the CBO metric (you can see the
full code on my GitHub). The implementation looks at any declared or used type in
the class and adds it to a set. Later, it returns the number of types in the set. Note all
the visit methods: they are called by the JDT whenever there is, for example, a
method invocation or a field declaration.
public class CBO implements CKASTVisitor {   
  private Set<String> coupling = new HashSet<String>();  
  @Override
  public void visit(MethodInvocation node) {      
    IMethodBinding binding = node.resolveMethodBinding();
    if(binding!=null)
      coupleTo(binding.getDeclaringClass());
  }
  @Override
  public void visit(FieldDeclaration node) {  
    coupleTo(node.getType());
  }
  // this continues for all the possible places where a type can appear...
  private void coupleTo(Type type) {
    // some complex code here to extract the name of the type.
    String fullyQualifiedName = ...;
    addToSet(fullyQualifiedName);   
  }
  private void addToSet(String name) {
    this.coupling.add(name);
  }
}
How can we write a unit test for the CBO class? The CBO class offers many visit
methods called by the JDT once the JDT builds the AST out of real Java code. We could
Listing 9.12
Fictitious class A that depends on B and C
Listing 9.13
CBO implementation in CK
I created my own interface, instead of using 
JDT’s ASTVisitor, but it is the same thing.
Declares a set 
to keep all the 
unique types 
this class uses
If there is a method 
invocation, gets the 
type of the class of 
the invoked method
If there is a field 
declaration, gets the 
type of the field
Adds the full 
name of the 
type to the set


---
**Page 226**

226
CHAPTER 9
Writing larger tests
try to mock all the types that these visit methods receive, such as MethodInvocation
and FieldDeclaration, and then make a sequence of calls to these methods. But in
my opinion, that would be too far from what will happen when we run JDT for real.
 I do not see a way to unit-test this class without starting up JDT, asking JDT to build
an AST out of a small but real Java class, using CBO to visit the generated AST, and
comparing the result. So, I used real integration testing in this case.
 The test class in listing 9.14 runs CK (which runs JDT) in a specific directory. This
directory contains fake Java classes that I created for the sole purpose of the tests. In
the code, it is the cbo directory. I have one directory per metric. Because running JDT
takes a few seconds, I run it once for the entire test class (see the @BeforeAll
method). The test method then asks for the report of a specific class. In the case of
the countDifferentDependencies test, I am interested in the coupling of the fake
Coupling1 class. I then assert that its coupling is 6.
public class CBOTest extends BaseTest {   
  @BeforeAll
  public void setUp() {
    report = run(fixturesDir() + "/cbo");   
  }
  @Test
  public void countDifferentDependencies() {
    CKClassResult result = report.get("cbo.Coupling1");   
    assertEquals(6, result.getCbo());   
  }
}
To help you better understand why the CBO is 6, listing 9.15 shows the Coupling1
class. This code makes no sense, but it is enough for us to count dependencies. This
class uses classes A, B, C, D, C2, and CouplingHelper: that makes six dependencies.
public class Coupling1 {
  private B b;      
  public D m1() {     
    A a = new A();   
    C[] x = new C[10];   
    CouplingHelper h = new CouplingHelper();    
    C2 c2 = h.m1();   
    return d;
  }
}
Listing 9.14
CBOTest 
Listing 9.15
Coupling1 fixture
The BaseTest class provides 
basic functionality for all 
the test classes.
Runs JDT on all code in the cbo 
directory. This directory contains 
Java code I created solely for 
testing purposes.
CK returns a report, 
which we use to get the 
results of a specific Java 
class we created for this 
test (see listing 9.15).
We expect this class to be
coupled with six classes.
B
D
A
C
CouplingHelper
C2


---
**Page 227**

227
When to use larger tests
The CBOTest class contains many other test methods, each exercising a different case.
For example, it tests whether CK can count a dependency even though the depen-
dency’s code is not available (imagine that class A in the example is not in the direc-
tory). It also tests whether it counts interfaces and inherited classes, types in method
parameters, and so on.
 It was challenging to come up with good test cases here; and it was not easy to
apply specification-based testing, because the input could be virtually any Java class.
You may face similar challenges when implementing classes for a plug-and-play archi-
tecture. This is a good example of a specific context where we need to learn more
about how to test. Testing compilers, which is a related problem, is also a significant
area of research. 
TESTING THE ANDY TOOL
Another example where I could not write isolated unit tests involved a tool my teaching
assistants and I wrote to assess the test suites that our students engineered. The tool,
named Andy (https://github.com/cse1110/andy), compiles the test code provided by a
student, runs all the provided JUnit tests, calculates code coverage, runs some static
analysis, and checks whether the test suite is strong enough to kill mutant versions of the
code under test. Andy then gives a grade and a detailed description of its assessment.
 Each step is implemented in its own class. For example, CompilationStep is
responsible for compiling the student’s code, RunJUnitTestsStep is responsible for
executing all the unit tests in the student’s submission, and RunMetaTestsStep checks
whether the test suite kills all the manually engineered mutants we expect it to kill.
Figure 9.1 illustrates Andy’s overall flow.
 If we were to unit-test everything, we would need a unit test for the compilation
step, another for the step that runs JUnit, and so on. But how could we exercise the
“run JUnit” step without compiling the code first? It is not possible.
Student’s
test
(“submission”)
Program to
test
(“exercise”)
Student
Tests
Engineers
test cases
Submits
Andy
Compiles
the code
Runs tests
Calculates
coverage
Runs meta
tests
Generates a ﬁnal
assessment
Final grade: 78/100
Coverage: 85/100
Meta tests: 2/3
Meta test 1: Killed
Meta test 2: Survived
…
Prints the assessment
Figure 9.1
Simplified flow of Andy


---
**Page 228**

228
CHAPTER 9
Writing larger tests
We decided to use larger tests. For example, the tests that exercise RunMetaTestsStep
run the entire engine we developed. Thus our test provides a real Java file that simulates
the student’s submission and another Java file that contains the class under test. Andy
gets these files, compiles them, runs the JUnit tests, and finally runs the meta tests.
 Listing 9.16 shows one of the tests in the test suite. The run() method, which is
implemented in the IntegrationTestBase test base so all the test classes can use it,
runs the entire Andy engine. The parameters are real Java files: 

NumberUtilsAddLibrary.java, which contains the code of the class under test 

NumberUtilsAddOfficialSolution.java, which contains a possible solution
submitted by the student (in this case, the official solution of this exercise)

NumberUtilsAddConfiguration.java, a configuration class that should be pro-
vided by the teacher
The run() method returns a Result class: an entity containing all the results of each
step. Because this test case focuses on the meta tests, the assertions also focus on them.
In this test method, we expect Andy to run four meta tests—AppliesMultipleCarries-
Wrongly, DoesNotApplyCarryAtAll, DoesNotApplyLastCarry, and DoesNotCheck-
NumbersOutOfRange—and we expect them all to pass.
public class MetaTestsTest extends IntegrationTestBase {
  @Test
  void allMetaTestsPassing() {
    Result result =
      run(         
      "NumberUtilsAddLibrary.java",
      "NumberUtilsAddOfficialSolution.java",
      "NumberUtilsAddConfiguration.java");
    assertThat(result.getMetaTests().getTotalTests())
      .isEqualTo(4);  
    assertThat(result.getMetaTests().getPassedMetaTests())
      .isEqualTo(4);
    assertThat(result.getMetaTests())
      .has(passedMetaTest("AppliesMultipleCarriesWrongly"))
      .has(passedMetaTest("DoesNotApplyCarryAtAll"))
      .has(passedMetaTest("DoesNotApplyLastCarry"))
      .has(passedMetaTest("DoesNotCheckNumbersOutOfRange"));
  }
}
NOTE
You may be curious about the passedMetaTest method in this test
method. AssertJ enables us to extend its set of assertions, and we created one
specifically for meta tests. I will show how to do this in chapter 10.
These two examples illustrate situations where unit-testing a class in isolation does not
make sense. In general, my advice is to use unit testing as much as possible, because—as
Listing 9.16
Integration test for the MetaTests step
Runs the full 
Andy engine
Asserts that
the meta tests
step executed
as expected


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


