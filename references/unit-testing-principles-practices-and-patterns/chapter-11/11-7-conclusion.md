# 11.7 Conclusion (pp.273-273)

---
**Page 273**

273
Summary
inquiry.Approve(_dateTimeServer.Now);      
SaveInquiry(inquiry);
}
}
Of these two options, prefer injecting the time as a value rather than as a service. It’s
easier to work with plain values in production code, and it’s also easier to stub those
values in tests.
 Most likely, you won’t be able to always inject the time as a plain value, because
dependency injection frameworks don’t play well with value objects. A good compro-
mise is to inject the time as a service at the start of a business operation and then
pass it as a value in the remainder of that operation. You can see this approach in
listing 11.17: the controller accepts DateTimeServer (the service) but then passes a
DateTime value to the Inquiry domain class. 
11.7
Conclusion
In this chapter, we looked at some of the most prominent real-world unit testing use
cases and analyzed them using the four attributes of a good test. I understand that it
may be overwhelming to start applying all the ideas and guidelines from this book at
once. Also, your situation might not be as clear-cut. I publish reviews of other people’s
code and answer questions (related to unit testing and code design in general) on my
blog at https://enterprisecraftsmanship.com. You can also submit your own question
at https://enterprisecraftsmanship.com/about. You might also be interested in taking
my online course, where I show how to build an application from the ground up,
applying all the principles described in this book in practice, at https://unittesting-
course.com.
 You can always catch me on twitter at @vkhorikov, or contact me directly through
https://enterprisecraftsmanship.com/about. I look forward to hearing from you!
Summary
Exposing private methods to enable unit testing leads to coupling tests to
implementation and, ultimately, damaging the tests’ resistance to refactoring.
Instead of testing private methods directly, test them indirectly as part of the
overarching observable behavior.
If the private method is too complex to be tested as part of the public API that
uses it, that’s an indication of a missing abstraction. Extract this abstraction into
a separate class instead of making the private method public.
In rare cases, private methods do belong to the class’s observable behavior.
Such methods usually implement a non-public contract between the class and
an ORM or a factory.
Don’t expose state that you would otherwise keep private for the sole purpose
of unit testing. Your tests should interact with the system under test exactly the
same way as the production code; they shouldn’t have any special privileges.
Injects time as 
a plain value


