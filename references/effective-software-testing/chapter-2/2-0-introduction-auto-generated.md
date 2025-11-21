# 2.0 Introduction [auto-generated] (pp.30-31)

---
**Page 30**

30
Specification-based
testing
Software requirements are undoubtedly the most valuable artifact of software test-
ing. By requirements, I mean any textual document that describes what a functional-
ity should do. Requirements tell us precisely what the software needs to do and
what it should not do. They describe the intricacies of the business rules that the
software has to implement and we need to validate. Therefore, requirements
should be the first artifact you go for when it comes to testing!
 In this chapter, we explore specification-based testing. These techniques use the
program requirements—such as agile user stories or UML use cases—as testing
input. We will discuss how to use all the information available in a requirement to
systematically derive a set of tests that exercise that requirement extensively.
 Where does specification-based testing fit into the entire testing process? Imag-
ine that a software developer receives a new feature to implement. The developer
writes the implementation code, guided by test-driven development (TDD)
This chapter covers
Creating test cases using specification-based 
testing
Identifying and creating test cases for program 
boundaries


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
 
 
 


