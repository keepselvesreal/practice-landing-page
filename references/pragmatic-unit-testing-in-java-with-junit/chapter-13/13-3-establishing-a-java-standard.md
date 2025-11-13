# 13.3 Establishing a Java Standard (pp.247-248)

---
**Page 247**

relay in this chapter demonstrates an approach that will work—and will only
get better with time—with virtually any current LLM.
I was responsible for producing an event check-in list. Given a list of attendees, I
needed to write code that sorted them. Attendee names started with a first
name, followed by zero or more “middle” names, followed by the surname or
last name. Some examples:
Jeffrey John Langr
John Jacob Jingleheimer-Schmidt
John Yossarian
Arthur Ignatius Conan Doyle
The check-in list needed to show names in alphabetical order based on the last
name, not the first name. I had to “normalize” each name, then, into the form
“Last, First M. I.”:
Langr, Jeffrey J.
Jingleheimer-Schmidt, John J.
Yossarian, John
Doyle, Arthur I. C.
Oh I. C. indeed: the middle names are transformed into initials. Other rules
implicit in these examples include the obvious fact that names are separated
by spaces and that a comma should appear after each last name.
I focused on the task of normalizing a single name, deferring the trivial task
of sorting a list of names. First, however, I wanted to teach my LLM how to
write code to help me and ChatGPT work better together.
Establishing a Java Standard
By default, ChatGPT generates stepwise code that requires too much time to
fully comprehend. I wanted it to do better, so I supplied a prompt describing
the kind of code I wanted:
YOU:
I will be asking you to write Java code. Write all code as Jeff Langr. Jeff
Langr (Jeff) has a specific coding standard. Here are the rules for your standard
for Java language programming, which I will refer to as Jeff-Java when appropriate.
1. Use ‘var‘ when declaring local variables and the compiler allows it.
2. Where possible, prefer use of the streams functionality and implement iterative
operations using stream functions, such as ‘map‘ and ‘filter‘.
3. For any and all complex expressions—mathematics, complex conditionals, pred-
icates, and so on—extract the code to a separate function. This should also hold
true for lambdas within a chained stream expression.
report erratum  •  discuss
Establishing a Java Standard • 247


---
**Page 248**

4. In general, create very short, intention-revealing functions for any complexity.
5. Avoid the use of temporaries in most cases unless there is a strong reason to use
them (for example, to use them more than once within a single expression). Instead,
extract the temporary’s initialization to a separate function with the same name as
the temporary, then inline the temporary to remove it.
ChatGPT affirmed my request:
CHAT-GPT:
Understood! Blah blah blah...
You might wonder why I even bothered telling my LLM to improve the code.
If an LLM can generate the code I need, I shouldn’t have to read it.
However, hearken back to the earlier mentioned limitations of LLMs like
ChatGPT. They’re gonna be wrong at times…just like you and me. You’ll have
to read and manually update some amount of code. Even as that need likely
diminishes over time, keeping your code organized (by predominantly creating
small classes and methods) appears to increase the odds that the LLM-
generated code is correct.
Providing Examples to ChatGPT
Incrementally test driving small, unit behaviors into a system remains the
best choice for humans. For an LLM, maybe not.
I first tried getting ChatGPT to consume all my requirements for the name
normalizer at once. The code was a mess, and it didn’t work. I took the next-
smaller step, which was to first give it a subset containing the four core cases
it needed to cover. I helped ChatGPT focus on what I believe to be a proper
design—one that, in general, is based on small classes and small methods.
With such an improved design, I believe ChatGPT had a much better chance
to correctly generate new increments.
One of the best ways to get good results from an LLM is to provide examples
in your prompts. I followed that advice for the name normalizer after first
describing in English what I wanted. My prompt provided five examples for
four core cases:
YOU:
Write Java code for a feature known as the name normalizer. Given a per-
son’s name, the name normalizer should return the last name first, followed by a
comma, then the first name.
If there is one or more middle names, return the initial of each. The initial is the first
letter followed by a period.
Assume that the name provided to the method is never empty or null.
Chapter 13. Keeping AI Honest with Unit Tests • 248
report erratum  •  discuss


