# 1.3.4 Aiming at a particular coverage number (pp.15-15)

---
**Page 15**

15
What makes a successful test suite?
You can fall into numerous edge cases, and there’s no way to see if your tests account
for all of them.
 This is not to say that coverage metrics should take into account code paths in
external libraries (they shouldn’t), but rather to show you that you can’t rely on
those metrics to see how good or bad your unit tests are. Coverage metrics can’t
possibly tell whether your tests are exhaustive; nor can they say if you have enough
tests. 
1.3.4
Aiming at a particular coverage number
At this point, I hope you can see that relying on coverage metrics to determine the
quality of your test suite is not enough. It can also lead to dangerous territory if you
start making a specific coverage number a target, be it 100%, 90%, or even a moder-
ate 70%. The best way to view a coverage metric is as an indicator, not a goal in and
of itself.
 Think of a patient in a hospital. Their high temperature might indicate a fever and
is a helpful observation. But the hospital shouldn’t make the proper temperature of
this patient a goal to target by any means necessary. Otherwise, the hospital might end
up with the quick and “efficient” solution of installing an air conditioner next to the
patient and regulating their temperature by adjusting the amount of cold air flowing
onto their skin. Of course, this approach doesn’t make any sense.
 Likewise, targeting a specific coverage number creates a perverse incentive that
goes against the goal of unit testing. Instead of focusing on testing the things that
matter, people start to seek ways to attain this artificial target. Proper unit testing is dif-
ficult enough already. Imposing a mandatory coverage number only distracts develop-
ers from being mindful about what they test, and makes proper unit testing even
harder to achieve.
TIP
It’s good to have a high level of coverage in core parts of your system.
It’s bad to make this high level a requirement. The difference is subtle but
critical.
Let me repeat myself: coverage metrics are a good negative indicator, but a bad posi-
tive one. Low coverage numbers—say, below 60%—are a certain sign of trouble. They
mean there’s a lot of untested code in your code base. But high numbers don’t mean
anything. Thus, measuring the code coverage should be only a first step on the way to
a quality test suite. 
1.4
What makes a successful test suite?
I’ve spent most of this chapter discussing improper ways to measure the quality of a
test suite: using coverage metrics. What about a proper way? How should you mea-
sure your test suite’s quality? The only reliable way is to evaluate each test in the
suite individually, one by one. Of course, you don’t have to evaluate all of them at


