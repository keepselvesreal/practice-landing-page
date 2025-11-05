# 6.0 Introduction [auto-generated] (pp.119-120)

---
**Page 119**

119
Styles of unit testing
Chapter 4 introduced the four attributes of a good unit test: protection against
regressions, resistance to refactoring, fast feedback, and maintainability. These attri-
butes form a frame of reference that you can use to analyze specific tests and unit
testing approaches. We analyzed one such approach in chapter 5: the use of mocks.
 In this chapter, I apply the same frame of reference to the topic of unit testing
styles. There are three such styles: output-based, state-based, and communication-
based testing. Among the three, the output-based style produces tests of the highest
quality, state-based testing is the second-best choice, and communication-based
testing should be used only occasionally.
 Unfortunately, you can’t use the output-based testing style everywhere. It’s only
applicable to code written in a purely functional way. But don’t worry; there are
techniques that can help you transform more of your tests into the output-based
style. For that, you’ll need to use functional programming principles to restructure
the underlying code toward a functional architecture.
This chapter covers
Comparing styles of unit testing
The relationship between functional and 
hexagonal architectures
Transitioning to output-based testing


---
**Page 120**

120
CHAPTER 6
Styles of unit testing
 Note that this chapter doesn’t provide a deep dive into the topic of functional pro-
gramming. Still, by the end of this chapter, I hope you’ll have an intuitive understand-
ing of how functional programming relates to output-based testing. You’ll also learn
how to write more of your tests using the output-based style, as well as the limitations
of functional programming and functional architecture.
6.1
The three styles of unit testing
As I mentioned in the chapter introduction, there are three styles of unit testing:
Output-based testing 
State-based testing 
Communication-based testing
You can employ one, two, or even all three styles together in a single test. This sec-
tion lays the foundation for the whole chapter by defining (with examples) those
three styles of unit testing. You’ll see how they score against each other in the sec-
tion after that.
6.1.1
Defining the output-based style
The first style of unit testing is the output-based style, where you feed an input to the sys-
tem under test (SUT) and check the output it produces (figure 6.1). This style of unit
testing is only applicable to code that doesn’t change a global or internal state, so the
only component to verify is its return value.
The following listing shows an example of such code and a test covering it. The Price-
Engine class accepts an array of products and calculates a discount.
public class PriceEngine
{
public decimal CalculateDiscount(params Product[] products)
Listing 6.1
Output-based testing
Output
Production code
Input
Output
veriﬁcation
Figure 6.1
In output-based testing, tests verify the output the system 
generates. This style of testing assumes there are no side effects and the only 
result of the SUT’s work is the value it returns to the caller.


