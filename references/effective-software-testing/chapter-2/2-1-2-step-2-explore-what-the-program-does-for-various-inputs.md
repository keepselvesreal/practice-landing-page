# 2.1.2 Step 2: Explore what the program does for various inputs (pp.34-35)

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


---
**Page 35**

35
The requirements say it all
    StringUtils.substringsBetween("abcdabcdab", "a", "d")
  ).isEqualTo(new String[] { "bc", "bc" });
}
@Test
void openAndCloseTagsThatAreLongerThan1Char() {    
  assertThat(
    StringUtils.substringsBetween("aabcddaabfddaab", "aa", "dd")
  ).isEqualTo(new String[] { "bc", "bf" });
}
I stop this exploration phase when I have a clear mental model of how the program
should work. Note that I do not expect you to perform the same exploration I did—it
is personal and guided by my hypothesis about the program. Also note that I did not
explore any corner cases; that comes later. At this moment, I am only interested in
better understanding the program. 
2.1.3
Step 3: Explore possible inputs and outputs, and identify partitions
We should find a way to prioritize and select a subset of inputs and outputs that will
give us sufficient certainty about the correctness of the program. Although the num-
ber of possible program inputs and outputs is nearly infinite, some sets of inputs make
the program behave the same way, regardless of the precise input value.
 In the case of our example, for testing purposes, the input “abcd” with open tag “a”
and close tag “d”, which makes the program return “bc”, is the same as the input
“xyzw” with open tag “x” and close tag “w”. You change the letters, but you expect the
program to do the same thing for both inputs. Given your resource constraints, you
will test just one of these inputs (it does not matter which), and you will trust that this
single case represents that entire class of inputs. In testing terminology, we say that
these two inputs are equivalent.
 Once you have identified this class (or partition), you repeat the process and look
for another class that will make the program behave in a different way that you have
not yet tested. If you keep dividing the domain, you will eventually identify all the dif-
ferent possible classes (or partitions) of inputs.
 A systematic way to do such an exploration is to think of the following:
1
Each input individually: “What are the possible classes of inputs I can provide?”
2
Each input in combination with other inputs: “What combinations can I try
between the open and close tags?”
3
The different classes of output expected from this program: “Does it return
arrays? Can it return an empty array? Can it return nulls?”
I find it easiest to start with individual inputs. Follow me:

str parameter—The string can be any string. The specification mentions the
null and empty cases; I would have tested those anyway, because they are always
I wrote all the test code in 
a single line, although you 
cannot see that in the 
printed book. Feel free to 
write it any way you prefer.


