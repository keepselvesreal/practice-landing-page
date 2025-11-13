# 4.1.4 Aim at the end result instead of implementation details (pp.74-76)

---
**Page 74**

74
CHAPTER 4
The four pillars of a good unit test
Therefore, tests that couple to the SUT’s implementation details are not resistant to refactoring.
Such tests exhibit all the shortcomings I described previously:
They don’t provide an early warning in the event of regressions—you simply
ignore those warnings due to little relevance.
They hinder your ability and willingness to refactor. It’s no wonder—who would
like to refactor, knowing that the tests can’t tell which way is up when it comes
to finding bugs?
The next listing shows the most egregious example of brittleness in tests that I’ve ever
encountered, in which the test reads the source code of the MessageRenderer class
and compares it to the “correct” implementation.
[Fact]
public void MessageRenderer_is_implemented_correctly()
{
string sourceCode = File.ReadAllText(@"[path]\MessageRenderer.cs");
Assert.Equal(@"
public class MessageRenderer : IRenderer
{
public IReadOnlyList<<IRenderer> SubRenderers { get; }
public MessageRenderer()
{
SubRenderers = new List<<IRenderer>
{
new HeaderRenderer(),
new BodyRenderer(),
new FooterRenderer()
};
}
public string Render(Message message) { /* ... */ }
}", sourceCode);
}
Of course, this test is just plain ridiculous; it will fail should you modify even the slight-
est detail in the MessageRenderer class. At the same time, it’s not that different from
the test I brought up earlier. Both insist on a particular implementation without tak-
ing into consideration the SUT’s observable behavior. And both will turn red each
time you change that implementation. Admittedly, though, the test in listing 4.3 will
break more often than the one in listing 4.2. 
4.1.4
Aim at the end result instead of implementation details
As I mentioned earlier, the only way to avoid brittleness in tests and increase their resis-
tance to refactoring is to decouple them from the SUT’s implementation details—keep
as much distance as possible between the test and the code’s inner workings, and
Listing 4.3
Verifying the source code of the MessageRenderer class


---
**Page 75**

75
Diving into the four pillars of a good unit test
instead aim at verifying the end result. Let’s do that: let’s refactor the test from list-
ing 4.2 into something much less brittle.
 To start off, you need to ask yourself the following question: What is the final out-
come you get from MessageRenderer? Well, it’s the HTML representation of a mes-
sage. And it’s the only thing that makes sense to check, since it’s the only observable
result you get out of the class. As long as this HTML representation stays the same,
there’s no need to worry about exactly how it’s generated. Such implementation
details are irrelevant. The following code is the new version of the test.
[Fact]
public void Rendering_a_message()
{
var sut = new MessageRenderer();
var message = new Message
{
Header = "h",
Body = "b",
Footer = "f"
};
string html = sut.Render(message);
Assert.Equal("<h1>h</h1><b>b</b><i>f</i>", html);
}
This test treats MessageRenderer as a black box and is only interested in its observable
behavior. As a result, the test is much more resistant to refactoring—it doesn’t care
what changes you make to the SUT as long as the HTML output remains the same
(figure 4.2).
 Notice the profound improvement in this test over the original version. It aligns
itself with the business needs by verifying the only outcome meaningful to end users—
Listing 4.4
Verifying the outcome that MessageRenderer produces
Step 1
Step 2
Step 3
Client
System under test
Good test: “Is
the end result
correct?”
Step 1
Step 2
Step 3
Client
System under test
Bad test: “Are
these steps
correct?”
Figure 4.2
The test on the left couples to the SUT’s observable behavior as opposed to implementation 
details. Such a test is resistant to refactoring—it will trigger few, if any, false positives.


---
**Page 76**

76
CHAPTER 4
The four pillars of a good unit test
how a message is displayed in the browser. Failures of such a test are always on point:
they communicate a change in the application behavior that can affect the customer
and thus should be brought to the developer’s attention. This test will produce few, if
any, false positives.
 Why few and not none at all? Because there could still be changes in Message-
Renderer that would break the test. For example, you could introduce a new parame-
ter in the Render() method, causing a compilation error. And technically, such an
error counts as a false positive, too. After all, the test isn’t failing because of a change
in the application’s behavior.
 But this kind of false positive is easy to fix. Just follow the compiler and add a new
parameter to all tests that invoke the Render() method. The worse false positives are
those that don’t lead to compilation errors. Such false positives are the hardest to deal
with—they seem as though they point to a legitimate bug and require much more
time to investigate.
4.2
The intrinsic connection between the first 
two attributes
As I mentioned earlier, there’s an intrinsic connection between the first two pillars of
a good unit test—protection against regressions and resistance to refactoring. They both con-
tribute to the accuracy of the test suite, though from opposite perspectives. These two
attributes also tend to influence the project differently over time: while it’s important
to have good protection against regressions very soon after the project’s initiation, the
need for resistance to refactoring is not immediate.
 In this section, I talk about
Maximizing test accuracy
The importance of false positives and false negatives
4.2.1
Maximizing test accuracy
Let’s step back for a second and look at the broader picture with regard to test results.
When it comes to code correctness and test results, there are four possible outcomes,
as shown in figure 4.3. The test can either pass or fail (the rows of the table). And the
functionality itself can be either correct or broken (the table’s columns).
 The situation when the test passes and the underlying functionality works as
intended is a correct inference: the test correctly inferred the state of the system (there
are no bugs in it). Another term for this combination of working functionality and a
passing test is true negative.
 Similarly, when the functionality is broken and the test fails, it’s also a correct infer-
ence. That’s because you expect to see the test fail when the functionality is not work-
ing properly. That’s the whole point of unit testing. The corresponding term for this
situation is true positive.
 But when the test doesn’t catch an error, that’s a problem. This is the upper-right
quadrant, a false negative. And this is what the first attribute of a good test—protection


