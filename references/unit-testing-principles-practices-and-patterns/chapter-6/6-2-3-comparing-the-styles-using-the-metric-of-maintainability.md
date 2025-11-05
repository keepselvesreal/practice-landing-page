# 6.2.3 Comparing the styles using the metric of maintainability (pp.125-127)

---
**Page 125**

125
Comparing the three styles of unit testing
doubles end up being brittle. This is always the case for interactions with stubs—you
should never check such interactions. Mocks are fine only when they verify interac-
tions that cross the application boundary and only when the side effects of those
interactions are visible to the external world. As you can see, using communication-
based testing requires extra prudence in order to maintain proper resistance to
refactoring.
 But just like shallowness, brittleness is not a definitive feature of the communication-
based style, either. You can reduce the number of false positives to a minimum by
maintaining proper encapsulation and coupling tests to observable behavior only.
Admittedly, though, the amount of due diligence varies depending on the style of
unit testing. 
6.2.3
Comparing the styles using the metric of maintainability
Finally, the maintainability metric is highly correlated with the styles of unit testing;
but, unlike with resistance to refactoring, there’s not much you can do to mitigate
that. Maintainability evaluates the unit tests’ maintenance costs and is defined by the
following two characteristics:
How hard it is to understand the test, which is a function of the test’s size
How hard it is to run the test, which is a function of how many out-of-process
dependencies the test works with directly
Larger tests are less maintainable because they are harder to grasp or change when
needed. Similarly, a test that directly works with one or several out-of-process depen-
dencies (such as the database) is less maintainable because you need to spend time
keeping those out-of-process dependencies operational: rebooting the database
server, resolving network connectivity issues, and so on.
MAINTAINABILITY OF OUTPUT-BASED TESTS
Compared with the other two types of testing, output-based testing is the most main-
tainable. The resulting tests are almost always short and concise and thus are easier to
maintain. This benefit of the output-based style stems from the fact that this style boils
down to only two things: supplying an input to a method and verifying its output,
which you can often do with just a couple lines of code.
 Because the underlying code in output-based testing must not change the global
or internal state, these tests don’t deal with out-of-process dependencies. Hence,
output-based tests are best in terms of both maintainability characteristics. 
MAINTAINABILITY OF STATE-BASED TESTS
State-based tests are normally less maintainable than output-based ones. This is
because state verification often takes up more space than output verification. Here’s
another example of state-based testing.
 
 


---
**Page 126**

126
CHAPTER 6
Styles of unit testing
[Fact]
public void Adding_a_comment_to_an_article()
{
var sut = new Article();
var text = "Comment text";
var author = "John Doe";
var now = new DateTime(2019, 4, 1);
sut.AddComment(text, author, now);
Assert.Equal(1, sut.Comments.Count);
    
Assert.Equal(text, sut.Comments[0].Text);
    
Assert.Equal(author, sut.Comments[0].Author);     
Assert.Equal(now, sut.Comments[0].DateCreated);   
}
This test adds a comment to an article and then checks to see if the comment
appears in the article’s list of comments. Although this test is simplified and con-
tains just a single comment, its assertion part already spans four lines. State-based
tests often need to verify much more data than that and, therefore, can grow in size
significantly.
 You can mitigate this issue by introducing helper methods that hide most of the
code and thus shorten the test (see listing 6.5), but these methods require significant
effort to write and maintain. This effort is justified only when those methods are going
to be reused across multiple tests, which is rarely the case. I’ll explain more about
helper methods in part 3 of this book.
[Fact]
public void Adding_a_comment_to_an_article()
{
var sut = new Article();
var text = "Comment text";
var author = "John Doe";
var now = new DateTime(2019, 4, 1);
sut.AddComment(text, author, now);
sut.ShouldContainNumberOfComments(1)    
.WithComment(text, author, now);    
}
Another way to shorten a state-based test is to define equality members in the class
that is being asserted. In listing 6.6, that’s the Comment class. You could turn it into a
value object (a class whose instances are compared by value and not by reference), as
shown next; this would also simplify the test, especially if you combined it with an
assertion library like Fluent Assertions.
Listing 6.4
State verification that takes up a lot of space
Listing 6.5
Using helper methods in assertions
Verifies the state 
of the article
Helper 
methods


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


