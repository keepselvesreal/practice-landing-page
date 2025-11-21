# 3.8 Boundary testing and structural testing (pp.82-82)

---
**Page 82**

82
CHAPTER 3
Structural testing and code coverage
@Test
void sameInstance() {
  String str = "sometext";
  assertThat(leftPad(str, 5, "-")).isSameAs(str);
}
We are now much more confident that our test suite covers all the critical behavior of
the program. Structural testing and code coverage helped us identify parts of the code
that we did not test (or partitions we missed) during our specification-based testing—
and that is what structural testing is all about. 
3.8
Boundary testing and structural testing
The most challenging part of specification-based testing is identifying boundaries.
They are tricky to find, given the way we write specifications. Luckily, they are much
easier to find in source code, given how precise code has to be. All the boundary test-
ing ideas we discussed in the previous chapter apply here.
 The idea of identifying and testing on and off points fits nicely in structural testing.
For example, we can analyze the if statements in the leftPad program:

if (pads <= 0)—The on point is 0 and evaluates the expression to true. The off
point is the nearest point to the on point that makes the expression evaluate to
false. In this case, given that pads is an integer, the nearest point is 1.

if (pads == padLen)—The on point is padLen. Given the equality and that padLen
is an integer, we have two off points: one that happens when pads == padLen - 1
and another that happens when pads = padLen + 1.

if (pads < padLen)—The on point is again padLen. The on point evaluates the
expression to false. The off point is, therefore, pads == padLen - 1.
As a tester, you may want to use this information to see whether you can augment your
test suite.
 We discussed the loop boundary criterion earlier, which helps us try different pos-
sible boundaries. If a loop has a less conventional, more complicated expression, con-
sider applying on and off analysis there as well. 
3.9
Structural testing alone often is not enough
If code is the source of all truth, why can’t we just do structural testing? This is a very
interesting question. Test suites derived only with structural testing can be reasonably
effective, but they may not be strong enough. Let’s look at an example (see the
“counting clumps” problem, inspired by a CodingBat assignment: https://codingbat
.com/prob/p193817):
 
Listing 3.8
Another extra test for leftPad


