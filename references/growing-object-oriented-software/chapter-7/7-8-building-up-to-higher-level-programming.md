# 7.8 Building Up to Higher-Level Programming (pp.65-67)

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


---
**Page 66**

context.checking(new Expectations() {{
    oneOf(example).doSomething(with(any(String.class)));
}});
The Expectations object is a Builder [Gamma94] that constructs expectations.
It deﬁnes “sugar” methods that construct the assembly of expectations and
matchers and load it into the Mockery, as shown in Figure 7.2.
Figure 7.2
A syntax-layer constructs the interpreter
Most of the time, such a declarative layer emerges from continual “merciless”
refactoring. We start by writing code that directly composes objects and keep
factoring out duplication. We also add helper methods to push the syntax noise
out of the main body of the code and to add explanation. Taking care to notice
when an area of code is not clear, we add or move structure until it is; this is
very easy to do in a modern refactoring IDE. Eventually, we ﬁnd we have our
two-layer structure. Occasionally, we start from the declarative code we’d like
to have and work down to ﬁll in its implementation, as we do with the ﬁrst
end-to-end test in Chapter 10.
Our purpose, in the end, is to achieve more with less code. We aspire to raise
ourselves from programming in terms of control ﬂow and data manipulation, to
composing programs from smaller programs—where objects form the smallest
unit of behavior. None of this is new—it’s the same concept as programming
Unix by composing utilities with pipes [Kernighan76],4 or building up layers of
language in Lisp [Graham93]—but we still don’t see it in the ﬁeld as often as we
would like.
4. Kernighan and Plauger attribute the idea of pipes to Douglas McIlroy, who wrote a
memo in 1964 suggesting the metaphor of data passing through a segmented garden
hose. It’s currently available at http://plan9.bell-labs.com/who/dmr/mdmpipe.pdf.
Chapter 7
Achieving Object-Oriented Design
66


---
**Page 67**

And What about Classes?
One last point. Unusually for a book on object-oriented software, we haven’t
said much about classes and inheritance. It should be obvious by now that we’ve
been pushing the application domain into the gaps between the objects, the
communication protocols. We emphasize interfaces more than classes because
that’s what other objects see: an object’s type is deﬁned by the roles it plays.
We view classes for objects as an “implementation detail”—a way of imple-
menting types, not the types themselves. We discover object class hierarchies by
factoring out common behavior, but prefer to refactor to delegation if possible
since we ﬁnd that it makes our code more ﬂexible and easier to understand.5
Value types, on the other hand, are less likely to use delegation since they don’t
have peers.
There’s plenty of good advice on how to work with classes in, for example,
[Fowler99], [Kerievsky04], and [Evans03].
5. The design forces, of course, are different in languages that support multiple
inheritance well, such as Eiffel [Meyer91].
67
And What about Classes?


