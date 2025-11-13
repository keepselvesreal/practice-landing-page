# 6.5.0 Introduction [auto-generated] (pp.146-147)

---
**Page 146**

146
CHAPTER 6
Styles of unit testing
6.4.4
Looking forward to further developments
Let’s step back for a minute and look at further developments that could be done in
our sample project. The audit system I showed you is quite simple and contains only
three branches:
Creating a new file in case of an empty working directory
Appending a new record to an existing file
Creating another file when the number of entries in the current file exceeds
the limit
Also, there’s only one use case: addition of a new entry to the audit log. What if
there were another use case, such as deleting all mentions of a particular visitor?
And what if the system needed to do validations (say, for the maximum length of the
visitor’s name)?
 Deleting all mentions of a particular visitor could potentially affect several files, so
the new method would need to return multiple file instructions:
public FileUpdate[] DeleteAllMentions(
FileContent[] files, string visitorName)
Furthermore, business people might require that you not keep empty files in the
working directory. If the deleted entry was the last entry in an audit file, you would
need to remove that file altogether. To implement this requirement, you could
rename FileUpdate to FileAction and introduce an additional ActionType enum
field to indicate whether it was an update or a deletion.
 Error handling also becomes simpler and more explicit with functional architec-
ture. You could embed errors into the method’s signature, either in the FileUpdate
class or as a separate component:
public (FileUpdate update, Error error) AddRecord(
FileContent[] files,
string visitorName,
DateTime timeOfVisit)
The application service would then check for this error. If it was there, the service
wouldn’t pass the update instruction to the persister, instead propagating an error
message to the user. 
6.5
Understanding the drawbacks of functional 
architecture
Unfortunately, functional architecture isn’t always attainable. And even when it is, the
maintainability benefits are often offset by a performance impact and increase in
the size of the code base. In this section, we’ll explore the costs and the trade-offs
attached to functional architecture.


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


