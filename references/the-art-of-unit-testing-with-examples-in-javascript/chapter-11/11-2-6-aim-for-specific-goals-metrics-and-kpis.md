# 11.2.6 Aim for specific goals, metrics, and KPIs (pp.220-222)

---
**Page 220**

220
CHAPTER 11
Integrating unit testing into the organization
Set up a big-screen display that’s always showing, in big bold graphics, the status
of the builds, what’s currently running, and what’s failing. Put that in a visible
place where all developers can see—in a well-trafficked corridor, for example,
or at the top of the team room’s main wall.
Your aim in using these charts is to connect with two groups: 
The group undergoing the change—People in this group will gain a greater feeling
of accomplishment and pride as the charts (which are open to everyone) are
updated, and they’ll feel more compelled to complete the process because it’s
visible to others. They’ll also be able to keep track of how they’re doing com-
pared to other groups. They may push harder, knowing that another group
implemented specific practices more quickly.
Those in the organization who aren’t part of the process—You’re raising interest and
curiosity among these people, triggering conversations and buzz, and creating a
current that they can join if they choose.
11.2.6 Aim for specific goals, metrics, and KPIs
Without goals, the change will be hard to measure and to communicate to others. It
will be a vague “something” that can easily be shut down at the first sign of trouble.
LAGGING INDICATORS
At the organizational level, unit tests are generally part of a bigger set of goals, usually
related to continuous delivery. If that’s the case for you, I highly recommend using the
four common DevOps metrics:
Deployment frequency—How often an organization successfully releases to pro-
duction.
Lead time for changes—The time it takes a feature request to get into production.
Note that many places incorrectly publish this as the amount of time it takes a
commit to get into production, which is only a part of the journey that a feature
goes through, from an organizational standpoint. If you’re measuring from
commit time, you’re closer to measuring the “cycle time” of a feature from com-
mit up to a specific point. Lead time is made up of multiple cycle times. 
Escaped bugs/change failure rate—The number of failures found in production
per some unit, usually release, deployment, or time. You can also use the per-
centage of deployments causing a failure in production.
Time to restore service—How long it takes an organization to recover from a fail-
ure in production.
These four are what we’d call lagging indicators, and they’re very hard to fake (although
they’re pretty easy to measure in most places). They are great in making sure we do
not lie to ourselves about the results of experiments.


---
**Page 221**

221
11.2
Ways to succeed
LEADING INDICATORS
Often we’d like faster feedback to ensure that we’re going the right way. That’s where
leading indicators come in. Leading indicators are things we can control on a day-to-day
basis—code coverage, number of tests, build run time, and more. They are easier to
fake, but combined with lagging indicators, they can often provide us with early signs
that we might be going the right way.
 Figure 11.2 shows a sample structure and ideas for lagging and leading indicators
you can use in your organization. You can find a high-resolution image with color at
https://pipelinedriven.org/article/a-metrics-framework-for-continuous-delivery.
INDICATOR CATEGORIES AND GROUPS
I usually break up leading indicators into two groups:
Team level—Metrics that an individual team can control
Engineering management level—Metrics that require cross-team collaboration or
aggregate metrics across multiple teams
I also like to categorize them based on what they will be used to solve:
Progress—Used to solve visibility and decision making on the plan
Bottlenecks and feedback—As the name implies
Quality—Escaped bugs in production
Figure 11.2
An example of a metrics framework for use in continuous delivery


---
**Page 222**

222
CHAPTER 11
Integrating unit testing into the organization
Skills—Track that we are slowly removing knowledge barriers inside teams or
across teams
Learning—Acting like we’re a learning organization
QUALITATIVE METRICS
The metrics are mostly quantitative (i.e., they are numbers that can be measured), but
a few are qualitative, in that you ask people how they feel or think about something.
The ones I use are
How confident you are that the tests can and will find bugs in the code if they
arise (from 1 to 5)? Take the average of the responses from the team members
or across multiple teams.
Does the code do what it is supposed to do (from 1 to 5)?
These are surveys you can ask at each retrospective meeting, and they take five min-
utes to answer. 
TREND LINES ARE YOUR FRIEND
For all leading and lagging indicators, you want to see trend lines, not just snapshots of
numbers. Lines over time is how you see if you’re getting better or worse. 
 Don’t fall into the trap of having a nice dashboard with large numbers on it. Num-
bers without context are not good or bad. Trend lines tell you if you’re better this
week than you were last week. 
11.2.7 Realize that there will be hurdles
There are always hurdles. Most will come from within the organizational structure,
and some will be technical. The technical ones are easier to fix, because it’s a matter
of finding the right solution. The organizational ones need care and attention and a
psychological approach.
 It’s important not to surrender to a feeling of temporary failure when an iteration
goes bad, tests go slower than expected, and so on. It’s sometimes hard to get going,
and you’ll need to persist for at least a couple of months to start feeling comfortable
with the new process and to iron out all the kinks. Have management commit to con-
tinuing for at least three months even if things don’t go as planned. It’s important to
get their agreement up front. You don’t want to be running around trying to convince
people in the middle of a stressful first month.
 Also, absorb this short realization, shared by Tim Ottinger on Twitter (@Tottinge):
“If your tests don’t catch all defects, they still make it easier to fix the defects they
didn’t catch. It is a profound truth.”
 Now that we’ve looked at ways of ensuring things go right, let’s look at some things
that can lead to failure.
11.3
Ways to fail
In the preface to this book, I talked about one project I was involved with that failed,
partly because unit testing wasn’t implemented correctly. That’s one way a project can


