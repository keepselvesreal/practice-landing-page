# 10.2.4 Fixtures that are too general (pp.269-270)

---
**Page 269**

269
Test smells
itself. This can mean the test is responsible for populating a database, writing the
required files to the disk, or starting up a Tomcat server. This setup may require com-
plex code, and you should also make your best effort to abstract away such complexity
by, for example, moving such code to other classes (like DatabaseInitialization or
TomcatLoader) and allowing the test code to focus on the test cases.
 Another common test smell happens when the test assumes that the resource is
available all the time. Imagine a test method that interacts with a web service, which
may be down for reasons we do not control. To avoid this test smell, you have two
options: avoid depending on external resources by using stubs and mocks or, if the
test cannot avoid using the external dependency, make the test suite robust enough.
For example, make your test suite skip that test when the resource is unavailable, and
provide an alert explaining why that was the case. This may seem counterintuitive, but
remember that developers trust their test suites. Having a single test fail for the wrong
reasons can make you lose confidence in the entire test suite.
 From a readability perspective, it should be easy to understand all the (external)
resources required and used by the test. Imagine that a test requires a test file in some
directory. If the file is not there, the test fails. A first-time developer may have difficulty
understanding this prerequisite. Avoid having such mystery guests in your test suite.
The test code should be explicit about all its external dependencies.  
10.2.4
Fixtures that are too general
A fixture is the set of input values used to exercise the component under test. As you
may have noticed, fixtures are the stars of the test method, as they derive naturally
from the test cases we engineer using any of the techniques we have discussed.
 When testing more complex components, you may need to build several different
fixtures: one for each partition you want to exercise. These fixtures can then become
complex. And to make the situation worse, while tests are different from each other,
their fixtures may intersect. Given this possible intersection among the different fix-
tures, as well as the difficulty with building complex entities and fixtures, you may
decide to declare a large fixture that works for many different tests. Each test would
then use a small part of this large fixture.
 While this approach may work, and the tests may correctly implement the test
cases, they quickly become hard to maintain. Once a test fails, you will find yourself
with a large fixture that may not be completely relevant for that particular failing test.
You then must manually filter out parts of the fixture that are not exercised by the fail-
ing test. That is an unnecessary cost.
 Making sure the fixture of a test is as specific and cohesive as possible helps you com-
prehend the essence of a test (which is, again, highly relevant when the test starts to fail).
Build patterns (focusing on building test data) can help you avoid generic fixtures. More
specifically, the Test Data Builder pattern we discussed is often used in the test code of
enterprise applications. Such applications often deal with creating complex sets of inter-
related business entities, which can easily lead developers to write general fixtures. 


---
**Page 270**

270
CHAPTER 10
Test code quality
10.2.5
Sensitive assertions
Good assertions are fundamental in test cases. A bad assertion may result in a test not
failing when it should. However, a bad assertion may also cause a test to fail when it
should not. Engineering a good assertion statement is challenging—even more so when
components produce fragile outputs (outputs that change often). Test code should be
as resilient as possible to the implementation details of the component under test.
Assertions also should not be oversensitive to internal changes.
 In the tool we use to assess students’ submissions (https://github.com/cse1110/
andy), we have a class responsible for transforming the assessment results into a message
(string) that we show in our cloud-based IDE. The following listing shows the output for
one of our exercises.
--- Compilation 
Success
--- JUnit execution 
7/7 passed
--- JaCoCo coverage 
Line coverage: 13/13
Instruction coverage: 46/46
Branch coverage: 12/12 
--- Mutation testing     
10/10 killed
--- Code checks 
No code checks to be assessed
--- Meta tests 
13/13 passed
Meta test: always finds clumps (weight: 1) PASSED
Meta test: always returns zero (weight: 1) PASSED
Meta test: checks in pairs (weight: 1) PASSED
Meta test: does not support more than two per clump (weight: 1) PASSED
Meta test: does not support multiple clumps (weight: 1) PASSED
Meta test: no empty check (weight: 1) PASSED
Meta test: no null check (weight: 1) PASSED
Meta test: only checks first two elements (weight: 1) PASSED
Meta test: only checks last two elements (weight: 1) PASSED
Meta test: skips elements after clump (weight: 1) PASSED
Meta test: skips first element (weight: 1) PASSED
Meta test: skips last element (weight: 1) PASSED
Meta test: wrong result for one element (weight: 1) PASSED 
--- Assessment
Branch coverage: 12/12 (overall weight=0.10)
Mutation coverage: 10/10 (overall weight=0.10)
Listing 10.8
An example of the output of our tool
The result of the compilation
How many tests passed
Coverage information
Mutation testing 
information
Static code checks (in this 
case, none were executed)
The student’s final grade
The student’s 
final grade


