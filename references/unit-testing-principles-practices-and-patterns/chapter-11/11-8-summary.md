# 11.8 Summary (pp.273-Back cover)

---
**Page 273**

273
Summary
inquiry.Approve(_dateTimeServer.Now);      
SaveInquiry(inquiry);
}
}
Of these two options, prefer injecting the time as a value rather than as a service. It’s
easier to work with plain values in production code, and it’s also easier to stub those
values in tests.
 Most likely, you won’t be able to always inject the time as a plain value, because
dependency injection frameworks don’t play well with value objects. A good compro-
mise is to inject the time as a service at the start of a business operation and then
pass it as a value in the remainder of that operation. You can see this approach in
listing 11.17: the controller accepts DateTimeServer (the service) but then passes a
DateTime value to the Inquiry domain class. 
11.7
Conclusion
In this chapter, we looked at some of the most prominent real-world unit testing use
cases and analyzed them using the four attributes of a good test. I understand that it
may be overwhelming to start applying all the ideas and guidelines from this book at
once. Also, your situation might not be as clear-cut. I publish reviews of other people’s
code and answer questions (related to unit testing and code design in general) on my
blog at https://enterprisecraftsmanship.com. You can also submit your own question
at https://enterprisecraftsmanship.com/about. You might also be interested in taking
my online course, where I show how to build an application from the ground up,
applying all the principles described in this book in practice, at https://unittesting-
course.com.
 You can always catch me on twitter at @vkhorikov, or contact me directly through
https://enterprisecraftsmanship.com/about. I look forward to hearing from you!
Summary
Exposing private methods to enable unit testing leads to coupling tests to
implementation and, ultimately, damaging the tests’ resistance to refactoring.
Instead of testing private methods directly, test them indirectly as part of the
overarching observable behavior.
If the private method is too complex to be tested as part of the public API that
uses it, that’s an indication of a missing abstraction. Extract this abstraction into
a separate class instead of making the private method public.
In rare cases, private methods do belong to the class’s observable behavior.
Such methods usually implement a non-public contract between the class and
an ORM or a factory.
Don’t expose state that you would otherwise keep private for the sole purpose
of unit testing. Your tests should interact with the system under test exactly the
same way as the production code; they shouldn’t have any special privileges.
Injects time as 
a plain value


---
**Page 274**

274
CHAPTER 11
Unit testing anti-patterns
Don’t imply any specific implementation when writing tests. Verify the produc-
tion code from a black-box perspective; avoid leaking domain knowledge to
tests (see chapter 4 for more details about black-box and white-box testing).
Code pollution is adding production code that’s only needed for testing. It’s an
anti-pattern because it mixes up test and production code and increases the
maintenance costs of the latter.
The necessity to mock a concrete class in order to preserve part of its function-
ality is a result of violating the Single Responsibility principle. Separate that
class into two classes: one with the domain logic, and the other one communi-
cating with the out-of-process dependency.
Representing the current time as an ambient context pollutes the production
code and makes testing more difficult. Inject time as an explicit dependency—
either as a service or as a plain value. Prefer the plain value whenever possible.


---
**Page 275**

275
index
A
AAA (arrange, act, and assert) pattern 42–49
avoiding if statements 44–45
avoiding multiple AAA sections 43–44
differentiating system under test 47–48
dropping AAA comments 48–49
overview 42–43
reusing code in test sections 246–252
in act sections 249–250
in arrange sections 246–249
in assert sections 250
section size 45–47
arrange section 45
number of assertions in assert 
section 47
sections larger than a single line 45–47
teardown phase 47
abstractions 198, 260
Active Record pattern 159
adapters 227
aggregates 157
ambient context 212
anti-patterns 212
code pollution 266–268
exposing private state 263–264
leaking domain knowledge to tests
264–266
mocking concrete classes 268–271
private methods 260–263
acceptability of testing 261–263
insufficient coverage 260–261
test fragility 260
time 271–273
as ambient context 271–272
as explicit dependency 272–273
API (application programming interface) 104, 
111, 133, 191, 195, 227, 264
missing abstractions 260
public vs. private 99
well-designed 100–101, 105, 108, 262
application behavior 57
application services layer 133–134
arrange, act, and assert pattern. See AAA 
pattern
assertion libraries, using to improve test 
readability 62–63
assertion-free testing 12–13
asynchronous communications 191
atomic updates 236
automation concepts 87–90
black-box vs. white-box testing 89–90
Test Pyramid 87–89
B
backward migration 233
bad tests 189
black-box testing 68, 89–90
Boolean switches 266–268
branch coverage metric 10–11
brittle tests 83–84, 116, 216
brittleness 86, 125
bugs 68, 79, 104, 175, 189
business logic 106–107, 156, 169, 
179
C
CanExecute/Execute pattern 172, 174
CAP theorem 86–87
captured data 208


---
**Page 276**

INDEX
276
circular dependencies 203
defined 202
eliminating 202–204
classical school of unit testing 30–37
dependencies 30–34
end-to-end tests 38–39
integration tests 37–39
isolation issue 27–30
mocks 114–116
mocking out out-of-process dependencies
115–116
using mocks to verify behavior 116
precise bug location 36
testing large graph of interconnected classes 35
testing one class at a time 34–35
cleanup phase 244
clusters, grouping into aggregates 157
code complexity 104, 152
code coverage metric 9–10
code coverage tools 90
code depth 157
code pollution 127, 266–268, 272
code width 157
collaborators 32, 148, 153
command query separation. See CQS principle
commands 97
communication-based testing 122–123, 128
feedback speed 124
maintainability 127
overuse of 124
protection against regressions and feedback 
speed 124
resistance to refactoring 124–125
vulnerability to false alarms 124
communications
between applications 107, 110
between classes in application 110, 116
conditional logic 169–180
CanExecute/Execute pattern 172–174
domain events for tracking changes in the 
domain model 175–178
constructors, reusing test fixtures between 
tests 52
containers 244
controllers 153, 225
simplicity 171
coverage metrics, measuring test suite quality 
with 8–15
aiming for particular coverage number 15
branch coverage metric 10–11
code coverage metric 9–10
problems with 12–15
code paths in external libraries 14–15
impossible to verify all possible outcomes
12–13
CQS (command query separation) principle
97–98
CRUD (create, read, update, and delete) 
operations 89
CSV files 208–209
cyclic dependency 202
cyclomatic complexity 152
D
data inconsistencies 241
data mapping 254
data motion 234
data, bundling 104
database backup, restoring 244
database management system (DBMS) 246
database testing
common questions 252–255
testing reads 252–253
testing repositories 253–254
database transaction management 234–243
in integration tests 242–243
in production code 235–242
prerequisites for 230–234
keeping database in source control 
system 230–231
reference data as part of database 
schema 231
separate instances for every developer
232
state-based vs. migration-based database 
delivery 232–234
reusing code in test sections 246–252
creating too many database 
transactions 251–252
in act sections 249–250
in arrange sections 246–249
in assert sections 250
test data life cycle 243–246
avoiding in-memory databases 246
clearing data between test runs 244–245
parallel vs. sequential test execution
243–244
database transaction management 234–243
in integration tests 242–243
in production code 235–242
separating connections from transactions
236–239
upgrading transaction to unit of work
239–242
database transactions 244
daysFromNow parameter 60
DBMS (database management system) 246
dead code 260
deliveryDate parameter 62


---
**Page 277**

INDEX
277
dependencies 28–29, 35
classical school of unit testing 30–34
London school of unit testing 30–34
out-of-process 161, 190
shared 29, 31
types of 115
Detroit approach, unit testing 21
diagnostic logging 206, 212
discovered abstractions 198
Docker container 28
domain events, tracking changes in domain 
model 175–178
domain layers 106–107, 109, 133–134
domain model 16, 153, 225
connecting with external applications 111
testability 171
domain significance 153
dummy test double 93–94
E
EasyMock 25
edge cases 187, 189, 194
encapsulation 46, 252
end-to-end tests 88–89, 195–196, 205, 222
classical school of unit testing 38–39
London school of unit testing 38–39
possibility of creating ideal tests 81
enterprise applications 5
Entity Framework 240–242, 255
entropy 6
error handling 146
exceptions 130
expected parameter 62
explicit inputs and outputs 130
external libraries 81
external reads 170–171, 173
external state 130
external writes 170–171, 173
F
Fail Fast principle 185, 189
failing preconditions 190
fake dependencies 93
fake test double 93–94
false negatives 76–77
false positives 69–70, 77, 82, 86, 96, 99, 124
causes of 71–74
importance of 78–79
fast feedback 81–86, 88, 99, 123, 252, 260
fat controllers 154
feedback loop, shortening 189
feedback speed 79–80, 124
fixed state 50
Fluent Assertions 62
fragile tests 96, 113
frameworks 81
functional architecture 128–134
defined 132–133
drawbacks of 146–149
applicability of 147–148
code base size increases 149
performance drawbacks 148
functional programming 128–131
hexagonal architecture 133–134
transitioning to output-based testing 135–146
audit system 135–137
refactoring toward functional 
architecture 140–145
using mocks to decouple tests from 
filesystem 137–140
functional core 132–133, 143–144, 156
functional programming 121
functional testing 38, 121, 128
G
Git 230–231
Given-When-Then pattern 43
GUI (graphical user interface) tests 38
H
handwritten mocks 94, 222
happy paths 187, 194, 239
helper methods 126–127
hexagonal architecture 106–107, 128, 156
defining 106–110
functional architecture 133–134
purpose of 107
hexagons 106, 108, 134
hidden outputs 131
high coupling, reusing test fixtures between 
tests 52
HTML tags 72
humble controller 160
Humble Object pattern 155, 157–158, 167, 271
humble objects 157
humble wrappers 155
I
ideal tests 80–87
brittle tests 83–84
end-to-end tests 81
possibility of creating 81
trivial tests 82–83
if statements 10–11, 44–45, 143, 152, 173–174
immutability 133


---
**Page 278**

INDEX
278
immutable classes 133
immutable core 132, 134
immutable events 176
immutable objects 30, 132
implementation details 99–105
incoming interactions 94–95
infrastructure code 16
infrastructure layer 202
in-memory databases 246
in-process dependencies 199–200
INSERT statements 231
integer type 14
integration testing
best practices 200–205
eliminating circular dependencies
202–204
making domain model boundaries 
explicit 200
multiple act sections 204–205
reducing number of layers 200–202
classical school of unit testing 37–39
database transaction management in
242–243
defined 186–190
example of 193–197
categorizing database and message bus 195
end-to-end testing 195–196
first version 196–197
scenarios 194
failing fast 188–190
interfaces for abstracting dependencies
197–200
in-process dependencies 199–200
loose coupling and 198
out-of-process dependencies 199
logging functionality 205–213
amount of logging 212
introducing wrapper on top of ILogger
207–208
passing around logger instances 212–213
structured logging 208–209
whether to test or not 205–206
writing tests for support and diagnostic 
logging 209–211
London school of unit testing 37–39
out-of-process dependencies 190–193
types of 190–191
when real databases are unavailable
192–193
working with both 191–192
role of 186–187
Test Pyramid 187
interconnected classes 34
internal keyword 99
invariant violations 46, 103
invariants 100, 103
isolation issue
classical school of unit testing 27–30
London school of unit testing 21–27
isSuccess flag 113
J
JMock 25
JSON files 208–209
L
logging functionality testing 205–213
amount of logging 212
introducing wrapper on top of ILogger
207–208
passing around logger instances 212–213
structured logging 208–209
whether to test or not 205–206
writing tests for support and diagnostic 
logging 209–211
London school of unit testing 30–37
dependencies 30–34
end-to-end tests 38–39
integration tests 37–39
isolation issue 21–27
mocks 114–116
mocking out out-of-process dependencies
115–116
using mocks to verify behavior 116
precise bug location 36
testing large graph of interconnected classes 35
testing one class at a time 34–35
loose coupling, interfaces for abstracting depen-
dencies and 198
M
maintainability 79–80, 85, 88, 99, 137, 148, 
252, 260
comparing testing styles 125–127
communication-based tests 127
output-based tests 125
state-based tests 125–127
managed dependencies 190, 192, 246
mathematical functions 128–131
merging domain events 177
message bus 190–192, 199, 220, 224
method signatures 128
method under test (MUT) 25
Microsoft MSTest 49
migration-based database delivery 232–234
missing abstractions 260
mock chains 127


---
**Page 279**

INDEX
279
mocking frameworks 25
mockist style, unit testing 21
Mockito 25
mocks 25, 254
best practices 225–227
for integration tests only 225
not just one mock per test 225–226
only mock types that you own 227
verifying number of calls 226
decoupling tests from filesystem 137–140
defined 25
London school vs. classical school 114–116
mocking out out-of-process 
dependencies 115–116
using mocks to verify behavior 116
maximizing value of 217–225
IDomainLogger 224–225
replacing mocks with spies 222–224
verifying interactions at system edges
219–222
mocking concrete classes 268–271
observable behavior vs. implementation 
details 99–105
leaking implementation details 100–105
observable behavior vs. public API 99–100
well-designed API and encapsulation
103–104
stubs 93–98
asserting interactions with stubs 96–97
commands and queries 97–98
mock (tool) vs. mock (test double) 94–95
types of test doubles 93–94
using mocks and stubs together 97
test doubles 25
test fragility 106–114
defining hexagonal architecture 106–110
intra-system vs. inter-system 
communications 110–114
model database 230
Model-View-Controller (MVC) pattern 157
Moq 25, 95, 226
MSTest 49
MUT (method under test) 25
mutable objects 132
mutable shell 132–133, 143–144
MVC (Model-View-Controller) pattern 157
N
naming tests 54–58
guidelines for 56
renaming tests to meet guidelines 56–58
NHibernate 240
noise, reducing 78
NSubstitute 25
NuGet package 49
NUnit 49, 51
O
object graphs 22–23
Object Mother 248
object-oriented programming (OOP) 63, 133
object-relational mapping (ORM) 163, 177, 
227, 240, 243, 254–255, 263
observable behavior 99, 105, 108, 115, 263
leaking implementation details 100–105
public API 99–100
well-designed API and encapsulation 103–104
OCP (Open-Closed principle) 198
OOP (object-oriented programming) 63, 133
Open-Closed principle (OCP) 198
operations 99, 104
orchestration, separating business logic from
169, 179
ORM (object-relational mapping) 163, 177, 
227, 240, 243, 254–255, 263
outcoming interactions 94–95
out-of-process collaborators 159–160
out-of-process dependencies 28, 33, 38–39, 
115, 125, 148, 160–161, 167, 170, 176, 
186, 200, 229
integration testing 190–193
interfaces for abstracting dependencies 199
types of 190–191
when real databases are unavailable
192–193
working with both 191–192
output value 121
output-based testing 120–121, 124, 128
feedback speed 124
maintainability 125
protection against regressions and feedback 
speed 124
resistance to refactoring 124–125
transitioning to functional architecture 
and 135–146
audit system 135–137
refactoring toward functional 
architecture 140–145
using mocks to decouple tests from 
filesystem 137–140
overcomplicated code 154
overspecification 96
P
parallel test execution 243–244
parameterized tests 59, 61
partition tolerance 86


---
**Page 280**

INDEX
280
performance 171
persistence state 189
preconditions 190
private APIs 99
private constructors 263
private dependencies 28–29, 31, 115
private keyword 99
private methods 260–263
acceptability of testing 261–263
insufficient coverage and 260–261
reusing test fixtures between tests 52–54
test fragility and 260
Product array 129
production code 8
protection against regressions 68–69, 81, 84–86, 
88, 99, 260
comparing testing styles 124
importance of false positives and false 
negatives 78–79
maximizing test accuracy 76–78
Public API 99, 109
pure functions 128
Q
queries 97
R
random number generators 29
read operations 252
readability 53
read-decide-act approach 148
refactoring 165
analysis of optimal test coverage 167–169
testing domain layer and utility code 167–168
testing from other three quadrants 168
testing preconditions 169
conditional logic in controllers 169–180
CanExecute/Execute pattern 172–174
domain events for tracking changes in the 
domain model 175–178
identifying code to refactor 152–158
four types of code 152–155
Humble Object pattern for splitting overcom-
plicated code 155–158
resistance to 69–71
comparing testing styles 124–125
importance of false positives and false 
negatives 78–79
maximizing test accuracy 76–78
to parameterized tests
general discussion 58–62
generating data for parameterized tests
60–62
toward valuable unit tests 158–167
application services layer 160–162
Company class 164–167
customer management system 158–160
making implicit dependencies explicit 160
removing complexity from application 
service 163–164
reference data 231, 234, 245
referential transparency 130
regression errors 8, 69, 82
regressions 7, 229
repositories 236–237, 241, 253
resistance to refactoring 69–71, 79–81, 83–85, 
88–90, 92–93, 99, 123, 260, 265
comparing testing styles 124–125
importance of false positives and false 
negatives 78–79
maximizing test accuracy 76–78
return statement 10
return true statement 10
reusability 53
S
scalability 7
sequential test execution 243–244
shallowness 124–125
shared dependencies 28–29, 31, 33, 115, 148, 246
side effects 130–134, 190
signal-to-noise ratio 212
Single Responsibility principle 157, 268, 270
single-line act section 45
SMTP service 110, 112–115, 134, 190
software bugs 7, 68
software entropy 6
source of truth 231
spies 94, 222–224
spy test double 93
SQL scripts 231–232, 240, 245
SQLite 246
state 99, 101
state verification 125
state-based database delivery 232
state-based testing 120–122, 124, 128, 135
feedback speed 124
maintainability 125–127
protection against regressions and feedback 
speed 124
resistance to refactoring 124–125
stubs, mocks 93–98
asserting interactions with stubs 96–97
commands and queries 97–98
mock (tool) vs. mock (test double) 94–95
types of test doubles 93–94
using mocks and stubs together 97


---
**Page 281**

INDEX
281
sub-renderers collection 105
support logging 206, 212
sustainability 7
sustainable growth 6
SUT (system under test) 24–25, 29, 36–37, 43, 
45, 47–48, 57, 71, 73–75, 84, 93–94, 96–97, 
120–121, 123, 153, 244, 264, 266
switch statement 10
synchronous communications 191
system leaks 100
T
tables 191
tautology tests 82
TDD (test-driven development) 36, 43
tell-don’t-ask principle 104
test code 8
test coverage 9
Test Data Builder 248
test data life cycle 243–246
avoiding in-memory databases 246
clearing data between test runs 244–245
parallel vs. sequential test execution
243–244
test doubles 22–23, 25, 28, 93–94, 98, 199
test fixtures 248
defined 50
reusing between tests
constructors 52
high coupling 52
private factory methods 52–54
reusing between tests 50–54
test fragility, mocks and 106–114
defining hexagonal architecture 106–110
intra-system vs. inter-system 
communications 110–114
test isolation 115
Test Pyramid
general discussion 87–89
integration testing 187
test suites
characteristics of successful suites 15–17
integration into development cycle 16
maximum value with minimum maintenance 
costs 17
targeting most important parts of code 
base 16–17
coverage metrics, measuring test suite quality 
with 8–15
aiming for particular coverage number 15
branch coverage metric 10–11
code coverage metric 9–10
problems with 12–15
third-party applications 81, 112
tight coupling 5
time 271–273
as ambient context 271–272
as explicit dependency 272–273
trivial code 153–154
trivial tests 82–83
true negative 76
true positive 76
two-line act section 46
U
UI (user interface) tests 38
unit of behavior 56, 225
unit of work 239, 242
unit testing
anatomy of 41–63
AAA pattern 42–49
assertion libraries, using to improve test 
readability 62–63
naming tests 54–58
refactoring to parameterized tests 58–62
reusing test fixtures between tests 50–54
xUnit testing framework 49–50
automation concepts 87–90
black-box vs. white-box testing 89–90
Test Pyramid 87–89
characteristics of successful test suites 15–17
integration into development cycle 16
maximum value with minimum maintenance 
costs 17
targeting most important parts of code 
base 16–17
classical school of 30–37
dependencies 30–34
end-to-end tests 38–39
integration tests 37–39
isolation issue 27–30
precise bug location 36
testing large graph of interconnected 
classes 35
testing one class at a time 34–35
coverage metrics, measuring test suite quality 
with 8–15
aiming for particular coverage number 15
branch coverage metric 10–11
code coverage metric 9–10
problems with 12–15
current state of 4–5
defined 21–30
four pillars of 68–80
feedback speed 79–80
maintainability 79–80
protection against regressions 68–69
resistance to refactoring 69–71


---
**Page 282**

INDEX
282
unit testing (continued)
functional architecture 128–134
defined 132–133
drawbacks of 146–149
functional programming 128–131
hexagonal architecture 133–134
transitioning to output-based testing
135–146
goal of 5–8
good vs. bad tests 7–8
ideal tests 80–87
brittle tests 83–84
end-to-end tests 81
possibility of creating 81
trivial tests 82–83
London school of 30–37
dependencies 30–34
end-to-end tests 38–39
integration tests 37–39
isolation issue 21–27
precise bug location 36
testing large graph of interconnected 
classes 35
testing one class at a time 34–35
styles of 120–123
communication-based testing
122–123
comparing 123–128
output-based testing 120–121
state-based testing 121–122
units of behavior 34
units of code 21, 27–29, 34, 47, 225
unmanaged dependencies 190, 199, 211, 216, 
218, 220, 222, 226, 254
user controller 193
user interface (UI) tests 38
V
value objects 31, 126–127
void type 97
volatile dependencies 29
W
white-box testing 89–90
write operation 252
X
xUnit testing framework 49–50
Y
YAGNI (You aren’t gonna need it) principle
198–199


---
**Page Back cover**

Vladimir Khorikov
G
reat testing practices will help maximize your project 
quality and delivery speed. Wrong tests will break your 
code, multiply bugs, and increase time and costs. You 
owe it to yourself—and your projects—to learn how to do 
excellent unit testing to increase your productivity and the 
end-to-end quality of your software.
Unit Testing: Principles, Practices, and Patterns teaches you to 
design and write tests that target the domain model and 
other key areas of your code base. In this clearly written 
guide, you learn to develop professional-quality test suites, 
safely automate your testing process, and integrate testing 
throughout the application life cycle. As you adopt a testing 
mindset, you’ll be amazed at how better tests cause you to 
write better code. 
What’s Inside
● Universal guidelines to assess any unit test
● Testing to identify and avoid anti-patterns
● Refactoring tests along with the production code
● Using integration tests to verify the whole system
For readers who know the basics of unit testing. The C# 
examples apply to any language.
Vladimir Khorikov is an author, blogger, and Microsoft MVP. 
He has mentored numerous teams on the ins and outs of 
unit testing.
To download their free eBook in PDF, ePub, and Kindle formats, owners 
of this book should visit www.manning.com/books/unit-testing
$49.99 / Can $65.99  [INCLUDING eBOOK]
Unit Testing Principles, Practices, and Patterns
TESTING/SOFTWARE DEVELOPMENT
M A N N I N G
“
This book is an
 indispensable resource.”
 
—Greg Wright
Kainos Software Ltd.
“
Serves as a valuable and 
humbling encouragement 
to double down and test 
well, something we need 
no matter how experienced 
  we may be.”
 
—Mark Nenadov, BorderConnect
“
I wish I had this book 
twenty years ago when I was 
starting my career in 
  software development.”
—Conor Redmond
Incomm Product Control 
“
This is the kind of book 
on unit testing I have been 
 waiting on for a long time.”
 
—Jeremy Lange, G2
See first page
ISBN-13: 978-1-61729-627-7
ISBN-10: 1-61729-627-9


