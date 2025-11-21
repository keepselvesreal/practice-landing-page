# 10.5.1 Should you test reads? (pp.252-253)

---
**Page 252**

252
CHAPTER 10
Testing the database
x => x.UserTypeHasChanged(
user.UserId, UserType.Employee, UserType.Customer),
Times.Once);
}
}
Is the increased number of database transactions a problem? And, if so, what can
you do about it? The additional database contexts are a problem to some degree
because they make the test slower, but there’s not much that can be done about it.
It’s another example of a trade-off between different aspects of a valuable test: this
time between fast feedback and maintainability. It’s worth it to make that trade-off
and exchange performance for maintainability in this particular case. The perfor-
mance degradation shouldn’t be that significant, especially when the database is
located on the developer’s machine. At the same time, the gains in maintainability
are quite substantial. 
10.5
Common database testing questions
In this last section of the chapter, I’d like to answer common questions related to
database testing, as well as briefly reiterate some important points made in chapters 8
and 9.
10.5.1 Should you test reads?
Throughout the last several chapters, we’ve worked with a sample scenario of chang-
ing a user email. This scenario is an example of a write operation (an operation that
leaves a side effect in the database and other out-of-process dependencies). Most
applications contain both write and read operations. An example of a read operation
would be returning the user information to the external client. Should you test both
writes and reads?
 It’s crucial to thoroughly test writes, because the stakes are high. Mistakes in write
operations often lead to data corruption, which can affect not only your database but
also external applications. Tests that cover writes are highly valuable due to the protec-
tion they provide against such mistakes.
 This is not the case for reads: a bug in a read operation usually doesn’t have conse-
quences that are as detrimental. Therefore, the threshold for testing reads should be
higher than that for writes. Test only the most complex or important read operations;
disregard the rest.
 Note that there’s also no need for a domain model in reads. One of the main goals
of domain modeling is encapsulation. And, as you might remember from chapters 5
and 6, encapsulation is about preserving data consistency in light of any changes. The
lack of data changes makes encapsulation of reads pointless. In fact, you don’t need a
fully fledged ORM such as NHibernate or Entity Framework in reads, either. You are
better off using plain SQL, which is superior to an ORM performance-wise, thanks to
bypassing unnecessary layers of abstraction (figure 10.7).


---
**Page 253**

253
Common database testing questions
Because there are hardly any abstraction layers in reads (the domain model is one
such layer), unit tests aren’t of any use there. If you decide to test your reads, do so
using integration tests on a real database. 
10.5.2 Should you test repositories?
Repositories provide a useful abstraction on top of the database. Here’s a usage exam-
ple from our sample CRM project:
User user = _userRepository.GetUserById(userId);
_userRepository.SaveUser(user);
Should you test repositories independently of other integration tests? It might seem
beneficial to test how repositories map domain objects to the database. After all,
there’s significant room for a mistake in this functionality. Still, such tests are a net loss
to your test suite due to high maintenance costs and inferior protection against
regressions. Let’s discuss these two drawbacks in more detail.
HIGH MAINTENANCE COSTS
Repositories fall into the controllers quadrant on the types-of-code diagram from
chapter 7 (figure 10.8). They exhibit little complexity and communicate with an out-
of-process dependency: the database. The presence of that out-of-process dependency
is what inflates the tests’ maintenance costs.
 When it comes to maintenance costs, testing repositories carries the same burden
as regular integration tests. But does such testing provide an equal amount of benefits
in return? Unfortunately, it doesn’t.
Writes
Database
Client
Reads
Application
. . . not here
Domain model goes here . . .
Figure 10.7
There’s no need for a domain model in reads. And because the cost of a 
mistake in reads is lower than it is in writes, there’s also not as much need for integration 
testing.


