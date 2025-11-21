# 6.5.1 Applicability of functional architecture (pp.147-148)

---
**Page 147**

147
Understanding the drawbacks of functional architecture
6.5.1
Applicability of functional architecture
Functional architecture worked for our audit system because this system could gather
all the inputs up front, before making a decision. Often, though, the execution flow is
less straightforward. You might need to query additional data from an out-of-process
dependency, based on an intermediate result of the decision-making process.
 Here’s an example. Let’s say the audit system needs to check the visitor’s access
level if the number of times they have visited during the last 24 hours exceeds some
threshold. And let’s also assume that all visitors’ access levels are stored in a database.
You can’t pass an IDatabase instance to AuditManager like this:
public FileUpdate AddRecord(
FileContent[] files, string visitorName,
DateTime timeOfVisit, IDatabase database
)
Such an instance would introduce a hidden input to the AddRecord() method. This
method would, therefore, cease to be a mathematical function (figure 6.16), which
means you would no longer be able to apply output-based testing.
There are two solutions in such a situation:
You can gather the visitor’s access level in the application service up front,
along with the directory content.
You can introduce a new method such as IsAccessLevelCheckRequired() in
AuditManager. The application service would call this method before Add-
Record(), and if it returned true, the service would get the access level from
the database and pass it to AddRecord().
Both approaches have drawbacks. The first one concedes performance—it uncondi-
tionally queries the database, even in cases when the access level is not required. But this
approach keeps the separation of business logic and communication with external
Application
service
ReadDirectory
Audit manager
Filesystem
and database
Add
record
ApplyUpdate
Get
access
level
Figure 6.16
A dependency on the database introduces a hidden input to 
AuditManager. Such a class is no longer purely functional, and the whole 
application no longer follows the functional architecture.


---
**Page 148**

148
CHAPTER 6
Styles of unit testing
systems fully intact: all decision-making resides in AuditManager as before. The second
approach concedes a degree of that separation for performance gains: the decision as
to whether to call the database now goes to the application service, not AuditManager.
 Note that, unlike these two options, making the domain model (AuditManager)
depend on the database isn’t a good idea. I’ll explain more about keeping the balance
between performance and separation of concerns in the next two chapters.
NOTE
A class from the functional core should work not with a collaborator,
but with the product of its work, a value. 
6.5.2
Performance drawbacks
The performance impact on the system as a whole is a common argument against
functional architecture. Note that it’s not the performance of tests that suffers. The
output-based tests we ended up with work as fast as the tests with mocks. It’s that the
system itself now has to do more calls to out-of-process dependencies and becomes
less performant. The initial version of the audit system didn’t read all files from the
working directory, and neither did the version with mocks. But the final version does
in order to comply with the read-decide-act approach.
 The choice between a functional architecture and a more traditional one is a
trade-off between performance and code maintainability (both production and test
code). In some systems where the performance impact is not as noticeable, it’s better
to go with functional architecture for additional gains in maintainability. In others,
you might need to make the opposite choice. There’s no one-size-fits-all solution. 
Collaborators vs. values
You may have noticed that AuditManager’s AddRecord() method has a dependency
that’s not present in its signature: the _maxEntriesPerFile field. The audit man-
ager refers to this field to make a decision to either append an existing audit file or
create a new one.
Although this dependency isn’t present among the method’s arguments, it’s not hid-
den. It can be derived from the class’s constructor signature. And because the _max-
EntriesPerFile field is immutable, it stays the same between the class instantiation
and the call to AddRecord(). In other words, that field is a value.
The situation with the IDatabase dependency is different because it’s a collaborator,
not a value like _maxEntriesPerFile. As you may remember from chapter 2, a col-
laborator is a dependency that is one or the other of the following:
Mutable (allows for modification of its state)
A proxy to data that is not yet in memory (a shared dependency)
The IDatabase instance falls into the second category and, therefore, is a collabo-
rator. It requires an additional call to an out-of-process dependency and thus pre-
cludes the use of output-based testing.


