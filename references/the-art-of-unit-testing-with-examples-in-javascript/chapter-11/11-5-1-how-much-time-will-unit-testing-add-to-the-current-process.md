# 11.5.1 How much time will unit testing add to the current process? (pp.226-227)

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


