# 2.6.1 beforeEach() and scroll fatigue (pp.47-49)

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


---
**Page 48**

48
CHAPTER 2
A first unit test
The code duplication has been reduced to a minimum, but now we also need to look
up where and how we got the errors array if we want to understand each it(). 
 Let’s double down and add a few more basic scenarios, and see if this approach is
scalable as the problem space increases.
describe('v6 PasswordVerifier', () => {
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
  describe('with a passing rule', () => {
    let fakeRule, errors;
    beforeEach(() => {
      fakeRule = input => ({passed: true, reason: ''});
      verifier.addRule(fakeRule);
      errors = verifier.verify('any value');
    });
    it('has no errors', () => {
      expect(errors.length).toBe(0);
    });
  });
  describe('with a failing and a passing rule', () => {
    let fakeRulePass,fakeRuleFail, errors;
    beforeEach(() => {
      fakeRulePass = input => ({passed: true, reason: 'fake success'});
      fakeRuleFail = input => ({passed: false, reason: 'fake reason'});
      verifier.addRule(fakeRulePass);
      verifier.addRule(fakeRuleFail);
      errors = verifier.verify('any value');
    });
    it('has one error', () => {
      expect(errors.length).toBe(1);
    });
    it('error text belongs to failed rule', () => {
      expect(errors[0]).toContain('fake reason');
    });
  });
});
Listing 2.15
Adding extra scenarios


---
**Page 49**

49
2.7
Trying the factory method route
Do we like this? I don’t. Now we’re seeing a couple of extra problems:
I can already start to see lots of repetition in the beforeEach() parts.
The potential for scroll fatigue has increased dramatically, with more options of
which beforeEach() affects which it() state.
In real projects, beforeEach() functions tend to be the garbage bin of the test file.
People throw all kinds of test-initialized stuff in there: things that only some tests need,
things that affect all the other tests, and things that nobody uses anymore. It’s human
nature to put things in the easiest place possible, especially if everyone else before you
has done so as well. 
 I’m not crazy about the beforeEach() approach. Let’s see if we can mitigate some
of these issues while still keeping duplication to a minimum. 
2.7
Trying the factory method route
Factory methods are simple helper functions that help us build objects or special states
and reuse the same logic in multiple places. Perhaps we can reduce some of the dupli-
cation and clunky-feeling code by using a couple of factory methods for the failing
and passing rules in listing 2.16.
describe('PasswordVerifier', () => {
  let verifier;
  beforeEach(() => verifier = new PasswordVerifier1());
  describe('with a failing rule', () => {
    let errors;
    beforeEach(() => {
      verifier.addRule(makeFailingRule('fake reason'));
      errors = verifier.verify('any value');
    });
    it('has an error message based on the rule.reason', () => {
      expect(errors[0]).toContain('fake reason');
    });
    it('has exactly one error', () => {
      expect(errors.length).toBe(1);
    });
  });
  describe('with a passing rule', () => {
    let errors;
    beforeEach(() => {
      verifier.addRule(makePassingRule());
      errors = verifier.verify('any value');
    });
    it('has no errors', () => {
      expect(errors.length).toBe(0);
    });
  });
  describe('with a failing and a passing rule', () => {
    let errors;
Listing 2.16
Adding a couple of factory methods to the mix


