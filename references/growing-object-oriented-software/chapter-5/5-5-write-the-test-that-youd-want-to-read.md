# 5.5 Write the Test That You'd Want to Read (pp.42-42)

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


