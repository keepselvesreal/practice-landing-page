# 13.10 Will I Go Faster? (pp.263-264)

---
**Page 263**

2.
If a person has a salutation, it should precede the first name in the result.
Known salutations include Dr, Mr, Mrs, Ms, Sir, Miss, Lord, and Esq.
Each salutation may optionally be terminated by a period. Retain the
period if it exists.
input: Dr. Martin Luther King, Jr.
output: King, Jr., Dr. Martin L.
input: Sir Patrick Stewart
output: Stewart, Sir Patrick
If you really want to get wild, a version supporting non-Western names would
no doubt involve numerous additional rules.
Increasing Odds of Success with AI-Generated Code
The most important thing to remember when developing software with an LLM
is you can’t trust the code it generates. The skills you obtained in Pragmatic
Unit Testing in Java with JUnit, however, provide you with a basis for verifying
the code. Consider always following the CAX cycle, as demonstrated in this
chapter, for generating code:
• Create both production code and tests when prompting the LLM, using
(ZOM-inclusive) examples as the basis for the tests.
• Assess the fidelity of the generated tests with the examples you provided.
• e*Xecute the tests. Repeat the cycle (with alterations) if they don’t all pass.
Also, provide a small set of programming style guidelines to your LLM to
improve the solution’s design and potentially increase the likelihood of a
correct solution. Jeff-Java style represents a good starting point.
Will I Go Faster?
AI tools are only now emerging from their infancy, but they show a lot of
promise. As with human toddlers, they thrive when you provide them with
some direction and safeguards, but they can also surprise you with their
cleverness, particularly when you let them explore.
Good design makes so many things easier: writing tests around code, under-
standing code, extending code, and so on. Generating code via an LLM is also
easier when you direct it to follow a small set of guidelines for design that
promote small, focused methods and intention-revealing names.
report erratum  •  discuss
Increasing Odds of Success with AI-Generated Code • 263


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


