# 8.2.2 Working with both managed and unmanaged dependencies (pp.191-192)

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


---
**Page 192**

192
CHAPTER 8
Why integration testing?
other applications as an unmanaged dependency. Such tables in effect act as a mes-
sage bus, with their rows playing the role of messages. Use mocks to make sure the
communication pattern with these tables remains unchanged. At the same time, treat
the rest of your database as a managed dependency and verify its final state, not the
interactions with it (figure 8.5).
It’s important to differentiate these two parts of your database because, again, the
shared tables are observable externally, and you need to be careful about how your
application communicates with them. Don’t change the way your system interacts with
those tables unless absolutely necessary! You never know how other applications will
react to such a change. 
8.2.3
What if you can’t use a real database in integration tests?
Sometimes, for reasons outside of your control, you just can’t use a real version of a
managed dependency in integration tests. An example would be a legacy database
that you can’t deploy to a test automation environment, not to mention a developer
machine, because of some IT security policy, or because the cost of setting up and
maintaining a test database instance is prohibitive.
 What should you do in such a situation? Should you mock out the database anyway,
despite it being a managed dependency? No, because mocking out a managed depen-
dency compromises the integration tests’ resistance to refactoring. Furthermore, such
External applications
Table
Table
Table
Table
Managed part
Table
Table
Unmanaged part
Test directly
Replace with mocks
Database
Your application
Figure 8.5
Treat the part of the database that is visible to external 
applications as an unmanaged dependency. Replace it with mocks in 
integration tests. Treat the rest of the database as a managed dependency. 
Verify its final state, not interactions with it.


