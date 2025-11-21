# 5.1 Introduction (pp.39-39)

---
**Page 39**

Chapter 5
Maintaining the Test-Driven
Cycle
Every day you may make progress. Every step may be fruitful. Yet there
will stretch out before you an ever-lengthening, ever-ascending,
ever-improving path. You know you will never get to the end of the
journey. But this, so far from discouraging, only adds to the joy and
glory of the climb.
—Winston Churchill
Introduction
Once we’ve kick-started the TDD process, we need to keep it running smoothly.
In this chapter we’ll show how a TDD process runs once started. The rest of the
book explores in some detail how we ensure it runs smoothly—how we write
tests as we build the system, how we use tests to get early feedback on internal
and external quality issues, and how we ensure that the tests continue to support
change and do not become an obstacle to further development.
Start Each Feature with an Acceptance Test
As we described in Chapter 1, we start work on a new feature by writing failing
acceptance tests that demonstrate that the system does not yet have the feature
we’re about to write and track our progress towards completion of the
feature (Figure 5.1).
We write the acceptance test using only terminology from the application’s
domain, not from the underlying technologies (such as databases or web servers).
This helps us understand what the system should do, without tying us to any of
our initial assumptions about the implementation or complicating the test with
technological details. This also shields our acceptance test suite from changes to
the system’s technical infrastructure. For example, if a third-party organization
changes the protocol used by their services from FTP and binary ﬁles to web
services and XML, we should not have to rework the tests for the system’s
application logic.
We ﬁnd that writing such a test before coding makes us clarify what we want
to achieve. The precision of expressing requirements in a form that can be auto-
matically checked helps us uncover implicit assumptions. The failing tests keep
39


