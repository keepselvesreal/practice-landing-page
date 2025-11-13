# 6.4.3 Refactoring toward functional architecture (pp.140-146)

---
**Page 140**

140
CHAPTER 6
Styles of unit testing
"Jack; 2019-04-06T17:00:00"
});
var sut = new AuditManager(3, "audits", fileSystemMock.Object);
sut.AddRecord("Alice", DateTime.Parse("2019-04-06T18:00:00"));
fileSystemMock.Verify(x => x.WriteAllText(
@"audits\audit_3.txt",
"Alice;2019-04-06T18:00:00"));
}
This test verifies that when the number of entries in the current file reaches the limit
(3, in this example), a new file with a single audit entry is created. Note that this is a
legitimate use of mocks. The application creates files that are visible to end users
(assuming that those users use another program to read the files, be it specialized soft-
ware or a simple notepad.exe). Therefore, communications with the filesystem and
the side effects of these communications (that is, the changes in files) are part of the
application’s observable behavior. As you may remember from chapter 5, that’s the
only legitimate use case for mocking.
 This alternative implementation is an improvement over the initial version. Since
tests no longer access the filesystem, they execute faster. And because you don’t need
to look after the filesystem to keep the tests happy, the maintenance costs are also
reduced. Protection against regressions and resistance to refactoring didn’t suffer
from the refactoring either. Table 6.3 shows the differences between the two versions.
We can still do better, though. The test in listing 6.11 contains convoluted setups,
which is less than ideal in terms of maintenance costs. Mocking libraries try their best
to be helpful, but the resulting tests are still not as readable as those that rely on plain
input and output. 
6.4.3
Refactoring toward functional architecture
Instead of hiding side effects behind an interface and injecting that interface into
AuditManager, you can move those side effects out of the class entirely. Audit-
Manager is then only responsible for making a decision about what to do with the
files. A new class, Persister, acts on that decision and applies updates to the filesys-
tem (figure 6.14).
Table 6.3
The version with mocks compared to the initial version of the audit system
Initial version
With mocks
Protection against regressions
Good
Good
Resistance to refactoring
Good
Good
Fast feedback
Bad
Good
Maintainability
Bad
Moderate


---
**Page 141**

141
Transitioning to functional architecture and output-based testing
Persister in this scenario acts as a mutable shell, while AuditManager becomes a func-
tional (immutable) core. The following listing shows AuditManager after the refactoring.
public class AuditManager
{
private readonly int _maxEntriesPerFile;
public AuditManager(int maxEntriesPerFile)
{
_maxEntriesPerFile = maxEntriesPerFile;
}
public FileUpdate AddRecord(
FileContent[] files,
string visitorName,
DateTime timeOfVisit)
{
(int index, FileContent file)[] sorted = SortByIndex(files);
string newRecord = visitorName + ';' + timeOfVisit;
if (sorted.Length == 0)
{
return new FileUpdate(
  
"audit_1.txt", newRecord);  
}
(int currentFileIndex, FileContent currentFile) = sorted.Last();
List<string> lines = currentFile.Lines.ToList();
Listing 6.12
The AuditManager class after refactoring
FileContent
FileUpdate
AuditManager
(functional core)
Persister
(mutable shell)
Figure 6.14
Persister and 
AuditManager form the functional 
architecture. Persister gathers files 
and their contents from the working 
directory, feeds them to AuditManager, 
and then converts the return value into 
changes in the filesystem.
Returns an update 
instruction


---
**Page 142**

142
CHAPTER 6
Styles of unit testing
if (lines.Count < _maxEntriesPerFile)
{
lines.Add(newRecord);
string newContent = string.Join("\r\n", lines);
return new FileUpdate(
     
currentFile.FileName, newContent);     
}
else
{
int newIndex = currentFileIndex + 1;
string newName = $"audit_{newIndex}.txt";
return new FileUpdate(
                   
newName, newRecord);                   
}
}
}
Instead of the working directory path, AuditManager now accepts an array of File-
Content. This class includes everything AuditManager needs to know about the filesys-
tem to make a decision:
public class FileContent
{
public readonly string FileName;
public readonly string[] Lines;
public FileContent(string fileName, string[] lines)
{
FileName = fileName;
Lines = lines;
}
}
And, instead of mutating files in the working directory, AuditManager now returns an
instruction for the side effect it would like to perform:
public class FileUpdate
{
public readonly string FileName;
public readonly string NewContent;
public FileUpdate(string fileName, string newContent)
{
FileName = fileName;
NewContent = newContent;
}
}
The following listing shows the Persister class.
 
 
Returns an 
update 
instruction


---
**Page 143**

143
Transitioning to functional architecture and output-based testing
public class Persister
{
public FileContent[] ReadDirectory(string directoryName)
{
return Directory
.GetFiles(directoryName)
.Select(x => new FileContent(
Path.GetFileName(x),
File.ReadAllLines(x)))
.ToArray();
}
public void ApplyUpdate(string directoryName, FileUpdate update)
{
string filePath = Path.Combine(directoryName, update.FileName);
File.WriteAllText(filePath, update.NewContent);
}
}
Notice how trivial this class is. All it does is read content from the working directory
and apply updates it receives from AuditManager back to that working directory. It has
no branching (no if statements); all the complexity resides in the AuditManager
class. This is the separation between business logic and side effects in action.
 To maintain such a separation, you need to keep the interface of FileContent and
FileUpdate as close as possible to that of the framework’s built-in file-interaction com-
mands. All the parsing and preparation should be done in the functional core, so that
the code outside of that core remains trivial. For example, if .NET didn’t contain the
built-in File.ReadAllLines() method, which returns the file content as an array of
lines, and only has File.ReadAllText(), which returns a single string, you’d need to
replace the Lines property in FileContent with a string too and do the parsing in
AuditManager:
public class FileContent
{
public readonly string FileName;
public readonly string Text; // previously, string[] Lines;
}
To glue AuditManager and Persister together, you need another class: an applica-
tion service in the hexagonal architecture taxonomy, as shown in the following listing.
public class ApplicationService
{
private readonly string _directoryName;
private readonly AuditManager _auditManager;
private readonly Persister _persister;
Listing 6.13
The mutable shell acting on AuditManager’s decision
Listing 6.14
Gluing together the functional core and mutable shell 


---
**Page 144**

144
CHAPTER 6
Styles of unit testing
public ApplicationService(
string directoryName, int maxEntriesPerFile)
{
_directoryName = directoryName;
_auditManager = new AuditManager(maxEntriesPerFile);
_persister = new Persister();
}
public void AddRecord(string visitorName, DateTime timeOfVisit)
{
FileContent[] files = _persister.ReadDirectory(_directoryName);
FileUpdate update = _auditManager.AddRecord(
files, visitorName, timeOfVisit);
_persister.ApplyUpdate(_directoryName, update);
}
}
Along with gluing the functional core together with the mutable shell, the application
service also provides an entry point to the system for external clients (figure 6.15).
With this implementation, it becomes easy to check the audit system’s behavior. All
tests now boil down to supplying a hypothetical state of the working directory and ver-
ifying the decision AuditManager makes.
[Fact]
public void A_new_file_is_created_when_the_current_file_overflows()
{
var sut = new AuditManager(3);
var files = new FileContent[]
{
new FileContent("audit_1.txt", new string[0]),
Listing 6.15
The test without mocks
Audit manager
Persister
Persister
Application service
External client
Figure 6.15
ApplicationService glues the functional core (AuditManager) 
and the mutable shell (Persister) together and provides an entry point for external 
clients. In the hexagonal architecture taxonomy, ApplicationService and 
Persister are part of the application services layer, while AuditManager 
belongs to the domain model.


---
**Page 145**

145
Transitioning to functional architecture and output-based testing
new FileContent("audit_2.txt", new string[]
{
"Peter; 2019-04-06T16:30:00",
"Jane; 2019-04-06T16:40:00",
"Jack; 2019-04-06T17:00:00"
})
};
FileUpdate update = sut.AddRecord(
files, "Alice", DateTime.Parse("2019-04-06T18:00:00"));
Assert.Equal("audit_3.txt", update.FileName);
Assert.Equal("Alice;2019-04-06T18:00:00", update.NewContent);
}
This test retains the improvement the test with mocks made over the initial version
(fast feedback) but also further improves on the maintainability metric. There’s no
need for complex mock setups anymore, only plain inputs and outputs, which helps
the test’s readability a lot. Table 6.4 compares the output-based test with the initial ver-
sion and the version with mocks.
Notice that the instructions generated by a functional core are always a value or a set of
values. Two instances of such a value are interchangeable as long as their contents
match. You can take advantage of this fact and improve test readability even further by
turning FileUpdate into a value object. To do that in .NET, you need to either convert
the class into a struct or define custom equality members. That will give you compar-
ison by value, as opposed to the comparison by reference, which is the default behavior
for classes in C#. Comparison by value also allows you to compress the two assertions
from listing 6.15 into one:
Assert.Equal(
new FileUpdate("audit_3.txt", "Alice;2019-04-06T18:00:00"),
update);
Or, using Fluent Assertions,
update.Should().Be(
new FileUpdate("audit_3.txt", "Alice;2019-04-06T18:00:00"));
Table 6.4
The output-based test compared to the previous two versions
Initial version
With mocks
Output-based
Protection against regressions
Good
Good
Good
Resistance to refactoring
Good
Good
Good
Fast feedback
Bad
Good
Good
Maintainability
Bad
Moderate
Good


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


