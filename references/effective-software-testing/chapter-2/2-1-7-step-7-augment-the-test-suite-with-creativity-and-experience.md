# 2.1.7 Step 7: Augment the test suite with creativity and experience (pp.43-45)

---
**Page 43**

43
The requirements say it all
    assertThat(substringsBetween("aabcc", "xx", "cc")).isEqualTo(null);
    assertThat(substringsBetween("aabbcc", "aa", "cc"))
      .isEqualTo(new String[] {"bb"});
    assertThat(substringsBetween("aabbccaaeecc", "aa", "cc"))
      .isEqualTo(new String[] {"bb", "ee"});
  }
Finally, here is the test for when there is no substring between the open and close tags.
@Test
void noSubstringBetweenOpenAndCloseTags() {
  assertThat(substringsBetween("aabb", "aa", "bb"))
    .isEqualTo(new String[] {""});
  }
}
I decided to group the assertions in five different methods. They almost match my
groups when engineering the test cases in step 5. The only difference is that I broke
the exceptional cases into three test methods: strIsNullOrEmpty, openIsNullOr-
Empty, and closeIsNullOrEmpty.
 Some developers would vouch for a single method per test case, which would
mean 21 test methods, each containing one method call and one assertion. The
advantage would be that the test method’s name would clearly describe the test case.
JUnit also offers the ParameterizedTest feature (http://mng.bz/voKp), which could
be used in this case.
 I prefer simple test methods that focus on one test case, especially when imple-
menting complex business rules in enterprise systems. But in this case, there are lots
of inputs to test, and many of them are variants of a larger partition, so it made more
sense to me to code the way I did.
 Deciding whether to put all tests in a single method or in multiple methods is
highly subjective. We discuss test code quality and how to write tests that are easy to
understand and debug in chapter 10.
 Also note that sometimes there are values we do not care about. For example, con-
sider test case 1: str is null. We do not care about the values we pass to the open and
close tags here. My usual approach is to select reasonable values for the inputs I do
not care about—that is, values that will not interfere with the test. 
2.1.7
Step 7: Augment the test suite with creativity and experience
Being systematic is good, but we should never discard our experience. In this step, we
look at the partitions we’ve devised and see if we can develop interesting variations.
Variation is always a good thing to have in testing.
 In the example, when revisiting the tests, I noticed that we never tried strings with
spaces. I decided to engineer two extra tests based on T15 and T20, both about “str
contains both open and close tags multiple times”: one for open and close tags with
Listing 2.7
Tests for substringsBetween, part 5


---
**Page 44**

44
CHAPTER 2
Specification-based testing
lengths 1, another for open and close tags with larger lengths. These check whether
the implementation works if there are whitespaces in the string. You see them in list-
ing 2.8.
NOTE
It’s possible we don’t need to test for this extra case. Maybe the imple-
mentation handles strings in a generic way. For now, we are only looking at
the requirements, and testing special characters is always a good idea. If you
have access to the implementation (as we discuss in the next chapter), the
code can help you decide whether a test is relevant.
@Test
void openAndCloseOfLength1() {
  // ... previous assertions here
  assertThat(substringsBetween("abcabyt byrc", "a", "c"))
    .isEqualTo(new String[] {"b", "byt byr"});
}
@Test
void openAndCloseTagsOfDifferentSizes() {
  // ... previous assertions here
  assertThat(substringsBetween("a abb ddc ca abbcc", "a a", "c c")).
  ➥ isEqualTo(new String[] {"bb dd"});
}
We end up with 23 test cases. Take time to revisit all the steps we have worked through,
and then consider this question: are we finished?
 We are finished with specification testing. However, we are not done testing. After
specification testing, the next step is to bring the implementation into play and aug-
ment our test suite with what we see in the code. That is the topic of chapter 3.
Listing 2.8
Tests for substringsBetween using parameterized tests, part 6
Four eyes are better than two
A reviewer of this book had an interesting question: what about a test case where the
input is aabcddaabeddaab, open is aa, and close is d? “bc” and “be” are the sub-
strings between the provided open and the close tags (aa<bc>ddaa<be>ddaab), but
“bcddaabed” could also be considered a substring (aa<bcddaabed>daab).
At first, I thought I had missed this test case. But in fact, it is the same as T15 and T20.
Different people approach problems in different ways. My thought process was,
“Let’s see if the program breaks if we have multiple open and close tags in the
string.” The reviewer may have thought, “Let’s see if the program will incorrectly go
for the longer substring.”
We want to make testing as systematic as possible, but a lot depends on how the
developer models the problem. Sometimes you will not see all the test cases. When
you do come up with a new test, add it to the test suite!


---
**Page 45**

45
Specification-based testing in a nutshell
2.2
Specification-based testing in a nutshell
I propose a seven-step approach to derive systematic tests based on a specification.
This approach is a mix of the category-partition method proposed by Ostrand and Balcer
in their seminal 1988 work, and Kaner et al.’s Domain Testing Workbook (2013), with my
own twist: see figure 2.4.
The steps are as follows:
1
Understand the requirement, inputs, and outputs. We need an overall idea of what
we are about to test. Read the requirements carefully. What should the program
do? What should it not do? Does it handle specific corner cases? Identify the
input and output variables in play, their types (integers, strings, and so on),
and their input domain (for example, is the variable a number that must be
between 5 and 10?). Some of these characteristics can be found in the pro-
gram’s specification; others may not be stated explicitly. Try to understand the
nitty-gritty details of the requirements.
2
Explore the program. If you did not write the program yourself, a very good way to
determine what it does (besides reading the documentation) is to play with it.
Call the program under test with different inputs and see what it produces as
output. Continue until you are sure your mental model matches what the pro-
gram does. This exploration does not have to be (and should not be) system-
atic. Rather, focus on increasing your understanding. Remember that you are
still not testing the program.
3
Judiciously explore the possible inputs and outputs, and identify the partitions. Identify-
ing the correct partitions is the hardest part of testing. If you miss one, you may
let a bug slip through. I propose three steps to identify the partitions:
a
Look at each input variable individually. Explore its type (is it an integer? is it
a string?) and the range of values it can receive (can it be null? is it a number
ranging from 0 to 100? does it allow negative numbers?).
b
Look at how each variable may interact with another. Variables often have
dependencies or put constraints on each other, and those should be tested.
Understand the
requirement.
Explore the
program.
Identify the
partitions.
Analyze the
boundaries.
Devise test
cases.
Automate test
cases.
Augment
(creativity and
experience).
Figure 2.4
The seven steps I propose to derive test cases based on specifications. The solid 
arrows indicate the standard path to follow. The dashed arrows indicate that, as always, the 
process should be iterative, so in practice you’ll go back and forth until you are confident about the 
test suite you’ve created.


