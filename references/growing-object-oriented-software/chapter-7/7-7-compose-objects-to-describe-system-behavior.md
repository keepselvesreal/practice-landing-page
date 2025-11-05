# 7.7 Compose Objects to Describe System Behavior (pp.64-65)

---
**Page 64**

malleable because more components will be “plug-compatible,” so we can work
at a higher level of abstraction. For the developer, there’s a secondary advantage
that there will be fewer concepts that cost time to understand.
Alternatively, if similar interfaces turn out to represent different concepts, we
can make a point of making them distinct, so that the compiler can ensure that
we only combine objects correctly. A decision to separate similar-looking inter-
faces is a good time to reconsider their naming. It’s likely that there’s a more
appropriate name for at least one of them.
Finally, another time to consider refactoring interfaces is when we start imple-
menting them. For example, if we ﬁnd that the structure of an implementing class
is unclear, perhaps it has too many responsibilities which might be a hint that
the interface is unfocused too and should be split up.
Compose Objects to Describe System Behavior
TDD at the unit level guides us to decompose our system into value types and
loosely coupled computational objects. The tests give us a good understanding
of how each object behaves and how it can be combined with others. We then
use lower-level objects as the building blocks of more capable objects; this is the
web of objects we described in Chapter 2.
In jMock, for example, we assemble a description of the expected calls for a
test in a context object called a Mockery. During a test run, the Mockery will pass
calls made to any of its mocked objects to its Expectations, each of which will
attempt to match the call. If an Expectation matches, that part of the test suc-
ceeds. If none matches, then each Expectation reports its disagreement and the
test fails. At runtime, the assembled objects look like Figure 7.1:
Figure 7.1
jMock Expectations are assembled from many objects
The advantage of this approach is that we end up with a ﬂexible application
structure built from relatively little code. It’s particularly suitable where the code
has to support many related scenarios. For each scenario, we provide a different
Chapter 7
Achieving Object-Oriented Design
64


---
**Page 65**

assembly of components to build, in effect, a subsystem to plug into the rest of
the application. Such designs are also easy to extend—just write a new plug-
compatible component and add it in; you’ll see us write several new Hamcrest
matchers in Part III.
For example, to have jMock check that a method example.doSomething() is
called exactly once with an argument of type String, we set up our test context
like this:
InvocationExpectation expectation = new InvocationExpectation();
expectation.setParametersMatcher(
  new AllParametersMatcher(Arrays.asList(new IsInstanceOf(String.class)));
expectation.setCardinality(new Cardinality(1, 1));
expectation.setMethodMatcher(new MethodNameMatcher("doSomething"));
expectation.setObjectMatcher(new IsSame<Example>(example));
context.addExpectation(expectation);
Building Up to Higher-Level Programming
You have probably spotted a difﬁculty with the code fragment above: it doesn’t
explain very well what the expectation is testing. Conceptually, assembling a
web of objects is straightforward. Unfortunately, the mainstream languages we
usually work with bury the information we care about (objects and their relation-
ships) in a morass of keywords, setters, punctuation, and the like. Just assigning
and linking objects, as in this example, doesn’t help us understand the behavior
of the system we’re assembling—it doesn’t express our intent.2
Our response is to organize the code into two layers: an implementation layer
which is the graph of objects, its behavior is the combined result of how its objects
respond to events; and, a declarative layer which builds up the objects in the
implementation layer, using small “sugar” methods and syntax to describe
the purpose of each fragment. The declarative layer describes what the code will
do, while the implementation layer describes how the code does it. The declarative
layer is, in effect, a small domain-speciﬁc language embedded (in this case)
in Java.3
The different purposes of the two layers mean that we use a different coding
style for each. For the implementation layer we stick to the conventional object-
oriented style guidelines we described in the previous chapter. We’re more ﬂexible
for the declarative layer—we might even use “train wreck” chaining of method
calls or static methods to help get the point across.
A good example is jMock itself. We can rewrite the example from the previous
section as:
2. Nor does the common alternative of moving the object construction into a separate
XML ﬁle.
3. This became clear to us when working on jMock. We wrote up our experiences in
[Freeman06].
65
Building Up to Higher-Level Programming


