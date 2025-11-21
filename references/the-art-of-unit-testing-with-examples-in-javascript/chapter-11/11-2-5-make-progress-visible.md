# 11.2.5 Make progress visible (pp.219-220)

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


