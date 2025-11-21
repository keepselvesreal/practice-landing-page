# 8.2.1 The two types of out-of-process dependencies (pp.190-191)

---
**Page 190**

190
CHAPTER 8
Why integration testing?
8.2
Which out-of-process dependencies to test directly
As I mentioned earlier, integration tests verify how your system integrates with out-of-
process dependencies. There are two ways to implement such verification: use the real
out-of-process dependency, or replace that dependency with a mock. This section
shows when to apply each of the two approaches.
8.2.1
The two types of out-of-process dependencies
All out-of-process dependencies fall into two categories:
Managed dependencies (out-of-process dependencies you have full control over)—These
dependencies are only accessible through your application; interactions with
them aren’t visible to the external world. A typical example is a database. Exter-
nal systems normally don’t access your database directly; they do that through
the API your application provides.
Unmanaged dependencies (out-of-process dependencies you don’t have full control over)—
Interactions with such dependencies are observable externally. Examples include
an SMTP server and a message bus: both produce side effects visible to other
applications.
I mentioned in chapter 5 that communications with managed dependencies are
implementation details. Conversely, communications with unmanaged dependencies
are part of your system’s observable behavior (figure 8.4). This distinction leads to the
difference in treatment of out-of-process dependencies in integration tests.
IMPORTANT
Use real instances of managed dependencies; replace unman-
aged dependencies with mocks.
As discussed in chapter 5, the requirement to preserve the communication pattern
with unmanaged dependencies stems from the necessity to maintain backward com-
patibility with those dependencies. Mocks are perfect for this task. With mocks, you
can ensure communication pattern permanence in light of any possible refactorings.
(continued)
Stopping the current operation is normally done by throwing exceptions, because
exceptions have semantics that are perfectly suited for the Fail Fast principle: they
interrupt the program flow and pop up to the highest level of the execution stack,
where you can log them and shut down or restart the operation.
Preconditions are one example of the Fail Fast principle in action. A failing precondi-
tion signifies an incorrect assumption made about the application state, which is
always a bug. Another example is reading data from a configuration file. You can
arrange the reading logic such that it will throw an exception if the data in the config-
uration file is incomplete or incorrect. You can also put this logic close to the appli-
cation startup, so that the application doesn’t launch if there’s a problem with its
configuration. 


---
**Page 191**

191
Which out-of-process dependencies to test directly
However, there’s no need to maintain backward compatibility in communications with
managed dependencies, because your application is the only one that talks to them.
External clients don’t care how you organize your database; the only thing that mat-
ters is the final state of your system. Using real instances of managed dependencies in
integration tests helps you verify that final state from the external client’s point of
view. It also helps during database refactorings, such as renaming a column or even
migrating from one database to another. 
8.2.2
Working with both managed and unmanaged dependencies
Sometimes you’ll encounter an out-of-process dependency that exhibits attributes of
both managed and unmanaged dependencies. A good example is a database that
other applications have access to.
 The story usually goes like this. A system begins with its own dedicated database. After
a while, another system begins to require data from the same database. And so the team
decides to share access to a limited number of tables just for ease of integration with that
other system. As a result, the database becomes a dependency that is both managed and
unmanaged. It still contains parts that are visible to your application only; but, in addi-
tion to those parts, it also has a number of tables accessible by other applications.
 The use of a database is a poor way to implement integration between systems
because it couples these systems to each other and complicates their further develop-
ment. Only resort to this approach when all other options are exhausted. A better way
to do the integration is via an API (for synchronous communications) or a message
bus (for asynchronous communications).
 But what do you do when you already have a shared database and can’t do any-
thing about it in the foreseeable future? In this case, treat tables that are visible to
SMTP service
(unmanaged
dependency)
Observable behavior (contract)
Implementation details
Application
database
(managed
dependency)
Third-party
system
(external
client)
Figure 8.4
Communications with managed dependencies are implementation 
details; use such dependencies as-is in integration tests. Communications 
with unmanaged dependencies are part of your system’s observable behavior. 
Such dependencies should be mocked out.


