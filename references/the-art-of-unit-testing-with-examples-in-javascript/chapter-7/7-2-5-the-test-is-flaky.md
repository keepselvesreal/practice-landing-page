# 7.2.5 The test is flaky (pp.153-153)

---
**Page 153**

153
7.3
Avoiding logic in unit tests
WHAT CAN YOU DO NOW?
The root cause is that one of the tests has become irrelevant, which means it needs to
be removed. Which one should be removed? That’s a question we’d need to ask a
product owner, because the answer is related to which behavior is correct and
expected from the application. 
AVOIDING THIS IN THE FUTURE
I feel this is a healthy dynamic, and I’m fine with not avoiding it. 
7.2.5
The test is flaky
A test can fail inconsistently. Even if the production code under test hasn’t changed, a
test can suddenly fail without any apparent reason, then pass again, then fail again.
We call a test like that “flaky.” 
 Flaky tests are a special beast, and I’ll deal with them in section 7.5.
7.3
Avoiding logic in unit tests
The chances of having bugs in your tests increase almost exponentially as you include
more and more logic in them. I’ve seen plenty of tests that should have been simple
become dynamic, random-number-generating, thread-creating, file-writing monsters
that are little test engines in their own right. Sadly, because they were “tests,” the
writer didn’t consider that they might have bugs or didn’t write them in a maintain-
able manner. Those test monsters take more time to debug and verify than they save. 
 But all monsters start out small. Often, an experienced developer in the company
will look at a test and start thinking, “What if we made the function loop and create
random numbers as input? We’d surely find lots more bugs that way!” And you will,
especially in your tests. 
 Test bugs are one of the most annoying things for developers, because you’ll
almost never search for the cause of a failing test in the test itself. I’m not saying that
tests with logic don’t have any value. In fact, I’m likely to write such tests myself in
some special situations. But I try to avoid this practice as much as possible. 
 If you have any of the following inside a unit test, your test contains logic that I usu-
ally recommend be reduced or removed completely:

switch, if, or else statements

foreach, for, or while loops
Concatenations (+ sign, etc.)

try, catch
7.3.1
Logic in asserts: Creating dynamic expected values
Here’s a quick example of a concatenation to start us off.
describe("makeGreeting", () => {
  it("returns correct greeting for name", () => {
Listing 7.1
A test with logic in it


