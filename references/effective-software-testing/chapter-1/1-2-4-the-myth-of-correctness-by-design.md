# 1.2.4 The myth of “correctness by design” (pp.15-15)

---
**Page 15**

15
Effective software testing for developers
1.2.4
The myth of “correctness by design”
Now that you have a clearer picture of what I mean by effective and systematic soft-
ware testing, let me debunk a myth. There is a perception among software developers
that if you design code in a simple way, it will not have bugs, as if the secret of bug-free
code is simplicity.
 Empirical research in software engineering has repeatedly shown that simple,
non-smelly code is less prone to defects than complex code (see, for example, the
2006 paper by Shatnawi and Li). However, simplicity is far from enough. It is naive
to believe that testing can be fully replaced by simplicity. The same is true for
“correctness by design”: designing your code well does not mean you avoid all pos-
sible bugs.
1.2.5
The cost of testing
You may be thinking that forcing developers to apply rigorous testing may be too
costly. Figure 1.4 shows the many techniques developers have to apply if they follow
the flow I am proposing. It is true: testing software properly is more work than not
doing so. Let me convince you why it is worth it:
The cost of bugs that happen in production often outweighs the cost of preven-
tion (as shown by Boehm and Papaccio, 1988). Think of a popular web shop
and how much it would cost the shop if the payment application goes down for
30 minutes due to a bug that could have been easily prevented via testing.
Teams that produce many bugs tend to waste time in an eternal loop where
developers write bugs, customers (or dedicated QAs) find the bugs, developers
fix the bugs, customers find a different set of bugs, and so on.
Practice is key. Once developers are used to engineering test cases, they can do
it much faster. 
1.2.6
The meaning of effective and systematic
I have been using two words to describe how I expect a developer to test: effectively and
systematically. Being effective means we focus on writing the right tests. Software testing
is all about trade-offs. Testers want to maximize the number of bugs they find while
minimizing the effort required to find the bugs. How do we achieve this? By knowing
what to test.
 All the techniques I present in this book have a clear beginning (what to test) and
a clear end (when to stop). Of course, I do not mean your systems will be bug-free if you
follow these techniques. As a community, we still do not know how to build bug-free
systems. But I can confidently say that the number of bugs will be reduced, hopefully
to tolerable levels.
 Being systematic means that for a given piece of code, any developer should come
up with the same test suite. Testing often happens in an ad hoc manner. Developers
engineer the test cases that come to mind. It is common to see two developers devel-


