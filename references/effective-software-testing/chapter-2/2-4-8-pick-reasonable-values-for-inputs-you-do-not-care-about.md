# 2.4.8 Pick reasonable values for inputs you do not care about (pp.56-56)

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


