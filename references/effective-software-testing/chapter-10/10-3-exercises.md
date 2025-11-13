# 10.3 Exercises (pp.272-275)

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


---
**Page 273**

273
Exercises
  Payment bill = new Payment();
  bill.setOrigin(user);
  bill.setValue(150.0);
  bill.setDescription("Energy bill");
  bill.setCode("YHG45LT");
  bank.pay(bill);
  Thread.sleep(5000);
  double newBalance = bank.getBalance();
  Thread.sleep(2000);
  // new balance should be previous balance - 150
  Assertions.assertEquals(newBalance, balance - 150);
}
A Flaky test
B Test code duplication
C Obscure test
D Long method
10.3
RepoDriller is a project that extracts information from Git repositories. Its inte-
gration tests use a lot of real Git repositories (that are created solely for the
test), each with a different characteristic: one repository contains a merge com-
mit, another contains a revert operation, and so on.
Its tests look like this:
@Test
public void test01() {
  // arrange: specific repo
  String path = "test-repos/git-4";
  // act
  TestVisitor visitor = new TestVisitor();
  new RepositoryMining()
    .in(GitRepository.singleProject(path))
    .through(Commits.all())
    .process(visitor)
    .mine();
  // assert
  Assert.assertEquals(3, visitor.getVisitedHashes().size());
  Assert.assertTrue(visitor.getVisitedHashes().get(2).equals("b8c2"));
  Assert.assertTrue(visitor.getVisitedHashes().get(1).equals("375d"));
  Assert.assertTrue(visitor.getVisitedHashes().get(0).equals("a1b6"));
}
Which test smell might this piece of code suffer from?
A Condition logic in the test
B General fixture


---
**Page 274**

274
CHAPTER 10
Test code quality
C Flaky test
D Mystery guest
10.4
In the following code, we show an actual test from Apache Commons Lang, a
very popular open source Java library. This test focuses on the static random()
method, which is responsible for generating random characters. An interesting
detail in this test is the comment Will fail randomly about 1 in 1000 times.
/**
 * Test homogeneity of random strings generated --
 * i.e., test that characters show up with expected frequencies
 * in generated strings.  Will fail randomly about 1 in 1000 times.
 * Repeated failures indicate a problem.
 */
@Test
public void testRandomStringUtilsHomog() {
  final String set = "abc";
  final char[] chars = set.toCharArray();
  String gen = "";
  final int[] counts = {0, 0, 0};
  final int[] expected = {200, 200, 200};
  for (int i = 0; i < 100; i++) {
    gen = RandomStringUtils.random(6,chars);
    for (int j = 0; j < 6; j++) {
      switch (gen.charAt(j)) {
        case 'a': {counts[0]++; break;}
        case 'b': {counts[1]++; break;}
        case 'c': {counts[2]++; break;}
        default: {fail("generated character not in set");}
      }
    }
  }
  // Perform chi-square test with df = 3-1 = 2, testing at .001 level
  assertTrue("test homogeneity -- will fail about 1 in 1000 times",
    chiSquare(expected,counts) < 13.82);
}
Which one of the following statements is incorrect about the test?
A The test is flaky because of the randomness that exists in generating
characters.
B The test checks for invalidly generated characters and also checks that
characters are picked in the same proportion.
C The method being static has nothing to do with its flakiness.
D To avoid flakiness, a developer should have mocked the random() function.
10.5
A developer observes that two tests pass when executed in isolation but fail
when executed together.
Which of the following is the least likely fix for this problem (also known as
Test Run War)?


---
**Page 275**

275
Summary
A Make each test runner a specific sandbox.
B Use fresh fixtures in every test.
C Remove and isolate duplicated test code.
D Clean up the state during teardown.
Summary
Writing good test code is as challenging as writing good production code. We
should ensure that our test code is easy to maintain and evolve.
We desire many things in a test method. Tests should be fast, cohesive, and
repeatable; they should fail for a reason and contain strong assertions; they
should be easy to read, write, and evolve; and they should be loosely coupled
with the production code.
Many things can hinder the maintainability of test methods: too much duplica-
tion, too many bad assertions, bad handling of complex (external) resources, too
many general fixtures, too many sensitive assertions, and flakiness. You should
avoid these.


