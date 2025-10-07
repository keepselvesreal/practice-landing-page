Line 1: 
Line 2: --- 페이지 54 ---
Line 3: 3
Line 4: Dispelling Common 
Line 5: Myths about TDD
Line 6: Test-driven development (TDD) brings many benefits to developers and the business. However, it 
Line 7: is not always used in real projects. This is something I find surprising. TDD has been demonstrated 
Line 8: to improve internal and external code quality in different industrial settings. It works for frontend 
Line 9: and backend code. It works across verticals. I have experienced it working in embedded systems, web 
Line 10: conferencing products, desktop applications, and microservice fleets.
Line 11: To better understand how perceptions have gone wrong, let’s review the common objections to TDD, 
Line 12: then explore how we can overcome them. By understanding the perceived difficulties, we can equip 
Line 13: ourselves to be TDD advocates and help our colleagues reframe their thinking. We will examine six 
Line 14: popular myths that surround TDD and form constructive responses to them.
Line 15: In this chapter, we’re going to cover the following myths:
Line 16: •	 “Writing tests slows me down”
Line 17: •	 “Tests cannot prevent every bug”
Line 18: •	 “How do you know the tests are right”
Line 19: •	 “TDD guarantees good code”
Line 20: •	 “Our code is too complex to test”
Line 21: •	 “I don’t know what to test until I write the code”
Line 22: Writing tests slows me down
Line 23: Writing tests slowing development down is a popular complaint about TDD. This criticism has some 
Line 24: merit. Personally, I have only ever felt that TDD has made me faster, but academic research disagrees. 
Line 25: A meta-analysis of 18 primary studies by the Association for Computing Machinery showed that TDD 
Line 26: did improve productivity in academic settings but added extra time in industrial contexts. However, 
Line 27: that’s not the full story.
Line 28: 
Line 29: --- 페이지 55 ---
Line 30: Dispelling Common Myths about TDD
Line 31: 32
Line 32: Understanding the benefits of slowing down
Line 33: The aforementioned research indicates that the payback for taking extra time with TDD is a reduction 
Line 34: in the number of defects that go live in the software. With TDD, these defects are identified and 
Line 35: eliminated far sooner than with other approaches. By resolving issues before manual quality assurance 
Line 36: (QA), deployment, and release, and before potentially facing a bug report from an end user, TDD 
Line 37: allows us to cut out a large chunk of that wasted effort.
Line 38: We can see the difference in the amount of work to be done in this figure:
Line 39: Figure 3.1 – Not using TDD slows us down due to rework
Line 40: The top row represents developing a feature using TDD, where we have sufficient tests to prevent 
Line 41: any defects from going into production. The bottom row represents developing the same feature in 
Line 42: a code-and-fix style, without TDD, and finding that a defect has gone live in production. Without 
Line 43: TDD, we discover faults very late, annoy the user, and pay a heavy time penalty in rework. Note that 
Line 44: the code-and-fix solution looks like it gets us into the QA stage faster, until we consider all the rework 
Line 45: caused by undiscovered defects. The rework is what isn’t taken into account in this myth.
Line 46: Using TDD, we simply make all our design and testing thinking explicit and upfront. We capture and 
Line 47: document it using executable tests. Whether we write tests or not, we still spend that same thinking 
Line 48: time considering what the specifics that our code needs to cover are. It turns out that the mechanical 
Line 49: writing of the test code takes very little time. You can measure that yourself when we write our first 
Line 50: test in Chapter 5, Writing Our First Test. The total time spent writing a piece of code is the time to 
Line 51: design it, plus the time to write the code, plus the time to test it. Even without writing automated tests, 
Line 52: the design and coding time remain constant and dominant factors.
Line 53: The other area conveniently ignored through all this is the time taken to manually test. Without a 
Line 54: doubt, our code will be tested. The only question is when and by who. If we write a test first, it is by 
Line 55: us, the developers. It happens before any faulty code gets checked into our system. If we leave testing 
Line 56: to a manual testing colleague, then we slow down the whole development process. We need to spend 
Line 57: time helping our colleague understand what the success criteria are for our code. They must then 
Line 58: devise a manual test plan, which often must be written up, reviewed, and accepted into documentation.
Line 59: 
Line 60: --- 페이지 56 ---
Line 61: Writing tests slows me down
Line 62: 33
Line 63: Executing manual tests is very time-consuming. Generally, the whole system must be built and deployed 
Line 64: to a test environment. Databases must be manually set up to contain known data. The user interface 
Line 65: (UI) must be clicked through to get to a suitable screen where our new code might be exercised. 
Line 66: The output must be manually inspected and a decision made on its correctness. These steps must be 
Line 67: manually performed every time we make a change.
Line 68: Worse still, the later we leave it to test, the greater the chance is that we will have built on top of any 
Line 69: faulty code that exists. We cannot know we are doing that, as we haven’t tested our code yet. This often 
Line 70: becomes difficult to unpick. In some projects, we get so far out of step with the main code branch that 
Line 71: developers start emailing patch files to each other. This means we start building on top of this faulty 
Line 72: code, making it even harder to remove. These are bad practices but they do occur in real projects.
Line 73: The contrast to writing a TDD test first could not be greater. With TDD, the setup is automated, the 
Line 74: steps are captured and automated, and the result checking is automated. We are talking timescale 
Line 75: reductions of minutes for a manual test down to milliseconds using a TDD unit test. This time saving 
Line 76: is made every single time we need to run that test.
Line 77: While manual testing is not as efficient as TDD, there is still one far worse option: no testing at all. 
Line 78: Having a defect released to production means that we leave it to our users to test the code. Here, there 
Line 79: may be financial considerations and the risk of reputation damage. At the very least, this is a very 
Line 80: slow way to discover a fault. Isolating the defective lines of code from production logs and databases 
Line 81: is extraordinarily time-consuming. It is also usually frustrating, in my experience.
Line 82: It’s funny how a project that can never find time to write unit tests can always find time to trawl 
Line 83: production logs, roll back released code, issue marketing communications, and stop all other work 
Line 84: to do a Priority 1 (P1) fix. Sometimes, it feels like days are easier to find than minutes for some 
Line 85: management approaches.
Line 86: TDD certainly places a time cost up front in writing a test, but in return, we gain fewer faults to rectify 
Line 87: in production – with a huge saving in overall cost, time, and reputation compared to multiple rework 
Line 88: cycles with defects occurring in live code.
Line 89: Overcoming objections to tests slowing us down
Line 90: Build a case that tracks the time spent on undiscovered defects in manual QA and failed deployments. 
Line 91: Find some rough figures for the time taken for the most recent live issue to be fixed. Work out which 
Line 92: missing unit test could have prevented it. Now work out how long that would have taken to write. 
Line 93: Present these figures to stakeholders. It can be even more effective to work out the cost of all that 
Line 94: engineering time and any lost revenue.
Line 95: Knowing that tests do have an overall benefit in terms of fewer defects, let’s examine another common 
Line 96: objection that tests are of no value, as they cannot prevent every bug.
Line 97: 
Line 98: --- 페이지 57 ---
Line 99: Dispelling Common Myths about TDD
Line 100: 34
Line 101: Tests cannot prevent every bug
Line 102: A very old objection to testing of any kind is this one: you cannot catch every bug. While this is 
Line 103: certainly true, if anything, it means that we need more and better testing, not less. Let’s understand 
Line 104: the motivations behind this one to prepare an appropriate response.
Line 105: Understanding why people say tests cannot catch every bug
Line 106: Straight away, we can agree with this statement. Tests cannot catch every bug. More precisely, it has 
Line 107: been proven that testing in software systems can only reveal the presence of defects. It can never 
Line 108: prove that no defects exist. We can have many passing tests, and defects can still hide in the places 
Line 109: we haven’t tested.
Line 110: This seems to apply in other fields as well. Medical scans will not always reveal problems that are too 
Line 111: faint to notice. Wind tunnel tests for aircraft will not always reveal problems under specific flight 
Line 112: conditions. Batch sampling in a chocolate factory will not catch every substandard sweet.
Line 113: Just because we cannot catch every bug, does not mean this invalidates our testing. Every test we 
Line 114: write that catches one defect results in one less defect running through our workflow. TDD gives us 
Line 115: a process to help us think in terms of testing as we develop, but there are still areas where our tests 
Line 116: will not be effective:
Line 117: •	 Tests you have not thought to write
Line 118: •	 Defects that arise due to system-level interactions
Line 119: Tests that we have not written are a real problem. Even when writing tests first in TDD, we must be 
Line 120: disciplined enough to write a test for every scenario that we want to function. It is easy to write a test 
Line 121: and then write the code to make it pass. The temptation is to then just keep adding code because we 
Line 122: are on a roll. It is easy to miss an edge case and so not write a test for it. If we have a missing test, we 
Line 123: open up the possibility of a defect existing and being found later.
Line 124: The problem with system-level interactions here refers to the behavior that emerges when you take 
Line 125: tested units of software and join them. The interactions between units can sometimes be more complex 
Line 126: than anticipated. Basically, if we join up two well-tested things, the new combination itself is still not 
Line 127: yet tested. Some interactions have faults that only show up in these interactions, even though the units 
Line 128: that they are made up of passed all tests.
Line 129: These two problems are real and valid. Testing will never cover every possible fault, but this misses 
Line 130: the main value of testing. Every test we do write will reduce one defect.
Line 131: By not testing anything, we will never spot anything wrong. We will not prevent any defects. If we test, 
Line 132: no matter how little, then we will improve the quality of our code. Every defect that these tests can 
Line 133: detect will be prevented. We can see the straw-man nature of this argument: just because we cannot 
Line 134: cover every eventuality, it does not mean we should not do what we can.
Line 135: 
Line 136: --- 페이지 58 ---
Line 137: How do you know the tests are right?
Line 138: 35
Line 139: Overcoming objections to not catching every bug
Line 140: The way to reframe this is for us to have confidence that TDD prevents many classes of errors from 
Line 141: happening. Not all kinds of errors, certainly, but a bank of thousands of tests is going to make a 
Line 142: noticeable improvement to the quality of our applications.
Line 143: To explain this to our colleagues, we can draw on familiar analogies: just because a strong password 
Line 144: cannot prevent every hacker, this does not mean we should not use passwords and leave ourselves 
Line 145: vulnerable to any and every hacker. Staying healthy will not prevent every kind of medical problem 
Line 146: but it will prevent many kinds of serious problems.
Line 147: Ultimately, this is a question of balance. Zero testing is clearly not enough – every single defect will 
Line 148: end up going live in this case. We know that testing can never eliminate defects. So, where should we 
Line 149: stop? What constitutes enough? We can argue that TDD helps us decide on this balance at the best 
Line 150: possible time: while we are thinking about writing code. The automated TDD tests we create will save 
Line 151: us manual QA time. It’s manual work that no longer needs to be done. These time and cost savings 
Line 152: compound, repaying us in every single iteration of code.
Line 153: Now that we understand why testing as much as possible always beats not testing at all, we can look 
Line 154: into the next common objection: how do we know the tests themselves were written correctly?
Line 155: How do you know the tests are right?
Line 156: This is an objection that has merit, so we need to deeply understand the logic behind it. This is a 
Line 157: common objection from people unfamiliar with writing automated tests, as they misunderstand 
Line 158: how we avoid incorrect tests. By helping them see the safeguards we put in place, we can help them 
Line 159: reframe their thinking.
Line 160: Understanding the concerns behind writing broken tests
Line 161: One objection you will hear is, “How do we know the tests are right if the tests themselves don’t have 
Line 162: tests?” This objection was raised the first time I introduced unit tests to a team. It was polarizing. Some 
Line 163: of the team understood the value right away. Others were indifferent, but some were actively hostile. 
Line 164: They saw this new practice as suggesting they were somehow deficient. It was perceived as a threat. 
Line 165: Against that background, one developer pointed out a flaw in the logic I had explained.
Line 166: I told the team that we could not trust our visual reading of production code. Yes, we are all skilled at 
Line 167: reading code, but we are humans, so we miss things. Unit tests would help us avoid missing things. 
Line 168: One bright developer asked a great question: if visual inspection does not work for production code, 
Line 169: why are we saying that it does work for test code? What’s the difference between the two?
Line 170: The right illustration for this came after I needed to test some XML output (which was in 2005, I 
Line 171: remember). The code I had written for checking the XML output was truly complex. The criticism was 
Line 172: correct. There was no way I could visually inspect that test code and honestly say it was without defects.
Line 173: 
Line 174: --- 페이지 59 ---
Line 175: Dispelling Common Myths about TDD
Line 176: 36
Line 177: So, I applied TDD to the problem. I used TDD to write a utility class that could compare two XML 
Line 178: strings and report either that they were the same or what the first difference was. It could be configured 
Line 179: to ignore the order of XML elements. I extracted this complex code out of my original test and replaced 
Line 180: it with a call to this new utility class. I knew the utility class did not have any defects, as it passed 
Line 181: every TDD test that I had written for it. There were many tests, covering every happy path and every 
Line 182: edge case I cared about. The original test that had been criticized now became very short and direct.
Line 183: I asked my colleague who had raised the point to review the code. They agreed that in this new, 
Line 184: simpler form, they were happy to agree that the test was correct, visually. They added the caveat “if 
Line 185: the utility class works right.” Of course, we had the confidence that it passed every TDD test we had 
Line 186: written it against. We were certain that it did all the things we specifically wanted it to do, as proven 
Line 187: by tests for these things.
Line 188: Providing reassurance that we test our tests
Line 189: The essence of this argument is that short, simple code can be visually inspected. To ensure this, we 
Line 190: keep most of our unit tests simple and short enough to reason about. Where tests get too complex, 
Line 191: we extract that complexity into its own code unit. We develop that using TDD and end up making 
Line 192: both the original test code simple enough to inspect and the test utility simple enough for its tests to 
Line 193: inspect, a classic example of divide and conquer.
Line 194: Practically, we invite our colleagues to point out where they feel our test code is too complex to trust. 
Line 195: We refactor it to use simple utility classes, these themselves written using simple TDD. This approach 
Line 196: helps us build trust, respects the valid concerns of our colleagues, and shows how we can find ways 
Line 197: to reduce all TDD tests to simple, reviewable code blocks.
Line 198: Now that we have addressed knowing our tests are right, another common objection involves having 
Line 199: overconfidence in TDD: that simply following the TDD process will therefore guarantee good code. 
Line 200: Can that be true? Let’s examine the arguments.
Line 201: TDD guarantees good code
Line 202: Just as there are often overly pessimistic objections to TDD, here is an opposite view: TDD guarantees 
Line 203: good code. As TDD is a process, and it claims to improve code, it is quite reasonable to assume that 
Line 204: using TDD is all you need to guarantee good code. Unfortunately, that is not at all correct. TDD 
Line 205: helps developers write good code and it helps as feedback to show us where we have made mistakes 
Line 206: in design and logic. It cannot guarantee good code, however.
Line 207: Understanding problem-inflated expectations
Line 208: The issue here is a misunderstanding. TDD is not a set of techniques that directly affect your design 
Line 209: decisions. It is a set of techniques that help you specify what you expect a piece of code to do, when, 
Line 210: under what conditions, and given a particular design. It leaves you free to choose that design, what 
Line 211: you expect it to do, and how you are going to implement that code.
Line 212: 
Line 213: --- 페이지 60 ---
Line 214: Our code is too complex to test
Line 215: 37
Line 216: TDD has no suggestions regarding choosing a long variable name over a short one. It does not tell 
Line 217: you whether you should choose an interface or an abstract class. Should you choose to split a feature 
Line 218: over two classes or five? TDD has no advice there. Should you eliminate duplicated code? Invert a 
Line 219: dependency? Connect to a database? Only you can decide. TDD offers no advice. It is not intelligent. It 
Line 220: cannot replace you and your expertise. It is a simple process, enabling you to validate your assumptions 
Line 221: and ideas.
Line 222: Managing your expectations of TDD
Line 223: TDD is hugely beneficial in my view but we must regard it in context. It provides instant feedback on 
Line 224: our decisions but leaves every important software design decision to us.
Line 225: Using TDD, we are free to write code using the SOLID principles (which will be covered in Chapter 7, 
Line 226: Driving Design  — TDD and SOLID, of this book) or we can use a procedural approach, an object-
Line 227: oriented approach, or a functional approach. TDD allows us to choose our algorithm as we see fit. 
Line 228: It enables us to change our minds about how something should be implemented. TDD works across 
Line 229: every programming language. It works across every vertical.
Line 230: Helping our colleagues see past this objection helps them realize that TDD is not some magic system 
Line 231: that replaces the intelligence and skill of the programmer. It harnesses this skill by providing instant 
Line 232: feedback on our decisions. While this may disappoint colleagues who hoped it would allow perfect code 
Line 233: to come from imperfect thinking, we can point out that TDD gives us time to think. The advantage 
Line 234: is that it puts thinking and design up front and central. By writing a failing test before writing the 
Line 235: production code that makes the test pass, we have ensured that we have thought about what that code 
Line 236: should do and how it should be used. That’s a great advantage.
Line 237: Given that we understand that TDD does not design our code for us, yet is still a developer’s friend, 
Line 238: how can we approach testing complex code?
Line 239: Our code is too complex to test
Line 240: Professional developers routinely deal with highly complex code. That’s just a fact of life. It leads to one 
Line 241: valid objection: our code is too difficult to write unit tests for. The code we work on might be highly 
Line 242: valuable, trusted legacy code that brings in significant top-line revenue. This code may be complex. 
Line 243: But is it too complex to test? Is it true to say that every piece of complex code simply cannot be tested?
Line 244: Understanding the causes of untestable code
Line 245: The answer lies in the three ways that code becomes complex and hard to test:
Line 246: •	 Accidental complexity: We chose a hard way over a simpler way by accident
Line 247: •	 External systems cannot be controlled to set up for our tests
Line 248: •	 The code is so entangled that we no longer understand it
Line 249: 
Line 250: --- 페이지 61 ---
Line 251: Dispelling Common Myths about TDD
Line 252: 38
Line 253: Accidental complexity makes code hard to read and hard to test. The best way to think about this is 
Line 254: to know that any given problem has many valid solutions. Say we want to add a total of five numbers. 
Line 255: We could write a loop. We could create five concurrent tasks that take each number, then report that 
Line 256: number to another concurrent task that computes the total (bear with me, please… I’ve seen this 
Line 257: happen). We could have a complex design pattern-based system that has each number trigger an 
Line 258: observer, which places each one in a collection, which triggers an observer to add to the total, which 
Line 259: triggers an observer every 10 seconds after the last input.
Line 260: Yes, I know some of those are silly. I just made them up. But let’s be honest – what kinds of silly designs 
Line 261: have you worked on before? I know I have written code that was more complex than it needed to be.
Line 262: The key point of the addition of five numbers example is that it really should use a simple loop. 
Line 263: Anything else is accidental complexity, neither necessary nor intentional. Why would we do that? 
Line 264: There are many reasons. There may be some project constraints, a management directive, or simply 
Line 265: a personal preference that steers our decision. However it happened, a simpler solution was possible, 
Line 266: yet we did not take it.
Line 267: Testing more complex solutions generally requires more complex tests. Sometimes, our team thinks 
Line 268: it is not worth spending time on that. The code is complex, it will be hard to write tests for, and we 
Line 269: think it works already. We think it is best not to touch it.
Line 270: External systems cause problems in testing. Suppose our code talks to a third-party web service. It is 
Line 271: hard to write a repeatable test for that. Our code consumes the external service and the data it sends 
Line 272: to us is different each time. We cannot write a test and verify what the service sent us, as we do not 
Line 273: know what the service should be sending to us. If we could replace that external service with some 
Line 274: dummy service that we could control, then we could fix this problem easily. But if our code does not 
Line 275: permit that, then we are stuck.
Line 276: Entangled code is a further development of this. To write a test, we need to understand what that 
Line 277: code does to an input condition: what do we expect the outputs to be? If we have a body of code that 
Line 278: we simply do not understand, then we cannot write a test for it.
Line 279: While these three problems are real, there is one underlying cause to them all: we allowed our software 
Line 280: to get into this state. We could have arranged it to only use simple algorithms and data structures. 
Line 281: We could have isolated external systems so that we could test the rest of the code without them. We 
Line 282: could have modularized our code so that it was not overly entangled.
Line 283: However, how can we persuade our teams with these ideas?
Line 284: Reframing the relationship between good design and simple 
Line 285: tests
Line 286: All the preceding problems relate to making software that works yet does not follow good design 
Line 287: practices. The most effective way to change this, in my experience, is pair programming – working 
Line 288: together on the same piece of code and helping each other find these better design ideas. If pair 
Line 289: 
Line 290: --- 페이지 62 ---
Line 291: I don’t know what to test until I write the code
Line 292: 39
Line 293: programming is not an option, then code reviews also provide a checkpoint to introduce better designs. 
Line 294: Pairing is better as by the time you get to code review, it can be too late to make major changes. It’s 
Line 295: cheaper, better, and faster to prevent poor design than it is to correct it.
Line 296: Managing legacy code without tests
Line 297: We will encounter legacy code without tests that we need to maintain. Often, this code has grown to 
Line 298: be quite unmanageable and ideally needs replacing, except that nobody knows what it does anymore. 
Line 299: There may be no written documentation or specification to help us understand it. Whatever written 
Line 300: material there is may be completely outdated and unhelpful. The original authors of the code may 
Line 301: have moved on to a different team or different company.
Line 302: The best advice here is to simply leave this code alone if possible. Sometimes though, we need to add 
Line 303: features that require that code to be changed. Given that we have no existing tests, it is quite likely 
Line 304: we will find that adding a new test is all but impossible. The code simply is not split up in a way that 
Line 305: gives us access points to hang a test off.
Line 306: In this case, we can use the Characterization Test technique. We can describe this in three steps:
Line 307: 1.	
Line 308: Run the legacy code, supplying it with every possible combination of inputs.
Line 309: 2.	
Line 310: Record all the outputs that result from each one of these input runs. This output is traditionally 
Line 311: called the Golden Master.
Line 312: 3.	
Line 313: Write a Characterization Test that runs the code with all inputs again. Compare every output 
Line 314: against the captured Golden Master. The test fails if any are different.
Line 315: This automated test compares any changes that we have made to the code against what the original 
Line 316: code did. This will guide us as we refactor the legacy code. We can use standard refactoring techniques 
Line 317: combined with TDD. By preserving the defective outputs in the Golden Master, we ensure that we 
Line 318: are purely refactoring in this step. We avoid the trap of restructuring the code at the same time as 
Line 319: fixing the bugs. When bugs are present in the original code, we work in two distinct phases: first, 
Line 320: refactor the code without changing observable behavior. Afterwards, fix the defects as a separate task. 
Line 321: We never fix bugs and refactor together. The Characterization Test ensures we do not accidentally 
Line 322: conflate the two tasks.
Line 323: We’ve seen how TDD helps tackle accidental complexity and the difficulty of changing legacy code. 
Line 324: Surely writing a test before production code means we need to know what the code looks like before 
Line 325: we test it though? Let’s review this common objection next.
Line 326: I don’t know what to test until I write the code
Line 327: A great frustration for TDD learners is knowing what to test without having written the production 
Line 328: code beforehand. This is another criticism that has merit. In this case, once we understand the issue 
Line 329: that developers face, we can see that the solution is a technique we can apply to our workflow, not a 
Line 330: reframing of thinking.
Line 331: 
Line 332: --- 페이지 63 ---
Line 333: Dispelling Common Myths about TDD
Line 334: 40
Line 335: Understanding the difficulty of starting with testing
Line 336: To an extent, it’s natural to think about how we implement code. It’s how we learn, after all. We write 
Line 337: System.out.println("Hello, World!"); instead of thinking up some structure to place 
Line 338: around the famous line. Small programs and utilities work just fine when we write them as linear 
Line 339: code, similar to a shopping list of instructions.
Line 340: We begin to face difficulties as programs get larger. We need help organizing the code into understandable 
Line 341: chunks. These chunks need to be easy to understand. We want them to be self-documenting and it to be 
Line 342: easy for us to know how to call them. The larger the code gets, the less interesting the insides of these 
Line 343: chunks are, and the more important the external structure of these chunks – the outsides – becomes.
Line 344: As an example, let’s say we are writing a TextEditorWidget class, and we want to check the spelling 
Line 345: on the fly. We find a library with a SpellCheck class in it. We don’t care that much about how the 
Line 346: SpellCheck class works. We only care about how we can use this class to check the spelling. We 
Line 347: want to know how to create an object of that class, what methods we need to call to get it to do its 
Line 348: spellchecking job, and how we can access the output.
Line 349: This kind of thinking is the definition of software design – how components fit together. It is critical 
Line 350: that we emphasize design as code bases grow if we want to maintain them. We use encapsulation 
Line 351: to hide the details of data structures and algorithms inside our functions and classes. We provide a 
Line 352: simple-to-use programming interface.
Line 353: Overcoming the need to write production code first
Line 354: TDD scaffolds design decisions. By writing the test before the production code, we are defining how 
Line 355: we want the code under test to be created, called, and used. This helps us see very quickly how well 
Line 356: our decisions are working out. If the test shows that creating our object is hard, that shows us that our 
Line 357: design should simplify the creation step. The same applies if the object is difficult to use; we should 
Line 358: simplify our programming interface as a result.
Line 359: However, how do we cope with the times when we simply do not yet know what a reasonable design 
Line 360: should be? This situation is common when we either use a new library, integrate with some new code 
Line 361: from the rest of our team, or tackle a large user story.
Line 362: To solve this, we use a spike, a short section of code that is sufficient to prove the shape of a design. 
Line 363: We don’t aim for the cleanest code at this stage. We do not cover many edge cases or error conditions. 
Line 364: We have the specific and limited goal of exploring a possible arrangement of objects and functions 
Line 365: to make a credible design. As soon as we have that, we sketch out some notes on the design and then 
Line 366: delete it. Now that we know what a reasonable design looks like, we are better placed to know what 
Line 367: tests to write. We can now use normal TDD to drive our design.
Line 368: Interestingly, when we start over in this way, we often end up driving out a better design than our 
Line 369: spike. The feedback loop of TDD helps us spot new approaches and improvements.
Line 370: 
Line 371: --- 페이지 64 ---
Line 372: Summary
Line 373: 41
Line 374: We’ve seen how natural it is to want to start implementing code before tests, and how we can use TDD 
Line 375: and spikes to create a better process. We make decisions at the last responsible moment – the latest 
Line 376: possible time to decide before we are knowingly making an irreversible, inferior decision. When in 
Line 377: doubt, we can learn more about the solution space by using a spike – a short piece of experimental 
Line 378: code designed to learn from and then throw away.
Line 379: Summary
Line 380: In this chapter, we’ve learned six common myths that prevent teams from using TDD and discussed 
Line 381: the right approach to reframing those conversations. TDD really deserves a much wider application 
Line 382: in modern software development than it has now. It’s not that the techniques don’t work. TDD simply 
Line 383: has an image problem, often among people who haven’t experienced its true power.
Line 384: In the second part of this book, we will start to put the various rhythms and techniques of TDD into 
Line 385: practice and build out a small web application. In the next chapter, we will start our TDD journey 
Line 386: with the basics of writing a unit test with the Arrange-Act-Assert (AAA) pattern.
Line 387: Questions and answers
Line 388: 1.	
Line 389: Why is it believed that TDD slows developers down?
Line 390: When we don’t write a test, we save the time spent writing the test. What this fails to consider 
Line 391: is the extra time costs of finding, reproducing, and fixing a defect in production.
Line 392: 2.	
Line 393: Does TDD eliminate human design contributions?
Line 394: No. Quite the opposite. We still design our code using every design technique at our disposal. 
Line 395: What TDD gives us is a fast feedback loop on whether our design choices have resulted in 
Line 396: easy-to-use, correct code.
Line 397: 3.	
Line 398: Why doesn’t my project team use TDD?
Line 399: What a fantastic question to ask them! Seriously. See whether any of their objections have been 
Line 400: covered by this chapter. If so, you can gently lead the conversation using the ideas presented.
Line 401: Further reading
Line 402: •	 https://en.wikipedia.org/wiki/Characterization_test
Line 403: More detail on the Characterization Test technique, where we capture the output of an existing 
Line 404: software module exactly as-is, with a view to restructuring the code without changing any of its 
Line 405: behavior. This is especially valuable in older code where the original requirements have become 
Line 406: unclear, or that has evolved over the years to contain defects that other systems now rely on.
Line 407: •	 https://effectivesoftwaredesign.com/2014/03/27/lean-software-
Line 408: development-before-and-after-the-last-responsible-moment/
Line 409: An in-depth look at what deciding at the last responsible moment means for software design.
Line 410: 
Line 411: --- 페이지 65 ---