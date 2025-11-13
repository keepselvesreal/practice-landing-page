# Integrating unit testing into the organization (pp.213-231)

---
**Page 213**

213
Integrating unit testing
into the organization
As a consultant, I’ve helped several companies, big and small, integrate continuous
delivery processes and various engineering practices, such as test-driven develop-
ment and unit testing, into their organizational culture. Sometimes this has failed,
but those companies that succeeded had several things in common. In any type of
organization, changing people’s habits is more psychological than technical. Peo-
ple don’t like change, and change is usually accompanied with plenty of FUD (fear,
uncertainty, and doubt) to go around. It won’t be a walk in the park for most peo-
ple, as you’ll see in this chapter.
11.1
Steps to becoming an agent of change
If you’re going to be the agent of change in your organization, you should first
accept that role. People will view you as the person responsible (and sometimes
This chapter covers
Becoming an agent of change
Implementing change from the top down or from 
the bottom up
Preparing to answer the tough questions about 
unit testing


---
**Page 214**

214
CHAPTER 11
Integrating unit testing into the organization
accountable) for what’s happening, whether or not you want them to, and there’s no
use in hiding. In fact, hiding can cause things to go terribly wrong.
 As you start to implement or push for changes, people will start asking tough ques-
tions related to what they care about. How much time will this “waste”? What does this
mean for me as a QA engineer? How do we know it works? Be prepared to answer. The
answers to the most common questions are discussed in section 11.5. You’ll find that
convincing others inside the organization before you start making changes will help
you immensely when you need to make tough decisions and answer those questions.
 Finally, someone will have to stay at the helm, making sure the changes don’t die
for lack of momentum. That’s you. There are ways to keep things alive, as you’ll see in
the next sections.
11.1.1 Be prepared for the tough questions
Do your research. Read the questions and answers at the end of this chapter, and look
at the related resources. Read forums, mailing lists, and blogs, and consult with your
peers. If you can answer your own tough questions, there’s a good chance you can
answer someone else’s.
11.1.2 Convince insiders: Champions and blockers
Few things make you feel as lonely in an organization as the decision to go against the
current. If you’re the only one who thinks what you’re doing is a good idea, there’s lit-
tle reason for anyone to make an effort to implement what you’re advocating. Con-
sider who can help and hurt your efforts: the champions and blockers.
CHAMPIONS
As you start pushing for change, identify the people you think are most likely to help
in your quest. They’ll be your champions. They’re usually early adopters, or people who
are open minded enough to try the things you’re advocating. They may already be
half convinced but are looking for an impetus to start the change. They may have even
tried it and failed on their own.
 Approach them before anyone else and ask for their opinions on what you’re
about to do. They may tell you some things that you hadn’t considered, including 
Teams that might be good candidates to start with 
Places where people are more accepting of such changes 
What (and who) to watch out for in your quest
By approaching them, you’re helping to ensure that they’re part of the process. Peo-
ple who feel part of the process usually try to help make it work. Make them your
champions: ask them if they can help you and be the ones people can come to with
questions. Prepare them for such events.
BLOCKERS
Next, identify the blockers. These are the people in the organization who are most
likely to resist the changes you’re making. For example, a manager might object to


---
**Page 215**

215
11.1
Steps to becoming an agent of change
adding unit tests, claiming that they’ll add too much time to the development effort
and increase the amount of code that needs to be maintained. Make them part of the
process instead of resisters of it by giving them (at least those who are willing and
able) an active role in the process.
 The reasons why people might resist changes vary. Answers to some of the possible
objections are covered in section 11.4 on influence forces. Some will be worried about
job security, and some will just feel too comfortable with the way things currently are.
Approaching potential blockers and detailing all the things they could have done bet-
ter is often not constructive, as I’ve found out the hard way. People don’t like to be
told that their baby is ugly. 
 Instead, ask blockers to help you in the process by being in charge of defining cod-
ing standards for unit tests, for example, or by doing code and test reviews with peers
every other day. Or make them part of the team that chooses the course materials or
outside consultants. You’ll give them a new responsibility that will help them feel
relied on and relevant in the organization. They need to be part of the change or
they’ll almost certainly undermine it.
11.1.3 Identify possible starting points
Identify where in the organization you can start implementing changes. Most success-
ful implementations take a steady route. Start with a pilot project in a small team, and
see what happens. If all goes well, move on to other teams and other projects.
 Here are some tips that will help you along the way:
Choose smaller teams.
Create subteams.
Consider project feasibility.
Use code and test reviews as teaching tools.
These tips can take you a long way in a mostly hostile environment.
CHOOSE SMALLER TEAMS
Identifying possible teams to start with is usually easy. You’ll generally want a small
team working on a low-profile project with low risks. If the risk is minimal, it’s easier to
convince people to try your proposed changes. 
 One caveat is that the team needs to have members who are open to changing the
way they work and to learning new skills. Ironically, the people with less experience on
a team are usually most likely to be open to change, and people with more experience
tend to be more entrenched in their way of doing things. If you can find a team with
an experienced leader who’s open to change, but that also includes less-experienced
developers, it’s likely that team will offer little resistance. Go to the team and ask their
opinion on holding a pilot project. They’ll tell you if this is (or is not) the right place
to start.


---
**Page 216**

216
CHAPTER 11
Integrating unit testing into the organization
CREATE SUBTEAMS
Another possible candidate for a pilot test is to form a subteam within an existing
team. Almost every team will have a “black hole” component that needs to be main-
tained, and while it does many things right, it also has many bugs. Adding features for
such a component is a tough task, and this kind of pain can drive people to experi-
ment with a pilot project. 
CONSIDER PROJECT FEASIBILITY
For a pilot project, make sure you’re not biting off more than you can chew. It takes
more experience to run more difficult projects, so you might want to have at least
two options—a complicated project and an easier project—so that you can choose
between them.
USE CODE AND TEST REVIEWS AS TEACHING TOOLS
If you’re the technical lead on a small team (up to eight people), one of the best ways
of teaching is instituting code reviews that also include test reviews. The idea is that as
you review other people’s code and tests, you teach them what you look for in the tests
and your way of thinking about writing tests or approaching TDD. Here are some tips:
Do the reviews in person, not through remote software. The personal connec-
tion lets much more information pass between you in nonverbal ways, so learn-
ing happens better and faster.
In the first couple of weeks, review every line of code that gets checked in. This
will help you avoid the “we didn’t think this code needs reviewing” problem. 
Add a third person to your code reviews—one who will sit on the side and learn
how you review the code. This will allow them to later do code reviews them-
selves and teach others, so that you won’t become a bottleneck for the team as
the only person capable of doing reviews. The idea is to develop others’ ability
to do code reviews and accept more responsibility.
If you want to learn more about this technique, I wrote about it in my blog for techni-
cal leaders: “What Should a Good Code Review Look and Feel Like?” at https://5whys
.com/blog/what-should-a-good-code-review-look-and-feel-like.html.
11.2
Ways to succeed
There are two main ways an organization or team can start changing a process: from
the bottom-up or the top-down (and sometimes both). The two ways are very differ-
ent, as you’ll see, and either could be the right approach for your team or company.
There’s no one right way.
 As you proceed, you’ll need to learn how to convince management that your efforts
should also be their efforts, or when it would be wise to bring in someone from outside
to help. Making progress visible is important, as is setting clear goals that can be mea-
sured. Identifying and avoiding obstacles should also be high on your list. There are
many battles that can be fought, and you need to choose the right ones.


---
**Page 217**

217
11.2
Ways to succeed
11.2.1 Guerrilla implementation (bottom-up)
Guerrilla-style implementation is all about starting out with a team, getting results,
and only then convincing other people that the practices are worthwhile. Usually the
driver for guerrilla implementation is a team who’s tired of doing things the pre-
scribed way. They set out to do things differently; they study on their own and make
changes happen. When the team shows results, other people in the organization may
decide to start implementing similar changes in their own teams.
 In some cases, guerrilla-style implementation is a process adopted first by develop-
ers and then by management. At other times, it’s a process advocated for first by devel-
opers and then by management. The difference is that you can accomplish the first
covertly, without the higher powers knowing about it. The latter is done in conjunc-
tion with management. It’s up to you to figure out which approach will work better.
Sometimes the only way to change things is by covert operations. Avoid this if you can,
but if there’s no other way, and you’re sure the change is needed, you can just do it.
 Don’t take this as a recommendation to make a career-limiting move. Developers
do things without permission all the time: debugging code, reading email, writing
code comments, creating flow diagrams, and so on. These are all tasks that developers
do as a regular part of the job. The same goes for unit testing. Most developers already
write tests of some sort (automated or not). The idea is to redirect the time spent on
tests into something that will provide benefits in the long term.
11.2.2 Convincing management (top-down)
The top-down move usually starts in one of two ways. A manager or a developer will
initiate the process and start the rest of the organization moving in that direction,
piece by piece. Or a mid-level manager may see a presentation, read a book (such as
this one), or talk to a colleague about the benefits of specific changes to the way they
work. Such a manager will usually initiate the process by giving a presentation to peo-
ple in other teams or even using their authority to make the change happen.
11.2.3 Experiments as door openers
Here’s a powerful way to get started with unit testing in a large organization (it could
also fit other types of transformation or new skills). Declare an experiment that will
last two to three months. It will apply to only one pre-picked team and relate to only
one or two components in a real application. Make sure it’s not too risky. If it fails, the
company won’t go under or lose a major client. It also shouldn’t be useless: the exper-
iment must provide real value and not just serve as a playground. It has to be some-
thing you’ll end up pushing into your codebase and use in production eventually; it
shouldn’t be a write-and-forget piece of code.
 The word “experiment” conveys that the change is temporary, and if it doesn’t
work out, the team can go back to the way they were before. Also, the effort is time-
boxed, so we know when the experiment is finished.


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


---
**Page 223**

223
11.3
Ways to fail
fail. I’ll discuss several others here, along with one that cost me that project, and some
things that can be done about them.
11.3.1 Lack of a driving force
In the places where I’ve seen change fail, the lack of a driving force was the most pow-
erful factor in play. Being a consistent driving force of change has its price. It will take
time away from your normal job to teach others, help them, and wage internal politi-
cal wars for change. You need to be willing to surrender time for these tasks, or the
change won’t happen. Bringing in an outside person, as mentioned in section 11.2.4,
will help you in your quest for a consistent driving force.
11.3.2 Lack of political support
If your boss explicitly tells you not to make the change, there isn’t a whole lot you can
do, besides trying to convince management to see what you see. But sometimes the
lack of support is much more subtle than that, and the trick is to realize that you’re
facing opposition. 
 For example, you may be told, “Sure, go ahead and implement those tests. We’re
adding 10% to your time to do this.” Anything below 30% isn’t realistic for beginning
a unit testing effort. This is one way a manager may try to stop a trend—by choking it
out of existence. 
 You need to recognize that you’re facing opposition, but once you know what to
look for, it’s easy to identify. When you tell them that their limitations aren’t realistic,
you’ll be told, “So don’t do it.”
11.3.3 Ad hoc implementations and first impressions
If you’re planning to implement unit testing without prior knowledge of how to write
good unit tests, do yourself one big favor: involve someone who has experience and
follow good practices (such as those outlined in this book). 
 I’ve seen developers jump into the deep water without a proper understanding of
what to do or where to start, and that’s not a good place to be. Not only will it take a
huge amount of time to learn how to make changes that are acceptable for your situa-
tion, but you’ll also lose a lot of credibility along the way for starting out with a bad
implementation. This can lead to the pilot project being shut down.
 If you read this book’s preface, you’ll know that this happened to me. You have
only a couple of months to get things up to speed and convince the higher-ups that
you’re achieving results with experiments. Make that time count, and remove any risks
that you can. If you don’t know how to write good tests, read a book or get a consul-
tant. If you don’t know how to make your code testable, do the same. Don’t waste time
reinventing testing methods.


---
**Page 224**

224
CHAPTER 11
Integrating unit testing into the organization
11.3.4 Lack of team support
If your team doesn’t support your efforts, it will be nearly impossible to succeed,
because you’ll have a hard time consolidating your extra work on the new process with
your regular work. You should strive to have your team be part of the new process or at
least not interfere with it. 
 Talk to your team members about the changes. Getting their support one by one is
sometimes a good way to start, but talking to them as a group about your efforts—and
answering their hard questions—can also prove valuable. Whatever you do, don’t take
the team’s support for granted. Make sure you know what you’re getting into; these
are the people you have to work with on a daily basis.
11.4
Influence factors
I’ve written and covered influencing behaviors as a full chapter in my book Elastic
Leadership (Manning, 2016). If you find this topic interesting, I recommend picking
that one up, or reading more about it at 5whys.com. 
 One of the things I find even more fascinating than unit tests is people and why
they behave the way they do. It can be very frustrating to try to get someone to start
doing something (like TDD, for example), and regardless of your best efforts, they
just won’t do it. You may have already tried reasoning with them, but you see they
don’t do anything in response to your little talk. 
 In the book Influencer: The Power to Change Anything (McGraw-Hill, 2007) by Kerry
Patterson, Joseph Grenny, David Maxfield, Ron McMillan, and Al Switzler, you’ll find
the following mantra (paraphrased):
For every behavior that you see, the world is perfectly designed for that behavior to
happen. That means that there are other factors besides the person wanting to do
something or being able to do it that influence their behavior. Yet we rarely look beyond
those two factors.
The book exposes us to six influence factors:
Personal ability—Does the person have all the skills or knowledge to perform
what is required? 
Personal motivation—Does the person take satisfaction from the right behavior
or dislike the wrong behavior? Do they have the self-control to engage in the
behavior when it’s hardest to do so?
Social ability—Do you or others provide the help, information, and resources
required by that person, particularly at critical times?
Social motivation—Are the people around them actively encouraging the right
behavior and discouraging the wrong behavior? Are you or others modeling the
right behavior in an effective way?
Structural (environmental) ability—Are there aspects in the environment (build-
ing, budget, and so on) that make the behavior convenient, easy, and safe? Are
there enough cues and reminders to stay on course?


---
**Page 225**

225
11.4
Influence factors
Structural motivation—Are there clear and meaningful rewards (such as pay,
bonuses, or incentives) when you or others behave the right or wrong way? Do
short-term rewards match the desired long-term results and behaviors you want
to reinforce or want to avoid?
Consider this a short checklist for starting to understand why things aren’t going your
way. Then consider another important fact: there might be more than one factor in
play. For the behavior to change, you should change all the factors in play. If you
change just one, the behavior won’t change.
 Table 11.1 is an example of an imaginary checklist about someone not performing
TDD. (Keep in mind that this will differ for each person in each organization.)
I put asterisks next to the items in the right column that require work. Here I’ve iden-
tified two issues that need to be resolved. Solving only the build machine budget prob-
lem won’t change the behavior. They have to get a build machine and deter their
managers from giving a bonus on shipping crappy stuff quickly.
Table 11.1
Influence factors checklist
Influence factor
Question to ask
Example answer 
Personal ability
Does the person have all the skills or knowl-
edge to perform what is required? 
Yes. They went through a 
three-day TDD course with 
Roy Osherove.
Personal motivation
Does the person take satisfaction from the 
right behavior or dislike the wrong behavior? 
Do they have the self-control to engage in 
the behavior when it’s hardest to do so?
I spoke with them, and they 
like doing TDD.
Social ability
Do you or others provide the help, informa-
tion, and resources required by that person, 
particularly at critical times?
Yes.
Social motivation
Are the people around them actively encour-
aging the right behavior and discouraging 
the wrong behavior?
Are you or others modeling the right behav-
ior in an effective way?
As much as possible.
Structural (environmen-
tal) ability
Are there aspects in the environment (build-
ing, budget, and so on) that make the behav-
ior convenient, easy, and safe?
Are there enough cues and reminders to 
stay on course?
They don’t have a budget for 
a build machine.*
Structural motivation
Are there clear and meaningful rewards 
(such as pay, bonuses, or incentives) when 
you or others behave the right or wrong way?
Do short-term rewards match the desired 
long-term results and behaviors you want to 
reinforce or want to avoid?
When they try to spend time 
unit testing, their managers 
tell them they’re wasting 
time. If they ship early and 
crappy, they get a bonus.*


---
**Page 226**

226
CHAPTER 11
Integrating unit testing into the organization
 I write much more on this in Notes to a Software Team Leader (Team Agile Publishing,
2014), a book about running a technical team. You can find it at 5whys.com.
11.5
Tough questions and answers
This section covers some questions I’ve come across in various places. They usually arise
from the premise that implementing unit testing can hurt someone personally—a man-
ager concerned about their deadlines or a QA employee concerned about their rele-
vance. Once you understand where a question is coming from, it’s important to address
the issue, directly or indirectly. Otherwise, there will always be subtle resistance.
11.5.1 How much time will unit testing add to the current process?
Team leaders, project managers, and clients are the ones who usually ask how much
time unit testing will add to the process. They’re the people at the front lines in terms
of timing. 
 Let’s begin with some facts. Studies have shown that raising the overall code quality
in a project can increase productivity and shorten schedules. How does this match up
with the fact that writing tests makes coding slower? Through maintainability and the
ease of fixing bugs, mostly.
NOTE
For studies on code quality and productivity, see Programming Productiv-
ity (McGraw-Hill College, 1986) and Software Assessments, Benchmarks, and Best
Practices (Addison-Wesley Professional, 2000), both by Capers Jones.
When asking about time, team leaders may really be asking, “What should I tell my
project manager when we go way past our due date?” They may actually think the pro-
cess is useful but be looking for ammunition for the upcoming battle. They may also
be asking the question not in terms of the whole product but in terms of specific fea-
ture sets or functionality. A project manager or customer who asks about timing, on
the other hand, will usually be talking in terms of full product releases.
 Because different people care about different scopes, your answers may vary. For
example, unit testing can double the time it takes to implement a specific feature, but
the overall release date for the product may actually be reduced. To understand this,
let’s look at a real example I was involved with.
A TALE OF TWO FEATURES
A large company I consulted with wanted to implement unit testing in their process,
beginning with a pilot project. The pilot consisted of a group of developers adding a
new feature to a large existing application. The company’s main livelihood was in cre-
ating this large billing application and customizing parts of it for various clients. The
company had thousands of developers around the world.
 The following measures were taken to test the pilot’s success:
The time the team spent on each of the development stages 
The overall time for the project to be released to the client
The number of bugs found by the client after the release


---
**Page 227**

227
11.5
Tough questions and answers
The same statistics were collected for a similar feature created by a different team for
a different client. The two features were nearly the same size, and the teams were
roughly at the same skill and experience level. Both tasks were customization efforts—
one with unit tests, the other without. Table 11.2 shows the differences in time.
Overall, the time it took to release with tests was less than without tests. Still, the man-
agers on the team with unit tests didn’t initially believe the pilot would be a success,
because they only looked at the implementation (coding) statistic (the first row in
table 11.2) as the criteria for success, instead of the bottom line. It took twice the
amount of time to code the feature (because unit tests require you to write more
code). Despite this, the extra time was more than compensated for when the QA team
found fewer bugs to deal with.
 That’s why it’s important to emphasize that although unit testing can increase the
amount of time it takes to implement a feature, the overall time requirements balance
out over the product’s release cycle because of increased quality and maintainability.
11.5.2 Will my QA job be at risk because of unit testing?
Unit testing doesn’t eliminate QA-related jobs. QA engineers will receive the applica-
tion with full unit test suites, which means they can make sure all the unit tests pass
before they start their own testing process. Having unit tests in place will actually make
their job more interesting. Instead of doing UI debugging (where every second but-
ton click results in an exception of some sort), they’ll be able to focus on finding more
logical (applicative) bugs in real-world scenarios. Unit tests provide the first layer of
defense against bugs, and QA work provides the second layer—the user acceptance
layer. As with security, the application always needs to have more than one layer of
protection. Allowing the QA process to focus on the larger issues can produce better
applications.
Table 11.2
Team progress and output measured with and without tests 
Stage
Team without tests
Team with tests
Implementation (coding)
7 days
14 days
Integration
7 days
2 days
Testing and bug fixing
Testing, 3 days 
Fixing, 3 days 
Testing, 3 days 
Fixing, 2 days 
Testing, 1 day
Total: 12 days
Testing, 3 days 
Fixing, 1 day
Testing, 1 day
Fixing, 1 day
Testing, 1 day
Total: 7 days
Overall release time
26 days
23 days
Bugs found in production
71
11


---
**Page 228**

228
CHAPTER 11
Integrating unit testing into the organization
 In some places, QA engineers write code, and they can help write unit tests for the
application. That happens in conjunction with the work of the application developers
and not instead of it. Both developers and QA engineers can write unit tests.
11.5.3 Is there proof that unit testing helps?
There aren’t any specific studies on whether unit testing helps achieve better code
quality that I can point to. Most related studies talk about adopting specific agile
methods, with unit testing being just one of them. Some empirical evidence can be
gleaned from the web, of companies and colleagues having great results and never
wanting to go back to a codebase without tests. A few studies on TDD can be found at
The QA Lead here: http://mng.bz/dddo. 
11.5.4 Why is the QA department still finding bugs?
You may not have a QA department anymore, but this is still a very prevalent practice.
Either way, you’ll still be finding bugs. Please use tests at multiple levels, as described
in chapter 10, to gain confidence across many layers of your application. Unit tests
give you fast feedback and easy maintainability, but they leave some confidence
behind, which can only be gained through some levels of integration tests. 
11.5.5 We have lots of code without tests: Where do we start?
Studies conducted in the 1970s and 1980s showed that, typically, 80% of bugs are
found in 20% of the code. The trick is to find the code that has the most problems.
More often than not, any team can tell you which components are the most prob-
lematic. Start there. You can always add some metrics related to the number of bugs
per class.
Testing legacy code requires a different approach than when writing new code with
tests. See chapter 12 for more details.
Sources for the 80/20 figure
Studies that show 80% of the bugs are in 20% of the code include the following:
Albert Endres, “An analysis of errors and their causes in system programs,” IEEE
Transactions on Software Engineering 2 (June 1975), 140–49; Lee L. Gremillion,
“Determinants of program repair maintenance requirements,” Communications of the
ACM 27, no. 8 (August 1984), 826–32; Barry W. Boehm, “Industrial software metrics
top 10 list,” IEEE Software 4, no. 9 (September 1987), 84–85 (reprinted in an IEEE
newsletter and available online at http://mng.bz/rjjJ); and Shull and others, “What
we have learned about fighting defects,” Proceedings of the 8th International Sympo-
sium on Software Metrics (2002), 249–58.


---
**Page 229**

229
Summary
11.5.6 What if we develop a combination of software and hardware?
You can use unit tests even if you develop a combination of software and hardware.
Look into the test layers mentioned in the previous chapter to make sure you cover
both software and hardware. Hardware testing usually requires the use of simulators
and emulators at various levels, but it is a common practice to have a suite of tests both
for low-level embedded and high-level code.
11.5.7 How can we know we don’t have bugs in our tests?
You need to make sure your tests fail when they should and pass when they should.
TDD is a great way to make sure you don’t forget to check those things. See chapter 1
for a short walk-through of TDD.
11.5.8 Why do I need tests if my debugger shows that my code works?
Debuggers don’t help much with multithreaded code. Also, you may be sure your
code works fine, but what about other people’s code? How do you know it works? How
do they know your code works and that they haven’t broken anything when they make
changes? Remember that coding is the first step in the life of the code. Most of its life,
the code will be in maintenance mode. You need to make sure it will tell people when
it breaks, using unit tests.
 A study held by Curtis, Krasner, and Iscoe (“A field study of the software design
process for large systems,” Communications of the ACM 31, no. 11 (November 1988),
1268–87) showed that most defects don’t come from the code itself but result from
miscommunication between people, requirements that keep changing, and a lack of
application domain knowledge. Even if you’re the world’s greatest coder, chances are
that if someone tells you to code the wrong thing, you’ll do it. When you need to
change it, you’ll be glad you have tests for everything else, to make sure you don’t
break it.
11.5.9 What about TDD?
TDD is a style choice. I personally see a lot of value in TDD, and many people find it
productive and beneficial, but others find that writing tests after the code is good
enough for them. You can make your own choice.
Summary
Implementing unit testing in their organization is something that many readers
of this book will have to face at one time or another.
Make sure that you don’t alienate the people who can help you. Recognize
champions and blockers inside the organization. Make both groups part of the
change process.


---
**Page 230**

230
CHAPTER 11
Integrating unit testing into the organization
Identify possible starting points. Start with a small team or project with a limited
scope to get a quick win and minimize project duration risks.
Make the progress visible to everyone. Aim for specific goals, metrics, and KPIs.
Take note of potential causes of failure, such as the lack of a driving force and
lack of political or team support.
Be prepared to have good answers to the questions you’re likely to be asked. 


---
**Page 231**

231
Working with legacy code
I once consulted for a large development shop that produced billing software.
They had over 10,000 developers and mixed .NET, Java, and C++ in products, sub-
products, and intertwined projects. The software had existed in one form or
another for over five years, and most of the developers were tasked with maintain-
ing and building on top of existing functionality. 
 My job was to help several divisions (using all languages) learn TDD techniques.
For about 90% of the developers I worked with, this never became a reality for sev-
eral reasons, some of which were a result of legacy code:
It was difficult to write tests against existing code.
It was next to impossible to refactor the existing code (or there wasn’t
enough time to do it).
Some people didn’t want to change their designs.
Tooling (or a lack of tooling) was getting in the way.
It was difficult to determine where to begin.
This chapter covers
Examining common problems with legacy code
Deciding where to begin writing tests


