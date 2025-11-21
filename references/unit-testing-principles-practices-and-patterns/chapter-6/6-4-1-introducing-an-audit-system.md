# 6.4.1 Introducing an audit system (pp.135-137)

---
**Page 135**

135
Transitioning to functional architecture and output-based testing
6.4
Transitioning to functional architecture and output-
based testing
In this section, we’ll take a sample application and refactor it toward functional archi-
tecture. You’ll see two refactoring stages:
Moving from using an out-of-process dependency to using mocks
Moving from using mocks to using functional architecture
The transition affects test code, too! We’ll refactor state-based and communication-
based tests to the output-based style of unit testing. Before starting the refactoring,
let’s review the sample project and tests covering it.
6.4.1
Introducing an audit system
The sample project is an audit system that keeps track of all visitors in an organization.
It uses flat text files as underlying storage with the structure shown in figure 6.11. The
system appends the visitor’s name and the time of their visit to the end of the most
recent file. When the maximum number of entries per file is reached, a new file with
an incremented index is created.
The following listing shows the initial version of the system.
public class AuditManager
{
private readonly int _maxEntriesPerFile;
private readonly string _directoryName;
public AuditManager(int maxEntriesPerFile, string directoryName)
{
_maxEntriesPerFile = maxEntriesPerFile;
_directoryName = directoryName;
}
Listing 6.8
Initial implementation of the audit system
Jane;
Jack;
Peter; 2019-04-06T16:30:00
2019-04-06T16:40:00
2019-04-06T17:00:00
Mary;
2019-04-06T17:30:00
New Person; Time of visit
audit_01.txt
audit_02.txt
Figure 6.11
The audit system stores information 
about visitors in text files with a specific format. 
When the maximum number of entries per file is 
reached, the system creates a new file.


---
**Page 136**

136
CHAPTER 6
Styles of unit testing
public void AddRecord(string visitorName, DateTime timeOfVisit)
{
string[] filePaths = Directory.GetFiles(_directoryName);
(int index, string path)[] sorted = SortByIndex(filePaths);
string newRecord = visitorName + ';' + timeOfVisit;
if (sorted.Length == 0)
{
string newFile = Path.Combine(_directoryName, "audit_1.txt");
File.WriteAllText(newFile, newRecord);
return;
}
(int currentFileIndex, string currentFilePath) = sorted.Last();
List<string> lines = File.ReadAllLines(currentFilePath).ToList();
if (lines.Count < _maxEntriesPerFile)
{
lines.Add(newRecord);
string newContent = string.Join("\r\n", lines);
File.WriteAllText(currentFilePath, newContent);
}
else
{
int newIndex = currentFileIndex + 1;
string newName = $"audit_{newIndex}.txt";
string newFile = Path.Combine(_directoryName, newName);
File.WriteAllText(newFile, newRecord);
}
}
}
The code might look a bit large, but it’s quite simple. AuditManager is the main class
in the application. Its constructor accepts the maximum number of entries per file
and the working directory as configuration parameters. The only public method in
the class is AddRecord, which does all the work of the audit system:
Retrieves a full list of files from the working directory
Sorts them by index (all filenames follow the same pattern: audit_{index}.txt
[for example, audit_1.txt])
If there are no audit files yet, creates a first one with a single record
If there are audit files, gets the most recent one and either appends the new
record to it or creates a new file, depending on whether the number of entries
in that file has reached the limit
The AuditManager class is hard to test as-is, because it’s tightly coupled to the file-
system. Before the test, you’d need to put files in the right place, and after the test
finishes, you’d read those files, check their contents, and clear them out (figure 6.12).


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


