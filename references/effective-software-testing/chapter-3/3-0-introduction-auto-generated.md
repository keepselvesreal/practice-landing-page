# 3.0 Introduction [auto-generated] (pp.63-64)

---
**Page 63**

63
Structural testing
and code coverage
In the previous chapter, we discussed using software requirements as the main
element to guide the testing. Once specification-based testing is done, the next
step is to augment the test suite with the help of the source code. There are several rea-
sons to do so.
 First, you may have forgotten a partition or two when analyzing the require-
ments, and you may notice that while looking at the source code. Second, when
implementing code, you take advantage of language constructs, algorithms, and
data structures that are not explicit in the documentation. Implementation-specific
details should also be exercised to increase the likelihood of ensuring the pro-
gram’s full correctness.
This chapter covers
Creating test cases based on the code structure
Combining structural testing and specification-
based testing
Using code coverage properly
Why some developers (wrongly) dislike code 
coverage


---
**Page 64**

64
CHAPTER 3
Structural testing and code coverage
 In this chapter, we learn how to systematically reflect on the source code, see
what is being exercised by the test suite we derived with the help of the specification,
and what remains to be tested. Using the structure of the source code to guide test-
ing is also known as structural testing. Understanding structural testing techniques
means understanding the coverage criteria. The remainder of this chapter explores
using code coverage information to gain more confidence that the program works
as expected.
3.1
Code coverage, the right way
Consider the following requirement for a small program that counts the number of
words in a string that end with either “r” or “s” (inspired by a CodingBat problem,
https://codingbat.com/prob/p199171):
Given a sentence, the program should count the number of words that end
with either “s” or “r”. A word ends when a non-letter appears. The program
returns the number of words.
A developer implements this requirement as shown in the following listing.
public class CountWords {
  public int count(String str) {
    int words = 0;
    char last = ' ';
    for (int i = 0; i < str.length(); i++) {   
      if (!isLetter(str.charAt(i)) &&   
       (last == 's' || last == 'r')) {
          words++;
      }
      last = str.charAt(i);   
    }
    if (last == 'r' || last == 's') {    
      words++;
    }
    return words;
  }
}
Now, consider a developer who does not know much about specification-based testing
techniques and writes the following two JUnit tests for the implementation.
 
 
 
Listing 3.1
Implementing the CountWords program
Loops through 
each character 
in the string
If the current character is a non-
letter and the previous character 
was “s” or “r”, we have a word!
Stores the current 
character as the 
“last” one
Counts one more 
word if the string 
ends in “r” or “s”


