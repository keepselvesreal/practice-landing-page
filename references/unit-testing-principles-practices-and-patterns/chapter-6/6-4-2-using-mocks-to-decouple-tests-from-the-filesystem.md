# 6.4.2 Using mocks to decouple tests from the filesystem (pp.137-140)

---
**Page 137**

137
Transitioning to functional architecture and output-based testing
You won’t be able to parallelize such tests—at least, not without additional effort
that would significantly increase maintenance costs. The bottleneck is the filesys-
tem: it’s a shared dependency through which tests can interfere with each other’s
execution flow.
 The filesystem also makes the tests slow. Maintainability suffers, too, because you
have to make sure the working directory exists and is accessible to tests—both on your
local machine and on the build server. Table 6.2 sums up the scoring.
By the way, tests working directly with the filesystem don’t fit the definition of a unit
test. They don’t comply with the second and the third attributes of a unit test, thereby
falling into the category of integration tests (see chapter 2 for more details):
A unit test verifies a single unit of behavior,
Does it quickly,
And does it in isolation from other tests. 
6.4.2
Using mocks to decouple tests from the filesystem
The usual solution to the problem of tightly coupled tests is to mock the filesystem.
You can extract all operations on files into a separate class (IFileSystem) and inject
that class into AuditManager via the constructor. The tests will then mock this class
and capture the writes the audit system do to the files (figure 6.13).
 
 
 
Table 6.2
The initial version of the audit system scores badly on two out 
of the four attributes of a good test.
Initial version
Protection against regressions
Good
Resistance to refactoring
Good
Fast feedback
Bad
Maintainability
Bad
Audit system
Filesystem
Test
input
input
input
output
assert
Figure 6.12
Tests covering the initial version of the audit system would 
have to work directly with the filesystem.


---
**Page 138**

138
CHAPTER 6
Styles of unit testing
The following listing shows how the filesystem is injected into AuditManager.
public class AuditManager
{
private readonly int _maxEntriesPerFile;
private readonly string _directoryName;
private readonly IFileSystem _fileSystem;    
public AuditManager(
int maxEntriesPerFile,
string directoryName,
IFileSystem fileSystem)
{
_maxEntriesPerFile = maxEntriesPerFile;
_directoryName = directoryName;
_fileSystem = fileSystem;                
}
}
And next is the AddRecord method.
public void AddRecord(string visitorName, DateTime timeOfVisit)
{
string[] filePaths = _fileSystem                                
.GetFiles(_directoryName);                                  
(int index, string path)[] sorted = SortByIndex(filePaths);
string newRecord = visitorName + ';' + timeOfVisit;
if (sorted.Length == 0)
{
string newFile = Path.Combine(_directoryName, "audit_1.txt");
_fileSystem.WriteAllText(                                   
newFile, newRecord);                                    
return;
}
Listing 6.9
Injecting the filesystem explicitly via the constructor
Listing 6.10
Using the new IFileSystem interface
mock
stub
input
Audit system
Test
Filesystem
Figure 6.13
Tests can mock the 
filesystem and capture the writes 
the audit system makes to the files.
The new interface 
represents the 
filesystem.
The new
interface
in action


---
**Page 139**

139
Transitioning to functional architecture and output-based testing
(int currentFileIndex, string currentFilePath) = sorted.Last();
List<string> lines = _fileSystem
          
.ReadAllLines(currentFilePath);          
if (lines.Count < _maxEntriesPerFile)
{
lines.Add(newRecord);
string newContent = string.Join("\r\n", lines);
_fileSystem.WriteAllText(
        
currentFilePath, newContent);        
}
else
{
int newIndex = currentFileIndex + 1;
string newName = $"audit_{newIndex}.txt";
string newFile = Path.Combine(_directoryName, newName);
_fileSystem.WriteAllText(                
newFile, newRecord);                 
}
}
In listing 6.10, IFileSystem is a new custom interface that encapsulates the work with
the filesystem:
public interface IFileSystem
{
string[] GetFiles(string directoryName);
void WriteAllText(string filePath, string content);
List<string> ReadAllLines(string filePath);
}
Now that AuditManager is decoupled from the filesystem, the shared dependency is
gone, and tests can execute independently from each other. Here’s one such test.
[Fact]
public void A_new_file_is_created_when_the_current_file_overflows()
{
var fileSystemMock = new Mock<IFileSystem>();
fileSystemMock
.Setup(x => x.GetFiles("audits"))
.Returns(new string[]
{
@"audits\audit_1.txt",
@"audits\audit_2.txt"
});
fileSystemMock
.Setup(x => x.ReadAllLines(@"audits\audit_2.txt"))
.Returns(new List<string>
{
"Peter; 2019-04-06T16:30:00",
"Jane; 2019-04-06T16:40:00",
Listing 6.11
Checking the audit system’s behavior using a mock
The new
interface
in action


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


