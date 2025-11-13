# 2.1.4 Step 4: Analyze the boundaries (pp.37-39)

---
**Page 37**

37
The requirements say it all
c
Single item
d
Multiple items
Each individual string (output)
a
Empty
b
Single character
c
Multiple characters
You may think that reflecting on the outputs is not necessary. After all, if you reasoned
correctly about the inputs, you are probably exercising all the possible kinds of out-
puts. This is a valid argument. Nevertheless, for more complex programs, reflecting
on the outputs may help you see an input case that you did not identify before. 
2.1.4
Step 4: Analyze the boundaries
Bugs in the boundaries of the input domain are common in software systems. As
developers, we have all made mistakes such as using a “greater than” operator (>)
where it should have been a “greater than or equal to” operator (>=). Programs with
such bugs tend to work well for most provided inputs, but they fail when the input is
near the boundary. Boundaries are everywhere, and our goal in this section is to learn
how to identify them.
 When we devise partitions, they have close boundaries with the other partitions. Imag-
ine a simple program that prints “hiphip” if the given input is a number smaller than 10
or “hooray” if the given input is greater than or equal to 10. A tester can divide the input
domain into two partitions: (1) the set of inputs that make the program print “hiphip”
and (2) the set of inputs that make the program print “hooray”. Figure 2.2 illustrates
this program’s inputs and partitions. Note that the input value 9 belongs to the “hiphip”
partition, while the input value 10 belongs to the “hooray” partition.
The odds of a programmer writing a bug near the boundary (in this case, near the
input values 9 and 10) are greater than for other input values. This is what boundary
testing is about: making the program behave correctly when inputs are near a bound-
ary. And this is what this fourth step is about: boundary testing.
hooray
hiphip
1
1
2 3 4 5 6 7 8 9 10 11 12
3 14 15 …
Boundary
When we cross this boundary, the program
suddenly changes its behavior completely.
We want to make sure this works perfectly!
Figure 2.2
The boundary between the 
“hiphip” and “hooray” partitions. Numbers 
up to 9 belong to the “hiphip” partition, 
and numbers greater than 9 belong to the 
“hooray” partition.


---
**Page 38**

38
CHAPTER 2
Specification-based testing
 Whenever a boundary is identified, I suggest that you test what happens to the pro-
gram when inputs go from one boundary to the other. In the previous example, this
would mean having a test with 9 as input and another test with 10 as input. This idea is
similar to what Jeng and Weyuker proposed in their 1994 paper: testing two points
whenever there is a boundary. One test is for the on point, which is the point that is on
the boundary; and the other test is for the off point, which is the point closest to the
boundary that belongs to the partition the on point does not belong to (that is, the
other partition).
 In the hiphip-hooray example, the on point is 10. Note that 10 is the number that
appears in the specification of the program (input >= 10) and is likely to also be the
number the developer uses in the if statement. The value 10 makes the program
print “hooray”. The off point is the point closest to the boundary that belongs to the
other partition. In this case, the off point is 9. The number 9 is the closest number to
10, and it belongs to the “hiphip” partition.
 Let’s discuss two more common terms: in point and out point. In points are points
that make the condition true. You may have an infinite number of them. In the
hiphip-hooray example, 11, 12, 25, and 42 are all examples of in points. Out points,
on the other hand, are points that make the condition false. 8, 7, 2, and –42 are all
examples of out points. In equalities, the in point is the one in the condition, and all
others are out points. For example, in a == 10, 10 is the (only) in point and the on
point; 12 is an out point and an off point; and 56 is an out point. Whenever you find a
boundary, two tests (for the on and off points) are usually enough, although, as I will
discuss later, I do not mind throwing in some interesting in and out points to have a
more complete test suite.
 Another common situation in boundary testing is finding boundaries that deal
with equalities. In the previous example, suppose that instead of input >= 10, the spec-
ification says that the program prints “hooray” whenever the input is 10 or “hiphip”
otherwise. Given that this is an equality, we now have one on point (10) but two off
points (9 and 11), because the boundary applies to both sides. In this case, as a tester,
you would write three test cases.
 My trick to explore boundaries is to look at all the partitions and think of inputs
between them. Whenever you find one that is worth testing, you test it.
 In our example, a straightforward boundary happens when the string passes from
empty to non-empty, as you know that the program stops returning empty and will
(possibly) start to return something. You already covered this boundary, as you have
partitions for both cases. As you examine each partition and how it makes boundaries
with others, you analyze the partitions in the (str, open, close) category. The pro-
gram can have no substrings, one substring, or multiple substrings. And the open and
close tags may not be in the string; or, more importantly, they may be in the string,
but with no substring between them. This is a boundary you should exercise! See fig-
ure 2.3.


---
**Page 39**

39
The requirements say it all
Whenever we identify a boundary, we devise two tests for it, one for each side of the
boundary. For the “no substring”/“one substring” boundary, the two tests are as follows:

str contains both open and close tags, with no characters between them.

str contains both open and close tags, with characters between them.
The second test is not necessary in this case, as other tests already exercise this situa-
tion. Therefore, we can discard it. 
2.1.5
Step 5: Devise test cases
With the inputs, outputs, and boundaries properly dissected, we can generate con-
crete test cases. Ideally, we would combine all the partitions we’ve devised for each of
the inputs. The example has four categories, each with four or five partitions: the str
category with four partitions (null string, empty string, string of length 1, and string of
length > 1), the open category with four partitions (the same as str), the close cate-
gory with four partitions (also the same as str), and the (str, open, close) category
with five partitions (string does not contain either the open or close tags, string contains the
open tag but does not contain the close tag, string contains the close tag but does not contain
the open tag, string contains both the open and close tags, string contains both the open and
close tags multiple times). This means you would start with the str null partition and
combine it with the partitions of the open, close, and (str, open, close) categories.
You would end up with 4 × 4 × 4 × 5 = 320 tests. Writing 320 tests may be an effort that
will not pay off.
 In such situations, we pragmatically decide which partitions should be combined
with others and which should not. A first idea to reduce the number of tests is to test
exceptional cases only once and not combine them. For example, the null string parti-
tion may be tested only once and not more than that. What would we gain from com-
bining null string with open being null, empty, length = 1, and length > 1 as well as
with close being null, empty, length = 1, length > 1, and so on? It would not be
worth the effort. The same goes for empty string: one test may be good enough. If we
When the input contains both the “open” and “close” tags, and the length
of the substring changes from 0 to greater than 0, the program starts to
return this substring. It’s a boundary, and we should exercise it!
One substring
len(substring)
len = 0
len > 0
No
substring
Figure 2.3
Some of the boundaries in the substringsBetween() problem.


