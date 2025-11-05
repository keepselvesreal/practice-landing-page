# 13.2 Exploring a Simple Example with ChatGPT (pp.246-247)

---
**Page 246**

help your LLM do a better job with that challenge in this chapter. But left to
its own devices, an LLM is increasingly likely to break existing functionality
as it adds new increments.
Do not trust any AI-generated code to be correct.
I’ve been pleasantly surprised, though: more often than not, the code LLMs
(including ChatGPT, Meta.ai, and Claude) have produced for me has been
correct. But I’ve also seen them generate enough wrong code to know that I
could never fully depend on it.
From these limitations arises a critical need: if you’re going to use AI tools to
generate code, you’ll need to create and run tests.
Fortunately, you’ve read the rest of this book (right?) and know how to do
just that. Even better, AI will speed you up by coding the tests.
Give the benefit of the doubt to your pair programmer—whether artificial or
human—but assume that you can both make mistakes. доверяй, но проверяй.
(“Trust, but verify.”)
Note: as I write this, you can also use tools like GitHub Copilot, JetBrains AI
Assistant, and Duet to help you develop. These tools sit atop one or more
LLMs and provide what can best be described as AI-assisted code completion.
I highly recommend incorporating them into your regular code development
process. In this chapter, however, you’ll focus on using a test-driven process
for generating code at the class level—with the intent of maximizing the
amount of (verified) code that AI can generate for you.
Exploring a Simple Example with ChatGPT
Interaction with an LLM via prompting is a conversation. That conversation
may play out very differently the next time I have it. As a result, it’s probably
best if this chapter reads as a story about my personal interaction with
ChatGPT on a small example. Accordingly, unlike the rest of the book, this
chapter is written in first-person past tense.
I held my conversation with OpenAI’s chatbot, ChatGPT, which at the time
was based on the GPT-4 LLM. My subsequent mentions of ChatGPT refer to
this configuration. While other models may exist that have been trained to be
optimized for programming tasks (Code Llama for example), the experience I
Chapter 13. Keeping AI Honest with Unit Tests • 246
report erratum  •  discuss


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


