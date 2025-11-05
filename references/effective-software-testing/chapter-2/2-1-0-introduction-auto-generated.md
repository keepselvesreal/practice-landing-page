# 2.1.0 Introduction [auto-generated] (pp.31-33)

---
**Page 31**

31
The requirements say it all
cycles, and always ensures that the code is testable. With all the classes ready, the
developer switches to “testing mode.” It is time to systematically look for bugs. This is
where specification testing fits in: it is the first testing technique I recommend using
once you’re in testing mode.
 As I mentioned, the idea of specification-based testing is to derive tests from the
requirements themselves. The specific implementation is less important. Of course,
we use source code to test, too—this structural testing is the next technique in the work-
flow. Once you have a complete picture of all the techniques, you will be able to use
them iteratively and go back and forth between them.
2.1
The requirements say it all
Let’s start with an example. A new set of requirements comes in for you to develop. As
soon as you begin to analyze the requirements, you identify a particular method you
need to implement: a method that searches for substrings between two tags in a given
string and returns all the matching substrings. Let’s call this method substrings-
Between(), inspired by the Apache Commons Lang library (http://mng.bz/nYR5).
You are about to test a real-world open source method.
 After some thinking, you end up with the following requirements for the sub-
stringsBetween() method:
Method: substringsBetween()
Searches a string for substrings delimited by a start and end tag, returning all
matching substrings in an array.

str—The string containing the substrings. Null returns null; an empty
string returns another empty string.

open—The string identifying the start of the substring. An empty string
returns null.

close—The string identifying the end of the substring. An empty string
returns null.
The program returns a string array of substrings, or null if there is no match.
Example: if str = “axcaycazc”, open = “a”, and close = “c”, the output will be
an array containing [“x”, “y”, “z”]. This is the case because the “a<something>c”
substring appears three times in the original string: the first contains “x” in
the middle, the second “y,” and the last “z.”
With these requirements in mind, you write the implementation shown in listing 2.1.
You may or may not use TDD (discussed in chapter 8) to help you develop this feature.
You are somewhat confident that the program works. Slightly, but not completely.
 
 
 


---
**Page 32**

32
CHAPTER 2
Specification-based testing
public static String[] substringsBetween(final String str,
 final String open, final String close) {
  if (str == null || isEmpty(open) || isEmpty(close)) {   
    return null;
  }
  int strLen = str.length();
  if (strLen == 0) {    
    return EMPTY_STRING_ARRAY;
  }
  int closeLen = close.length();
  int openLen = open.length();
  List<String> list = new ArrayList<>();
  int pos = 0;               
  while (pos < strLen - closeLen) {
    int start = str.indexOf(open, pos);   
    if (start < 0) {  
      break;
    }
    start += openLen;
    int end = str.indexOf(close, start);   
    if (end < 0) {      
      break;
    }
    list.add(str.substring(start, end));    
    pos = end + closeLen;     
  }
  if (list.isEmpty()) {   
    return null;
  }
  return list.toArray(EMPTY_STRING_ARRAY);
}
Let’s walk through an example. Consider the inputs str = “axcaycazc”, open = “a”, and
close = “c”. None of the three strings are empty, so the method goes straight to the
openLen and closeLen variables. These two variables store the length of the open and
close strings, respectively. In this case, both are equal to 1, as “a” and “c” are strings
with a single character.
 The program then goes into its main loop. This loop runs while there still may be
substrings in the string to check. In the first iteration, pos equals zero (the beginning
of the string). We call indexOf, looking for a possible occurrence of the open tag. We
Listing 2.1
Implementing the substringsBetween() method
If the pre-
conditions do not 
hold, returns null 
right away
If the string is empty, 
returns an empty 
array immediately
A pointer that indicates 
the position of the string 
we are looking at
Looks for the next 
occurrence of the 
open tag
Breaks the loop if the 
open tag does not appear 
again in the string
Looks for
the close
tag
Breaks the loop if the 
close tag does not appear 
again in the string
Gets the substring 
between the open 
and close tags
Moves the pointer to 
after the close tag we 
just found
Returns
null if we
do not
find any
substrings


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


