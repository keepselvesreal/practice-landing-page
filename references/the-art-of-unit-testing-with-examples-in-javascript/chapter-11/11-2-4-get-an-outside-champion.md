# 11.2.4 Get an outside champion (pp.218-219)

---
**Page 218**

218
CHAPTER 11
Integrating unit testing into the organization
 Such an approach helps people feel more at ease with big changes, because it
reduces the risk to the organization, the number of people affected (and thus the
number of people objecting), and the number of objections relating to fear of chang-
ing things “forever.” 
 Here’s another hint: when faced with multiple options for an experiment, or if you
get objections pushing for another way of working, ask, “Which idea do we want to
experiment with first?”
WALK THE WALK
Be prepared that your idea might not be selected from among all the options for an
experiment. When push comes to shove, you have to hold experiments based on what
the consensus of leadership decides, whether you like it or not.
 The nice thing about going with other people’s experiments is that, like with
yours, they are time-boxed and temporary! The best outcome might be that another
approach fixes what you were trying to fix, and you might want to keep someone else’s
experiment going. However, if you hate the experiment, just remember that it’s tem-
porary, and you can push for the next experiment.
METRICS AND EXPERIMENTS
Be sure to record a baseline set of metrics before and after the experiment. These
metrics should be related to things you’re trying to change, such as eliminating wait-
ing times for a build, reducing the lead time for a product to go out the door, or
reducing the number of bugs found in production.
 To dive deeper into the various metrics you might use, take a look at my talk “Lies,
Damned Lies, and Metrics,” which you can find in my blog at https://pipelinedriven
.org/article/video-lies-damned-lies-and-metrics. 
11.2.4 Get an outside champion
I highly recommend getting an outside person to help with the change. An outside
consultant coming in to help with unit testing and related matters has advantages over
someone who works in the company: 
Freedom to speak—A consultant can say things that people inside the company
may not be willing to hear from someone who works there (“The code integrity
is bad,” “Your tests are unreadable,” and so on). 
Experience—A consultant will have more experience dealing with resistance
from the inside, coming up with good answers to tough questions, and knowing
which buttons to push to get things going. 
Dedicated time—For a consultant, this is their job. Unlike other employees in the
company who have better things to do than push for change (like writing soft-
ware), the consultant does this full time and is dedicated to this purpose. 
I’ve often seen a change break down because an overworked champion doesn’t have
the time to dedicate to the process.


---
**Page 219**

219
11.2
Ways to succeed
11.2.5 Make progress visible
It’s important to keep the progress and status of the change visible. Hang white-
boards or posters on walls in corridors or in the food-related areas where people
congregate. The data displayed should be related to the goals you’re trying to achieve.
For example:
Show the number of passing or failing tests in the last nightly build. 
Keep a chart showing which teams are already running an automated build
process. 
Put up a Scrum burndown chart of iteration progress or a test-code-coverage
report (as shown in figure 11.1) if that’s what you have your goals set to. (You
can learn more about Scrum at www.controlchaos.com.) 
Put up contact details for yourself and all the champions, so someone can
answer any questions that arise. 
Figure 11.1
An example of a test-code-coverage report in TeamCity with NCover


