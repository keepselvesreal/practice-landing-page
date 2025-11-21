# 11.1.3 Identify possible starting points (pp.215-216)

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


