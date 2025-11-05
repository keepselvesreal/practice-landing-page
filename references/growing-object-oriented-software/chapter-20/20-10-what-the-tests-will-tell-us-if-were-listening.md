# 20.10 What the Tests Will Tell Us (If We're Listening) (pp.244-247)

---
**Page 244**

Special Bonus Prize
We always have problems coming up with good examples. There’s actually a
better improvement to this code, which is to notice that we’ve pulled out a chain
of objects to get to the case object, exposing dependencies that aren’t relevant
here. Instead, we should have told the nearest object to do the work for us,
like this:
public void adjudicateIfReady(ThirdParty thirdParty, Issue issue) {
  if (firstParty.isReady()) {
organization.adjudicateBetween(firstParty, thirdParty, issue);
  } else {
    thirdParty.adjourn();
  }
}
or, possibly,
public void adjudicateIfReady(ThirdParty thirdParty, Issue issue) {
  if (firstParty.isReady()) {
    thirdParty.startAdjudication(organization, firstParty, issue);
  } else{
    thirdParty.adjourn();
  }
}
which looks more balanced. If you spotted this, we award you a Moment of
Smugness™ to be exercised at your convenience.
What the Tests Will Tell Us (If We’re Listening)
We’ve found these beneﬁts from learning to listen to test smells:
Keep knowledge local
Some of the test smells we’ve identiﬁed, such as needing “magic” to create
mocks, are to do with knowledge leaking between components. If we can
keep knowledge local to an object (either internal or passed in), then its im-
plementation is independent of its context; we can safely move it wherever
we like. Do this consistently and your application, built out of pluggable
components, will be easy to change.
If it’s explicit, we can name it
One reason why we don’t like mocking concrete classes is that we like to
have names for the relationships between objects as well the objects them-
selves. As the legends say, if we have something’s true name, we can control
it. If we can see it, we have a better chance of ﬁnding its other uses and so
reducing duplication.
Chapter 20
Listening to the Tests
244


---
**Page 245**

More names mean more domain information
We ﬁnd that when we emphasize how objects communicate, rather than
what they are, we end up with types and roles deﬁned more in terms of the
domain than of the implementation. This might be because we have a greater
number of smaller abstractions, which gets us further away from the under-
lying language. Somehow we seem to get more domain vocabulary into
the code.
Pass behavior rather than data
We ﬁnd that by applying “Tell, Don’t Ask” consistently, we end up with a
coding style where we tend to pass behavior (in the form of callbacks) into
the system instead of pulling values up through the stack. For example, in
Chapter 17, we introduced a SniperCollector that responds when told about
a new Sniper. Passing this listener into the Sniper creation code gives us
better information hiding than if we’d exposed a collection to be added
to. More precise interfaces give us better information-hiding and clearer
abstractions.
We care about keeping the tests and code clean as we go, because it helps to
ensure that we understand our domain and reduces the risk of being unable
to cope when a new requirement triggers changes to the design. It’s much easier to
keep a codebase clean than to recover from a mess. Once a codebase starts
to “rot,” the developers will be under pressure to botch the code to get the next
job done. It doesn’t take many such episodes to dissipate a team’s good intentions.
We once had a posting to the jMock user list that included this comment:
I was involved in a project recently where jMock was used quite heavily. Looking
back, here’s what I found:
1.
The unit tests were at times unreadable (no idea what they were doing).
2.
Some tests classes would reach 500 lines in addition to inheriting an abstract
class which also would have up to 500 lines.
3.
Refactoring would lead to massive changes in test code.
A unit test shouldn’t be 1000 lines long! It should focus on at most a few
classes and should not need to create a large ﬁxture or perform lots of preparation
just to get the objects into a state where the target feature can be exercised. Such
tests are hard to understand—there’s just so much to remember when reading
them. And, of course, they’re brittle, all the objects in play are too tightly coupled
and too difﬁcult to set to the state the test requires.
Test-driven development can be unforgiving. Poor quality tests can slow devel-
opment to a crawl, and poor internal quality of the system being tested will result
in poor quality tests. By being alert to the internal quality feedback we get from
245
What the Tests Will Tell Us (If We’re Listening)


---
**Page 246**

writing tests, we can nip this problem in the bud, long before our unit tests ap-
proach 1000 lines of code, and end up with tests we can live with. Conversely,
making an effort to write tests that are readable and ﬂexible gives us more feed-
back about the internal quality of the code we are testing. We end up with tests
that help, rather than hinder, continued development.
Chapter 20
Listening to the Tests
246


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


