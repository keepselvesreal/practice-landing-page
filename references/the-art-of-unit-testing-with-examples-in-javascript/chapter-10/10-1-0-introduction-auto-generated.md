# 10.1.0 Introduction [auto-generated] (pp.195-196)

---
**Page 195**

195
10.1
Common test types and levels
How can we optimize the speed of tests without sacrificing trust in them?
Who should write each type of test? 
The answers to these questions, and many more, are what I’d call a testing strategy. 
 The first step in our journey is to frame the scope of the testing strategy in terms of
test types. 
10.1
Common test types and levels
Different industries might have different test types and levels. Figure 10.1, which we
first discussed in chapter 7, is a rather generic set of test types that I feel fits 90% of the
organizations I consult with, if not more. The higher the level of the tests, the more
real dependencies they use, which gives us confidence in the overall system’s correct-
ness. The downside is that such tests are slower and flakier.
Most speed
• Easier to maintain
• Easier to write
• Faster feedback loop
Most conﬁdence
• Harder to maintain
• Harder to write
• Slower feedback loop
Conﬁdence
E2E/UI system tests
E2E/UI isolated tests
API tests (out of process)
Integration tests (in memory)
Component tests (in memory)
Unit tests (in memory)
Figure 10.1
Common software test levels 


---
**Page 196**

196
CHAPTER 10
Developing a testing strategy
Nice diagram, but what do we do with it? We use it when we design a framework for
decision making about which test to write. There are several criteria (things that
make our jobs easier or harder) I like to pinpoint; these help me decide which test
type to use.
10.1.1 Criteria for judging a test
When we’re faced with more than two options to choose from, one of the best ways
I’ve found to help me decide is to figure out what my obvious values are for the prob-
lem at hand. These obvious values are the things we can all pretty much agree are use-
ful or should be avoided when making the choice. Table 10.1 lists my obvious values
for tests.
All values are scaled from 1 to 5. As you’ll see, each level in figure 10.1 has pros and
cons in each of these criteria. 
10.1.2 Unit tests and component tests
Unit tests and component tests are the types of tests we’ve been discussing in this book
so far. They both fit under the same category, with the only differentiation being that
component tests might have more functions, classes, or components as part of the
unit of work. In other words, component tests include more “stuff” between the entry
and exit points.
 Here are two test examples to illustrate the difference:
Test A—A unit test of a custom UI button object in memory. You can instantiate
it, click it, and see that it triggers some form of click event. 
Test B—A component test that instantiates a higher-level form component and
includes the button as part of its structure. The test verifies the higher-level
form, with the button playing a small role as part of the higher-level scenario.
Table 10.1
Generic test scorecard
Criterion
Rating scale
Notes
Complexity
1–5
How complicated a test is to write, read, or debug. 
Lower is better. 
Flakiness
1–5
How likely a test is to fail because of things it does 
not control—code from other groups, networks, data-
bases, configuration, and more. Lower is better.
Confidence when passes
1–5
How much confidence is generated in our minds and 
hearts when a test passes. Higher is better.  
Maintainability
1–5
How often the test needs to change, and how easy it 
is to change. Higher is better. 
Execution speed
1–5
How quickly does the test finish? Higher is better. 


