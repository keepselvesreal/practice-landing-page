# 2.5.9 Refactoring the production code (pp.43-45)

---
**Page 43**

43
2.5
The first Jest test for verifyPassword
2.5.9
Refactoring the production code
Since there are many ways to build the same thing in JavaScript, I thought I’d show a
couple of variations on our design and what happens if we change it. Suppose we’d
like to make the password verifier an object with state.
 One reason to change the design into a stateful one might be that I intend for dif-
ferent parts of the application to use this object. One part will configure and add rules
to it, and a different part will use it to do the verification. Another reason is that we
need to know how to handle a stateful design and look at which directions it pulls our
tests in, and what we can do about that.
 Let’s look at the production code first.
class PasswordVerifier1 {
  constructor () {
    this.rules = [];
  }
  addRule (rule) {
    this.rules.push(rule);
  }
  verify (input) {
    const errors = [];
    this.rules.forEach(rule => {
      const result = rule(input);
      if (result.passed === false) {
        errors.push(result.reason);
      }
BDD’s dark present
BDD has quite an interesting background that might be worth talking about. BDD isn’t
related to TDD. Dan North, the person most associated with inventing the term, refers
to BDD as using stories and examples to describe how an application should behave.
Mainly this is targeted at working with non-technical stakeholders—product owners,
customers, etc. RSpec (inspired by RBehave) brought the story-driven approach to
the masses, and in the process, many other frameworks came along, including the
famous Cucumber.
There is also a dark side to this story: many frameworks have been developed and
used solely by developers without working with non-technical stakeholders, in com-
plete opposition to the main ideas of BDD.
Today, to me, the term BDD frameworks mainly means “test frameworks with some
syntactic sugar,” since they are almost never used to create real conversations
between stakeholders and are almost always used as just another shiny or pre-
scribed tool for performing developer-based automated tests. I’ve even seen the
mighty Cucumber fall into this pattern.
Listing 2.10
Refactoring a function to a stateful class


---
**Page 44**

44
CHAPTER 2
A first unit test
    });
    return errors;
  }
}
I’ve highlighted the main changes from listing 2.9. There’s nothing really special
going on here, though this may feel more comfortable if you’re coming from an
object-oriented background. It’s important to note that this is just one way to design
this functionality. I’m using the class-based approach so that I can show how this
design affects the test.
 In this new design, where are the entry and exit points for the current scenario?
Think about it for a second. The scope of the unit of work has increased. To test a sce-
nario with a failing rule, we would have to invoke two functions that affect the state of
the unit under test: addRule and verify.
 Now let’s see what the test might look like (changes are highlighted as usual).
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
  });
});
So far, so good; nothing fancy is happening here. Note that the surface of the unit of
work has increased. It now spans two related functions that must work together
(addRule and verify). There is a coupling that occurs due to the stateful nature of the
design. We need to use two functions to test productively without exposing any inter-
nal state from the object.
 The test itself looks innocent enough. But what happens when we want to write sev-
eral tests for the same scenario? That would happen if we have multiple exit points, or
if we want to test multiple results from the same exit point. For example, let’s say we
want to verify that we have only a single error. We could simply add a line to the test
like this:
verifier.addRule(fakeRule);
const errors = verifier.verify('any value');
expect(errors.length).toBe(1);       
expect(errors[0]).toContain('fake reason');
Listing 2.11
Testing the stateful unit of work
A new 
assertion


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


