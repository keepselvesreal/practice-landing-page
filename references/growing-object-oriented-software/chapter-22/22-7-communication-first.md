# 22.7 Communication First (pp.264-267)

---
**Page 264**

Then, Raise the Game
The test code is looking better, but it still reads like a script. We can change its
emphasis to what behavior is expected, rather than how the test is implemented,
by rewording some of the names:
@Test public void reportsTotalSalesOfOrderedProducts() {
havingReceived(anOrder()
      .withLine("Deerstalker Hat", 1)
      .withLine("Tweed Cape", 1));
havingReceived(anOrder()
      .withLine("Deerstalker Hat", 1));
  TotalSalesReport report = gui.openSalesReport();
  report.displaysTotalSalesFor("Deerstalker Hat", equalTo(2));
  report.displaysTotalSalesFor("Tweed Cape", equalTo(1));
}
@Test public void takesAmendmentsIntoAccountWhenCalculatingTotalSales() {
  Customer theCustomer = aCustomer().build();
havingReceived(anOrder().from(theCustomer)
    .withLine("Deerstalker Hat", 1)
    .withLine("Tweed Cape", 1));
havingReceived(anOrderAmendment().from(theCustomer)
    .withLine("Deerstalker Hat", 2));
  TotalSalesReport report = user.openSalesReport();
  report.containsTotalSalesFor("Deerstalker Hat", equalTo(2));
  report.containsTotalSalesFor("Tweed Cape", equalTo(1));
}
We started with a test that looked procedural, extracted some of its behavior
into builder objects, and ended up with a declarative description of what the
feature does. We’re nudging the test code towards the sort of language we could
use when discussing the feature with someone else, even someone non-technical;
we push everything else into supporting code.
Communication First
We use test data builders to reduce duplication and make the test code more ex-
pressive. It’s another technique that reﬂects our obsession with the language of
code, driven by the principle that code is there to be read. Combined with factory
methods and test scaffolding, test data builders help us write more literate,
declarative tests that describe the intention of a feature, not just a sequence of
steps to drive it.
Using these techniques, we can even use higher-level tests to communicate di-
rectly with non-technical stakeholders, such as business analysts. If they’re willing
Chapter 22
Constructing Complex Test Data
264


---
**Page 265**

to ignore the obscure punctuation, we can use the tests to help us narrow down
exactly what a feature should do, and why.
There are other tools that are designed to foster collaboration across the
technical and non-technical members in a team, such as FIT [Mugridge05]. We’ve
found, as have others such as the LiFT team [LIFT], that we can achieve much
of this while staying within our development toolset—and, of course, we can
write better tests for ourselves.
265
Communication First


---
**Page 266**

This page intentionally left blank 


---
**Page 267**

Chapter 23
Test Diagnostics
Mistakes are the portals of discovery.
—James Joyce
Design to Fail
The point of a test is not to pass but to fail. We want the production code to
pass its tests, but we also want the tests to detect and report any errors that
do exist. A “failing” test has actually succeeded at the job it was designed to do.
Even unexpected test failures, in an area unrelated to where we are working, can
be valuable because they reveal implicit relationships in the code that we hadn’t
noticed.
One situation we want to avoid, however, is when we can’t diagnose a test
failure that has happened. The last thing we should have to do is crack open the
debugger and step through the tested code to ﬁnd the point of disagreement. At
a minimum, it suggests that our tests don’t yet express our requirements clearly
enough. In the worst case, we can ﬁnd ourselves in “debug hell,” with deadlines
to meet but no idea of how long a ﬁx will take. At this point, the temptation will
be high to just delete the test—and lose our safety net.
Stay Close to Home
Synchronize frequently with the source code repository—up to every few minutes—
so that if a test fails unexpectedly it won’t cost much to revert your recent changes
and try another approach.
The other implication of this tip is not to be too inhibited about dropping code and
trying again. Sometimes it’s quicker to roll back and restart with a clear head than
to keep digging.
We’ve learned the hard way to make tests fail informatively. If a failing test
clearly explains what has failed and why, we can quickly diagnose and correct
the code. Then, we can get on with the next task.
Chapter 21 addressed the static readability of tests. This chapter describes
some practices that we ﬁnd helpful to make sure the tests give us the information
we need at runtime.
267


