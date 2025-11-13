# 12.12 A.4.5 Stubbing a module with testdouble (pp.248-Back cover)

---
**Page 248**

248
APPENDIX
Monkey-patching functions and modules
const fakeDataFromModule = fakeData => {
  sinon.stub(dataModule, 'getAllMachines')
    .returns(fakeData);
};
const resetAndRequireModules = () => {
  jest.resetModules();
  dataModule = require('../my-data-module');
};
const requireAndCall_findRecentlyRebooted = (maxDays, someDate) => {
  const { findRecentlyRebooted } = require('../machine-scanner4');
  return findRecentlyRebooted(maxDays, someDate);
};
describe('4  sinon sandbox findRecentlyRebooted', () => {
  beforeEach(resetAndRequireModules);
  test('given no machines, returns empty results', () => {
    const someDate = new Date('01 01 2000');
    fakeDataFromModule([]);
    const result = requireAndCall_findRecentlyRebooted(2, someDate);
    expect(result.length).toBe(0);
  });
Let’s map the relevant parts with Sinon.
A.4.5
Stubbing a module with testdouble
Testdouble is another isolation framework that can easily be used to stub things out.
Due to the refactoring already done in previous tests, the code changes are minimal.
let td;
const resetAndRequireModules = () => {
  jest.resetModules();
  td = require('testdouble');
  require('testdouble-jest')(td, jest);
};
Clear
Before each test:
jest.resetModules + re-require fake module 
Fake
Before each test:
sinon.stub(module,'function')
.returns(fakeData)
Require (module under test)
Before invoking the entry point
Act
After re-requiring the module under test
Listing A.8
Stubbing a module with testdouble


---
**Page 249**

249
A.4
Faking module behavior in each test
const fakeDataFromModule = fakeData => {
  td.replace('../my-data-module', {
    getAllMachines: () => fakeData
  });
};
const requireAndCall_findRecentlyRebooted = (maxDays, fromDate) => {
  const { findRecentlyRebooted } = require('../machine-scanner4');
  return findRecentlyRebooted(maxDays, fromDate);
};
Here are the important parts with testdouble.
The test implementation is exactly the same as with the Sinon example. We’re also
using testdouble-jest, as it connects to the Jest module replacement facility. This is
not needed if we’re using a different test framework.
 These techniques will work, but I recommend staying away from them unless
there’s absolutely no other way. There is almost always another way, and you can see
many of those in chapter 3.
Clear
Before each test:
jest.resetModules +  require('testdouble');
require('testdouble-jest')
                     (td, jest);
Fake
Before each test:
Td.replace(module, fake object)
Require (module under test)
Before invoking the entry point
Act
After re-requiring the module under test


---
**Page 250**

 


---
**Page 251**

251
index
Symbols
<+> sign 154
A
AAA (Arrange-Act-Assert) pattern 38
add() function 142
addDefaultUser() function 173
Adder class 141
addRule() function 44
adopted process 217
advantages and traps of isolation frameworks
117–120
overspecifying tests 119
verifying wrong things 118
advocated process 217
afterAll() function 45
afterEach() function 45, 173, 240
alias to test() function 42
antipatterns
at test level 199
low-level-only test antipattern 202
test-level, end-to-end-only antipattern 199
API (application programming interface) 
tests 198
Arg.is() function 113
Array.prototype.every() method 40–41
describe() function 40–41
verifyPassword() function 40–41
assertEquals() function 14
assertion library 33
assertion roulette 89
assert module 14
async/await 124–125
async/await function structures 129
asynchronous code, unit testing 121–145
async/await mechanism 122
asynchronous data fetching 122
callback approach 124–125
dealing with 124–125
callback mechanism 122
common events 141–142
click events 142–144
dealing with event emitters 141–142
dealing with timers 138–139
DOM testing library 144–145
Extract Adapter pattern 125
functional adapter 135–136
modular adapter 133–134
object-oriented-interface-based adapter
136–138
Extract Entry Point pattern 125
extracting entry points 126
with await 129–131
making code unit-test friendly 125, 
127–129
timers 138–139
faking with Jest 139–141
stubbing out with monkey-patching
138–139
unit-test-friendly code 125–138
Extract Adapter pattern 131–133
functional adapter 135–136
unit testing 121–146
challenges with integration tests 125
DOM testing library 144–145
See also unit-test-friendly code


---
**Page 252**

INDEX
252
asynchronous processing, emulating with linear, 
synchronous tests 16
avoiding setup methods 175–176
B
BDD (behavior-driven development) 42–43
Beck, Kent 25
beforeAll() function 45
beforeEach() function 45–47, 50–51, 240
overview of 47–49
scroll fatigue and 47–49
blockers 215
bottom-up implementation 217
buggy tests, what to do once you’ve found 151
bugs, real bug in production code 151
build whisperers 201
business goals and metrics
breaking up into groups 221–222
leading indicators 221
C
calculator example, factory methods 49–50
callback mechanism 122
catch() expectation 55
CFRA (Clear-Fake-Require-Act) pattern 243
change agents
blockers 215
considering project feasibility 216
convincing insiders 214
change management
identifying starting points 215
making progress visible 219–220
changes
colleagues’ attitudes, being prepared for tough 
questions 214
forced by failing tests 166
in functionality, avoiding or preventing test 
failure due to 152
in other tests 169
testing culture and using code and test reviews 
as teaching tools 216
check() function 14, 245
Clean Code (Martin) 26
clearAllMocks() function 246
click events 142–144
code reviews, using as teaching tools 216
CodeScene, investigating production code 
with 236
code without tests 228
command 106
command/query separation 9, 106
common test types and levels, E2E/UI system 
tests 199
complicated interfaces, example of 98–99
component tests, overview of 196
concerns, testing multiple exit points 158–160
confidence 202
constrained test order 170–173
constructor functions 73–74
constructor injection 74–76
continuous testing 33
control 68
control flow code 22
_.curry() function 93
currying, not using 93
CUT (component, class, or code under test) 6
cyclomatic complexity 232
D
database, replacing with stubs 16
Date.now global 239–240
debug() function 88
debuggers, need for tests if code works 229
decoupling, factory functions decouple creation 
of object under test 168–169
delivery-blocking tests 208
delivery pipelines
delivery vs. discovery pipelines 208
test layer parallelization 210–211
dependencies 62, 68
breaking with stubs, object-oriented injection 
techniques 74
types of 62–64
dependencies object 71
dependencies variable 72
dependency injection (DI) 138
breaking with stubs 61
design approaches to stubbing 66
functional injection techniques 69–70
modular injection techniques 70–73
object-oriented injection techniques 79–81
Dependency Injection (DI) containers 77
Dependency Inversion 67
describe() block 41, 46
describe() function 30, 40–41, 52
describe-driven syntax 42
describe structure 188
destructured() function 244
differentiating between mocks and stubs 88–89
diminishing returns from E2E (end-to-end) 
tests 199


---
**Page 253**

INDEX
253
direct dependencies, abstracting away 109
discovery pipelines, vs. delivery pipelines 208
document.load event 144
DOM (Document Object Model) testing 
library 144–145
doMock() function 246
done() callback 124
done() function 124, 129, 142
DRY (don’t repeat yourself) principle 175
duck typing 79
dummy data 67
dummy value 67
dynamic mocks and stubs 104, 109–110
functional 109–110
dynamic stubbing 114–116
E
E2E (end-to-end) tests 198–199
avoiding completely 202
build whisperer 201
diminishing returns from 199
E2E/UI isolated tests 198
edge cases 205
end-to-end-only antipattern 199–201
avoiding build whisperers 201
avoiding E2E tests completely 202
throw it over the wall mentality 201
when it happens 202
entry points 6–10, 241
extracting, with await 129–131
errors array 46
event-driven programming 142–144
event emitters 141–142
exact:false flag 145
exceptions, checking for expected thrown 
errors 55–56
executing Jest 31–33
exit points 6, 9–11, 158–160, 241
different exit points, different techniques 12
expect 33
expect() function 30
expect().toThrowError() method 55
experiments
as door openers 218
metrics and 218
Extract Adapter pattern 131–133
functional adapter 135–136
modular adapter 133–134
object-oriented-interface-based adapter 136–138
extracting adapter pattern 125
extracting entry point pattern 125
F
factory functions 168–169
factory methods 49–50, 168
replacing beforeEach() completely with
50–51
failed tests
buggy tests 151
reasons tests fail 152
fake 241
FakeComplicatedLogger class 100
fakeDataFromModule() method 245, 247
fakeImplementation 242
FakeLogger class 96, 98, 168
fake module behavior
avoiding Jest’s manual mocks 247
stubbing modules with Sinon.js 247
fake modules, dynamically 106–108
fake objects and functions
faking module behavior in each test 248–249
stubbing with testdouble 248–249
FakeTimeProvider 78
fake (xUnit Test Patterns, Meszaros) 64
false failures 166
feature toggles 166
findFailedRules() function 178–179
findResultFor() function 181
first unit test, setting test categories 56–57
flaky tests 153, 161
dealing with 163
mixing unit tests and integration tests 158
preventing flakiness in higher-level tests 163
folders, preparing for Jest 29–30
Freeman, Steve 26
full control 15
functional dynamic mocks and stubs 109–110
functional injection techniques 69
injecting functions 69–70
partial application 70
functionality, change in, out of date tests 152
functional style
higher-order functions 93
mocks, currying 92–93
functions
injecting 69–70
injecting instead of objects 76–79
it() function 42
monkey-patching 238
faking module behavior in each test 243–244, 
247–249
globals and possible issues 239–241
ignoring whole modules with Jest 242


---
**Page 254**

INDEX
254
functions (continued)
setup 175–176
test() 52
verifyPassword 43–45
G
genMockFromModule() function 246
getDay() function 72, 76
getLogLevel() function 107
globals
Jest spies 241
monkey-patching functions and modules
239–241
goals, specific 220
good-to-know tests 208
Growing Object-Oriented Software, Guided by Tests 
(Freeman and Pryce) 26
guerrilla implementation 217
H
happy path 205
hard-first strategy, pros and cons of 234
hexagonal architecture 109
higher-order functions 93
high-level tests, disconnected low-level 
and 204
I
IComplicatedLogger interface 99
if/else 155
ILogger interface 96, 98, 166
incoming dependencies 62
indicators
breaking up into groups 221–222
lagging indicators 220
INetworkAdapter parameter 136
info function 88, 96, 107
info method 88
inject() function 72
injectDate() function 72
injectDependencies() function 91
inject function 72
injections 68
modular-style injection, example of 92
insiders, convincing 214
integration of unit testing
into organization, convincing management
217
metrics and experiments 218
integration testing
async/await 124–125
challenges with 125
unit testing, integrating into organization 228
integration tests 123, 197
flaky, mixing with unit tests 158
interaction testing
complicated interfaces 98–101
depending on loggers 85–86
differentiating between mocks and stubs 88–89
mock objects 83–103
functional style 92
in object-oriented style 94, 96
mocks and stubs 84
partial mocks 101
interfaces, complicated, ISP 101
interface segregation principle 131, 133
internal behavior, overspecification with 
mocks 177–179
Inversion of Control (IoC) containers 77
isolated tests 198
isolation facilities 33
isolation frameworks 104–120
advantages and traps of
overspecifying tests 119
unreadable test code 118
verifying wrong things 118
defining 105
loose vs. typed 105
faking modules dynamically 106–108
abstracting away direct dependencies 109
Jest API 108
functional dynamic mocks and stubs 109–110
object-oriented dynamic mocks and stubs 110
using loosely typed framework 110–112
stubbing behavior dynamically 114–117
object-oriented example with mock and 
stub 114–116
with substitute.js 116–117
type-friendly frameworks 112–113
ISP (interface segregation principle) 101
isWebsiteAlive() function 129, 133
it() function 30, 42, 51
it.each() function 53, 176
it.only keyword 172
IUserDetails interface 170
J
Jest 29
API of 108
avoiding manual mocks 247


---
**Page 255**

INDEX
255
Jest (continued)
creating test files 30–31
executing 31–33
fake timers with 139–141
ignoring whole modules with 242
installing 30
library, assert, runner, and reporter 33
monkey-patching functions 241
preparing environment 29
preparing working folder 29–30
spies 241
verifyPassword() function 37
for Jest syntax flavors 42
jest command 30
jest.fn() function 112
jest.mock() function 134
jest.mock API, abstracting away direct 
dependencies 109
jest.mock([module name]) function 108
jest.restoreAllMocks function 242
Jest snapshots 56
Jest unit testing framework 36
jest - -watch command 33
K
Khorikov, Vladimir 236
KPIs (key performance indicators) 208, 220
L
lagging indicators 220
leading indicators 221
breaking up into groups 221–222
legacy code 231–237
integration tests, writing before refactoring 236
selection strategies
easy-first strategy 234
hard-first strategy, pros and cons of 234
where to start adding tests 232–233
writing integration tests before refactoring 235
using CodeScene to investigate production 
code 236
loadHtmlAndGetUIElements method 144
loadHtml method 144
lodash library 92
logged variable 96
logger.debug 90
logger.info 90
loggers, depending on 85–86
loose isolation frameworks 105
loosely typed frameworks 110–112
low-level-only test antipattern 202
low-level tests, disconnected high-level and 204
LTS (long-term support) release 29
M
magic values 189–190
maintainability 89, 165–183
avoiding overspecification 177–179
changes forced by failing tests
changes in other tests 169
constrained test order 170–173
of code, exact outputs and ordering 
overspecification 179–183
of tests
changes forced by failing tests 166
changes in production code’s API 166–168
test is not relevant or conflicts with another 
test 166
refactoring to increase 173
avoiding setup methods 175–176
avoiding testing private or protected 
methods 175
keeping tests DRY 175
using parameterized tests to remove 
duplication 176–177
maintainable tests 36
MaintenanceWindow interface 115–116
makeFailingRule() method 50
makePassingRule() method 50
makePerson() function 160
makeSpecialApp() factory function 173
makeStubNetworkWithResult() helper 
function 136
makeVerifier() function 94
Meszaros, Gerard 11, 64, 89
methods, making public 174
metrics, experiments and 218
metrics and KPIs 222
mock functions 98, 246
mockImplementation() function 241–242
mockImplementation() method 114
mockImplementationOnce() method 114, 247
mockLog variable 191
mock objects 12, 83, 98–103, 247
advantages of isolation frameworks 118
complicated interfaces 98
downsides of using directly 100
example of 98–99
depending on loggers 85–86
differentiating between mocks and stubs 88–89
functional style 92


---
**Page 256**

INDEX
256
mock objects (continued)
in object-oriented style 94
interaction testing with complicated 
interfaces 99–100
modular-style mocks 89
refactoring production code in modular injec-
tion style 91
overview of 84
partial mocks 101
object-oriented partial mock example 102–103
standard style, introducing parameter 
refactoring 87–88
mockReturnValue() method 114
mockReturnValueOnce() method 114
mocks 63, 84
advantages of, having more than one mock per 
test 119
functional style
currying 92–93
higher-order functions and not currying 93
in object-oriented style
refactoring production code for injection 95
refactoring production code with interface 
injection 96
internal behavior overspecification with 177–179
object-oriented design example with 114–116
object-oriented dynamic mocks and stubs 110
modular adapter 133–134
modular injection techniques 70–73
modular-style mocks 89
example of production code 90–91
modular-style injection, example of 92
refactoring production code in modular injec-
tion style 91
modules
faking behavior in each test 243–249
stubbing with Sinon.js 247
stubbing with testdouble 248–249
faking dynamically 106–108
abstracting away direct dependencies 109
monkey-patching 238
moment.js 64
monkey-patching 138, 238
functions and modules
faking module behavior in each test 248–249
stubbing module with vanilla 
require.cache 244–245
stubbing with Sinon.js 247
stubbing with testdouble 248–249
possible issues 239–241
spyOn with mockImplementation() 241–242
warning about 238
N
network-adapter module 132–134
node-fetch module 132
Node.js 7
node package manager (NPM) 29
npm commands 30
NPM (node package manager) 4, 29
npm run testw command 38
npx jest command 30
numbers string 12
O
object-oriented design, example with mock and 
stub 114–116
object-oriented dynamic mocks and stubs 110
type-friendly frameworks 112–113
using loosely typed framework 110–112
object-oriented injection techniques 74–81
constructor injection 74–76
extracting common interface 79–81
injecting objects instead of functions 76–79
overview 79–81
object-oriented style, mocks in 94
obvious values 196
onion architecture 109
organization, integrating unut testing into 229
originalDependencies object 71
originalDependencies variable 91
outgoing dependencies 62
overspecification
avoiding 177–179
exact outputs and ordering 179–183
P
parameter injection 66–67
parameterized tests
refactoring to 53–55
removing duplication with 176–177
parameter refactoring 87–88
partial application, dependency injection via 70
partial mocks 101
functional example 101–102
object-oriented partial mock example 102–103
PASSED result 90
passVerify() function 94
password-verifier0.spec.js file 37
PasswordVerifier1 46
PasswordVerifier class 97
passwordVerifierFactory() function 76


---
**Page 257**

INDEX
257
Password Verifier project 37
patching functions and modules
avoiding Jest’s manual mocks 247
faking module behavior in each test 243–244
ignoring whole modules with Jest 242
person object 160
polymorphism 96
ports and adapters architecture 109
preconfigured verifier function 94
private and protected methods, avoiding 
testing 175
making methods public 174
production code
changing API of 166–167
modular-style mocks, example of 90–91
real bug in 151
refactoring for injection 95
refactoring in modular injection style 91
refactoring with interface injection 96
production code, investigating with 
CodeScene 236
production code, refactoring 43–45
production module 13
progress, making visible 219–220
protected methods 174
Pryce, Nat 26
Q
qualitative metrics 222
query 106
R
readability 89
magic values and naming variables 189–190
of unit tests 187–193
separating asserts from actions 190
readable tests 36
reason string 41
.received() function 113, 116
refactoring 24
avoiding testing private or protected 
methods 175
keeping tests DRY 175
making methods public 174
production code for injection 95
to increase maintainability
avoiding setup methods 175–176
avoiding testing private or protected 
methods 174
to parameterized tests 53–55
using parameterized tests to remove 
duplication 176–177
writing integration tests before 235
requireAndCall_findRecentlyRebooted() 
function 245
require.cache, stubbing module with vanilla
244–245
require.cache mechanism 243
reset() function 72
resetAllMocks() function 246
resetDependencies() function 91–92
resetModules() function 246
restoreAllMocks() function 246
.returns() function 116
rules array 166
rules verification functions 37
S
safe green zone 158
scripts item 38
seams 71, 232
abstracting dependencies using 86
selection strategies 234
easy-first strategy 234
setTimeout function 138–139
setTimeout method 138
setup methods 191–192
SimpleLogger class 96–97
Sinon.js, stubbing modules with 247
smaller teams 215
SpecialApp implementation 170–171
spies, Jest 241
spyOn() function 241–242
state-based test 179
stateless private methods, making public static 175
string comparisons 40
stringMatching function 110
strings, comparing 40
stub 88, 108, 241
stubbing
dynamically 114–117
modules 248–249
with Sinon.js 247
with substitute.js 116–117
with testdouble 248–249
stubs 61, 63, 84
constructor functions 73–74
design approaches to 66
dependencies, injections, and control 68
stubbing out time with parameter injection
66–67


---
**Page 258**

INDEX
258
stubs (continued)
functional injection techniques 69
injecting functions 69–70
modular injection techniques 70–73
object-oriented injection techniques 74–81
constructor injection 74–76
extracting common interface 79–81
injecting objects instead of functions 76–79
overview 79–81
overview of 84
reasons to use 64–66
replacing database (or another dependency) 
with 16
types of dependencies 62–64
subject, system, or suite under test (SUT) 6
Substitute.for<T>() function 116
substitute.js 116–117
subteams, creating 216
sum() function 12
SUnit 36
SUT (subject, system, or suite under test) 6
T
tape framework 36
TAP (Test Anything Protocol) 36
TDD (test-driven development) 5, 22, 152–229
core skills for 25
pitfalls of, not a substitute for good unit tests 24
teardown methods 191–192
test() function, overview of 52
testableLog variable 101
test categories 56–57
test conflicts with another test 152–153
testdouble-jest 249
test doubles 64, 243
stubbing modules with 248–249
test-driven development (TDD) 5, 25, 152
test.each function 53, 176
test failure
reasons for 152
test conflicts with another test 152–153
test out of date due to change in 
functionality 152
test-feasibility table 232
test-first development 22
test flakiness 82
test function 30
testing
reasons tests fail
buggy test gives false failure 151
test conflicts with another test 152
smelling false sense of trust in passing tests 156
trustworthy tests 164
testing strategy 194–212
common test types and levels 195
API tests 198
criteria for judging tests 196
E2E/UI isolated tests 198
E2E/UI system tests 199
integration tests 197
unit tests and component tests 196
developing, using test recipes 205
low-level-only test antipattern 202
managing delivery pipelines 208
delivery vs. discovery pipelines 208
test layer parallelization 210–211
test-level antipatterns
disconnected low-level and high-level 
tests 203
end-to-end-only antipattern 199, 201
test recipes
rules for 207–208
writing and using 207
test layer parallelization 210–211
test library 33
test maintainability, constrained test order
170–173
test method 13
testPathPattern command-line flag 56
- -testPathPattern flag 58
test recipes
as testing strategy 205
rules for 207–208
writing 205
writing and using 207
testRegex configuration 56
test reporter 33
test reviews, using as teaching tools 216
test runner 33
tests, criteria for judging 196
__tests__ folder 37–38
test syntax 42
then() callback 124
third-party test 179
time, added to process 226–227
TimeProviderInterface type 79
timers 138
faking with Jest 139–141
stubbing out with monkey-patching 138–139
.toContain('fake reason') function 38
.toContain matcher 40
toMatchInlineSnapshot() method 56
.toMatch matcher 40


---
**Page 259**

INDEX
259
.toMatch(/string/) function 38
top-down approach 217
totalSoFar() function 9
toThrowError method 56
transpiler 96
trend lines 222
true failures 166
trust 89
trustworthy tests 36, 149–164
avoiding logic in unit tests 153, 155–156
creating dynamic expected values 153–155
even more logic 156
buggy tests
criteria for judging tests 196
what to do once you’ve found 151
dealing with flaky tests 163
failed tests 151
flaky tests 161, 163
reasons for test failure 150–152
buggy test gives false failure 151
flaky tests 153
out of date due to change in functionality
152
real bug in production code 151
test conflicts with another test 152
smelling false sense of trust in passing 
tests 156
mixing unit tests and flaky integration 
tests 158
testing multiple exit points 158–160
tests that don’t assert anything 157
tests that keep changing 160
test conflicts with another test 153
type-friendly frameworks 112–113
U
UI (user interface) tests 198–199
unit of work 6, 241
unit test 15, 21
unit testing 3–27
asynchronous code 121–146
basics of 5
characteristics of good unit tests 15–16
creating unit tests from scratch 12–15
defining 5
different exit points, different techniques 12
educating colleagues about, being prepared 
for tough questions 214
entry points and exit points 6–10
exit point types 11
first unit test 28–58
frameworks, advantages of 34–36
integrating into organization 213–230
ad hoc implementations and first 
impressions 223
aiming for specific goals, metrics, and 
KPIs 220
code without tests 228
experiments as door openers 217
getting outside champion 218
guerrilla implementation 217
influence factors 224
lack of political support 223
need for tests if debugger shows that code 
works 229
steps to becoming agent of change 214–216
TDD (test-driven development) 25, 
226–230
time added to process 226–227
tough questions and answers 226–229
proof that unit testing helps 228
QA jobs at risk 227
ways to fail 223
lack of driving force 223
lack of team support 224
ways to succeed 216
convincing management 217
realize that there will be hurdles 222
interaction testing using mock objects
83–103
legacy code 237
selection strategies 234
where to start adding tests 232–233
writing integration tests before 
refactoring 235–236
maintainability 183
stubs, reasons to use 64–66
unit testing asynchronous code, example of 
extracting unit of work 127–129
Unit Testing Principles, Practices, and Patterns 
(Khorikov) 236
unit tests 28
avoiding logic in 153
creating dynamic expected values 153–155
other forms of logic 155–156
avoiding overspecification 177
characteristics of 15
checklist for 16
emulating asynchronous processing with lin-
ear, synchronous tests 16
overview 15
replacing database (or another dependency) 
with stub 16
characteristics of good unit tests 15


---
**Page 260**

INDEX
260
unit tests (continued)
creating
beforeEach() function 45–47
from scratch 12–15
using test() function 52
exceptions, checking for expected thrown 
errors 55–56
faking module behavior in each test 244–245
first unit test 28–58
factory method route 49–50
refactoring to beforeEach() function 47–49
replacing beforeEach() completely with fac-
tory methods 50–51
verifyPassword() function 37
Jest
creating test files 30–31
first test with, preparing working folder 29–30
library, assert, runner, and reporter 33
naming 188–189
overview of 196
parameterized tests, refactoring to 53–55
Password Verifier project 37
readability 187–193
magic values and naming variables 189–190
separating asserts from actions 190
setting up and tearing down 191–192
refactoring production code 43–45
setting test categories 56–57
unit testing frameworks 36
unreadable test code 118
UserCache object 170
USE (unit, scenario, expectation) naming 39
V
value-based test 179
vanilla require.cache 244–245
verification 87
verifier 78
verifier variable 46
verify() function 55, 95, 178–180
verifyPassword() function 45, 86, 90
Arrange-Act-Assert pattern 38
describe() function 40–41
first test for 37
Jest syntax flavors 42
Jest test for 42
refactoring production code 43–45
structure can imply context 41–42
testing strings, comparing 40
testing test 39
verifyPassword(rules) function 37
W
WebsiteVerifier class 136–137
website-verifier example 135–136
written class 98
X
xUnit frameworks 36
xUnit test patterns and naming things 64
xUnit Test Patterns: Refactoring Test Code 
(Meszaros) 11, 64, 89


---
**Page Back cover**

ISBN-13: 978-1-61729-748-9
T
he art of unit testing is more than just learning the right 
collection of tools and practices. It’s about understanding 
what makes great tests tick, fi nding the right strategy for each 
unique situation, and knowing what to do when the testing process 
gets messy. Th is book delivers insights and advice that will trans-
form the way you test your soft ware. 
The Art of Unit Testing, Third Edition shows you how to create 
readable and maintainable tests. It goes well beyond basic test 
creation into organization-wide test strategies, troubleshooting, 
working with legacy code, and “merciless” refactoring. You’ll love 
the practical examples and familiar scenarios that make testing 
come alive as you read. Th is third edition has been updated with 
techniques specifi c to object-oriented, functional, and modular 
coding styles. Th e examples use JavaScript.
What’s Inside
Deciding on test types and strategies 
Test Entry & Exit Points
Refactoring legacy code 
Fakes, stubs, mock objects, and isolation frameworks
Object-Oriented, Functional, and Modular testing styles
Examples use JavaScript, TypeScript, and Node.js.
Roy Osherove is an internationally-recognized expert 
in unit testing and agile soft ware methodology. 
Vladimir Khorikov is the author of Manning’s Unit 
Testing Principles, Practices, and Patterns, a Plural-
sight author, and a Microsoft  MVP. 
For print book owners, all ebook formats are free:
https://www.manning.com/freebook
The Art of Unit Testing THIRD EDITION
DEVELOPMENT
 
“
Our testing bible. Th e Java-
Script community is fortunate 
to have it adapted to our favorite 
language.”
 
—Yoni Goldberg, 
Node.js testing consultant, author of 
Node.js Best Practices 
“
A testing masterpiece!”
—Jaume López, Institut Guttmann
“
Teaches you the philosophy 
as well as the nuts and bolts 
  for eff ective unit testing.”
—Matteo Gildone
Springer Nature
“
A proper view of what 
to test, when, and how 
  to do it well.”
 
—Rich Yonts, Teradata
M A N N I N G
Osherove ● Khorikov
See first page
Roy Osherove


