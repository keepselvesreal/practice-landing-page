# 8.2 Reflecting on our first TDD experience (pp.206-208)

---
**Page 206**

206
CHAPTER 8
Test-driven development
   finalNumber +=
     table.get(numberInRoman.charAt(i)) * multiplier; 
   lastNeighbor = current; 
  }
  return finalNumber;
}
The tests pass. Is there anything we want to improve in the production code? We use
numberInRoman.charAt(i) when summing the final number, but this value is already
stored in the current variable, so we can reuse it. Also, extracting a variable to store
the current digit after it is multiplied by 1 or -1 will help developers understand the
algorithm. We can refactor the code, as shown in the following listing, and run the
tests again.
public int convert(String numberInRoman) {
  int finalNumber = 0;
  int lastNeighbor = 0; 
  for(int i = numberInRoman.length() - 1; i >= 0; i--) {
   int current = table.get(numberInRoman.charAt(i));
   int multiplier = 1;
   if(current < lastNeighbor) multiplier = -1;
   int currentNumeralToBeAdded = current * multiplier; 
   finalNumber += currentNumeralToBeAdded;
   lastNeighbor = current;
  }
  return finalNumber;
}
Now that we have implemented all the examples in our initial list, we can think of other
cases to handle. We are not handling invalid numbers, for example. The program must
reject inputs such as "VXL" and "ILV". When we have new examples, we repeat the
entire procedure until the whole program is implemented. I will leave that as an exer-
cise for you—we have done enough that we are ready to more formally discuss TDD. 
8.2
Reflecting on our first TDD experience
Abstractly, the cycle we repeated in the previous section’s development process was
as follows:
1
We wrote a (unit) test for the next piece of functionality we wanted to imple-
ment. The test failed.
Listing 8.14
Refactored version
Adds the current digit 
to the finalNumber 
variable. The current 
digit is positive or 
negative depending on 
whether we should 
add or subtract it, 
respectively.
Updates 
lastNeighbor 
to be the 
current digit
Keeps the last 
digit visited
Uses the current
variable and introduces the
currentNumeralToBeAdded variable


---
**Page 207**

207
Reflecting on our first TDD experience
2
We implemented the functionality. The test passed.
3
We refactored our production and test code.
This TDD process is also called the red-green-refactor cycle. Figure 8.1 shows a popular
way to represent the TDD cycle.
TDD practitioners say this approach can be very advantageous for the development
process. Here are some of the advantages:
Looking at the requirements first—In the TDD cycle, the tests we write to support
development are basically executable requirements. Whenever we write one of
them, we reflect on what the program should and should not do.
This approach makes us write code for the specific problem we are supposed
to solve, preventing us from writing unnecessary code. And exploring the
requirement systematically forces us to think deeply about it. Developers often
go back to the requirements engineer and ask questions about cases that are
not explicit in the requirement.
Full control over the pace of writing production code—If we are confident about the
problem, we can take a big step and create a test that involves more compli-
cated cases. However, if we are still unsure how to tackle the problem, we can
break it into smaller parts and create tests for these simpler pieces first.
Quick feedback—Developers who do not work in TDD cycles produce large
chunks of production code before getting any feedback. In a TDD cycle, devel-
opers are forced to take one step at a time. We write one test, make it pass, and
reflect on it. These many moments of reflection make it easier to identify new
problems as they arise, because we have only written a small amount of code
since the last time everything was under control.
Testable code—Creating the tests first makes us think from the beginning about a
way to (easily) test the production code before implementing it. In the tradi-
tional flow, developers often think about testing only in the later stages of devel-
oping a feature. At that point, it may be expensive to change how the code
works to facilitate testing.
Test
passes
Test fails
Refactor
Write a
(simple)
test.
Make it
pass.
Figure 8.1
TDD, also known as the 
red-green-refactor cycle


---
**Page 208**

208
CHAPTER 8
Test-driven development
Feedback about design—The test code is often the first client of the class or com-
ponent we are developing. A test method instantiates the class under test,
invokes a method passing all its required parameters, and asserts that the
method produces the expected results. If this is hard to do, perhaps there is a
better way to design the class. When doing TDD, these problems arise earlier in
the development of the feature. And the earlier we observe such issues, the
cheaper it is to fix them.
NOTE
TDD shows its advantages best in more complicated problems. I sug-
gest watching James Shore’s YouTube playlist on TDD (2014), where he TDDs
an entire software system. I also recommend Freeman and Pryce’s book Grow-
ing Object-Oriented Systems Guided by Tests (2009). They also TDD an entire system,
and they discuss in depth how they use tests to guide their design decisions.
8.3
TDD in the real world
This section discusses the most common questions and discussions around TDD.
Some developers love TDD and defend its use fiercely; others recommend not
using it.
 As always, software engineering practices are not silver bullets. The reflections I
share in this section are personal and not based on scientific evidence. The best way to
see if TDD is beneficial for you is to try it!
8.3.1
To TDD or not to TDD?
Skeptical readers may be thinking, “I can get the same benefits without doing TDD. I
can think more about my requirements, force myself to only implement what is
needed, and consider the testability of my class from the beginning. I do not need to
write tests for that!” That is true. But I appreciate TDD because it gives me a rhythm to
follow. Finding the next-simplest feature, writing a test for it, implementing nothing
more than what is needed, and reflecting on what I did gives me a pace that I can fully
control. TDD helps me avoid infinite loops of confusion and frustration.
 The more defined development cycle also reminds me to review my code often.
The TDD cycle offers a natural moment to reflect: as soon as the test passes. When
all my tests are green, I consider whether there is anything to improve in the cur-
rent code.
 Designing classes is one of the most challenging tasks of a software engineer. I
appreciate the TDD cycle because it forces me to use the code I am developing from
the very beginning. The perception I have about the class I am designing is often dif-
ferent from my perception when I try to use the class. I can combine both of these
perceptions and make the best decision about how to model the class.
 If you write the tests after the code, and not before, as in TDD, the challenge is
making sure the time between writing code and testing is small enough to provide
developers with timely feedback. Don’t write code for an entire day and then start test-
ing—that may be too late.


