# 2.1.1 Step 1: Understanding the requirements, inputs, and outputs (pp.33-34)

---
**Page 33**

33
The requirements say it all
pass the open tag and the position to start the search, which at this point is 0. indexOf
returns 0, which means we found an open tag. (The first element of the string is
already the open tag.)
 The program then looks for the end of the substring by calling the indexOf
method again, this time on the close tag. Note that we increase the start position by
the length of the open tag because we want to look for the close tag after the end of
the entire open tag. Remember that the open tag has a length of one but can have any
length. If we find a close tag, this means there is a substring to return to the user. We
get this substring by calling the substring method with the start and end positions as
parameters. We then reposition our pos pointer, and the loop iterates again. Figure 2.1
shows the three iterations of the loop as well as the locations to which the main point-
ers (start, end, and pos) are pointing.
Now that you have finished the first implementation, you flip your mind to testing
mode. It is time for specification and boundary testing. As an exercise, before we work
on this problem together, look at the requirements one more time and write down all
the test cases you can come up with. The format does not matter—it can be something
like “all parameters null.” When you are finished with this chapter, compare your ini-
tial test suite with the one we are about to derive together.
 The best way to ensure that this method works properly would be to test all the pos-
sible combinations of inputs and outputs. Given that substringsBetween() receives
three string parameters as an input, we would need to pass all possible valid strings to
the three parameters, combined in all imaginable ways. As we discussed in chapter 1,
exhaustive testing is rarely possible. We have to be pragmatic.
2.1.1
Step 1: Understanding the requirements, inputs, and outputs
Regardless of how your requirements are written (or even if they are only in your
mind), they include three parts. First is what the program/method must do: its busi-
ness rules. Second, the program receives data as inputs. Inputs are a fundamental part
of our reasoning, as it is through them that we can test the different cases. Third, rea-
soning about the output will help us better understand what the program does and
how the inputs are converted to the expected output.
1st iteration: axcaycazc
pos
open
close
pos (in the end of the loop)
2nd iteration: axcaycazc
pos
open
close
pos
3rd iteration: axcaycazc
pos
open
close
pos
Figure 2.1
The three iterations of 
the substringsBetween method 
for our example


---
**Page 34**

34
CHAPTER 2
Specification-based testing
 For the substringsBetween() method, my reasoning would be
1
The goal of this method is to collect all substrings in a string that are delimited
by an open tag and a close tag (the user provides these).
2
The program receives three parameters:
a
str, which represents the string from which the program will extract sub-
strings
b
The open tag, which indicates the start of a substring
c
The close tag, which indicates the end of the substring
3
The program returns an array composed of all the substrings found by the
program.
Such reflection is useful to think about what you want from the method. 
2.1.2
Step 2: Explore what the program does for various inputs
An ad hoc exploration of what the method does may increase your understanding of
it. I have noticed this when observing professional software developers writing test
cases for methods they have never seen before (Aniche, Treude, and Zaidman, 2021).
This step is more relevant when you did not write the code—if you wrote it, this explo-
ration phase may not be needed.
 To illustrate this step, suppose you did not write this code (which, in this case, is
true). My process would be as follows (see the JUnit code in listing 2.2):
 Let’s see the program working on a happy case. I will pass the string “abcd” with
the open tag “a” and the close tag “d”. I expect it to return an array with a single ele-
ment: ["bc"]. I try that (in a unit test), and the program returns what I expect.
 Next, let’s see what happens if there are multiple substrings in the main string. I
will pass the string “abcdabcdab” with the same open and close tags. I expect it to
return an array with two strings: ["bc", "bc"]. The program returns what I expect.
 I expect the program to behave the same with open and close tags larger than a
single character. I will repeat the second test, doubling the “a”s and the “d”s in all the
parameters. I will also change one of the “bc”s to “bf”, so it is easier to check that the
method returns two different substrings: ["bc", "bf"]. The program returns what I
expect.
@Test
void simpleCase() {   
  assertThat(
    StringUtils.substringsBetween("abcd", "a", "d")
  ).isEqualTo(new String[] { "bc" });
}
@Test
void manySubstrings() {   
  assertThat(
Listing 2.2
Exploratory tests for substringsBetween()
We write these test cases based on our feelings. 
What do we want to explore next?
I don’t care if they are good 
tests, as long as they teach me 
something about the code.


