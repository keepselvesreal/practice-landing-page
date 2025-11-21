# 4.1.3 What causes false positives? (pp.71-74)

---
**Page 71**

71
Diving into the four pillars of a good unit test
This story is typical of most projects with brittle tests. First, developers take test failures
at face value and deal with them accordingly. After a while, people get tired of tests
crying “wolf” all the time and start to ignore them more and more. Eventually, there
comes a moment when a bunch of real bugs are released to production because devel-
opers ignored the failures along with all the false positives.
 You don’t want to react to such a situation by ceasing all refactorings, though. The
correct response is to re-evaluate the test suite and start reducing its brittleness. I
cover this topic in chapter 7. 
4.1.3
What causes false positives?
So, what causes false positives? And how can you avoid them?
 The number of false positives a test produces is directly related to the way the test
is structured. The more the test is coupled to the implementation details of the system
under test (SUT), the more false alarms it generates. The only way to reduce the
chance of getting a false positive is to decouple the test from those implementation
details. You need to make sure the test verifies the end result the SUT delivers: its
observable behavior, not the steps it takes to do that. Tests should approach SUT veri-
fication from the end user’s point of view and check only the outcome meaningful to
that end user. Everything else must be disregarded (more on this topic in chapter 5).
 The best way to structure a test is to make it tell a story about the problem domain.
Should such a test fail, that failure would mean there’s a disconnect between the story
and the actual application behavior. It’s the only type of test failure that benefits you—
such failures are always on point and help you quickly understand what went wrong.
All other failures are just noise that steer your attention away from things that matter.
 Take a look at the following example. In it, the MessageRenderer class generates
an HTML representation of a message containing a header, a body, and a footer.
public class Message
{
public string Header { get; set; }
public string Body { get; set; }
public string Footer { get; set; }
}
At first, the developers tried to deal with the test failures. However, since the vast
majority of them were false alarms, the situation got to the point where the develop-
ers ignored such failures and disabled the failing tests. The prevailing attitude was,
“If it’s because of that old chunk of code, just disable the test; we’ll look at it later.”
Everything worked fine for a while—until a major bug slipped into production. One of
the tests correctly identified the bug, but no one listened; the test was disabled along
with all the others. After that accident, the developers stopped touching the old code
entirely.
Listing 4.1
Generating an HTML representation of a message


---
**Page 72**

72
CHAPTER 4
The four pillars of a good unit test
public interface IRenderer
{
string Render(Message message);
}
public class MessageRenderer : IRenderer
{
public IReadOnlyList<IRenderer> SubRenderers { get; }
public MessageRenderer()
{
SubRenderers = new List<IRenderer>
{
new HeaderRenderer(),
new BodyRenderer(),
new FooterRenderer()
};
}
public string Render(Message message)
{
return SubRenderers
.Select(x => x.Render(message))
.Aggregate("", (str1, str2) => str1 + str2);
}
}
The MessageRenderer class contains several sub-renderers to which it delegates the
actual work on parts of the message. It then combines the result into an HTML docu-
ment. The sub-renderers orchestrate the raw text with HTML tags. For example:
public class BodyRenderer : IRenderer
{
public string Render(Message message)
{
return $"<b>{message.Body}</b>";
}
}
How can MessageRenderer be tested? One possible approach is to analyze the algo-
rithm this class follows.
[Fact]
public void MessageRenderer_uses_correct_sub_renderers()
{
var sut = new MessageRenderer();
IReadOnlyList<IRenderer> renderers = sut.SubRenderers;
Listing 4.2
Verifying that MessageRenderer has the correct structure


---
**Page 73**

73
Diving into the four pillars of a good unit test
Assert.Equal(3, renderers.Count);
Assert.IsAssignableFrom<HeaderRenderer>(renderers[0]);
Assert.IsAssignableFrom<BodyRenderer>(renderers[1]);
Assert.IsAssignableFrom<FooterRenderer>(renderers[2]);
}
This test checks to see if the sub-renderers are all of the expected types and appear in
the correct order, which presumes that the way MessageRenderer processes messages
must also be correct. The test might look good at first, but does it really verify Message-
Renderer’s observable behavior? What if you rearrange the sub-renderers, or replace
one of them with a new one? Will that lead to a bug?
 Not necessarily. You could change a sub-renderer’s composition in such a way that
the resulting HTML document remains the same. For example, you could replace
BodyRenderer with a BoldRenderer, which does the same job as BodyRenderer. Or you
could get rid of all the sub-renderers and implement the rendering directly in Message-
Renderer.
 Still, the test will turn red if you do any of that, even though the end result won’t
change. That’s because the test couples to the SUT’s implementation details and not
the outcome the SUT produces. This test inspects the algorithm and expects to see
one particular implementation, without any consideration for equally applicable alter-
native implementations (see figure 4.1).
Any substantial refactoring of the MessageRenderer class would lead to a test failure.
Mind you, the process of refactoring is changing the implementation without affecting
the application’s observable behavior. And it’s precisely because the test is concerned
with the implementation details that it turns red every time you change those details.
Step 1
Step 2
Step 3
Client
System under test
Test: “Are
these steps
correct?”
Figure 4.1
A test that couples to the SUT’s algorithm. Such a test expects to see one particular 
implementation (the specific steps the SUT must take to deliver the result) and therefore is 
brittle. Any refactoring of the SUT’s implementation would lead to a test failure.


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


