# 12.3 Practicing Continuous Integration (pp.241-243)

---
**Page 241**

disappear or are greatly simplified. Since everyone is in the room, you find
the problems sooner, you derive a better design that everyone can live with,
you converge on a team coding standard, you have all the expertise available
to use right now, and you write all the tests you need to write.
Most importantly (to me at least), mob sessions are usually a lot of fun, and
I often feel like we got a lot more done.
If you choose to practice either mob or pair programming, you’ll still end up
with some individual work product. Make sure you use a post facto review
process for this work.
Practicing Continuous Integration
“It works on my machine!” cries Joe. “Must be something wrong on yours,”
he says to Lucia.
Hearken to the call of the wild developer, heard ofttimes in olde shops that
weren’t practicing continuous integration (CI). With CI, all developers frequently
integrate their changes with the centralized repository (commonly in GitHub).
A tool known as a CI server monitors the repository. When the repository is
updated, the CI server triggers a new build and runs one or more sets of tests
prior to completion. The first of those test suites to execute is typically your
team’s unit tests.
CI demands a solid suite of fast unit tests.
CI servers can be hosted internally or available in the cloud. The most common
tools are Jenkins, GitHub Actions, and GitLab CI. Some alternative solutions
include Azure DevOps, CircleCI, and TeamCity.
5 Some of the tools are free,
some are licensed, and some are software as a service (SaaS).
The CI build’s tests verify that the integrated codebase works as expected. If
a developer pushes and any CI tests fail, the build fails and the team is notified
of the problem. The unit tests running in CI thus establish a centralized,
authoritative standard.
Broken CI tests indicate a system that cannot be deployed. Resolve
them before doing anything else.
5.
https://blog.jetbrains.com/teamcity/2023/07/best-ci-tools/
report erratum  •  discuss
Practicing Continuous Integration • 241


---
**Page 242**

Tools like Git can be configured to abort commit/push attempts
when unit tests fail locally.
CI is a foundation for practicing continuous deployment (CD), wherein each
successful build triggers a deployment to production. Amazon
6 and Netflix
7
are companies that deploy to production thousands of times daily using CD.
Conflicts and Merges
If two or more separate developers separately make changes to the same
codebase, it’s possible for their combined changes to break the system (even
though the individual contributions worked prior to integration). In order for
CI to work, each developer wishing to push must first pull the latest code
from the central repository. They run their fantastic unit test suite to ensure
nothing is broken and then push up what now becomes the latest version of
the system. If they don’t have a fantastic unit test suite, they must carefully
review the combined code first. (Corollary: folks without a fantastic unit test
suite or some other comprehensive test suite are not usually practicing CI.)
A healthy team that’s created a trustworthy test suite integrates frequently.
Some teams who practice TDD push up every TDD cycle, in other words, as often
as every few minutes. Once they get a new behavior working and clean up the
code, they integrate that new increment. This “continuous” aspect of CI helps
make it work and be successful. Feedback comes sooner and in smaller incre-
ments. It’s easier and faster to find and fix problems in such small increments.
In contrast, developers on less advanced teams defer integrating their changes
until a feature is complete. They typically make their changes on code
branches across the course of a day, a few days, and sometimes a few weeks.
The amount of new code that must subsequently be integrated can be consid-
erable, thus significantly likely to conflict with existing code.
Developers can spend hours, even days, managing a meticulous manual
merge process to integrate a long-lived branch. The correct technical term for
such a nightmare is “merge hell.” The duration of the nightmare often
increases proportionally with the age of the branch.
Better communication and division of labor can help minimize code conflicts
and merge hell. But consider also mob programming (see Active Review via
Mob Programming, on page 240).
6.
https://www.zdnet.com/article/how-amazon-handles-a-new-software-deployment-every-second/
7.
https://www.theserverside.com/feature/How-Netflix-built-tooling-for-multi-cloud-deployment
Chapter 12. Adopting Team Practices • 242
report erratum  •  discuss


---
**Page 243**

An Integration Process Checklist
Here’s a summary of your steps as a developer for practicing continuous
integration:
1.
Pull from your central repo to get your local codebase up to date.
2.
Change the code, running unit tests as you go.
3.
Pull from the repo to integrate any new changes from teammates.
4.
Manually review the incoming changes as appropriate.
5.
Run your tests to ensure that the integrated code works.
6.
Push your changes to the central repository.
Don’t advance to the next step if any of your tests are failing.
A CI process fosters healthy peer pressure against costly code. Developers
quickly habituate themselves to running their unit tests before check-in so
as not to waste their teammates’ time by causing the CI build process to fail.
A CI server is a minimum for building a modern development team.
Summary
You and your team must be on the same page when it comes to unit testing.
If it’s new to your team, it’ll take time to adopt and ingrain as a beneficial
habit. If it’s an existing practice, your team practices might need improvement.
In this chapter, you learned about establishing team-level standards for unit
testing from both implementation and process perspectives. You also learned
about the active review mechanisms that help ensure test quality—specifically,
mob and pair programming. Finally, you discovered the key role that CI plays
in unit testing.
Last up: times are changing rapidly. AI has dramatically made its way into
the software development arena. Unlike previous attempts (anyone remember
Prolog and 4GLs?), AI has made a ubiquitous impact not just in software
development but in day-to-day life for many of us. AI’s improvements are
accelerating and there’s little chance of its disappearance.
Yes, unit testing is quite relevant in the age of AI. Read on to discover how.
report erratum  •  discuss
Summary • 243


