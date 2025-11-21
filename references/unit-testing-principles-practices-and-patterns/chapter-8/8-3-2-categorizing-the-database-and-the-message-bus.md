# 8.3.2 Categorizing the database and the message bus (pp.195-195)

---
**Page 195**

195
Integration testing: An example
8.3.2
Categorizing the database and the message bus
Before writing the integration test, you need to categorize the two out-of-process
dependencies and decide which of them to test directly and which to replace with a
mock. The application database is a managed dependency because no other system
can access it. Therefore, you should use a real instance of it. The integration test will
Insert a user and a company into the database.
Run the change of email scenario on that database.
Verify the database state.
On the other hand, the message bus is an unmanaged dependency—its sole pur-
pose is to enable communication with other systems. The integration test will mock
out the message bus and verify the interactions between the controller and the
mock afterward. 
8.3.3
What about end-to-end testing?
There will be no end-to-end tests in our sample project. An end-to-end test in a sce-
nario with an API would be a test running against a deployed, fully functioning ver-
sion of that API, which means no mocks for any of the out-of-process dependencies
(figure 8.7). On the other hand, integration tests host the application within the same
process and substitute unmanaged dependencies with mocks (figure 8.8).
 As I mentioned in chapter 2, whether to use end-to-end tests is a judgment call. For
the most part, when you include managed dependencies in the integration testing
scope and mock out only unmanaged dependencies, integration tests provide a level
End-to-end test
Application
Message bus
Database
Out-of-process
In-process
Figure 8.7
End-to-end tests emulate the external client and therefore test a 
deployed version of the application with all out-of-process dependencies included 
in the testing scope. End-to-end tests shouldn’t check managed dependencies 
(such as the database) directly, only indirectly through the application.


