# 6.3.1 What is functional programming? (pp.128-132)

---
**Page 128**

128
CHAPTER 6
Styles of unit testing
State-based and communication-based tests are worse on both metrics. These are
more likely to couple to a leaking implementation detail, and they also incur higher
maintenance costs due to being larger in size.
 Always prefer output-based testing over everything else. Unfortunately, it’s easier
said than done. This style of unit testing is only applicable to code that is written in a
functional way, which is rarely the case for most object-oriented programming lan-
guages. Still, there are techniques you can use to transition more of your tests toward
the output-based style.
 The rest of this chapter shows how to transition from state-based and collaboration-
based testing to output-based testing. The transition requires you to make your code
more purely functional, which, in turn, enables the use of output-based tests instead
of state- or communication-based ones. 
6.3
Understanding functional architecture
Some groundwork is needed before I can show how to make the transition. In this sec-
tion, you’ll see what functional programming and functional architecture are and
how the latter relates to the hexagonal architecture. Section 6.4 illustrates the transi-
tion using an example.
 Note that this isn’t a deep dive into the topic of functional programming, but
rather an explanation of the basic principles behind it. These basic principles should
be enough to understand the connection between functional programming and out-
put-based testing. For a deeper look at functional programming, see Scott Wlaschin’s
website and books at https://fsharpforfunandprofit.com/books.
6.3.1
What is functional programming?
As I mentioned in section 6.1.1, the output-based unit testing style is also known as
functional. That’s because it requires the underlying production code to be written in
a purely functional way, using functional programming. So, what is functional pro-
gramming?
 Functional programming is programming with mathematical functions. A mathemati-
cal function (also known as pure function) is a function (or method) that doesn’t have
any hidden inputs or outputs. All inputs and outputs of a mathematical function must
be explicitly expressed in its method signature, which consists of the method’s name,
arguments, and return type. A mathematical function produces the same output for a
given input regardless of how many times it is called.
Table 6.1
The three styles of unit testing: The comparisons
Output-based
State-based
Communication-based
Due diligence to maintain 
resistance to refactoring
Low
Medium
Medium
Maintainability costs
Low
Medium
High


---
**Page 129**

129
Understanding functional architecture
 Let’s take the CalculateDiscount() method from listing 6.1 as an example (I’m
copying it here for convenience):
public decimal CalculateDiscount(Product[] products)
{
decimal discount = products.Length * 0.01m;
return Math.Min(discount, 0.2m);
}
This method has one input (a Product array) and one output (the decimal dis-
count), both of which are explicitly expressed in the method’s signature. There are
no hidden inputs or outputs. This makes CalculateDiscount() a mathematical func-
tion (figure 6.5).
Methods with no hidden inputs and outputs are called mathematical functions
because such methods adhere to the definition of a function in mathematics.
DEFINITION
In mathematics, a function is a relationship between two sets that
for each element in the first set, finds exactly one element in the second set.
Figure 6.6 shows how for each input number x, function f(x) = x + 1 finds a corre-
sponding number y. Figure 6.7 displays the CalculateDiscount() method using the
same notation as in figure 6.6.
public         CalculateDiscount
decimal
(Product[] products)
Method signature
Output
Name
Input
Figure 6.5
CalculateDiscount() has one input (a Product array) and 
one output (the decimal discount). Both the input and the output are explicitly 
expressed in the method’s signature, which makes CalculateDiscount() 
a mathematical function.
Y
1
2
3
4
2
3
4
5
f(x) = x + 1
X
Figure 6.6
A typical example of a function in 
mathematics is f(x) = x + 1. For each input 
number x in set X, the function finds a 
corresponding number y in set Y.


---
**Page 130**

130
CHAPTER 6
Styles of unit testing
Explicit inputs and outputs make mathematical functions extremely testable because
the resulting tests are short, simple, and easy to understand and maintain. Mathe-
matical functions are the only type of methods where you can apply output-based
testing, which has the best maintainability and the lowest chance of producing a
false positive.
 On the other hand, hidden inputs and outputs make the code less testable (and
less readable, too). Types of such hidden inputs and outputs include the following:
Side effects—A side effect is an output that isn’t expressed in the method signature
and, therefore, is hidden. An operation creates a side effect when it mutates the
state of a class instance, updates a file on the disk, and so on.
Exceptions—When a method throws an exception, it creates a path in the pro-
gram flow that bypasses the contract established by the method’s signature. The
thrown exception can be caught anywhere in the call stack, thus introducing an
additional output that the method signature doesn’t convey.
A reference to an internal or external state—For example, a method can get the cur-
rent date and time using a static property such as DateTime.Now. It can query
data from the database, or it can refer to a private mutable field. These are all
inputs to the execution flow that aren’t present in the method signature and,
therefore, are hidden.
A good rule of thumb when determining whether a method is a mathematical func-
tion is to see if you can replace a call to that method with its return value without
changing the program’s behavior. The ability to replace a method call with the
corresponding value is known as referential transparency. Look at the following method,
for example:
Arrays of products
Product(“Soap”)
Product(“Hand wash”)
Product(“Shampoo”)
Product(“Soap”)
Product(“Sea salt”)
Discounts
0.02
0.01
CalculateDiscount()
Figure 6.7
The CalculateDiscount() method represented using the same 
notation as the function f(x) = x + 1. For each input array of products, the 
method finds a corresponding discount as an output.


---
**Page 131**

131
Understanding functional architecture
public int Increment(int x)
{
return x + 1;
}
This method is a mathematical function. These two statements are equivalent to
each other:
int y = Increment(4);
int y = 5;
On the other hand, the following method is not a mathematical function. You can’t
replace it with the return value because that return value doesn’t represent all of the
method’s outputs. In this example, the hidden output is the change to field x (a side
effect):
int x = 0;
public int Increment()
{
x++;
return x;
}
Side effects are the most prevalent type of hidden outputs. The following listing shows
an AddComment method that looks like a mathematical function on the surface but
actually isn’t one. Figure 6.8 shows the method graphically.
public Comment AddComment(string text)
{
var comment = new Comment(text);
_comments.Add(comment);
   
return comment;
}
Listing 6.7
Modification of an internal state
Side effect 
Text
Comment
Side effect
Method
signature
Hidden
part
f
Figure 6.8
Method AddComment (shown as f) 
has a text input and a Comment output, which 
are both expressed in the method signature. The 
side effect is an additional hidden output.


---
**Page 132**

132
CHAPTER 6
Styles of unit testing
6.3.2
What is functional architecture?
You can’t create an application that doesn’t incur any side effects whatsoever, of
course. Such an application would be impractical. After all, side effects are what you
create all applications for: updating the user’s information, adding a new order line to
the shopping cart, and so on.
 The goal of functional programming is not to eliminate side effects altogether but
rather to introduce a separation between code that handles business logic and code
that incurs side effects. These two responsibilities are complex enough on their own;
mixing them together multiplies the complexity and hinders code maintainability in
the long run. This is where functional architecture comes into play. It separates busi-
ness logic from side effects by pushing those side effects to the edges of a business operation.
DEFINITION
Functional architecture maximizes the amount of code written in a
purely functional (immutable) way, while minimizing code that deals with
side effects. Immutable means unchangeable: once an object is created, its
state can’t be modified. This is in contrast to a mutable object (changeable
object), which can be modified after it is created.
The separation between business logic and side effects is done by segregating two
types of code:
Code that makes a decision—This code doesn’t require side effects and thus can
be written using mathematical functions.
Code that acts upon that decision—This code converts all the decisions made by
the mathematical functions into visible bits, such as changes in the database or
messages sent to a bus.
The code that makes decisions is often referred to as a functional core (also known as an
immutable core). The code that acts upon those decisions is a mutable shell (figure 6.9).
Input
Decisions
Functional core
Mutable shell
Figure 6.9
In functional architecture, 
the functional core is implemented using 
mathematical functions and makes all 
decisions in the application. The mutable 
shell provides the functional core with 
input data and interprets its decisions by 
applying side effects to out-of-process 
dependencies such as a database.


