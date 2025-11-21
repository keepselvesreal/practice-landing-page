# 3.10.3 What coverage criterion to use (pp.88-88)

---
**Page 88**

88
CHAPTER 3
Structural testing and code coverage
3.10.3 What coverage criterion to use
This is a popular question among practitioners and researchers. If we settle for a
less-rigorous criterion, such as line coverage instead of branch coverage, we might
miss something. Plus this question brings the focus back to the metric, which we do
not want.
 Which criterion to use depends on the context: what you are testing at that
moment and how rigorous you want the testing to be. Structural testing is meant to
complement specification-based testing. When you dive into the source code and look
for uncovered parts, you may decide to use branch coverage for a specific if expres-
sion but MC/DC for another if expression. This makes the approach less systematic
(and, therefore, more prone to errors and different developers using different crite-
ria), but it is the most pragmatic approach I know. You may want to perform some risk
assessment to determine how important it is to be thorough.
 My rule of thumb is branch coverage: I always try to at least reach all the branches
of the program. Whenever I see a more complicated expression, I evaluate the need
for condition + branch coverage. If I see an even more complex expression, I consider
MC/DC. 
3.10.4 MC/DC when expressions are too complex and 
cannot be simplified
MC/DC is increasingly valuable as expressions become more complicated. Listing 3.11
shows an example of a complex expression that I extracted from Chilenski’s 2001
paper. It is an anonymized version of a condition found in a level A flight simulation
program and contains an impressive 76 conditions. Achieving path coverage in such a
complex expression is impossible (276 = 7.5 × 1022 test cases), so smart approaches
such as MC/DC come in handy.
Bv or (Ev != El) or Bv2 or Bv3 or Bv4 or Bv5 or Bv6 or Bv7 or Bv8 or Bv9 or
Bv10 or Bv11 or Bv12 or Bv13 or Bv14 or Bv15 or Bv16 or Bv17 or Bv18 or
Bv19 or Bv20 or Bv21 or Bv22 or Bv23 or Bv24 or Bv25 or Bv26 or Bv27 or
Bv28 or Bv29 or Bv30 or Bv31 or Bv32 or Bv33 or Bv34 or Bv35 or Bv36 or
Bv37 or Bv38 or Bv39 or Bv40 or Bv41 or Bv42 or Bv43 or Bv44 or Bv45 or
Bv46 or Bv47 or Bv48 or Bv49 or Bv50 or Bv51 or (Ev2 = El2) or
((Ev3 = El2) and (Sav != Sac)) or Bv52 or Bv53 or Bv54 or Bv55 or Bv56
or Bv57 or Bv58 or Bv59 or Bv60 or Bv61 or Bv62 or Bv63 or Bv64 or Bv65
or Ev4 != El3 or Ev5 = El4 or Ev6 = El4 or Ev7 = El4 or Ev8 = El4 or
Ev9 = El4 or Ev10 = El4
Pragmatically speaking, testing such a complex expression, with or without MC/DC, is
a challenge, and you should avoid doing so when possible. Sometimes you can break
an expression into smaller bits that you can then test. But in cases where breaking
complex expressions is not possible, MC/DC shines.
Listing 3.11
Complex expression from flight simulation software


