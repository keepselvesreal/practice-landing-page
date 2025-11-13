# 2.6.0 Introduction [auto-generated] (pp.45-47)

---
**Page 45**

45
2.6
Trying the beforeEach() route
What happens if the new assertion fails? The second assertion would never execute,
because the test runner would receive an error and move on to the next test case.
 We’d still want to know if the second assertion would have passed, right? So maybe
we’d start commenting out the first one and rerunning the test. That’s not a healthy
way to run your tests. In Gerard Meszaros’ book xUnit Test Patterns, this human behav-
ior of commenting things out to test other things is called assertion roulette. It can cre-
ate lots of confusion and false positives in your test runs (thinking that something is
failing or passing when it isn’t).
 I’d rather separate this extra check into its own test case with a good name, as follows.
describe('PasswordVerifier', () => {
  describe('with a failing rule', () => {
    it('has an error message based on the rule.reason', () => {
      const verifier = new PasswordVerifier1();
      const fakeRule = input => ({ passed: false,
                                   reason: 'fake reason'});
      verifier.addRule(fakeRule);
      const errors = verifier.verify('any value');
      expect(errors[0]).toContain('fake reason');
    });
    it('has exactly one error', () => {
      const verifier = new PasswordVerifier1();
      const fakeRule = input => ({ passed: false,
                                   reason: 'fake reason'});
      verifier.addRule(fakeRule);
      const errors = verifier.verify('any value');
      expect(errors.length).toBe(1);
    });
  });
});
This is starting to look bad. Yes, we have solved the assertion roulette issue. Each it()
can fail separately and not interfere with the results from the other test case. But what
did it cost? Everything. Look at all the duplication we have now. At this point, those of
you with some unit testing background will start shouting at the book: “Use a
setup/beforeEach method!”
 Fine!
2.6
Trying the beforeEach() route
I haven’t introduced beforeEach() yet. This function and its sibling, afterEach(),
are used to set up and tear down a specific state required by the test cases. There’s also
beforeAll() and afterAll(), which I try to avoid using at all costs for unit testing sce-
narios. We’ll talk more about the siblings later in the book. 
Listing 2.12
Checking an extra end result from the same exit point


---
**Page 46**

46
CHAPTER 2
A first unit test
 beforeEach() can help us remove duplication in our tests because it runs once
before each test in the describe block in which we nest it. We can also nest it multiple
times, as the following listing demonstrates.
describe('PasswordVerifier', () => {
  let verifier;
  beforeEach(() => verifier = new PasswordVerifier1());   
  describe('with a failing rule', () => {
    let fakeRule, errors;
    beforeEach(() => {                             
      fakeRule = input => ({passed: false, reason: 'fake reason'});
      verifier.addRule(fakeRule);
    });
    it('has an error message based on the rule.reason', () => {
      const errors = verifier.verify('any value');
      expect(errors[0]).toContain('fake reason');
    });
    it('has exactly one error', () => {
      const errors = verifier.verify('any value');
      expect(errors.length).toBe(1);
    });
  });
});
Look at all that extracted code. 
 In the first beforeEach(), we’re setting up a new PasswordVerifier1 that will be
created for each test case. In the beforeEach() after that, we’re setting up a fake rule
and adding it to the new verifier for every test case under that specific scenario. If we
had other scenarios, the second beforeEach() in line 6 wouldn’t run for them, but
the first one would.
 The tests seem shorter now, which ideally is what you want in a test, to make it
more readable and maintainable. We removed the creation line from each test and
reused the same higher-level variable verifier. 
 There are a couple of caveats:
We forgot to reset the errors array in beforeEach() on line 6. That could bite
us later on. 
Jest runs unit tests in parallel by default. This means that moving the verifier to
line 2 may cause an issue with parallel tests, where the verifier could be over-
written by a different test on a parallel run, which would screw up the state of
our running test. Jest is quite different from unit test frameworks in most other
languages I know, which make a point of running tests in a single thread, not in
parallel (at least by default), to avoid such issues. With Jest, we have to remem-
ber that parallel tests are a reality, so stateful tests with a shared upper state, like
Listing 2.13
Using beforeEach() on two levels
Setting up a new 
verifier that will be 
used in each test
Setting up a fake
rule that will be
used within this
describe() method


---
**Page 47**

47
2.6
Trying the beforeEach() route
we have at line 2, can potentially be problematic and cause flaky tests that fail
for unknown reasons.
We’ll correct both of these issues soon.
2.6.1
beforeEach() and scroll fatigue
We lost a couple of things in the process of refactoring to beforeEach():
If I’m trying to read only the it() parts, I can’t tell where the verifier is cre-
ated and declared. I’d have to scroll up to understand.
The same goes for understanding what rule was added. I’d have to look one
level above the it() to see what rule was added, or look up the describe()
block description. 
Right now, this doesn’t seem so bad. But we’ll see later that this structure starts to get a
bit hairy as the scenario list increases in size. Larger files can bring about what I like to
call scroll fatigue, requiring the test reader to scroll up and down the test file to under-
stand the context and state of the tests. This makes maintaining and reading the tests
a chore instead of a simple act of reading. 
 This nesting is great for reporting, but it sucks for humans who have to keep look-
ing up where something came from. If you’ve ever tried to debug CSS styles in the
browser’s inspector window, you’ll know the feeling. You’ll see that a specific cell is
bold for some reason. Then you scroll up to see which style made that <div> inside
nested cells in a special table under the third node bold.
 Let’s see what happens when we take it one step further in the following listing.
Since we’re in the process of removing duplication, we can also call verify in
beforeEach() and remove an extra line from each it(). This is basically putting the
arrange and act parts from the AAA pattern into the beforeEach() function.
describe('PasswordVerifier', () => {
  let verifier;
  beforeEach(() => verifier = new PasswordVerifier1());
  describe('with a failing rule', () => {
    let fakeRule, errors;
    beforeEach(() => {
      fakeRule = input => ({passed: false, reason: 'fake reason'});
      verifier.addRule(fakeRule);
      errors = verifier.verify('any value');
    });
    it('has an error message based on the rule.reason', () => {
      expect(errors[0]).toContain('fake reason');
    });
    it('has exactly one error', () => {
      expect(errors.length).toBe(1);
    });
  });
});
Listing 2.14
Pushing the arrange and act parts into beforeEach()


