# 10.2.5 Sensitive assertions (pp.270-272)

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


---
**Page 271**

271
Test smells
Code checks: 0/0 (overall weight=0.00)
Meta tests: 13/13 (overall weight=0.80)
Final grade: 100/100
If we write tests without thinking too much, we end up writing lots of assertions that
check whether some string is in the output. And given that we will write many test
cases for many different outputs, our test suite will end up with lots of statements like
“assert output contains Final grade: 100/100”.
 Note how sensitive this assertion is. If we change the message slightly, the tests will all
break. Making assertions that are less sensitive to small changes is usually a good idea.
 In this situation, we have no other option than to assert that the string matches
what we have. To sort this out, we decided to create our own set of assertions for each
part of the message we need to assert. These assertions enable us to decouple our test
code from the strings themselves. And if the message changes in the future, all we will
need to do is change our assertion.
 In listing 10.9, the reportCompilationError test method ensures that we show the
proper message to the student when they submit a solution that does not compile. We
create a Result object (representing the final assessment of the student solution) with
a compilation error. We then call the method under test and get back the generated
string message.
@Test
void reportCompilationError() {
  Result result = new ResultTestDataBuilder()
    .withCompilationFail(
      new CompilationErrorInfo(
        ➥ "Library.java", 10, "some compilation error"),
      new CompilationErrorInfo(
        ➥ "Library.java", 11, "some other compilation error")
  ).build(); 
  writer.write(ctx, result); 
  String output = generatedResult();
  assertThat(output) 
    .has(noFinalGrade())
    .has(not(compilationSuccess()))
    .has(compilationFailure())
    .has(compilationErrorOnLine(10))
    .has(compilationErrorOnLine(11))
    .has(compilationErrorType("some compilation error"))
    .has(compilationErrorType("some other compilation error"));
}
Listing 10.9
A test that uses our own assertions
Creates a 
Result in 
which we tell 
the student 
that there is a 
compilation 
error in their 
solution
Calls the method 
under test and gets 
the generated message
Asserts that the message is as we expect. 
Note, however, our set of assertions: 
noFinalGrade, compilationSuccess, and 
so on. They decouple our test from the 
concrete string.


---
**Page 272**

272
CHAPTER 10
Test code quality
The trick happens in the assertions. Note the many assertions we created: noFinal-
Grade() ensures that the final grade is not displayed, compilationErrorOnLine(10)
ensures that we tell the student there is a compilation error on line 10, and so on. To
create these assertions, we use AssertJ’s extension capabilities. All we need to do is cre-
ate a method that returns AssertJ’s Condition<?> class. The generic type should be
the same as the type of the object on which we are performing the assertion. In this
case, the output variable is a string, so we need to create a Condition<String>.
 The implementation of the compilationErrorOnLine assertion is shown in listing
10.10. If a compilation error happens, we print "- line <number>: <error message>".
This assertion then looks for "- line <number>" in the string.
public static Condition<String> compilationErrorOnLine(int lineNumber) { 
  return new Condition<>() {
    @Override
    public boolean matches(String value) {
      return value.contains("- line " + lineNumber); 
    }
  };
}
Back to the big picture: make sure your assertions are not too sensitive, or your tests
may break for no good reason. 
Exercises
10.1
Jeanette hears that two tests are behaving strangely. Both of them pass when
executed in isolation, but they fail when executed together.
Which one of the following is not the cause of this problem?
A The tests depend on the same external resources.
B The execution order of the tests matters.
C Both tests are very slow.
D They do not perform a cleanup operation after execution.
10.2
Look at the following test code. What is the most likely test code smell that this
piece of code presents?
@Test
void test1() {
  // web service that communicates with the bank
  BankWebService bank = new BankWebService();
  User user = new User("d.bergkamp", "nl123");
  bank.authenticate(user);
  Thread.sleep(5000); // sleep for 5 seconds
  double balance = bank.getBalance();
  Thread.sleep(2000);
Listing 10.10
compilationErrorOnLine assertion
Makes the method
static, so we can
statically import it
in the test class
Checks whether value contains
the string we are looking for


