# 10.2.2 The low-level-only test antipattern (pp.202-204)

---
**Page 202**

202
CHAPTER 10
Developing a testing strategy
WHEN THIS ANTIPATTERN HAPPENS
These are some reasons why I see this happen:
Separation of duties—Separate QA and development departments with separate
pipelines (automated build jobs and dashboards) exist in many organizations.
When a QA department has its own pipeline, it is likely to write more tests of
the same kind. Also, a QA department tends to write only a specific type of
test—the ones they’re used to and are expected to write (sometimes based on
company policy).
An “if it works, don’t change it” mentality—A group might start with E2E tests and
see that they like the results. They continue to add all their new tests in the
same way, because it’s what they know, and it has proven to be useful. When the
time it takes to run tests gets too long, it’s already too late to change direction
(which relates to the next point).
Sunk-costs fallacy—“We have lots of these types of tests, and if we changed them
or replaced them with lower-level tests, it would mean we’ve wasted all that time
and effort on tests that we are removing.” This is a fallacy, because maintaining,
debugging, and understanding test failures costs a fortune in human time. If
anything, it costs less to delete such tests (keeping only a few basic scenarios)
and get that time back. 
SHOULD YOU AVOID E2E TESTS COMPLETELY?
No, we can’t avoid E2E tests. One of the good things they offer is confidence that the
application works. It’s a completely different level of confidence compared to unit
tests, because they test the integration of the full system, with all of its subsystems
and components, from the point of view of a user. When they pass, the feeling you
get is huge relief that the major scenarios you expect your users to encounter actu-
ally work.
 So don’t avoid them entirely. Instead, I highly recommend minimizing the number
of E2E tests. We’ll talk about what that minimum is in section 10.3.3.
10.2.2 The low-level-only test antipattern
The opposite of having only E2E tests is to have low-level tests only. Unit tests provide
fast feedback, but they don’t provide the amount of confidence needed to fully trust
that your application works as a single integrated unit (see figure 10.3). 
 In this antipattern, the organization’s automated tests are mostly or exclusively low-
level tests, such as unit tests or component tests. There may be hints of integration
tests, but there are no E2E tests in sight.
 The biggest issue with this is that the confidence level you get when these types of
tests pass is simply not enough to feel confident that your application works. That
means people will run the tests and then continue to do manual debugging and test-
ing to get the final sense of confidence needed to release something. Unless what
you’re shipping is a code library that’s meant to be used in the way your unit tests are


---
**Page 203**

203
10.2
Test-level antipatterns
using it, this won’t be enough. Yes, the tests will run quickly, but you’ll still spend lots
of time manually testing and verifying. 
 This antipattern often happens when your developers are only used to writing low-
level tests, if they don’t feel comfortable writing high-level tests, or if they expect the
QA people to write those types of tests.
 Does that mean you should avoid unit tests? Obviously not. But I highly recom-
mend that you have not only unit tests but also higher-level tests. We’ll discuss this rec-
ommendation in section 10.3. 
Conﬁdence
E2E/UI system tests
E2E/UI isolated tests
API tests (out of process)
Integration tests (in memory)
Component tests (in memory)
Unit tests (in memory)
Scenario
1
Scenario
1.6
Scenario
1.2
Scenario
1.10
Scenario
1.4
Scenario
1.5
Scenario
1.9
Figure 10.3
Low-level-only test antipattern


---
**Page 204**

204
CHAPTER 10
Developing a testing strategy
10.2.3 Disconnected low-level and high-level tests
This pattern might seem healthy at first, but it really isn’t. It might look a bit like fig-
ure 10.4.
Yes, you want to have both low-level tests (for speed) and high-level tests (for confi-
dence). But when you see something like this in an organization, you will likely
encounter one or more of these anti-behaviors:
Many of the tests repeat in multiple levels.
The people who write the low-level tests are not the same people who write the
high-level tests. This means they don’t care about each other’s test results, and
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
Scenario
1
Scenario
1.1
Scenario
1.2
Scenario
1.3
Scenario
1.4
Scenario
1.5
Scenario
1
Scenario
1.6
Scenario
1.2
Scenario
1.10
Scenario
1.4
Scenario
1.5
Scenario
1.9
Figure 10.4
Disconnected low-level and high-level tests


