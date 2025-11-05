# 2.1.3 Step 3: Explore possible inputs and outputs, and identify partitions (pp.35-37)

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


---
**Page 36**

36
CHAPTER 2
Specification-based testing
good exceptional test cases. Given that this is a string (which is basically a list of
characters), I will also test what happens if the string has length 1.
a
Null string
b
Empty string
c
String of length 1
d
String of length > 1 (any string)

open parameter—This can also be anything. I will try it with null and empty, as I
learned from the str parameter that those cases are special in this program. I
will also try strings with length 1 and greater than 1:
a
Null string
b
Empty string
c
String of length 1
d
String of length > 1

close parameter—This parameter is like the previous one:
a
Null string
b
Empty string
c
String of length 1
d
String of length > 1
Once the input variables are analyzed in detail, we explore possible combinations of
variables. A program’s input variables may be related to each other. In the example, it
is clear that the three variables have a dependency relationship. Follow me again:

(str, open, close)parameters—open and close may or may not be in the string.
Also, open may be there, but not close (and vice versa).
a
str contains neither the open nor the close tag.
b
str contains the open tag but not the close tag.
c
str contains the close tag but not the open tag.
d
str contains both the open and close tags.
e
str contains both the open and close tags multiple times.
Note that this thought process depended on my experience as a tester. The documen-
tation does not explicitly mention tags not being in the string, nor does it mention the
open tag being present but the close tag not. I saw this case because of my experience
as a tester.
 Finally, we reflect on the possible outputs. The method returns an array of sub-
strings. I can see a set of possible different outputs, both for the array itself and for the
strings within the array:
Array of strings (output)
a
Null array
b
Empty array


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


