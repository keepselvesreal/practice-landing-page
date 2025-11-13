# 6.2.4 Comparing the styles: The results (pp.127-128)

---
**Page 127**

127
Comparing the three styles of unit testing
[Fact]
public void Adding_a_comment_to_an_article()
{
var sut = new Article();
var comment = new Comment(
"Comment text",
"John Doe",
new DateTime(2019, 4, 1));
sut.AddComment(comment.Text, comment.Author, comment.DateCreated);
sut.Comments.Should().BeEquivalentTo(comment);
}
This test uses the fact that comments can be compared as whole values, without the
need to assert individual properties in them. It also uses the BeEquivalentTo method
from Fluent Assertions, which can compare entire collections, thereby removing the
need to check the collection size.
 This is a powerful technique, but it works only when the class is inherently a value
and can be converted into a value object. Otherwise, it leads to code pollution (pollut-
ing production code base with code whose sole purpose is to enable or, as in this case,
simplify unit testing). We’ll discuss code pollution along with other unit testing anti-
patterns in chapter 11.
 As you can see, these two techniques—using helper methods and converting
classes into value objects—are applicable only occasionally. And even when these tech-
niques are applicable, state-based tests still take up more space than output-based tests
and thus remain less maintainable. 
MAINTAINABILITY OF COMMUNICATION-BASED TESTS
Communication-based tests score worse than output-based and state-based tests on
the maintainability metric. Communication-based testing requires setting up test dou-
bles and interaction assertions, and that takes up a lot of space. Tests become even
larger and less maintainable when you have mock chains (mocks or stubs returning
other mocks, which also return mocks, and so on, several layers deep). 
6.2.4
Comparing the styles: The results
Let’s now compare the styles of unit testing using the attributes of a good unit test.
Table 6.1 sums up the comparison results. As discussed in section 6.2.1, all three styles
score equally with the metrics of protection against regressions and feedback speed;
hence, I’m omitting these metrics from the comparison.
 Output-based testing shows the best results. This style produces tests that rarely
couple to implementation details and thus don’t require much due diligence to main-
tain proper resistance to refactoring. Such tests are also the most maintainable due to
their conciseness and lack of out-of-process dependencies.
Listing 6.6
Comment compared by value


---
**Page 128**

128
CHAPTER 6
Styles of unit testing
State-based and communication-based tests are worse on both metrics. These are
more likely to couple to a leaking implementation detail, and they also incur higher
maintenance costs due to being larger in size.
 Always prefer output-based testing over everything else. Unfortunately, it’s easier
said than done. This style of unit testing is only applicable to code that is written in a
functional way, which is rarely the case for most object-oriented programming lan-
guages. Still, there are techniques you can use to transition more of your tests toward
the output-based style.
 The rest of this chapter shows how to transition from state-based and collaboration-
based testing to output-based testing. The transition requires you to make your code
more purely functional, which, in turn, enables the use of output-based tests instead
of state- or communication-based ones. 
6.3
Understanding functional architecture
Some groundwork is needed before I can show how to make the transition. In this sec-
tion, you’ll see what functional programming and functional architecture are and
how the latter relates to the hexagonal architecture. Section 6.4 illustrates the transi-
tion using an example.
 Note that this isn’t a deep dive into the topic of functional programming, but
rather an explanation of the basic principles behind it. These basic principles should
be enough to understand the connection between functional programming and out-
put-based testing. For a deeper look at functional programming, see Scott Wlaschin’s
website and books at https://fsharpforfunandprofit.com/books.
6.3.1
What is functional programming?
As I mentioned in section 6.1.1, the output-based unit testing style is also known as
functional. That’s because it requires the underlying production code to be written in
a purely functional way, using functional programming. So, what is functional pro-
gramming?
 Functional programming is programming with mathematical functions. A mathemati-
cal function (also known as pure function) is a function (or method) that doesn’t have
any hidden inputs or outputs. All inputs and outputs of a mathematical function must
be explicitly expressed in its method signature, which consists of the method’s name,
arguments, and return type. A mathematical function produces the same output for a
given input regardless of how many times it is called.
Table 6.1
The three styles of unit testing: The comparisons
Output-based
State-based
Communication-based
Due diligence to maintain 
resistance to refactoring
Low
Medium
Medium
Maintainability costs
Low
Medium
High


