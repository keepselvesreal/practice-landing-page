# 21.1 Introduction (pp.247-248)

---
**Page 247**

Chapter 21
Test Readability
To design is to communicate clearly by whatever means you can control
or master.
—Milton Glaser
Introduction
Teams that adopt TDD usually see an early boost in productivity because the
tests let them add features with conﬁdence and catch errors immediately. For
some teams, the pace then slows down as the tests themselves become a mainte-
nance burden. For TDD to be sustainable, the tests must do more than verify the
behavior of the code; they must also express that behavior clearly—they must
be readable. This matters for the same reason that code readability matters: every
time the developers have to stop and puzzle through a test to ﬁgure out what it
means, they have less time left to spend on creating new features, and the team
velocity drops.
We take as much care about writing our test code as about production code,
but with differences in style since the two types of code serve different purposes.
Test code should describe what the production code does. That means that it
tends to be concrete about the values it uses as examples of what results to expect,
but abstract about how the code works. Production code, on the other hand,
tends to be abstract about the values it operates on but concrete about how it
gets the job done. Similarly, when writing production code, we have to consider
how we will compose our objects to make up a working system, and manage
their dependencies carefully. Test code, on the other hand, is at the end of the
dependency chain, so it’s more important for it to express the intention of its
target code than to plug into a web of other objects. We want our test code to
read like a declarative description of what is being tested.
In this chapter, we’ll describe some practices that we’ve found helpful to keep
our tests readable and expressive.
247


---
**Page 248**

Could Do Better1
We’ve seen many unit test suites that could be much more effective given a
little extra attention. They have too many “test smells” of the kind cataloged in
[Meszaros07], as well as in our own Chapters 20 and 24.When cleaning up tests,
or just trying to write new ones, the readability problems we watch out for are:
•
Test names that do not clearly describe the point of each test case and its
differences from the other test cases;
•
Single test cases that seem to be exercising multiple features;
•
Tests with different structure, so the reader cannot skim-read them to
understand their intention;
•
Tests with lots of code for setting up and handling exceptions, which buries
their essential logic; and,
•
Tests that use literal values (“magic numbers”) but are not clear about what,
if anything, is signiﬁcant about those values.
Test Names Describe Features
The name of the test should be the ﬁrst clue for a developer to understand what
is being tested and how the target object is supposed to behave.
Not every team we’ve worked with follows this principle. Some naive developers
use names that don’t mean anything at all:
public class TargetObjectTest {
  @Test public void test1() { […]
  @Test public void test2() { […]
  @Test public void test3() { […]
We don’t see many of these nowadays; the world has moved on. A common
approach is to name a test after the method it’s exercising:
public class TargetObjectTest {
  @Test public void isReady() { […]
  @Test public void choose() { […]
  @Test public void choose1() { […]
public class TargetObject  {
  public void isReady() { […]
  public void choose(Picker picker) { […]
perhaps with multiple tests for different paths through the same method.
1. This is (or was) a common phrase in UK school reports for children whose schoolwork
isn’t as good as it could be.
Chapter 21
Test Readability
248


