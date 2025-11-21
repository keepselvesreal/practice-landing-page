# 5.4 Start Testing with the Simplest Success Case (pp.41-42)

---
**Page 41**

Start Testing with the Simplest Success Case
Where do we start when we have to write a new class or feature? It’s tempting
to start with degenerate or failure cases because they’re often easier. That’s a
common interpretation of the XP maxim to do “the simplest thing that could
possibly work” [Beck02], but simple should not be interpreted as simplistic.
Degenerate cases don’t add much to the value of the system and, more important-
ly, don’t give us enough feedback about the validity of our ideas. Incidentally,
we also ﬁnd that focusing on the failure cases at the beginning of a feature is bad
for morale—if we only work on error handling it feels like we’re not achieving
anything.
We prefer to start by testing the simplest success case. Once that’s working,
we’ll have a better idea of the real structure of the solution and can prioritize
between handling any possible failures we noticed along the way and further
success cases. Of course, a feature isn’t complete until it’s robust. This isn’t an
excuse not to bother with failure handling—but we can choose when we want
to implement ﬁrst.
We ﬁnd it useful to keep a notepad or index cards by the keyboard to jot down
failure cases, refactorings, and other technical tasks that need to be addressed.
This allows us to stay focused on the task at hand without dropping detail. The
feature is ﬁnished only when we’ve crossed off everything on the list—either
we’ve done each task or decided that we don’t need to.
Iterations in Space
We’re writing this material around the fortieth anniversary of the ﬁrst Moon landing.
The Moon program was an excellent example of an incremental approach (although
with much larger stakes than we’re used to). In 1967, they proposed a series of
seven missions, each of which would be a step on the way to a landing:
1.
Unmanned Command/Service Module (CSM) test
2.
Unmanned Lunar Module (LM) test
3.
Manned CSM in low Earth orbit
4.
Manned CSM and LM in low Earth orbit
5.
Manned CSM and LM in an elliptical Earth orbit with an apogee of 4600 mi
(7400 km)
6.
Manned CSM and LM in lunar orbit
7.
Manned lunar landing
At least in software, we can develop incrementally without building a new rocket
each time.
41
Start Testing with the Simplest Success Case


---
**Page 42**

Write the Test That You’d Want to Read
We want each test to be as clear as possible an expression of the behavior to be
performed by the system or object. While writing the test, we ignore the fact that
the test won’t run, or even compile, and just concentrate on its text; we act as
if the supporting code to let us run the test already exists.
When the test reads well, we then build up the infrastructure to support the
test. We know we’ve implemented enough of the supporting code when the test
fails in the way we’d expect, with a clear error message describing what needs
to be done. Only then do we start writing the code to make the test pass. We
look further at making tests readable in Chapter 21.
Watch the Test Fail
We always watch the test fail before writing the code to make it pass, and check
the diagnostic message. If the test fails in a way we didn’t expect, we know we’ve
misunderstood something or the code is incomplete, so we ﬁx that. When we get
the “right” failure, we check that the diagnostics are helpful. If the failure descrip-
tion isn’t clear, someone (probably us) will have to struggle when the code breaks
in a few weeks’ time. We adjust the test code and rerun the tests until the error
messages guide us to the problem with the code (Figure 5.2).
Figure 5.2
Improving the diagnostics as part of the TDD cycle
As we write the production code, we keep running the test to see our progress
and to check the error diagnostics as the system is built up behind the test. Where
necessary, we extend or modify the support code to ensure the error messages
are always clear and relevant.
There’s more than one reason for insisting on checking the error messages.
First, it checks our assumptions about the code we’re working on—sometimes
Chapter 5
Maintaining the Test-Driven Cycle
42


