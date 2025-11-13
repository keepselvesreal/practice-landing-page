# 11.4 Influence factors (pp.224-226)

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


