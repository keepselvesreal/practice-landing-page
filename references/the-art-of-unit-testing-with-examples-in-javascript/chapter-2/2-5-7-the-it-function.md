# 2.5.7 The it() function (pp.42-42)

---
**Page 42**

42
CHAPTER 2
A first unit test
For the next example, I’ll move this rule back into the test (I like it when things are
close together—more on that later).
 This nesting structure also implies very nicely that under a specific scenario you
could have more than one expected behavior. You could check multiple exit points
under a scenario, with each one as a separate test, and it will still make sense from the
reader’s point of view. 
2.5.7
The it() function
There’s one missing piece to the puzzle I’ve been building so far. Jest also exposes an
it() function. This function is, for all intents and purposes, an alias to the test()
function, but it fits in more nicely in terms of syntax with the describe-driven
approach outlined so far.
 The following listing shows what the test looks like when I replace test() with it().
describe('verifyPassword', () => {
  describe('with a failing rule', () => {
    it('returns errors', () => {
      const fakeRule = input => ({ passed: false,
                                   reason: 'fake reason' });
      const errors = verifyPassword('any value', [fakeRule]);
      expect(errors[0]).toContain('fake reason');
    });
  });
});
In this test, it’s very easy to understand what it refers to. This is a natural extension of
the previous describe() blocks. Again, it’s up to you whether you want to use this
style. I’m showing one variation of how I like to think about it.
2.5.8
Two Jest flavors
As you’ve seen, Jest supports two main ways to write tests: a terse test syntax, and a
more describe-driven (i.e., hierarchical) syntax. 
 The describe-driven Jest syntax can be largely attributed to Jasmine, one of the
oldest JavaScript test frameworks. The style itself can be traced back to Ruby-land and
the well-known RSpec Ruby test framework. This nested style is usually called BDD
style, referring to behavior-driven development. 
 You can mix and match these styles as you like (I do). You can use the test syntax
when it’s easy to understand your test target and all of its context, without going to too
much trouble. The describe syntax can help when you’re expecting multiple results
from the same entry point under the same scenario. I’m showing them both here
because I sometimes use the terse test flavor and sometimes use the describe-driven
flavor, depending on the complexity and expressiveness requirements.
Listing 2.9
Replacing test() with it()


