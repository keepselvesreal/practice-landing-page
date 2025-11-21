# 2.4.2 How far should specification testing go? (pp.55-55)

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


