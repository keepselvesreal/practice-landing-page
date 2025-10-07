Line 1: 
Line 2: --- 페이지 40 ---
Line 3: 2
Line 4: Using TDD to Create Good Code
Line 5: We’ve seen that bad code is bad news: bad for business, bad for users, and bad for developers. Test-
Line 6: driven development (TDD) is a core software engineering practice that helps us keep bad code out 
Line 7: of our systems.
Line 8: The goal of this chapter is to learn the specifics of how TDD helps us to create well-engineered, correct 
Line 9: code, and how it helps us to keep it that way. By the end, we will understand the basic principles behind 
Line 10: good code and how TDD helps us create it. It is important for us to understand why TDD works in 
Line 11: order to motivate us and so that we have a response to give to colleagues about why we recommend 
Line 12: that they use it as well.
Line 13: In this chapter, we’re going to cover the following main topics:
Line 14: •	 Designing good quality code
Line 15: •	 Revealing design flaws
Line 16: •	 Preventing logic flaws
Line 17: •	 Protecting against future defects
Line 18: •	 Documenting our code
Line 19: Designing good quality code
Line 20: Good quality code doesn’t happen by accident. It is intentional. It is the result of thousands of small 
Line 21: decisions, each one shaping how easy our code is to read, test, compose, and change. We must choose 
Line 22: between quick-and-dirty hacks, where we have no idea what edge cases are covered, and more robust 
Line 23: approaches, where we are confident that no matter how the user misuses our code, it will work 
Line 24: as expected.
Line 25: Every line of source code involves at least one of these decisions. That’s an awful lot of deciding that 
Line 26: we have to do.
Line 27: 
Line 28: --- 페이지 41 ---
Line 29: Using TDD to Create Good Code
Line 30: 18
Line 31: You’ll notice that we haven’t mentioned TDD so far. As we will see, TDD does not design your code 
Line 32: for you. It doesn’t remove that essential engineering sensibility and creative input that is needed to 
Line 33: turn requirements into code. To be honest, I’m grateful for that – it’s the part that I enjoy.
Line 34: However, that does cause a lot of early failure with TDD, which is worth noting. Expecting to implement 
Line 35: the TDD process and get good quality code out without your own design input will simply not work. 
Line 36: TDD, as we will see, is a tool that allows you to get rapid feedback on these design decisions. You can 
Line 37: change your mind and adapt while the code is still cheap and quick to change but they are still your 
Line 38: design decisions that are playing out.
Line 39: So, what is good code? What are we aiming for?
Line 40: Good code, for me, is all about readability. I optimize for clarity. I want to be kind to my future self 
Line 41: and my long-suffering colleagues by engineering code that is clear and safe to work with. I want to 
Line 42: create clear and simple code that is free of hidden traps.
Line 43: While there is a huge range of advice on what makes good code, the basics are straightforward:
Line 44: •	 Say what you mean, mean what you say
Line 45: •	 Take care of the details in private
Line 46: •	 Avoid accidental complexity
Line 47: It’s worth a quick review of what I mean by those things.
Line 48: Say what you mean, mean what you say
Line 49: Here’s an interesting experiment. Take a piece of source code (in any language) and strip out everything 
Line 50: that is not part of the language specification, then see if you can figure out what it does. To make 
Line 51: things really stand out, we will replace all method names and variable identifiers with the symbol ???.
Line 52: Here’s a quick example:
Line 53: public boolean ??? (int ???) {
Line 54:     if ( ??? > ??? ) {
Line 55:         return ???;
Line 56:     }
Line 57:     return ???;
Line 58: }
Line 59: Any ideas what this code does? No, me neither. I haven’t a clue.
Line 60: 
Line 61: --- 페이지 42 ---
Line 62: Designing good quality code
Line 63: 19
Line 64: I can tell by its shape that it is some kind of assessment method that passes something in and returns 
Line 65: true/false. Maybe it implements a threshold or limit. It uses a multipath return structure, where 
Line 66: we check something, then return an answer as soon as we know what that answer is.
Line 67: While the shape of the code and the syntax tell us something, it’s not telling us much. It is definitely 
Line 68: not enough. Nearly all the information we share about what our code does is a result of the natural 
Line 69: language identifiers we choose. Names are absolutely vital to good code. They are beyond important. 
Line 70: They are everything. They can reveal intent, explain outcomes, and describe why a piece of data is 
Line 71: important to us, but they can’t do any of this if we do a bad job choosing our names.
Line 72: I use two guidelines for names, one for naming active code – methods and functions – and one 
Line 73: for variables:
Line 74: •	 Method – Say what it does. What is the outcome? Why would I call this?
Line 75: •	 Variable – Say what it contains. Why would I access this?
Line 76: A common mistake with method naming is to describe how it works internally, instead of describing 
Line 77: what the outcome is. A method called addTodoItemToItemQueue is committing us to one specific 
Line 78: implementation of a method that we don’t really care about. Either that or it is misinformation. We 
Line 79: can improve the name by calling it add(Todo item). This name tells us why exactly we should 
Line 80: call this method. It leaves us free to revise how it is coded later.
Line 81: The classic mistake with variable names is to say what they are made of. For example, the variable 
Line 82: name String string helps nobody, whereas String firstName tells me clearly that this 
Line 83: variable is somebody’s first name. It tells me why I would want to read or write that variable.
Line 84: Perhaps more importantly, it tells us what not to write in that variable. Having one variable serve 
Line 85: multiple purposes in the same scope is a real headache. Been there, done that, never going back.
Line 86: It turns out that code is storytelling, pure and simple. We tell the story of what problem we are solving 
Line 87: and how we have decided to solve it to human programmers. We can throw any old code into a 
Line 88: compiler and the computer will make it work but we must take more care if we want humans to 
Line 89: understand our work.
Line 90: Take care of the details in private
Line 91: Taking care of the details in private is a simple way to describe the computer science concepts of 
Line 92: abstraction and information hiding. These are fundamental ideas that allow us to break complex 
Line 93: systems into smaller, simpler parts.
Line 94: The way I think about abstraction is the same way I think about hiring an electrician for my house.
Line 95: I know that my electric water heater needs to be fixed but I don’t want to know how. I don’t want to 
Line 96: learn how to do it. I don’t want to have to figure out what tools are needed and buy them. I want to 
Line 97: have nothing whatsoever to do with it, beyond asking that it gets done when I need it done. So, I’ll 
Line 98: 
Line 99: --- 페이지 43 ---
Line 100: Using TDD to Create Good Code
Line 101: 20
Line 102: call the electrician and ask them to do it. I’m more than happy to pay for a good job, as long as I don’t 
Line 103: have to do it myself.
Line 104: This is what abstraction means. The electrician abstracts the job of fixing my water heater. Complex 
Line 105: stuff gets done in response to my simple requests.
Line 106: Abstraction happens everywhere in good software.
Line 107: Every time you make some kind of detail less important, you have abstracted it. A method has a simple 
Line 108: signature but the code inside it may be complex. This is an abstraction of an algorithm. A local variable 
Line 109: might be declared as type String. This is an abstraction of the memory management of each text 
Line 110: character and the character encoding. A microservice that will send discount vouchers to our top 
Line 111: customers who haven’t visited the site in a while is an abstraction of a business process. Abstraction 
Line 112: is everywhere in programming, across all major paradigms – object-oriented programming (OOP), 
Line 113: procedural, and functional.
Line 114: The idea of splitting software into components, each of which takes care of something for us, is a 
Line 115: massive quality driver. We centralize decisions, meaning that we don’t make mistakes in duplicated 
Line 116: code. We can test a component thoroughly in isolation. We design out problems caused by hard-to-
Line 117: write code just by writing it once and having an easy-to-use interface.
Line 118: Avoid accidental complexity
Line 119: This is my personal favorite destroyer of good code – complex code that simply never needed to exist.
Line 120: There are always many ways of writing a piece of code. Some of them use complicated features or go 
Line 121: all around the houses; they use convoluted chains of actions to do a simple thing. All versions of the 
Line 122: code get the same result but some just do it in a more complicated way by accident.
Line 123: My goal for code is to tell at first sight the story of what problem I am solving, leaving the details 
Line 124: about how I am solving it for closer analysis. This is quite different from how I learned how to code 
Line 125: originally. I choose to emphasize domain over mechanism. The domain here means using the same 
Line 126: language as the user, for example, expressing the problem in business terms, not just raw computer 
Line 127: code syntax. If I am writing a banking system, I want to see money, ledgers, and transactions coming 
Line 128: to the forefront. The story the code is telling has to be that of banking.
Line 129: Implementation details such as message queues and databases are important but only as far as they 
Line 130: describe how we are solving the problem today. They may need to change later. Whether they change 
Line 131: or not, we still want the primary story to be about transactions going into an account and not message 
Line 132: queues talking to REST services.
Line 133: As our code gets better at telling the story of the problem we are solving, we make it easier to write 
Line 134: replacement components. Swapping out a database for another vendor’s product is simplified because 
Line 135: we know exactly what purpose it is serving in our system.
Line 136: 
Line 137: --- 페이지 44 ---
Line 138: Designing good quality code
Line 139: 21
Line 140: This is what we mean by hiding details. At some level, it is important to see how we wired up the 
Line 141: database, but only after we have seen why we even needed one in the first place.
Line 142: To give you a concrete example, here is a piece of code similar to some code that I found in a 
Line 143: production system:
Line 144: public boolean isTrue (Boolean b) {
Line 145:     boolean result = false;
Line 146:     if ( b == null ) {
Line 147:         result = false;
Line 148:     }
Line 149:     else if ( b.equals(Boolean.TRUE)) {
Line 150:         result = true;
Line 151:     }
Line 152:     else if ( b.equals(Boolean.FALSE)) {
Line 153:         result = false;
Line 154:     }
Line 155:     else {
Line 156:         result = false;
Line 157:     }
Line 158:     return result;
Line 159: }
Line 160: You can see the problem here. Yes, there is a need for a method like this. It is a low-level mechanism 
Line 161: that converts a Java true/false object into its equivalent primitive type and does it safely. It covers 
Line 162: all edge cases relating to a null value input, as well as valid true/false values.
Line 163: However, it has problems. This code is cluttered. It is unnecessarily hard to read and test. It has high 
Line 164: cyclomatic complexity (CYC). CYC is an objective measure of how complex a piece of code is, based 
Line 165: on the number of independent execution paths possible in a section of code.
Line 166: The previous code is unnecessarily verbose and over-complicated. I’m pretty sure it has a dead-code 
Line 167: path – meaning a path containing unreachable code – on that final else, as well.
Line 168: Looking at the logic needed, there are only three interesting input conditions: null, true, and 
Line 169: false. It certainly does not need all those else/if chains to decode that. Once you’ve got that 
Line 170: null-to-false conversion out of the way, you really only need to inspect one value before you can fully 
Line 171: decide what to return.
Line 172: 
Line 173: --- 페이지 45 ---
Line 174: Using TDD to Create Good Code
Line 175: 22
Line 176: A better equivalent would be the following:
Line 177:     public boolean isTrue (Boolean b) {
Line 178:         return Boolean.TRUE.equals(b);
Line 179:     }
Line 180: This code does the same thing with a lot less fuss. It does not have the same level of accidental complexity 
Line 181: as the previous code. It reads better. It is easier to test with fewer paths needing testing. It has a better 
Line 182: cyclomatic complexity figure, which means fewer places for bugs to hide. It tells a better story about 
Line 183: why the method exists. To be perfectly honest, I might even refactor this method by inlining it. I’m 
Line 184: not sure the method adds any worthwhile extra explanation to the implementation.
Line 185: This method was a simple example. Just imagine seeing this scaled up to thousands of lines of copy-
Line 186: pasted, slightly-changed code. You can see why accidental complexity is a killer. This cruft builds up 
Line 187: over time and grows exponentially. Everything becomes harder to read and harder to safely change.
Line 188: Yes, I have seen that. I will never stop being sad about it when I do. We can do better than this. As 
Line 189: professional software engineers, we really should.
Line 190: This section has been a lightning tour of good design fundamentals. They apply across all styles of 
Line 191: programming. However, if we can do things right, we can also do things wrong. In the next section, 
Line 192: we’ll take a look at how TDD tests can help us prevent bad designs.
Line 193: Revealing design flaws
Line 194: Bad design is truly bad. It is the root cause of software being hard to change and hard to work with. You 
Line 195: can never quite be sure whether your changes are going to work because you can never quite be sure 
Line 196: what a bad design is really doing. Changing that kind of code is scary and often gets put off. Whole 
Line 197: sections of code can be left to rot with only a /* Here be dragons! */ comment to show for it.
Line 198: The first major benefit of TDD is that it forces us to think about the design of a component. We do 
Line 199: that before we think about how we implement it. By doing things in this order, we are far less likely 
Line 200: to drift into a bad design by mistake.
Line 201: The way we consider the design first is to think about the public interfaces of a component. We think 
Line 202: about how that component will be used and how it will be called. We don’t yet consider how we will 
Line 203: make any implementations actually work. This is outside-in thinking. We consider the usage of the 
Line 204: code from outside callers before we consider any inside implementation.
Line 205: This is quite a different approach to take for many of us. Typically, when we need code to do something, 
Line 206: we start by writing the implementation. After that, we will ripple out whatever is needed in method 
Line 207: signatures, without a thought about the call site. This is inside-out thinking. It works, of course, but it 
Line 208: often leads to complex calling code. It locks us into implementation details that just aren’t important.
Line 209: 
Line 210: --- 페이지 46 ---
Line 211: Revealing design flaws
Line 212: 23
Line 213: Outside-in thinking means we get to dream up the perfect component for its users. Then, we will 
Line 214: bend the implementation to work with our desired code at the call site. Ultimately, this is far more 
Line 215: important than the implementation. This is, of course, abstraction being used in practice.
Line 216: We can ask questions like the following:
Line 217: •	 Is it easy to set up?
Line 218: •	 Is it easy to ask it to do something?
Line 219: •	 Is the outcome easy to work with?
Line 220: •	 Is it difficult to use it the wrong way?
Line 221: •	 Have we made any incorrect assumptions about it?
Line 222: You can see that by asking the right sort of questions, we’re going to get the right sort of results.
Line 223: By writing tests first, we cover all these questions. We decide upfront how we are going to set up our 
Line 224: component, perhaps deciding on a clear constructor signature for an object. We decide how we are 
Line 225: going to make the calling code look and what the call site will be. We decide how we will consume 
Line 226: any results returned or what the effect will be on collaborating components.
Line 227: This is the heart of software design. TDD does not do this for us, nor does it force us to do a good 
Line 228: job. We could still come up with terrible answers for all those questions and simply write a test to 
Line 229: lock those poor answers into place. I’ve seen that happen on numerous occasions in real code as well.
Line 230: TDD provides that early opportunity to reflect on our decisions. We are literally writing the first 
Line 231: example of a working, executable call site for our code before we even think about how it will work. 
Line 232: We are totally focused on how this new component is going to fit into the bigger picture.
Line 233: The test itself provides immediate feedback on how well our decisions have worked out. It gives three 
Line 234: tell-tale signals that we could and should improve. We’ll save the details for a later chapter but the 
Line 235: test code itself clearly shows when your component is either hard to set up, hard to call, or its outputs 
Line 236: are hard to work with.
Line 237: Analyzing the benefits of writing tests before production code
Line 238: There are three times you can choose to write tests: before the code, after the code, or never.
Line 239: Obviously, never writing any tests sends us back to the dark ages of development. We’re winging it. 
Line 240: We write code assuming it will work, then leave it all to a manual test stage later. If we’re lucky, we 
Line 241: will discover functional errors at this stage, before our customers do.
Line 242: Writing tests just after we complete a small chunk of code is a much better option. We get much faster 
Line 243: feedback. Our code isn’t necessarily any better though, because we write with the same mindset as 
Line 244: we do without the implementation of tests. The same kinds of functional errors will be present. The 
Line 245: good news is that we will then write tests to uncover them.
Line 246: 
Line 247: --- 페이지 47 ---
Line 248: Using TDD to Create Good Code
Line 249: 24
Line 250: This is a big improvement, but it still isn’t the gold standard, as it leads to a couple of subtle problems:
Line 251: •	 Missing tests
Line 252: •	 Leaky abstractions
Line 253: Missing tests – undetected errors
Line 254: Missing tests happen because of human nature. When we are busy writing code, we are juggling 
Line 255: many ideas in our heads at once. We focus on specific details at the expense of others. I always find 
Line 256: that I mentally move on a bit too quickly after a line of code. I just assume that it’s going to be okay. 
Line 257: Unfortunately, when I come to write my tests, that means I’ve forgotten some key points.
Line 258: Suppose I end up writing some code like this:
Line 259: public boolean isAllowed18PlusProducts( Integer age ) {
Line 260:     return (age != null)  && age.intValue() > 18;
Line 261: }
Line 262: I’ll probably have quickly started with the > 18 check, then moved on mentally and remembered that 
Line 263: the age could be null. I will have added the And clause to check whether it is or not. That makes 
Line 264: sense. My experience tells me that this particular snippet of code needs to do more than be a basic, 
Line 265: robust check.
Line 266: When I write my test, I’ll remember to write a test for what happens when I pass in null, as that is 
Line 267: fresh in my mind. Then, I will write another test for what happens with a higher age, say 21. Again, good.
Line 268: Chances are that I will forget about writing a test for the edge case of an age value of 18. That’s really 
Line 269: important here but my mind has moved on from that detail already. All it will take is one Slack 
Line 270: message from a colleague about what’s for lunch, and I will most likely forget all about that test and 
Line 271: start coding the next method.
Line 272: The preceding code has a subtle bug in it. It is supposed to return true for any age that is 18 or 
Line 273: above. It doesn’t. It returns true only for 19 and above. The greater-than symbol should have been 
Line 274: a greater-than-or-equal-to symbol but I missed this detail.
Line 275: Not only did I miss the nuance in the code but I missed out a vital test. I wrote two important tests 
Line 276: but I needed three.
Line 277: Because I wrote the other tests, I get no warning at all about this. You don’t get a failing test that you 
Line 278: haven’t written.
Line 279: We can avoid this by writing a failing test for every piece of code, then adding only enough code to 
Line 280: make that test pass. That workflow would have been more likely to steer us toward thinking through 
Line 281: the four tests needed to drive out null handling and the three boundary cases relating to age. It 
Line 282: cannot guarantee it, of course, but it can drive the right kind of thinking.
Line 283: 
Line 284: --- 페이지 48 ---
Line 285: Preventing logic flaws
Line 286: 25
Line 287: Leaky abstractions – exposing irrelevant details
Line 288: Leaky abstractions are a different problem. This is where we focus so much on the inside of the method 
Line 289: that we forget to think about our dream call site. We just ripple out whatever is easiest to code.
Line 290: We might be writing an interface where we store UserProfile objects. We might proceed 
Line 291: code-first, pick ourselves a JDBC library that we like, code up the method, then find that it needs a 
Line 292: database connection.
Line 293: We might simply add a Connection parameter to fix that:
Line 294: interface StoredUserProfiles {
Line 295:     UserProfile load( Connection conn, int userId );
Line 296: }
Line 297: At first sight, there’s nothing much wrong with it. However, look at that first parameter: it’s the JDBC-
Line 298: specific Connection object. We have locked our interface into having to use JDBC. Or at the very 
Line 299: least, having to supply some JDBC-related thing as a first parameter. We didn’t even mean to do that. 
Line 300: We simply hadn’t thought about it thoroughly.
Line 301: If we think about the ideal abstraction, it should load the corresponding UserProfile object for 
Line 302: the given userId. It should not know how it is stored. The JDBC-specific Connection parameter 
Line 303: should not be there.
Line 304: If we think outside-in and consider the design before the implementation, we are less likely to go 
Line 305: down this route.
Line 306: Leaky abstractions like this create accidental complexity. They make code harder to understand by 
Line 307: forcing future readers to wonder why we are insisting on JDBC use when we never meant to do so. 
Line 308: We just forgot to design it out.
Line 309: Writing tests first helps prevent this. It leads us to think about the ideal abstractions as a first step so 
Line 310: we can write the test for them.
Line 311: Once we have that test coded up, we have locked in our decision on how the code will be used. Then, 
Line 312: we can figure out how to implement that without any unwanted details leaking out.
Line 313: The previously explained techniques are simple but cover most of the basics of good design. Use clear 
Line 314: names. Use simple logic. Use abstraction to hide implementation details, so that we emphasize what 
Line 315: problem we are solving, rather than how we are solving it. In the next section, let’s review the most 
Line 316: obvious benefit of TDD: preventing flaws in our logic.
Line 317: Preventing logic flaws
Line 318: The idea of logic errors is perhaps what everybody thinks of first when we talk about testing: did it 
Line 319: work right?
Line 320: 
Line 321: --- 페이지 49 ---
Line 322: Using TDD to Create Good Code
Line 323: 26
Line 324: I can’t disagree here – this is really important. As far as users, revenues, our Net Promoter Score®™, 
Line 325: and market growth go, if your code doesn’t work right, it doesn’t sell. It’s that simple.
Line 326: Understanding the limits of manual testing
Line 327: We know from bitter experience that the simplest logic flaws are often the easiest to create. The 
Line 328: examples that we can all relate to are those one-off errors, that NullPointerException from an 
Line 329: uninitialized variable, and that exception thrown by a library that wasn’t in the documentation. They 
Line 330: are all so simple and small. It seems like it would be so obvious for us to realize that we were making 
Line 331: these mistakes, yet we all know they are often the hardest to spot. When we humans concentrate on 
Line 332: the big picture of our code, sometimes these critical details just go unnoticed.
Line 333: We know that manual testing can reveal these logic flaws but we also know from experience that 
Line 334: manual test plans are fragile. It is possible to miss steps out or rush and miss important errors. We 
Line 335: might simply assume that something does not need testing on this release because we did not change 
Line 336: that section of code. You guessed it – that doesn’t always work out so well for us. Bugs can arise in 
Line 337: sections of code that seem totally unrelated to the bug if some underlying assumption has changed.
Line 338: Manual testing costs money, which is money that can now not be spent on adding shiny new 
Line 339: features instead.
Line 340: Manual testing also gets blamed for delaying ship dates. Now, this is spectacularly unfair to our manual 
Line 341: test colleagues. The development team – obviously writing code without TDD tests – stumble over 
Line 342: their own bugs until there are only a couple of days left to ship. Then, we hand over the code to the 
Line 343: testers, who have to run a huge test document in next to no time. They sometimes get blamed for 
Line 344: delaying the release, even though the real cause was development taking longer than it should.
Line 345: Yet, we never truly had a release. If we define a release as including tested code, which we should, then 
Line 346: it is clear that the necessary testing never happened. You can’t ethically release code when you don’t 
Line 347: even know whether it works. If you do, your users will be quick to complain.
Line 348: It’s no wonder some of my testing colleagues get so grumpy by the end of a sprint.
Line 349: Solving problems by automating the tests
Line 350: TDD has this totally covered. These logic errors simply cannot arise, which sounds like fantasy, but 
Line 351: it really is true.
Line 352: Before you type any production code, you have already written a failing test. Once you add your new 
Line 353: code, you rerun the test. If you somehow typed in a logic error, the test still fails and you know about 
Line 354: it right away. That’s the magic here: your mistake happens but is highlighted right away. This enables 
Line 355: you to fix it when it is fresh in your mind. It also means you cannot forget about fixing it later on.
Line 356: You can often go to the exact line that’s wrong and make the change. It’s 10 seconds of work, not 
Line 357: months of waiting for a test silo to get to work and fill out a JIRA bug ticket.
Line 358: 
Line 359: --- 페이지 50 ---
Line 360: Protecting against future defects
Line 361: 27
Line 362: The kinds of unit tests we are talking about are also fast to run – very fast. Many of them run within 
Line 363: a millisecond. Compare that to the total time to write a test plan document, run the whole app, 
Line 364: set up stored data, operate the user interface (UI), record output, then write up a bug ticket. It is 
Line 365: incomparably better, isn’t it?
Line 366: You can see how this is a bug-squashing superpower. We are making significant time savings within 
Line 367: the code-test-debug cycle. This reduces development costs and increases delivery velocity. These are 
Line 368: big wins for our team and our users.
Line 369: Every time you write a test before code, you have kept bugs out of that code. You follow the most basic 
Line 370: rule that you do not check code with failing tests. You make them pass.
Line 371: It shouldn’t need saying but you also don’t cheat around that failing test by deleting it, ignoring it, 
Line 372: or making it always pass by using some technical hack. However, I am saying all this because I have 
Line 373: seen exactly that done in real code.
Line 374: We’ve seen how writing tests first helps prevent adding bugs in our new code but TDD is even better 
Line 375: than that: it helps prevent adding bugs in code that we will add in the future, which we will cover in 
Line 376: the next section.
Line 377: Protecting against future defects
Line 378: As we grow our code by writing tests first, we could always simply delete each test after it has passed. 
Line 379: I’ve seen some students do that when I’ve taught them TDD because I hadn’t explained that we shouldn’t 
Line 380: do that yet. Regardless, we don’t delete tests once they pass. We keep them all.
Line 381: Tests grow into large regression suites, automatically testing every feature of the code we have built. 
Line 382: By frequently running all the tests, we gain safety and confidence in the entire code base.
Line 383: As team members add features to this code base, keeping all the tests passing shows that nobody has 
Line 384: accidentally broken something. It is quite possible in software to add a perfectly innocent change 
Line 385: somewhere, only to find that some seemingly unrelated thing has now stopped working. This will be 
Line 386: because of the relationship between those two pieces that we previously did not understand.
Line 387: The tests have now caused us to learn more about our system and our assumptions. They have prevented 
Line 388: a defect from being written into the code base. These are both great benefits but the bigger picture 
Line 389: is that our team has the confidence to make changes safely and know they have tests automatically 
Line 390: looking after them.
Line 391: This is true agility, the freedom to change. Agility was never about JIRA tickets and sprints. It was 
Line 392: always about the ability to move quickly, with confidence, through an ever-changing landscape of 
Line 393: requirements. Having tens of thousands of fast-running automated tests is probably the biggest 
Line 394: enabling practice we have.
Line 395: 
Line 396: --- 페이지 51 ---
Line 397: Using TDD to Create Good Code
Line 398: 28
Line 399: The ability of tests to give team members confidence to work quickly and effectively is a huge benefit 
Line 400: of TDD. You may have heard the phrase move fast and break things, famous from the early days of 
Line 401: Facebook. TDD allows us to move fast and not break things.
Line 402: As we’ve seen, tests are great at providing fast feedback on design and logic correctness, as well as 
Line 403: providing a defense against future bugs, but one huge extra benefit is that tests document our code.
Line 404: Documenting our code
Line 405: Everybody likes helpful, clear documentation, but not when it is out of date and unrelated to the 
Line 406: current code base.
Line 407: There is a general principle in software that the more separation there is between two related ideas, 
Line 408: the more pain they will bring. As an example, think of some code that reads some obscure file format 
Line 409: that nobody remembers. All works well, so long as you are reading files in that old format. Then you 
Line 410: upgrade the application, that old file format is no longer supported, and everything breaks. The code 
Line 411: was separated from the data content in those old files. The files didn’t change but the code did. We 
Line 412: didn’t even realize what was going on.
Line 413: It’s the same with documentation. The worst documentation is often contained in the glossiest 
Line 414: productions. These are artifacts written a long time after the code was created by teams with separate 
Line 415: skillsets – copywriting, graphic design, and so on. Documentation updates are the first thing to get 
Line 416: dropped from a release when time gets tight.
Line 417: The solution is to bring documentation closer to the code. Get it produced by people closer to the 
Line 418: code who know how it works in detail. Get it read by people who need to work directly with that code.
Line 419: As with all other aspects of Extreme Programming (XP), the most obvious major win is to make it 
Line 420: so close to the code that it is the code. Part of this involves using our good design fundamentals to 
Line 421: write clear code and our test suite also plays a key role.
Line 422: Our TDD tests are code, not manual test documents. They are usually written in the same language and 
Line 423: repo as the main code base. They will be written by the same people who are writing the production 
Line 424: code – the developers.
Line 425: The tests are executable. As a form of documentation, you know that something that can run has to 
Line 426: be up to date. Otherwise, the compiler will complain, and the code will not run.
Line 427: Tests also form the perfect example of how to use our production code. They clearly define how it 
Line 428: should be set up, what dependencies it has, what its interesting methods and functions are, what its 
Line 429: expected effects are, and how it will report errors. Everything you would want to know about that 
Line 430: code is in the tests.
Line 431: 
Line 432: --- 페이지 52 ---
Line 433: Summary
Line 434: 29
Line 435: It may be surprising at first. Testing and documentation are not normally confused with each other. 
Line 436: Because of how TDD works, there is a huge overlap between the two. Our test is a detailed description 
Line 437: of what our code should do and how we can make it do that for us.
Line 438: Summary
Line 439: In this chapter, we’ve learned that TDD helps us create good designs, write correct logic, prevent 
Line 440: future defects, and provide executable documentation for our code. Understanding what TDD will 
Line 441: do for our projects is important to use it effectively and to persuade our teams to use it as well. There 
Line 442: are many advantages to TDD and yet it is not used as often as it should be in real-world projects.
Line 443: In the next chapter, we will look into some common objections to TDD, learn why they are not valid, 
Line 444: and how we can help our colleagues overcome them.
Line 445:  Questions and answers 
Line 446: 1.	
Line 447: What is the connection between testing and clean code?
Line 448: There is not a direct one, which is why we need to understand how to write clean code. How 
Line 449: TDD adds value is that it forces us to think about how our code will be used before we write it 
Line 450: and when it is easiest to clean up. It also allows us to refactor our code, changing its structure 
Line 451: without changing its function, with certainty that we have not broken that function.
Line 452: 2.	
Line 453: Can tests replace documentation?
Line 454: Well-written tests replace some but not all documentation. They become a detailed and 
Line 455: up-to-date executable specification for our code. What they cannot replace are documents 
Line 456: such as user manuals, operations manuals, or contractual specifications for public application 
Line 457: programming interfaces (APIs).
Line 458: 3.	
Line 459: What are the problems with writing production code before tests?
Line 460: If we write production code first, then add tests later, we are more likely to face the 
Line 461: following problems:
Line 462: 	 Missing broken edge cases on conditionals
Line 463: 	 Leaking implementation details through interfaces
Line 464: 	 Forgetting important tests
Line 465: 	 Having untested execution paths
Line 466: 	 Creating difficult-to-use code
Line 467: 	 Forcing more rework when design flaws are revealed later in the process
Line 468: 
Line 469: --- 페이지 53 ---
Line 470: Using TDD to Create Good Code
Line 471: 30
Line 472: Further reading
Line 473: A formal definition of cyclomatic complexity can be found in the WikiPedia link. Basically, every 
Line 474: conditional statement adds to the complexity, as it creates a new possible execution path:
Line 475: https://en.wikipedia.org/wiki/Cyclomatic_complexity