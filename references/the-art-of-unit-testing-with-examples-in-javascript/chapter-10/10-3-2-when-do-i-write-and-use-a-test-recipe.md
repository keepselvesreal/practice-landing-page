# 10.3.2 When do I write and use a test recipe? (pp.207-207)

---
**Page 207**

207
10.3
Test recipes as a strategy
Unit test – Check profile update logic with bad email
Unit test – Profile update logic with same email
Unit test – Profile serialization/deserialization
10.3.2 When do I write and use a test recipe?
Just before you start coding a feature or a user story, sit down with another person and
try to come up with various scenarios to be tested. Discuss at which level that scenario
should be best tested. This meeting will usually be no longer than 5 to 15 minutes,
and after it, coding begins, including the writing of the tests. (If you’re doing TDD,
you’ll start with the tests.)
 In organizations where there are automation or QA roles, the developer will write
the lower-level tests, and the QA will focus on writing the higher-level tests, while cod-
ing of the feature is taking place. Both people are working at the same time. One does
not wait for the other to finish their work before starting to write their tests.
 If you are working with feature toggles, they should also be checked as part of the
tests, so that if a feature is off, its tests will not run.
10.3.3 Rules for a test recipe
There are several rules to follow when writing a test recipe:
Faster—Prefer writing tests at lower levels, unless a high-level test is the only way
for you to gain confidence that the feature works.
Confidence—The recipe is done when you can tell yourself, “If all these tests
passed, I’ll feel pretty good about this feature working.” If you can’t say that,
write more scenarios that will allow you to say that.
Revise—Feel free to add or remove tests from the list as you code. Just make
sure you notify the other person you worked with on the recipe.
Just in time—Write this recipe just before starting to code, when you know who
is going to code it.
Pair—Don’t write it alone if you can help it. People think in different ways, and
it’s important to talk through the scenarios and learn from each other about
testing ideas and mindset.
Don’t repeat yourself from other features—If this scenario is already covered by an
existing test (perhaps an E2E test from a previous feature), there is no need to
repeat this scenario at that level.
Don’t repeat yourself from other layers—Try not to repeat the same scenario at multi-
ple levels. If you’re checking a successful login at the E2E level, lower-level tests
should only check variations of that scenario (logging in with different provid-
ers, unsuccessful login results, etc.). 
More, faster—A good rule of thumb is to end up with a ratio of at least one to
five between levels (for one E2E test, you might end up with five or more lower-
level tests).


