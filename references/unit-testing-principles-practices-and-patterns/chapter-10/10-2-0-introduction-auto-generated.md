# 10.2.0 Introduction [auto-generated] (pp.234-235)

---
**Page 234**

234
CHAPTER 10
Testing the database
Such a distinction leads to different sets of trade-offs. The explicitness of the database
state makes it easier to handle merge conflicts, while explicit migrations help to tackle
data motion.
DEFINITION
Data motion is the process of changing the shape of existing data
so that it conforms to the new database schema.
Although the alleviation of merge conflicts and the ease of data motion might look
like equally important benefits, in the vast majority of projects, data motion is much more
important than merge conflicts. Unless you haven’t yet released your application to pro-
duction, you always have data that you can’t simply discard.
 For example, when splitting a Name column into FirstName and LastName, you not
only have to drop the Name column and create the new FirstName and LastName col-
umns, but you also have to write a script to split all existing names into two pieces.
There is no easy way to implement this change using the state-driven approach; com-
parison tools are awful when it comes to managing data. The reason is that while the
database schema itself is objective, meaning there is only one way to interpret it, data
is context-dependent. No tool can make reliable assumptions about data when gener-
ating upgrade scripts. You have to apply domain-specific rules in order to implement
proper transformations.
 As a result, the state-based approach is impractical in the vast majority of projects.
You can use it temporarily, though, while the project still has not been released to pro-
duction. After all, test data isn’t that important, and you can re-create it every time you
change the database. But once you release the first version, you will have to switch to
the migration-based approach in order to handle data motion properly.
TIP
Apply every modification to the database schema (including reference
data) through migrations. Don’t modify migrations once they are committed
to the source control. If a migration is incorrect, create a new migration
instead of fixing the old one. Make exceptions to this rule only when the
incorrect migration can lead to data loss. 
10.2
Database transaction management
Database transaction management is a topic that’s important for both production and
test code. Proper transaction management in production code helps you avoid data
inconsistencies. In tests, it helps you verify integration with the database in a close-to-
production setting.
 In this section, I’ll first show how to handle transactions in the production code
(the controller) and then demonstrate how to use them in integration tests. I’ll con-
tinue using the same CRM project you saw in the earlier chapters as an example.


---
**Page 235**

235
Database transaction management
10.2.1 Managing database transactions in production code
Our sample CRM project uses the Database class to work with User and Company.
Database creates a separate SQL connection on each method call. Every such connec-
tion implicitly opens an independent transaction behind the scenes, as the following
listing shows.
public class Database
{
private readonly string _connectionString;
public Database(string connectionString)
{
_connectionString = connectionString;
}
public void SaveUser(User user)
{
bool isNewUser = user.UserId == 0;
using (var connection =
new SqlConnection(_connectionString))      
{
/* Insert or update the user depending on isNewUser */
}
}
public void SaveCompany(Company company)
{
using (var connection =
new SqlConnection(_connectionString))      
{
/* Update only; there's only one company */
}
}
}
As a result, the user controller creates a total of four database transactions during a
single business operation, as shown in the following listing.
public string ChangeEmail(int userId, string newEmail)
{
object[] userData = _database.GetUserById(userId);    
User user = UserFactory.Create(userData);
string error = user.CanChangeEmail();
if (error != null)
return error;
Listing 10.1
Class that enables access to the database
Listing 10.2
User controller
Opens a
database
transaction
Opens a new 
database 
transaction


