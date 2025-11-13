# 5.2.2 Leaking implementation details: An example with an operation (pp.100-103)

---
**Page 100**

100
CHAPTER 5
Mocks and test fragility
code needs to have an immediate connection to at least one such goal. The word client
can refer to different things depending on where the code resides. The common
examples are client code from the same code base, an external application, or the
user interface.
 Ideally, the system’s public API surface should coincide with its observable behav-
ior, and all its implementation details should be hidden from the eyes of the clients.
Such a system has a well-designed API (figure 5.4).
Often, though, the system’s public API extends beyond its observable behavior and
starts exposing implementation details. Such a system’s implementation details leak to
its public API surface (figure 5.5). 
5.2.2
Leaking implementation details: An example with an operation
Let’s take a look at examples of code whose implementation details leak to the public
API. Listing 5.5 shows a User class with a public API that consists of two members: a
Name property and a NormalizeName() method. The class also has an invariant: users’
names must not exceed 50 characters and should be truncated otherwise.
public class User
{
public string Name { get; set; }
Listing 5.5
User class with leaking implementation details
Observable behavior
Public API
Private API
Implementation detail
Figure 5.4
In a well-designed API, the 
observable behavior coincides with the public 
API, while all implementation details are 
hidden behind the private API.
Observable behavior
Public API
Private API
Leaking implementation detail
Figure 5.5
A system leaks implementation 
details when its public API extends beyond 
the observable behavior.


---
**Page 101**

101
Observable behavior vs. implementation details
public string NormalizeName(string name)
{
string result = (name ?? "").Trim();
if (result.Length > 50)
return result.Substring(0, 50);
return result;
}
}
public class UserController
{
public void RenameUser(int userId, string newName)
{
User user = GetUserFromDatabase(userId);
string normalizedName = user.NormalizeName(newName);
user.Name = normalizedName;
SaveUserToDatabase(user);
}
}
UserController is client code. It uses the User class in its RenameUser method. The
goal of this method, as you have probably guessed, is to change a user’s name.
 So, why isn’t User’s API well-designed? Look at its members once again: the Name
property and the NormalizeName method. Both of them are public. Therefore, in
order for the class’s API to be well-designed, these members should be part of the
observable behavior. This, in turn, requires them to do one of the following two things
(which I’m repeating here for convenience):
Expose an operation that helps the client achieve one of its goals.
Expose a state that helps the client achieve one of its goals.
Only the Name property meets this requirement. It exposes a setter, which is an opera-
tion that allows UserController to achieve its goal of changing a user’s name. The
NormalizeName method is also an operation, but it doesn’t have an immediate con-
nection to the client’s goal. The only reason UserController calls this method is to
satisfy the invariant of User. NormalizeName is therefore an implementation detail that
leaks to the class’s public API (figure 5.6).
 To fix the situation and make the class’s API well-designed, User needs to hide
NormalizeName() and call it internally as part of the property’s setter without relying
on the client code to do so. Listing 5.6 shows this approach.
 
 


---
**Page 102**

102
CHAPTER 5
Mocks and test fragility
 
public class User
{
private string _name;
public string Name
{
get => _name;
set => _name = NormalizeName(value);
}
private string NormalizeName(string name)
{
string result = (name ?? "").Trim();
if (result.Length > 50)
return result.Substring(0, 50);
return result;
}
}
public class UserController
{
public void RenameUser(int userId, string newName)
{
User user = GetUserFromDatabase(userId);
user.Name = newName;
SaveUserToDatabase(user);
}
}
User’s API in listing 5.6 is well-designed: only the observable behavior (the Name prop-
erty) is made public, while the implementation details (the NormalizeName method)
are hidden behind the private API (figure 5.7).
 
Listing 5.6
A version of User with a well-designed API
Observable behavior
Public API
Normalize
name
Name
Leaking implementation detail
Figure 5.6
The API of User is not well-
designed: it exposes the NormalizeName 
method, which is not part of the observable 
behavior.


---
**Page 103**

103
Observable behavior vs. implementation details
NOTE
Strictly speaking, Name’s getter should also be made private, because
it’s not used by UserController. In reality, though, you almost always want to
read back changes you make. Therefore, in a real project, there will certainly be
another use case that requires seeing users’ current names via Name’s getter.
There’s a good rule of thumb that can help you determine whether a class leaks its
implementation details. If the number of operations the client has to invoke on the
class to achieve a single goal is greater than one, then that class is likely leaking imple-
mentation details. Ideally, any individual goal should be achieved with a single operation. In
listing 5.5, for example, UserController has to use two operations from User:
string normalizedName = user.NormalizeName(newName);
user.Name = normalizedName;
After the refactoring, the number of operations has been reduced to one:
user.Name = newName;
In my experience, this rule of thumb holds true for the vast majority of cases where
business logic is involved. There could very well be exceptions, though. Still, be sure
to examine each situation where your code violates this rule for a potential leak of
implementation details. 
5.2.3
Well-designed API and encapsulation
Maintaining a well-designed API relates to the notion of encapsulation. As you might
recall from chapter 3, encapsulation is the act of protecting your code against inconsis-
tencies, also known as invariant violations. An invariant is a condition that should be
held true at all times. The User class from the previous example had one such invari-
ant: no user could have a name that exceeded 50 characters.
 Exposing implementation details goes hand in hand with invariant violations—the
former often leads to the latter. Not only did the original version of User leak its
implementation details, but it also didn’t maintain proper encapsulation. It allowed
the client to bypass the invariant and assign a new name to a user without normalizing
that name first.
Observable behavior
Public API
Normalize
name
Name
Private API
Implementation detail
Figure 5.7
User with a well-designed API. 
Only the observable behavior is public; the 
implementation details are now private.


