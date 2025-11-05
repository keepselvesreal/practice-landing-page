# 9.5 Summary (pp.187-189)

---
**Page 187**

private boolean anyMatches() {
return criteria.stream()
.anyMatch(criterion ->
criterion.isMatch(profileAnswerMatching(criterion)));
}
private Answer profileAnswerMatching(Criterion criterion) {
return answers.get(criterion.questionText());
}
public int score() {
return criteria.stream()
.filter(criterion ->
criterion.isMatch(profileAnswerMatching(criterion)))
.mapToInt(criterion -> criterion.weight().value())
.sum();
}
}
Left to you, dear reader: combining both matching logic and scoring logic in
Matcher decreases cohesion. Your mission: split off the scoring logic into a new
class, Scorer. It should take at most 15 minutes. Don’t forget to split off the
tests!
Summary
In this chapter, you improved the design of iloveyouboss, leaning mostly on
a couple of simple design concepts for guidance: the SRP and command-query
separation. You owe it to yourself to know as much as possible about these
and other concepts in design. (Take a look at Clean Code [Mar08], for example,
but keep reading.) And don’t forget what you learned in Chapter 8, Refactoring
to Cleaner Code, on page 147: small, continual code edits make a big difference.
Armed with a stockpile of design smarts, your unit tests will allow you to
reshape your system so that it more easily supports the inevitable changes
coming.
Your system’s design quality also inversely correlates to your pain and frus-
tration level. The worse your design, the longer it will take to understand the
code and make changes. Keeping the design incrementally clean will keep
costs to a small fraction of what they’ll become otherwise.
Be flexible. Be willing to create new, smaller classes and methods. Automated
refactoring tools make doing so easy. Even without such tools, it takes only
minutes. It’s worth the modest effort. Design flexibility starts with smaller,
more composed building blocks.
report erratum  •  discuss
Summary • 187


---
**Page 188**

Now that you’ve learned to continually address your system’s micro and
macro-level design because your unit tests allow you to do so with high confi-
dence, it’s time to take a look at those tests themselves. Next up, you’ll see
how streamlining your tests lets them pay off even more as concise, clear,
and correct documentation on all the unit capabilities you’ve built into your
system.
Chapter 9. Refactoring Your Code’s Structure • 188
report erratum  •  discuss


---
**Page 189**

CHAPTER 10
Streamlining Your Tests
You’ve wrapped up a couple of chapters that teach you how to use tests to
keep your code clean. Now, it’s time to focus on the tests themselves.
Your tests represent a significant investment. They’ll pay off by minimizing
defects and allowing you to keep your production system clean through
refactoring. But, they also represent a continual cost. You need to continually
revisit your tests as your system changes. At times, you’ll want to make
sweeping changes and might end up having to fix numerous broken tests as
a result.
In this chapter, you’ll learn to refactor your tests, much like you would
refactor your production system, to maximize understanding and minimize
maintenance costs. You’ll accomplish this by learning to identify a series of
“smells” in your tests that make it harder to quickly understand them. You’ll
work through an example or two of how you can transform each smell into
de-odorized code.
The deodorization process is quick. In reading through the chapter, you might
think it would take a long time to clean a test similar to the example in the
chapter. In reality, it’s often well under fifteen minutes of real work once you
learn how to spot the problems.
Tests as Documentation
Your unit tests should provide lasting and trustworthy documentation of the
capabilities of the classes you build. Tests provide opportunities to explain
things that the code itself can’t do as easily. Well-designed tests can supplant
a lot of the comments you might otherwise feel compelled to write.
report erratum  •  discuss


