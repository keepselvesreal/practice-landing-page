# 2.4.5 Use variations of the same input to facilitate understanding (pp.55-56)

---
**Page 55**

55
Specification-based testing in the real world
2.4.2
How far should specification testing go?
The pragmatic answer to this question is to understand the risks of a failure. What
would be the cost of a failure in that part of the program? If the cost is high, it may be
wise to invest more in testing, explore more corner cases, and try different techniques
to ensure quality. But if the cost is low, being less thorough may be good enough. Per-
sonally, I stop testing when I have been through all the steps a couple of times and
cannot see a case I am not testing. 
2.4.3
Partition or boundary? It does not matter!
When you are exploring inputs and outputs, identifying partitions, and devising test
cases, you may end up considering a boundary to be an exclusive partition and not a
boundary between two partitions. It does not matter if a specific case emerges when
you are identifying partitions or in the boundaries step. Each developer may interpret
the specification differently, and minor variations may result. The important thing is
that the test case emerges and the bug will not slip into the program. 
2.4.4
On and off points are enough, but feel free to add in 
and out points
On and off points belong to specific partitions, so they also serve as concrete test cases
for the partitions. This means testing all the boundaries of your input domain is
enough. Nevertheless, I often try some in and out points in my tests. They are redun-
dant, because the on and off points exercise the same partition as the in and out
points; but these extra points give me a better understanding of the program and may
better represent real-life inputs. Striving for the leanest test suite is always a good idea,
but a few extra points are fine. 
2.4.5
Use variations of the same input to facilitate understanding
You can simplify your understanding of the different test cases by using the same
input seed for all of them, as we noticed in an observational study with professional
developers described in my paper with Treude and Zaidman (2021). For each parti-
tion, you then make small modifications to the input seed: just enough to meet the
criteria of that partition. In the chapter example, all the test cases are based on the
string “abc”; as soon as one test case fails, it is easy to compare it to similar inputs from
other test cases that pass.
 Note that this trick goes against the common testing idea of varying inputs as
much as possible. Varying inputs is essential, as it allows us to explore the input space
and identify corner cases. However, when doing specification-based testing, I prefer to
focus on rigorously identifying and testing partitions. Later in the book, we will write
test cases that explore the input domain in an automated fashion via property-based
testing in chapter 5. 


---
**Page 56**

56
CHAPTER 2
Specification-based testing
2.4.6
When the number of combinations explodes, be pragmatic
If we had combined all the partitions we derived from the substringsBetween pro-
gram, we would have ended up with 320 tests. This number is even larger for more
complex problems. Combinatorial testing is an entire area of research in software test-
ing; I will not dive into the techniques that have been proposed for such situations,
but I will provide you with two pragmatic suggestions.
 First, reduce the number of combinations as much as possible. Testing exceptional
behavior isolated from other behaviors (as we did in the example) is one way to do so.
You may also be able to leverage your domain knowledge to further reduce the num-
ber of combinations.
 Second, if you are facing many combinations at the method level, consider breaking
the method in two. Two smaller methods have fewer things to test and, therefore, fewer
combinations to test. Such a solution works well if you carefully craft the method con-
tracts and the way they should pass information. You also reduce the chances of bugs
when the two simple methods are combined into a larger, more complex one. 
2.4.7
When in doubt, go for the simplest input
Picking concrete input for test cases is tricky. You want to choose a value that is realis-
tic but, at the same time, simple enough to facilitate debugging if the test fails.
 I recommend that you avoid choosing complex inputs unless you have a good rea-
son to use them. Do not pick a large integer value if you can choose a small integer
value. Do not pick a 100-character string if you can select a 5-character string. Simplic-
ity matters. 
2.4.8
Pick reasonable values for inputs you do not care about
Sometimes, your goal is to exercise a specific part of the functionality, and that part does
not use one of the input values. You can pass any value to that “useless” input variable. In
such scenarios, my recommendation is to pass realistic values for these inputs. 
2.4.9
Test for nulls and exceptional cases, but only when 
it makes sense
Testing nulls and exceptional cases is always important because developers often for-
get to handle such cases in their code. But remember that you do not want to write
tests that never catch a bug. Before writing such tests, you should understand the over-
all picture of the software system (and its architecture). The architecture may ensure
that the pre-conditions of the method are satisfied before calling it.
 If the piece of code you are testing is very close to the UI, exercise more corner
cases such as null, empty strings, uncommon integer values, and so on. If the code is
far from the UI and you are sure the data is sanitized before it reaches the component
under test, you may be able to skip such tests. Context is king. Only write tests that will
eventually catch a bug. 


