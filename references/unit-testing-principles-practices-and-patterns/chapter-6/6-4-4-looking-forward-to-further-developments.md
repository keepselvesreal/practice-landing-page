# 6.4.4 Looking forward to further developments (pp.146-146)

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


