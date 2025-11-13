# 13.9 Increasing Odds of Success with AI-Generated Code (pp.263-263)

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


