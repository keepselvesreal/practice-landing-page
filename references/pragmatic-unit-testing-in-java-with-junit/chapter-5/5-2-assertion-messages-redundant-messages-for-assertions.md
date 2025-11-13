# 5.2 Assertion Messages: Redundant Messages for Assertions (pp.103-104)

---
**Page 103**

account.deposit(100);
assertEquals(150, account.getBalance());
}
You design the example for each test, and you know the expected outcome.
Encode it in the test with assertEquals.
Assertion Messages: Redundant Messages for Assertions
Most verifications are self-explanatory, at least in terms of the code bits they’re
trying to verify. Sometimes, it’s helpful to have a bit of “why” or additional context
to explain an assertion. “Just why does this test expect the total to be 42?”
Most JUnit assert forms support an optional final argument named message.
The message argument allows you to supply a nice verbose explanation of the
rationale behind the assertion:
utj3-junit/01/src/test/java/scratch/AnAccount.java
@Test
void balanceRepresentsTotalOfDeposits() {
account.deposit(50);
account.deposit(51);
var balance = account.getBalance();
assertEquals(101, balance, "account balance must be total of deposits");
}
The assertion message displays when the test fails:
account balance must be total of deposits ==> expected: <101> but was: <102>
If you prefer lots of explanatory comments, you might get some mileage out
of assertion messages. However, this is the better route:
• Test only one behavior at a time
• Make your test names more descriptive
In fact, if you demonstrate only one behavior per test, you’ll usually only need
a single assertion. The name of the test will then naturally describe the reason
for that one assertion. No assertion failure message is needed.
Well-written tests document themselves.
Elements like explanatory constants, helper methods, and intention-revealing
variable names go a long way toward making tests accessible and to the point.
The existence of comments and assertion messages in unit tests is a smell
report erratum  •  discuss
Assertion Messages: Redundant Messages for Assertions • 103


---
**Page 104**

that usually indicates stinky test design. In Chapter 10, Streamlining Your
Tests, on page 189, you’ll step through an example of test clean-up.
In well-written tests, the assertion message becomes redundant clutter, just
one more thing to have to wade through and maintain.
Improved test failure messages can provide a small benefit since figuring out
the meaning or implication of an assertion failure can be frustrating. Rather
than use assertion failure messages, however, take a look at AssertJ, which
provides fluent assertions that generate more detailed failure messages.
1
Assertion messages can also provide value when you employ parameterized
tests, which are a JUnit mechanism for running the same test with a bunch
of different data. See Executing Multiple Data Cases with Parameterized Tests,
on page 131.
Other Common JUnit Assertion Forms
While assertEquals and assertTrue would cover almost all the assertions you’ll
need to write, you’ll want to learn about the other forms that JUnit supports.
Choosing the best assertion for the job will keep your tests concise and clear.
In this section, you’ll be introduced to the majority of JUnit’s other assertion
forms, including assertFalse, assertNotEquals, assertSame, assertNotSame, assertNull, and
assertNotNull. You’ll also get an experience-based opinion on the value and best
uses for each variant.
assertFalse
Nobody doesn’t dislike double negatives (or triple negatives, so says my editor).
To help you say things “straight up” in your tests, JUnit provides some inverse
assertions. Here’s assertFalse—the opposite of assertTrue—in action:
utj3-junit/01/src/test/java/scratch/AnAccount.java
@Test
void doesNotHavePositiveBalanceWhenAccountCreated() {
assertFalse(account.hasPositiveBalance());
}
You can code the equivalent by using assertTrue if you’re in a contrary mood:
utj3-junit/01/src/test/java/scratch/AnAccount.java
@Test
void doesNotHavePositiveBalanceWhenAccountCreated() {
assertTrue(!account.hasPositiveBalance());
}
1.
https://assertj.github.io/doc/
Chapter 5. Examining Outcomes with Assertions • 104
report erratum  •  discuss


