# 6.2.2 Comparing the styles using the metric of resistance to refactoring (pp.124-125)

---
**Page 124**

124
CHAPTER 6
Styles of unit testing
6.2.1
Comparing the styles using the metrics of protection against 
regressions and feedback speed
Let’s first compare the three styles in terms of the protection against regressions
and feedback speed attributes, as these attributes are the most straightforward in this
particular comparison. The metric of protection against regressions doesn’t depend
on a particular style of testing. This metric is a product of the following three
characteristics:
The amount of code that is executed during the test
The complexity of that code
Its domain significance
Generally, you can write a test that exercises as much or as little code as you like; no
particular style provides a benefit in this area. The same is true for the code’s com-
plexity and domain significance. The only exception is the communication-based
style: overusing it can result in shallow tests that verify only a thin slice of code and
mock out everything else. Such shallowness is not a definitive feature of communication-
based testing, though, but rather is an extreme case of abusing this technique.
 There’s little correlation between the styles of testing and the test’s feedback speed.
As long as your tests don’t touch out-of-process dependencies and thus stay in the
realm of unit testing, all styles produce tests of roughly equal speed of execution.
Communication-based testing can be slightly worse because mocks tend to introduce
additional latency at runtime. But the difference is negligible, unless you have tens of
thousands of such tests. 
6.2.2
Comparing the styles using the metric of resistance 
to refactoring
When it comes to the metric of resistance to refactoring, the situation is different.
Resistance to refactoring is the measure of how many false positives (false alarms) tests gen-
erate during refactorings. False positives, in turn, are a result of tests coupling to
code’s implementation details as opposed to observable behavior.
 Output-based testing provides the best protection against false positives because
the resulting tests couple only to the method under test. The only way for such tests to
couple to implementation details is when the method under test is itself an implemen-
tation detail.
 State-based testing is usually more prone to false positives. In addition to the
method under test, such tests also work with the class’s state. Probabilistically speak-
ing, the greater the coupling between the test and the production code, the greater
the chance for this test to tie to a leaking implementation detail. State-based tests tie
to a larger API surface, and hence the chances of coupling them to implementation
details are also higher.
 Communication-based testing is the most vulnerable to false alarms. As you may
remember from chapter 5, the vast majority of tests that check interactions with test


---
**Page 125**

125
Comparing the three styles of unit testing
doubles end up being brittle. This is always the case for interactions with stubs—you
should never check such interactions. Mocks are fine only when they verify interac-
tions that cross the application boundary and only when the side effects of those
interactions are visible to the external world. As you can see, using communication-
based testing requires extra prudence in order to maintain proper resistance to
refactoring.
 But just like shallowness, brittleness is not a definitive feature of the communication-
based style, either. You can reduce the number of false positives to a minimum by
maintaining proper encapsulation and coupling tests to observable behavior only.
Admittedly, though, the amount of due diligence varies depending on the style of
unit testing. 
6.2.3
Comparing the styles using the metric of maintainability
Finally, the maintainability metric is highly correlated with the styles of unit testing;
but, unlike with resistance to refactoring, there’s not much you can do to mitigate
that. Maintainability evaluates the unit tests’ maintenance costs and is defined by the
following two characteristics:
How hard it is to understand the test, which is a function of the test’s size
How hard it is to run the test, which is a function of how many out-of-process
dependencies the test works with directly
Larger tests are less maintainable because they are harder to grasp or change when
needed. Similarly, a test that directly works with one or several out-of-process depen-
dencies (such as the database) is less maintainable because you need to spend time
keeping those out-of-process dependencies operational: rebooting the database
server, resolving network connectivity issues, and so on.
MAINTAINABILITY OF OUTPUT-BASED TESTS
Compared with the other two types of testing, output-based testing is the most main-
tainable. The resulting tests are almost always short and concise and thus are easier to
maintain. This benefit of the output-based style stems from the fact that this style boils
down to only two things: supplying an input to a method and verifying its output,
which you can often do with just a couple lines of code.
 Because the underlying code in output-based testing must not change the global
or internal state, these tests don’t deal with out-of-process dependencies. Hence,
output-based tests are best in terms of both maintainability characteristics. 
MAINTAINABILITY OF STATE-BASED TESTS
State-based tests are normally less maintainable than output-based ones. This is
because state verification often takes up more space than output verification. Here’s
another example of state-based testing.
 
 


