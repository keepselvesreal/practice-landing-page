# 13.11 Summary (pp.264-280)

---
**Page 264**

Will using an LLM speed you up? I believe the answer will be increasingly
yes. For now, it will speed you up at least as much as any auto-code-complete
mechanisms speed you up. You’re typing far less, for one.
Personally, I can go considerably faster than an LLM for some pieces of pro-
ducing a solution, particularly around small adjustments to the way I want
the code expressed. But there are many operations that LLMs can do faster
than me. For example, it was quicker to change the array-based tuple to a
record than it would have been by hand. It’s also a lot faster to have the LLM
generate tests from examples.
Maybe my biggest speed-up is that I can take larger steps with an LLM than
with TDD, where I do one small thing at a time. Sure, AI will get some things
wrong as a result of the larger steps, but it’s a lot quicker to revert and try
something different when it does.
Summary
In Pragmatic Unit Testing in Java with JUnit, you’ve learned a wealth of
approaches, skills, practices, and design tips. You can apply these skills
immediately to your work and start to reap the multiple benefits of unit testing.
Whether or not you use AI to generate code, unit testing will remain an
important tool in your development toolbox. Without good unit tests, you will
always proceed with considerable risk. Done properly, unit tests will allow
you to go faster and ship with high confidence.
Chapter 13. Keeping AI Honest with Unit Tests • 264
report erratum  •  discuss


---
**Page 265**

Bibliography
[Bec02]
Kent Beck. Test-Driven Development: By Example. Addison-Wesley, Boston,
MA, 2002.
[HT03]
Andy Hunt and Dave Thomas. Pragmatic Unit Testing in Java with JUnit
(out of print). The Pragmatic Bookshelf, Dallas, TX, 2003.
[LN17]
Diana Larsen and Ainsley Nies. Liftoff, Second Edition (audio book). The
Pragmatic Bookshelf, Dallas, TX, 2017.
[Mar08]
Robert C. Martin. Clean Code: A Handbook of Agile Software Craftsmanship.
Prentice Hall, Englewood Cliffs, NJ, 2008.
report erratum  •  discuss


---
**Page 267**

Index
SYMBOLS
! (not) operator, tagging tests,
140
& (and) operator, tagging
tests, 140
{} (braces), omitting, xxii
| (or) operator, tagging tests,
140
A
AAA (Arrange, Act, Assert)
approach
in list examples, 45
scannability and, 18–20
setup and teardown, 123
streamlining tests, 195–
197, 203, 207
team standards for, 237
abstractions
Dependency Inversion
Principle (DIP), 172
missing, 197–199
readability and, 20–22
streamlining tests, 195–
199
ACC (atomic code concepts),
26–31
acceptance testing, xix
act step, see also AAA (Ar-
range, Act, Assert) ap-
proach
defined, 18
test organization, 203
action methods, see com-
mand methods
actual vs. expected value in as-
sertEquals, 15
@AfterAll, cleanup with, 125
@AfterEach
cleanup with, 125
databases and transac-
tion handling, 87
AI (artificial intelligence), 245–
264
CAX cycle, 263
coding style and, 247, 
251–252, 257
development of, 243–245
exercise, 262
providing examples to,
248
tools, 246
units approach, 248, 262
untrustworthiness of,
245, 263
allMatch (AssertJ), 119
Amazon, 242
ampersand (&), tagging tests,
140
and matcher (Mockito), 61
and operator (&), tagging
tests, 140
annotations
abstraction with, 20–22
expecting exceptions, 113
anyMatch (AssertJ), 119
anyString() (Mockito), 61
Apache Software Foundation,
5
arguments, order of in asser-
tions, 10, 16
@ArgumentsSource, 134
arrange step, see also AAA
(Arrange, Act, Assert) ap-
proach
mocks and, 67
streamlining tests, 207
using, 18–20
Arrange, Act, Assert ap-
proach, see AAA (Arrange,
Act, Assert) approach
artificial intelligence, see AI
(artificial intelligence)
assert step, see also AAA (Ar-
range, Act, Assert) ap-
proach
defined, 18
mocks and, 67
streamlining tests, 195–
197
assertAll, 111
assertArrayEquals, 102
assertDoesNotThrow, 115
assertEquals
about, 10
comparison between actual
and expected values, 15
floating-point values, 49
precision in assertions,
196
using, 100–103
assertFalse, 104
assertInstanceOf, 111
assertIterableEquals, 111
assertLinesMatch, 111
assertNotEquals, 105–107
assertNotNull, 110
assertNotSame, 108
assertNull, 110


---
**Page 268**

assertSame, 107
assertThrows, 50, 112
assertTimeout, 111
assertTimeout Preemptively, 111
assertTrue, 100
AssertionFailedError, 15–16, 99
assertions
core forms, 100–118
custom, 196
defined, 99
design and, 40
eliminating non-tests,
121
fluent assertions with
AssertJ, 99, 104, 118–
121
generalized, 101
inverting, 99, 116
messages, 103
multiple, streamlining,
200–202
order of arguments, 10, 
16
precision in, 196
single-statement asser-
tions, 40, 196
team standards for, 237
third-party libraries, 118–
121
weak, 105–107, 111
AssertJ
custom matchers, 197
fluent assertions, 99, 
104, 118–121
asserts, see assertions
assessing tests in CAX cycle,
263
assumptions, JUnit feature,
142
atomic code concepts (ACC),
26–31
Azure DevOps, 241
B
bar (|), tagging tests, 140
Beck, Kent, 24
@BeforeAll, setup with, 124
@BeforeEach
abstraction with, 20–22
databases and transac-
tion handling, 87
moving irrelevant details
to, 203
setup with, 124, 127–130
test-driven development
(TDD) example, 216
behavior-driven development,
191
bloated construction, 199
BlockingQueue, 80
boundary conditions
approaches to, 32, 51
CORRECT approach, 51
braces ({}), omitting, xxii
branch coverage, 71, 76
C
caching, 165
calculations
checking in tests, 49
mathematical computa-
tions and inverted as-
sertions, 118
verifying distance calcula-
tions, 47
cardinality, boundary condi-
tions and, 52
CAX cycle, 263
chaining methods, AssertJ,
119, 121
ChatGPT
coding style and, 247, 
251–252, 257
providing examples to,
248
testing with, 246–262
untrustworthiness of,
245, 263
checked exceptions, 116
CircleCI, 241
classes, see also test classes
extracting, 173–180
mapping to concepts, 180
names, 190
nested, 126–130, 136, 
191
Open-Closed Principle
(OCP), 172
running multiple tests in,
136
Single Responsibility
Principle, 170–180
SOLID design principles,
172
team standards for, 237
Clean Code, 187
clean code
characteristics of, 147
refactoring and, 187
cleaning, databases, 87–90
cleanup, see teardown
clutter, removing, 22, 100–
102, 192, 202
code
for this book, xx, 5–6
clean, 147, 187
dead code, 73
legacy code, streamlining,
193
style and AI, 247, 251–
252, 257
style for this book, xxii
testing common circum-
stances, 41–51
typing vs. pasting, 5–6
unnecessary test code,
streamlining, 194
code coverage, 71–79
branch coverage, 71, 76
condition coverage, 71, 
74–77
design and, 78
function coverage, 71
integration testing and,
89
level of, xvii, 77
line coverage, 71–74
merging metrics, 89
method coverage, 73
mocks, 68
path coverage, 71
statement coverage, 71–
74
test-driven development
(TDD), 78, 231
tools, 71, 73
code reviews, 237–241
command methods, 36
command-query separation
(CQS), 170, 180–182
comments
assertion messages and,
103
cautions about, 103
vs. names, 189, 192
removing, 195
commits, test-driven develop-
ment (TDD), 215
concepts
atomic code concepts
(ACC), 26–31
design and, 25–31
extracting, 159–162
implementing as meth-
ods, 31
mapping classes to, 180
refactoring with, 158–167
Index • 268


---
**Page 269**

concision
AssertJ and, 120
clean code and, 147
design and, 26–31
extracting methods, 157
readability and, 22
concurrency analysis tools,
80
concurrent code
JUnit feature, 143
testing, 79–84
conditionals
code coverage, 71, 74–77
common test situations,
44
extracting, 153
JUnit feature, 143
confidence
advantages of unit test-
ing, 35
in code by others, 35
design and, 170
fast tests and, 67
refactoring and, 148, 154
running tests after small
changes, 154
test-driven development
(TDD) and, 212, 219, 
231
conflicts in continuous inte-
gration, 242
conformance, boundary con-
ditions and, 52
console output standards,
237
constants, names, 192, 198
constructors, dependency in-
jection with, 56–58
consumer methods, verifying
a method was called, 63
contains (AssertJ), 119
contains (Mockito), 61
containsPattern (AssertJ), 119
context
implicit meaning, 204
naming tests, 190
continuous deployment, 242
continuous integration, 241–
243
continuous integration
servers, 241
costs, maintenance, 182
coupling
SOLID design principles,
172
temporal, 181
CQS (command-query separa-
tion), 170, 180–182
creating tests and code in
CAX cycle, 263
@CsvSource, 132–134
D
data
fuzz testing, 92
implicit meaning, 204
integration tests, 87–90
parameterized tests, 131–
134
viewing after tests, 89
data providers, fuzz testing,
92
databases
cleaning, 87–90
integration tests, 87–90
viewing data after tests,
89
dead code, 73
deadlocks, 80
delegation testing, 184–187
dependency injection
frameworks, 58, 62, 68
with mocks, 61–63
options for, 58
stubs, 56–58
Dependency Inversion Princi-
ple (DIP), 172
design
AI (artificial intelligence)
and, 246–264
assertions and, 40
bloated construction, 199
changeability and, 38
cleanup and, 125
cleanup and AI, 260–262
code coverage and, 78
command-query separa-
tion, 170, 180–182
concepts and, 25–31
concision, 26–31
confidence and, 170
flexibility, 187
functions and, 32–38
impure functions and,
34–38
intent and, 33, 165
multithreaded code and,
80
pure functions and, 32–
33
refactoring and, 169–188
Single Responsibility
Principle, 170–180
small methods and, 31
SOLID design principles,
172
speculative design, 239
test names and, 51
test-driven development
(TDD) and, 51
units and, 25–27
Developer Testing, 90
DIP (Dependency Inversion
Principle), 172
directories
temporary directory JUnit
feature, 143
for tests, 5
@Disabled, 140
disabling tests, 140–142
distance calculations, verify-
ing, 47
documentation
test names as, 19, 40, 
103, 190–192
test-driven development
(TDD) and, 231
tests as, 22, 189–192, 
195
drivers, mob programming,
240
dynamic analysis tooling, 80
dynamic testing, JUnit fea-
ture, 143
E
Eclipse, xix
edge cases
fuzz testing, 90–93
property testing, 93–95
empty tests, 6–8
endsWith (AssertJ), 119
ensemble programming,
see pair programming
@EnumSource, 134
exceptional conditions, ap-
proaches to, 32, 51
exceptions
about, 12
checked, 116
handling with try/catch,
113–115
ignoring, 194
Index • 269


---
**Page 270**

messages, 15
throwing exceptions and
mocks, 65
throwing exceptions
when a list condition is
met, 49–51
thrown during test execu-
tion, 16, 99
verifying that exceptions
are thrown, 112–118
exclamation point (!), tagging
tests, 140
executing tests in CAX cycle,
263
existence, boundary condi-
tions and, 52
expected vs. actual value in as-
sertEquals, 15
extracting
classes, 173–180
concepts, 159–162
methods, 153–154, 157
F
factories, dependency injec-
tion, 58
factory methods, dependency
injection, 58
Fagan inspections, 237
failing tests, see also excep-
tions
with assertThrows, 50
failure messages, 14
fluent assertions with
AssertJ, 99, 104, 120
information on, 11
making tests fail, 14–16
test-driven development
(TDD) and, 16
Feathers, Michael, 172
feedback
continuous integration
and, 242
number of tests to run
and, 136
filtering tests, with groups,
137–140
fixtures, setup and teardown,
123–130
floating-point values, 49
fluent assertions with As-
sertJ, 99, 104, 118–121
four-phase tests, 123
function coverage, 71
functions
design and, 32–38
pure functions, 32–33
side effects, 34–38
futures, multithreaded code
testing, 81–84
fuzz testing, 90–93
@FuzzTest, 92
G
generalized assertions, 101
generative testing, 90–95
Git, test-driven development
(TDD), 215
GitHub Actions, 241
GitHub and pull requests,
237
GitLab CI, 241
given-when-then naming pat-
tern, 191
Google Guice, 58, 62
Gradle
code for this book, xxi
disabled tests, 141
filtering tests, 138
IDE configuration, 8
Grenning, James, 32
H
Hamcrest, 118
happy path approach, 8
HashMap
defined, 220
multithreaded code test-
ing, 81–84
test-driven development
(TDD), 220, 222
headings, names, 49
helper methods
bloated construction, 199
moving irrelevant details
to, 203
hooks, abstraction with JU-
nit, 20–22
Hunt, Andy, 51
I
IDEs, see also IntelliJ IDEA
about, 4
automated refactoring,
158
configuration and Gradle,
8
keyboard shortcuts, 11, 
158
learning about, 17
options, xix
project view, 13
running single tests, 136
iloveyouboss example
fuzz testing, 90–93
integration testing, 84–90
multithreaded code, 80–
84
refactoring examples,
149–167, 170–188
immutability, records and, 39
implicit meaning and readabil-
ity, 204
impure functions, 31, 264,
see also functions
initialization, abstracting with
hooks and annotations, 20–
22
integration testing
about, xix
code coverage and, 89
speed, 86
testing multithreaded
code as, 79
writing tests, 84–90
IntelliJ IDEA
about, xix
code coverage tool, 71, 
73, 76
directories for tests, 6
disabling tests, 141
extracting methods, 153
inlining variables, 157
moving methods, 155
project view, 13
running single tests, 136
screenshots, 4
tag expressions, 139
tagging tests, 138–140
test classes, creating, 6
test summaries, 8
intent
deleting code and, 74
design and, 33, 165
Interface Segregation Princi-
ple (ISP), 172
inverting assertions, 99, 116
isEqualTo (AssertJ), 119
isInstanceOf (AssertJ), 119
isNotEqualTo (AssertJ), 119
isolation
extracting methods for
clarity, 153
Index • 270


---
**Page 271**

integration tests and, 87–
90
test classes, 10
ISP (Interface Segregation
Principle), 172
J
JaCoCo, 89
jacoco:merge, 89
Java
about, xix
coding style and AI, 247, 
251–252, 257
Persistence API, 84
versions, xix
Java Persistence API (JPA),
84
Jazzer, 92
Jenkins, 241
JMeter, 163
JPA (Java Persistence API),
84
jqwik, 93
JUnit, see also assertions;
setup; teardown; ZOM ap-
proach
about, xviii–xix
adding items to a list, 42
additional features, 142
assertion forms, core,
100–118
data source mechanisms,
133
disabling tests temporari-
ly, 140–142
empty test example, 6–8
executing tests, 135–143
grouping tests, 137–140
ignoring exceptions, 194
lifecyle, 127–130
new instances for each
test, 129
number of tests to run,
135–137
ordering tests, 130
organizing tests, 123–134
parameterized tests, 131–
134
versions, xix
JUnitPerf, 163
L
Large Language Models,
see LLMs (Large Language
Models)
Lea, Doug, 80
legacy code, streamlining, 193
lifecycle methods, 124–126
line breaks, 19
line coverage, 71–74
Liskov Substitution Principle
(LSP), 172
lists
adding items to, 41–44
AssertJ, 119
common testing circum-
stances, 41–51
conditionals and, 44
throwing exceptions
when a condition is
met, 49–51
updating/removing items
that match a predicate,
45–49
lists, test, 24, 206
LLMs (Large Language Mod-
els)
exercise, 262
mistakes, 245
providing examples to,
248
testing with, 246–264
untrustworthiness of,
263
locks, 80
LSP (Liskov Substitution
Principle), 172
M
magic literals, 197
maintenance
complexity and, 147
costs, 182
many-based testing
adding items to a list, 42
pure functions, 33
test-driven development
(TDD), 218
writing tests, 22–24
map example of updating list
items that match a predi-
cate, 45
maps, synchronized, 83
Martin, Robert C., 172
matchers
missing abstractions, 196
Mockito, 61
matches() method
command-query separa-
tion, 180–182
extracting classes exam-
ple, 173–180
refactoring example, 149–
162
mathematical computations
and inverted assertions,
118
Maven, 138
memory
assertNotSame and, 108
assertSame and, 107
merges, continuous integra-
tion and, 242
messages, assertion, 14, 103,
see also fluent assertions
method coverage, 73
methods
chaining in AssertJ, 119, 
121
command methods, 36
design and, 31
extracting, 153–154, 157
factory methods, 58
implementing concepts
as, 31
implementing units as,
26
method coverage, 73
moving in refactoring,
154–157, 174–180
names, 48, 157
order, 21, 69
spying on, 69
stringing concepts togeth-
er, 26
team standards for, 237
understanding policy,
153
verifying a method was
called with mocks, 63–
65
@MethodSource, 134
mob programming, 240, 242
mock method (Mockito), 60
Mockito
about, 60, 69
dependency injection, 61–
63
syntax, 62
throwing exceptions, 65
using, 60
verifying a method was
called, 63–65
mocks
exception handling, 65
speed and, 63, 66, 68
Index • 271


---
**Page 272**

syntax, 62
team standards for, 237
tips for, 67
using, 59–68
verifying a method was
called, 63–65
moving
cleanup after, 177–180
methods, 154–157, 174–
180
multithreaded code, 79–84
mutability, design and, 35, 
39
mutation testing, 90
N
names
classes, 190
constants, 192, 198
display names and JUnit,
143
headings, 49
methods, 48, 157
test classes, 126, 191
variables, 192
names, test
assertion messages and,
103
design and, 51
as documentation, 19, 
40, 103, 190–192
IntelliJ IDEA and, 6
length of, 190
readability, 40, 143, 190
renaming, 153
with sentences, 10
team standards for, 237
navigators, mob program-
ming, 240
@Nested, 126
nested classes, 126–130, 
136, 191
NetBeans, xix
Netflix, 242
non-tests, eliminating, 121
not operator (!), tagging tests,
140
null values
assertNotNull, 110
assertNull, 110
boundary conditions and,
52
null checks as zero-based
tests, 33
removing unnecessary
test code, 195
O
OCP (Open-Closed Principle),
172
one-based testing
pure functions, 33
test-driven development
(TDD), 216, 219, 221, 
227
writing tests, 14–17
Open-Closed Principle (OCP),
172
or operator (|), tagging tests,
140
order
arguments in assertions,
10, 16
AssertJ, 118
@BeforeEach, 125
boundary conditions, 52
JUnit tests, 130
methods, 21, 69
readability of expres-
sions, 179
tag expressions, 140
organization
directories for tests, 5
JUnit tests, 123–134
nested classes, 126–130
parameterized tests, 131–
134
setup/teardown hooks,
123–130
streamlining, 203
Ottinger, Tim, 32
P
pair programming, 239
“Pair Programming Benefits”,
239
“Pair Programming in a
Flash”, 239
pair swapping, 239
parameterized tests, 37, 131–
134
@ParameterizedTest, 132
pasting vs. typing code, 5–6
path coverage, 71
performance, see speed
PicoContainer, 62
policy, method, 153
portfolio example of test-driv-
en development (TDD),
213–231
predicates, updating/remov-
ing items that match, 45–
49
private modifier, omitting, 22
@Property, 94
property testing, 90, 93–95
public modifier, omitting, 22, 
100
pull requests (PRs), 237
pure functions, 32–33
Q
query separation, see com-
mand-query separation
R
readability
abstraction and, 20–22
clutter, removing, 22, 
100–102
concision and, 22
double-negatives, 179
fluent assertions with
AssertJ, 99, 104, 118–
121
implicit meaning, 204
line breaks and, 19
scannability, 18–20
streamlining tests, 207
test names, 40, 143, 190
tips for, 17–22
records, immutability of, 39
refactoring
with abstractions, 195–
199
advantages, 154
automated, 158
bloated construction, 199
with command-query
separation, 170, 180–
182
with conceptual analysis,
158–167
costs, 182
defined, 147–148
with delegation tests,
184–187
design and, 169–188
with extraction, 153–
154, 157, 159–162, 
173–180
with helper methods,
159–162
implicit meaning and,
204
irrelevant details, 202
Index • 272


---
**Page 273**

keyboard shortcuts for,
158
legacy code, 193
micro level, 147–168
with moving methods,
154–157, 174–180
multiple assertions,
streamlining, 200–202
performance and, 162–
166, 205
performance probe, 163–
166
removing temporary vari-
ables, 157
with renaming, 153
Single Responsibility
Principle, 170–180
with splitting tests, 192
streamlining tests, 189–
207
test-driven development
(TDD) and, 224
unnecessary test code,
194
reference, boundary condi-
tions and, 52
regression tests inputs and
Jazzer, 93
regular expressions, AssertJ,
119
renaming, refactoring with,
153
repositories, continuous inte-
gration, 241
resources, SOLID class-de-
sign principles, 172
reviews, see code reviews
@Rule, 114
rules, expecting exceptions,
113
runtime, generating tests at,
143
S
scannability
line breaks and, 19
with stepwise approach,
18–20
service classes, delegation
tests, 185
setters, dependency injection,
58
setup
hooks, 20–22, 123–130
moving irrelevant details
to, 203
side effects
command-query separa-
tion, 180
verifying, 34–38
Single Responsibility Principle
(SRP), 170–180
single-statement assertions,
40, 196
smart stubs, 58
SOLID class-design princi-
ples, 172
source control, test-driven
development (TDD), 215
Sources Root (IntelliJ IDEA),
6
speculative design, 239
speed
dependency injection
with Mockito, 63
importance of fast tests,
66
integration tests, 86
measuring, 66, 163–166
mocks and, 63, 66, 68
multithreaded code, 79–
80, 84
number of tests to run,
135
performance tools, 163
refactoring and, 162–
166, 205
running tests concurrent-
ly, 143
speculating on vs. data
on, 163
Spring DI, 58, 62
SRP (Single Responsibility
Principle), 170–180
standards, teams and, 236
startsWith (AssertJ), 119
statement coverage, 71–74
stepwise approach
scannability and, 18–20
streamlining tests, 195–
197
streamlining tests, 189–207
abstractions, 195–199
bloated construction, 199
implicit meaning, 204
irrelevant details, 202
legacy code, 193
multiple assertions, 200–
202
organization, 203
readability and, 207
unnecessary test code,
194
strings, assertLinesMatch, 111
stubs, 55–59
suites, JUnit feature, 143
synchronization blocks, test-
ing concurrent code, 80
synchronized maps, 83
T
tag expressions, 139
tagging tests, 137–140
Tarlinder, Alexander, 90
TDD, see test-driven develop-
ment (TDD)
team chartering, 236
TeamCity, 241
teams, 235–243
active reviews, 239–241
continuous deployment,
242
continuous integration,
241–243
mob programming, 240, 
242
pair programming, 239
pair swapping, 239
post-facto reviews, 237, 
241
reviews, 237–241
standards, 236
working agreements and
team chartering, 236
teardown, hooks, 123–130
temporary variables, remov-
ing, 157
@Test annotation, 113
test classes
creating, 6
isolation, 10
names, 126, 191
nested, 126–130, 136, 
191
splitting, 126
test doubles
address retriever exam-
ple, 53–68
defined, 53
minimizing use, 68
mocks, 59–68
stubs, 55–59
test-driven development
(TDD), 226
tips for, 67
Index • 273


---
**Page 274**

test lists, 24, 206
test objects, 43
Test Sources Root (IntelliJ
IDEA), 6
test summaries, 8, 202
test-after development, 231
test-driven development
(TDD), 211–233
advantages, 212
code coverage, 78, 231
confidence and, 212, 
219, 231
continuous integration,
242
cycle, 212, 231–232
defined, xxi
demonstrating failure
first, 16
design and, 51
example, 213–231
refactoring, 224
rhythm of, 232
rise of, xviii
test doubles, 226
vs. test-after develop-
ment, 231
writing tests first, 211
testSearch() method refactoring
test example, 192–206
testing, see also design; test-
driven development (TDD);
unit testing
acceptance, xix
integration, xix, 79, 84–
90
thenThrow (Mockito), 66
Thomas, Dave, 51
ThreadWeaver, 80
time, boundary conditions
and, 52
timeouts
assertions for, 111
JUnit feature, 143
transactions, database test-
ing, 87
transformations, automated
refactoring, 158
Truth, 118
try/catch
removing unnecessary
test code, 194
throwing exceptions,
113–115
type checking, AssertJ, 119
typing vs. pasting code, 5–6
U
unit testing, see also design;
names, test; refactoring;
test-driven development
(TDD); ZOM approach
advantages, 3
common code circum-
stances, 41–51
defined, xviii
disabling tests temporari-
ly, 140–142
edge cases, 90–95
empty test example, 6–8
happy path approach, 8
history and development
of, xvii
number to run, 135–137
ordering approaches, 8
ordering tests, 130
running a number of
times, 143
running tests concurrent-
ly, 143
splitting tests, 192, 201
tests as documentation,
22, 189–192, 195
when to use, xviii
units
approach to AI, 248, 262
defined, 25
design and, 25–27
implementing as meth-
ods, 26
updates, concurrent code
and, 80
V
@ValueSource, 134
variables
names, 192
removing temporary, 157
verify (Mockito), 64
VisualVM, 80
W
Wake, Bill, 20
weak assertions, 105–107, 
111
when (Mockito), 62, 65
working agreements, 236
Y
YourKit, 80
Z
zero-based testing
adding items to a list, 42
pure functions, 32
test-driven development
(TDD), 214, 219, 223, 
227
writing, 9–13
ZOM approach
adding items to a list, 42
generating tests with AI,
257
many-based testing, 22–
24, 33, 42, 218
one-based testing, 14–
17, 33, 216, 219, 221, 
227
pure functions, 32–33
test-driven development
(TDD), 214, 216, 218–
219, 221, 223, 227
zero-based testing, 9–13, 
32, 42, 214, 219, 223, 
227
ZOMBIES approach, 32
Index • 274


---
**Page 275**

Thank you!
We hope you enjoyed this book and that you’re already thinking about what
you want to learn next. To help make that decision easier, we’re offering
you this gift.
Head on over to https://pragprog.com right now, and use the coupon code
BUYANOTHER2024 to save 30% on your next ebook. Offer is void where
prohibited or restricted. This offer does not apply to any edition of The
Pragmatic Programmer ebook.
And if you’d like to share your own expertise with the world, why not propose
a writing idea to us? After all, many of our best authors started off as our
readers, just like you. With up to a 50% royalty, world-class editorial services,
and a name you trust, there’s nothing to lose. Visit https://pragprog.com/become-
an-author/ today to learn more and to get started.
Thank you for your continued support. We hope to hear from you again
soon!
The Pragmatic Bookshelf
SAVE 30%!
Use coupon code
BUYANOTHER2024


---
**Page 276**

Functional Programming in Java, Second Edition
Imagine writing Java code that reads like the problem
statement, code that’s highly expressive, concise, easy
to read and modify, and has reduced complexity. With
the functional programming capabilities in Java, that’s
not a fantasy. This book will guide you from the famil-
iar imperative style through the practical aspects of
functional programming, using plenty of examples.
Apply the techniques you learn to turn highly complex
imperative code into elegant and easy-to-understand
functional-style code. Updated to the latest version of
Java, this edition has four new chapters on error
handling, refactoring to functional style, transforming
data, and idioms of functional programming.
Venkat Subramaniam
(274 pages) ISBN: 9781680509793. $53.95
https://pragprog.com/book/vsjava2e
Java by Comparison
Improve your coding skills by comparing your code to
that of expert programmers so you can write code that’s
clean, concise, and to the point: code that others will
read with pleasure and reuse. Get hands-on advice to
level up your coding style through small and under-
standable examples that compare flawed code to an
improved solution. Discover handy tips and tricks, as
well as common bugs an experienced Java programmer
needs to know. Make your way from a Java novice to
a master craftsman.
Simon Harrer, Jörg Lenhard, Linus Dietz
(206 pages) ISBN: 9781680502879. $40.95
https://pragprog.com/book/javacomp


---
**Page 277**

Automate Your Home Using Go
Take control of your home and your data with the
power of the Go programming language. Build extraor-
dinary and robust home automation solutions that rival
much more expensive, closed commercial alternatives,
using the same tools found in high-end enterprise
computing environments. Best-selling Pragmatic
Bookshelf authors Ricardo Gerardi and Mike Riley
show how you can use inexpensive Raspberry Pi
hardware and excellent, open source Go-based software
tools like Prometheus and Grafana to create your own
personal data center. Using the step-by-step examples
in the book, build useful home automation projects
that you can use as a blueprint for your own custom
projects.
Ricardo Gerardi and Mike Riley
(160 pages) ISBN: 9798888650509. $40.95
https://pragprog.com/book/gohome
Small, Sharp Software Tools
The command-line interface is making a comeback.
That’s because developers know that all the best fea-
tures of your operating system are hidden behind a
user interface designed to help average people use the
computer. But you’re not the average user, and the
CLI is the most efficient way to get work done fast.
Turn tedious chores into quick tasks: read and write
files, manage complex directory hierarchies, perform
network diagnostics, download files, work with APIs,
and combine individual programs to create your own
workflows. Put down that mouse, open the CLI, and
take control of your software development environment.
Brian P. Hogan
(326 pages) ISBN: 9781680502961. $38.95
https://pragprog.com/book/bhcldev


---
**Page 278**

Seven Obscure Languages in Seven Weeks
Explore seven older computer languages and discover
new and fresh ideas that will change the way you think
about programming. These languages were invented
before we settled into our current C-style syntax and
OO biases, so language designers were free to imagine
what was possible. You’ll find their insights thought-
provoking, and their ideas will inspire you to try differ-
ent (and possibly more productive) ways of program-
ming. From a text manipulation language where every
line is a potential state machine event, to a concurrent
language where everything is done using actors, you’re
sure to come away from these seven languages inspired
and excited.
Dmitry Zinoviev
(270 pages) ISBN: 9798888650639. $55.95
https://pragprog.com/book/dzseven
Test-Driven React, Second Edition
Turn your React project requirements into tests and
get the feedback you need faster than ever before.
Combine the power of testing, linting, and typechecking
directly in your coding environment to iterate on React
components quickly and fearlessly!
Trevor Burnham
(172 pages) ISBN: 9798888650653. $45.95
https://pragprog.com/book/tbreact2


---
**Page 279**

Become a Great Engineering Leader
As you step into senior engineering leadership roles,
you need to make an impact, and you need to make it
fast. This book will uncover the secrets of what it
means to be a successful director of engineering, VP
of engineering, or CTO. With a hands-on, practical
approach, it will help you understand and develop the
skills that you need, ranging from how to manage
other managers, to how to define and execute strategy,
how to manage yourself and your limited time, and
how to navigate your own career journey to your de-
sired destination.
James Stanier
(400 pages) ISBN: 9798888650660. $64.95
https://pragprog.com/book/jsenglb
Machine Learning in Elixir
Stable Diffusion, ChatGPT, Whisper—these are just a
few examples of incredible applications powered by
developments in machine learning. Despite the ubiquity
of machine learning applications running in produc-
tion, there are only a few viable language choices for
data science and machine learning tasks. Elixir’s Nx
project seeks to change that. With Nx, you can leverage
the power of machine learning in your applications,
using the battle-tested Erlang VM in a pragmatic lan-
guage like Elixir. In this book, you’ll learn how to
leverage Elixir and the Nx ecosystem to solve real-world
problems in computer vision, natural language process-
ing, and more.
Sean Moriarity
(372 pages) ISBN: 9798888650349. $61.95
https://pragprog.com/book/smelixir


---
**Page 280**

The Pragmatic Bookshelf
The Pragmatic Bookshelf features books written by professional developers for professional
developers. The titles continue the well-known Pragmatic Programmer style and continue
to garner awards and rave reviews. As development gets more and more difficult, the Prag-
matic Programmers will be there with more titles and products to help you stay on top of
your game.
Visit Us Online
This Book’s Home Page
https://pragprog.com/book/utj3
Source code from this book, errata, and other resources. Come give us feedback, too!
Keep Up-to-Date
https://pragprog.com
Join our announcement mailing list (low volume) or follow us on Twitter @pragprog for new
titles, sales, coupons, hot tips, and more.
New and Noteworthy
https://pragprog.com/news
Check out the latest Pragmatic developments, new titles, and other offerings.
Buy the Book
If you liked this ebook, perhaps you’d like to have a paper copy of the book. Paperbacks are
available from your local independent bookstore and wherever fine books are sold.
Contact Us
https://pragprog.com/catalog
Online Orders:
support@pragprog.com
Customer Service:
translations@pragprog.com
International Rights:
academic@pragprog.com
Academic Use:
http://write-for-us.pragprog.com
Write for Us:


