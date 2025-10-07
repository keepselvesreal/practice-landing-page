Line 1: 
Line 2: --- 페이지 236 ---
Line 3: 12
Line 4: Test First, Test Later, Test Never
Line 5: In this chapter, we are going to review some of the nuances of Test-Driven Development (TDD). 
Line 6: We’ve already covered the broad techniques of writing unit tests as part of an overall test strategy. We 
Line 7: can use the test pyramid and hexagonal architecture to guide the scope of our tests in terms of what 
Line 8: specifically they need to cover.
Line 9: We have two more dimensions we need to decide on: when and where to start testing. The first 
Line 10: question is one of timing. Should we always write our tests before the code? What difference would it 
Line 11: make to write tests after the code? In fact, what about not testing at all – does that ever make sense? 
Line 12: Where to start testing is another variable to decide. There are two schools of thought when it comes to 
Line 13: TDD – testing from the inside out or the outside in. We will review what these terms mean and what 
Line 14: impact each has on our work. Finally, we will consider how these approaches work with a hexagonal 
Line 15: architecture to form a natural testing boundary.
Line 16: In this chapter we’re going to cover the following main topics:
Line 17: •	 Adding tests first
Line 18: •	 We can always test it later, right?
Line 19: •	 Tests? They’re for people who can’t write code!
Line 20: •	 Testing from the inside out
Line 21: •	 Testing from the outside in
Line 22: •	 Defining test boundaries with hexagonal architecture
Line 23: Adding tests first
Line 24: In this section, we will review the trade-offs of adding a test first before writing the production code 
Line 25: to make it pass.
Line 26: Previous chapters have followed a test-first approach to writing code. We write a test before writing 
Line 27: production code to make that test pass. This is a recommended approach, but it is important to 
Line 28: understand some of the difficulties associated with it as well as considering its benefits.
Line 29: 
Line 30: --- 페이지 237 ---
Line 31: Test First, Test Later, Test Never
Line 32: 214
Line 33: Test-first is a design tool
Line 34: The most important benefit of writing tests first is that a test acts as a design aid. As we decide what to 
Line 35: write in our test, we are designing the interface to our code. Each of the test stages helps us consider 
Line 36: an aspect of software design, as illustrated by the following diagram:
Line 37: Figure 12.1 – Test-first aids design
Line 38: The Arrange step helps us think about how the code under test relates to the bigger picture of the 
Line 39: whole code base. This step helps us design how the code will fit into the whole code base. It gives us 
Line 40: an opportunity to make the following design decisions:
Line 41: •	 What configuration data will be needed?
Line 42: •	 What connections to other objects or functions will be needed?
Line 43: •	 What behavior should this code provide?
Line 44: •	 What extra inputs are needed to provide that behavior?
Line 45: Coding the Act step allows us to think about how easy our code will be to use. We reflect on what we 
Line 46: would like the method signature of the code we are designing to be. Ideally, it should be simple and 
Line 47: unambiguous. Some general recommendations are the following:
Line 48: •	 The method name should describe the outcome of calling the method.
Line 49: •	 Pass in as few parameters as possible. Possibly group parameters into their own object.
Line 50: •	 Avoid Boolean flags that modify the behavior of the code. Use separate methods with 
Line 51: appropriate names.
Line 52: •	 Avoid requiring multiple method calls to do one thing. It is too easy to miss out on an important 
Line 53: call in the sequence if we are unfamiliar with the code.
Line 54: 
Line 55: --- 페이지 238 ---
Line 56: Adding tests first
Line 57: 215
Line 58: Writing the Act step allows us to see what the call to our code will look like everywhere it is used for 
Line 59: the first time. This provides the opportunity to simplify and clarify before our code gets widely used.
Line 60: The code in our Assert step is the first consumer of the results of our code. We can judge from this 
Line 61: step whether those results are easy to obtain. If we are unhappy with how the Assert code looks, this 
Line 62: is a chance to review how our object provides its output.
Line 63: Every test we write provides this opportunity for a design review. TDD is all about helping us uncover 
Line 64: better designs, even more than it is about testing correctness.
Line 65: In other industries, such as designing cars, it is common to have dedicated design tools. AutoCAD 
Line 66: 3D Studio is used to create 3D models for the chassis of a car on a computer. Before we manufacture 
Line 67: the car, we can use the tool to pre-visualize the end result, rotating it through space and viewing it 
Line 68: from several angles.
Line 69: Mainstream commercial software engineering lags far behind in terms of design tool support. We don’t 
Line 70: have an equivalent to 3D Studio for designing code. The 1980s to 2000s saw the rise of Computer-
Line 71: Aided Software Engineering (CASE) tools but these appear to have fallen into disuse. CASE tools 
Line 72: purported to simplify software engineering by allowing their users to enter various graphical forms 
Line 73: of software structures, then generate code that implemented those structures. Today, writing TDD 
Line 74: tests prior to writing the production code seems to be the closest thing we have to computer-aided 
Line 75: design for software at present.
Line 76: Tests form executable specifications
Line 77: Another advantage of test code is that it can form a highly accurate, repeatable form of documentation. 
Line 78: Simplicity and clarity in the test code are required to achieve that. Instead of writing a test planning 
Line 79: document, we write TDD tests as code, which can be run by a computer. This has the benefit of being 
Line 80: more immediate for developers. These executable specifications are captured alongside the production 
Line 81: code they test, stored in source control, and made continuously available to the whole team.
Line 82: Further documentation is useful. Documents such as RAID logs – documenting risks, actions, 
Line 83: issues, and decisions – and KDDs – documenting key design decisions – are often required. These 
Line 84: are non-executable documents. They serve the purpose of capturing who, when, and critically why an 
Line 85: important decision was made. Information of this kind cannot be captured using test code, meaning 
Line 86: that these kinds of documents have value.
Line 87: Test-first provides meaningful code coverage metrics
Line 88: Writing a test before we write production code gives each test a specific purpose. The test exists to 
Line 89: drive out a specific behavior in our code. Once we get this test to pass, we can run the test suite using 
Line 90: a code coverage tool, which will output a report similar to the following:
Line 91: 
Line 92: --- 페이지 239 ---
Line 93: Test First, Test Later, Test Never
Line 94: 216
Line 95: Figure 12.2 – Code coverage report
Line 96: A code coverage tool instruments our production code as we run the tests. This instrumentation 
Line 97: captures which lines of code were executed during running the tests. This report can suggest we have 
Line 98: missing tests, by flagging up lines of code that were never executed during the test run.
Line 99: The code coverage report in the image shows we have executed 100% of the code in the domain model 
Line 100: by our test run. Having 100% coverage is entirely down to us writing a TDD test before we write code 
Line 101: to make it pass. We do not add untested code with a test-first TDD workflow.
Line 102: Beware of making a code coverage metric a target
Line 103: A high code coverage metric doesn’t always indicate high code quality. If we are writing tests for 
Line 104: generated code or tests for code we’ve pulled from a library, that coverage does not tell us anything 
Line 105: new. We may assume – generally – that our code generators and libraries have already been tested 
Line 106: by their developers.
Line 107: However, a real problem with code coverage numbers happens when we mandate them as a metric. 
Line 108: As soon as we impose a minimum coverage target on developers, then Goodhart’s law applies – when 
Line 109: a measure becomes a target, it ceases to be a good measure. Humans will sometimes cheat the system 
Line 110: to achieve a target when under pressure. When that happens, you see code such as this:
Line 111: public class WordTest {
Line 112:     @Test
Line 113:     public void oneCorrectLetter() {
Line 114:         var word = new Word("A");
Line 115:         var score = word.guess("A");
Line 116: 
Line 117: --- 페이지 240 ---
Line 118: Adding tests first
Line 119: 217
Line 120:         // assertThat(score).isEqualTo(CORRECT);
Line 121:     }
Line 122: }
Line 123: Notice those comment symbols – // – just before assertThat()? That’s the hallmark of a test 
Line 124: case that was failing and could not be made to pass by a certain deadline. By retaining the test, we 
Line 125: keep our number of test cases up, and we keep our code coverage percentage up. A test such as this 
Line 126: will execute lines of production code, but it will not validate that they work. The code coverage target 
Line 127: will be hit – even though the code itself does not work.
Line 128: Now, I know what you’re thinking – no developer would ever cheat the test code like this. It is, however, 
Line 129: an example from a project I worked on for a major international client. The client had engaged both 
Line 130: the company I work for and another development team to work on some microservices. Due to a 
Line 131: time zone difference, the other team would check in their code changes while our team was asleep.
Line 132: We came in one morning to see our test results dashboards lit up red. The overnight code change 
Line 133: had caused large numbers of our tests to fail. We checked the pipelines of the other team and were 
Line 134: astonished to see all their tests passing. This made no sense. Our tests clearly revealed a defect in that 
Line 135: nightly code drop. We could even localize it from our test failures. This defect would have shown up in 
Line 136: the unit tests around that code, but those unit tests were passing. The reason? Commented-out asserts.
Line 137: The other team was under pressure to deliver. They obeyed their instructions to get that code change 
Line 138: checked in on that day. Those changes, in fact, had broken their unit tests. When they could not fix 
Line 139: them in the time available, they chose to cheat the system and defer the problem to another day. I’m 
Line 140: not sure I blame them. Sometimes, 100% code coverage and all tests passing mean nothing at all.
Line 141: Beware of writing all tests upfront
Line 142: One of the strengths of TDD is that it allows for emergent design. We do a small piece of design work, 
Line 143: captured in a test. We then do the next small piece of design, captured in a new test. We perform 
Line 144: varying depths of refactoring as we go. In this way, we learn about what is and is not working in our 
Line 145: approach. The tests provide fast feedback on our design.
Line 146: This can only happen if we write tests one at a time. A temptation for those familiar with waterfall 
Line 147: project approaches can be to treat the test code as one giant requirements document, to be completed 
Line 148: before development starts. While this seems more promising than simply writing a requirements 
Line 149: document in a word processor, it also means that developers cannot learn from test feedback. There 
Line 150: is no feedback cycle. This approach to testing should be avoided. Better results are obtained by taking 
Line 151: an incremental approach. We write one test at a time, together with the production code to make 
Line 152: that test pass.
Line 153: 
Line 154: --- 페이지 241 ---
Line 155: Test First, Test Later, Test Never
Line 156: 218
Line 157: Writing tests first helps with continuous delivery
Line 158: Perhaps the biggest benefit of writing tests first lies in continuous delivery situations. Continuous 
Line 159: delivery relies on a highly automated pipeline. Once a code change is pushed to source control, the 
Line 160: build pipeline is started, all tests run, and finally, a deployment occurs.
Line 161: The only reason for code not to deploy in this system – assuming the code compiles – is if the tests 
Line 162: fail. This implies that the automated tests we have in place are necessary and sufficient to create the 
Line 163: level of confidence required.
Line 164: Writing tests first cannot guarantee this – we may still have missing tests – but out of all the ways 
Line 165: of working with tests, it is perhaps the most likely to result in one meaningful test for each piece of 
Line 166: application behavior that we care about.
Line 167: This section has presented the case that writing tests first – before production code is written, to make 
Line 168: them pass – helps create confidence in our code, as well as useful executable specifications. However, 
Line 169: that’s not the only way to code. Indeed, a common approach we will see is to write a chunk of code 
Line 170: first and then write tests shortly after.
Line 171: The next section looks at the advantages and limitations of the test-later approach.
Line 172: We can always test it later, right?
Line 173: An alternative approach to writing tests before code is to write code first, then write tests. This section 
Line 174: compares and contrasts writing tests after the code with writing tests before the code.
Line 175: One approach to writing tests involves writing chunks of code and then retrofitting tests to those 
Line 176: pieces of code. It’s an approach that is used in commercial programming, and the workflow can be 
Line 177: illustrated as follows:
Line 178: Figure 12.3 – Test-after workflow
Line 179: Upon selecting a user story to develop, one or more pieces of production code are written. Tests follow! 
Line 180: Academic research seems mixed, to say the least, on whether or not test-after differs from test-first. 
Line 181: From one 2014 study by the ACM, an extract from the conclusion was this:
Line 182: “…static code analysis results were found statistically significant in the 
Line 183: favor of TDD. Moreover, the results of the survey revealed that the majority of 
Line 184: developers in the experiment prefer TLD over TDD, given the lesser required level 
Line 185: of learning curve.”
Line 186: (Source: https://dl.acm.org/doi/10.1145/2601248.2601267)
Line 187: 
Line 188: --- 페이지 242 ---
Line 189: We can always test it later, right?
Line 190: 219
Line 191: However, a commenter pointed out that in this research, the following applied:
Line 192: “…usable data was obtained from only 13 out of 31 developers. This meant the 
Line 193: statistical analysis was undertaken using groups of seven (TDD) and six (TLD). 
Line 194: There is no real surprise that the experiment was found to lack statistical power 
Line 195: and that the findings were inconclusive.”
Line 196: Other research papers seem to show similar lackluster results. Practically then, what should we take 
Line 197: away from this? Let’s consider some practical details of test-later development.
Line 198: Test-later is easier for a beginner to TDD
Line 199: One finding of the research was that beginners to TDD found test-later to be easier to get started 
Line 200: with. This seems reasonable. Before we attempt TDD, we may consider coding and testing as different 
Line 201: activities. We write code according to some set of heuristics, and then we figure out how to test that 
Line 202: code. Adopting a test-later approach means that the coding phase is essentially unchanged by the 
Line 203: demands of testing. We can continue coding as we always did. There is no impact from having to 
Line 204: consider the impacts of testing on the design of that code. This seeming advantage is short-lived, as 
Line 205: we discover the need to add access points for testing, but we can at least get started easily.
Line 206: Adding tests later works reasonably well if we keep writing tests in lockstep with the production 
Line 207: code: write a little code, and write a few tests for that code – but not having tests for every code path 
Line 208: remains a risk.
Line 209: Test-later makes it harder to test every code path
Line 210: A plausible argument against using a test-later approach is that it becomes harder to keep track of 
Line 211: having all the tests we need. On the face of it, this claim cannot be completely true. We can always 
Line 212: find some way to keep track of the tests we need. A test is a test, no matter when it is written.
Line 213: The problem comes as the time between adding tests increases. We are adding more code, which 
Line 214: means adding more execution paths throughout the code. For example, every if statement we write 
Line 215: represents two execution paths. Ideally, every execution path through our code will have a test. Every 
Line 216: untested execution path we add places us one test below this ideal number. This is illustrated directly 
Line 217: in flowcharts:
Line 218: 
Line 219: --- 페이지 243 ---
Line 220: Test First, Test Later, Test Never
Line 221: 220
Line 222: Figure 12.4 – Illustrating execution paths
Line 223: This flowchart depicts a process with nested decision points – the diamond shapes – which result 
Line 224: in three possible execution paths, labeled A, B, and C. The technical measure of the number of 
Line 225: execution paths is called cyclomatic complexity. The complexity score is the number calculated on 
Line 226: how many linearly independent execution paths exist in a piece of code. The code in the flowchart 
Line 227: has a cyclomatic complexity of three.
Line 228: As we increase the cyclomatic complexity of our code, we increase our cognitive load with the need 
Line 229: to remember all those tests that we need to write later. At some point, we might even find ourselves 
Line 230: periodically stopping coding and writing down notes for what tests to add later. This sounds like a 
Line 231: more arduous version of simply writing the tests as we go.
Line 232: The issue of keeping track of tests we are yet to write is avoided when using test-first development.
Line 233: Test-later makes it harder to influence the software design
Line 234: One of the benefits of test-first development is that the feedback loop is very short. We write one test 
Line 235: and then complete a small amount of production code. We then refactor as required. This moves away 
Line 236: from a waterfall-style pre-planned design to an emergent design. We change our design in response 
Line 237: to learning more about the problem we are solving as we incrementally solve more of it.
Line 238: When writing tests after a chunk of code has already been written, it gets harder to incorporate 
Line 239: feedback. We may find that the code we have created proves difficult to integrate into the rest of the 
Line 240: code base. Perhaps this code is confusing to use due to having unclear interfaces. Given all the effort 
Line 241: we have spent creating the messy code, it can be tempting to just live with the awkward design and 
Line 242: its equally awkward test code.
Line 243: 
Line 244: --- 페이지 244 ---
Line 245: Tests? They’re for people who can’t write code!
Line 246: 221
Line 247: Test-later may never happen
Line 248: Development tends to be a busy activity, especially when deadlines are involved. Time pressures may 
Line 249: mean that the time we hoped to get to write our tests simply never comes. It’s not uncommon for 
Line 250: project managers to be more impressed with new features than with tests. This seems a false economy 
Line 251: – as users only care about features that work – but it’s a pressure that developers sometimes face.
Line 252: This section has shown that writing tests shortly after writing code can work as well as writing tests 
Line 253: first if care is exercised. It also seems preferable to some developers at the start of their TDD journey – 
Line 254: but what about the ultimate extreme of never testing our code? Let’s quickly review the consequences 
Line 255: of that approach.
Line 256: Tests? They’re for people who can’t write code!
Line 257: This section discusses another obvious possibility when it comes to automated testing – simply not 
Line 258: writing automated tests at all. Perhaps not even testing at all. Is this viable?
Line 259: Not testing at all is a choice we could make, and this might not be as silly as it sounds. If we define 
Line 260: testing as verifying some outcome is achieved in its target environment, then things such as deep-space 
Line 261: probes cannot truly be tested on Earth. At best, we are simulating the target environment during our 
Line 262: testing. Giant-scale web applications can rarely be tested with realistic load profiles. Take any large 
Line 263: web application, launch a hundred million users at it – all doing invalid things – and see how most 
Line 264: applications hold up. It’s probably not as well as developer testing suggested.
Line 265: There are areas of development where we might expect to see fewer automated tests:
Line 266: •	 Extract, Transform, and Load (ETL) scripts for data migrations:
Line 267: ETL scripts are often one-off affairs, written to solve a specific migration problem with some 
Line 268: data. It’s not always worth writing automated tests for these, performing manual verification 
Line 269: on a similar set of source data instead.
Line 270: •	 Front-end user interface work:
Line 271: Depending on the programming approach, it may be challenging to write unit tests for the 
Line 272: frontend code. Whatever approach we take, assessing the visual look and feel cannot currently be 
Line 273: automated. As a result, manual testing is often used against a candidate release of a user interface.
Line 274: •	 Infrastructure-as-code scripts:
Line 275: Our applications need to be deployed somewhere for them to run. A recent approach to 
Line 276: deployment is to use languages such as Terraform to configure servers using code. This is an 
Line 277: area that’s not yet simple to automate tests for.
Line 278: So what actually happens when we abandon test automation, possibly not even testing at all?
Line 279: 
Line 280: --- 페이지 245 ---
Line 281: Test First, Test Later, Test Never
Line 282: 222
Line 283: What happens if we do not test during development?
Line 284: We might think that not testing at all is an option, but in reality, testing will always happen at some 
Line 285: point. We can illustrate this with a timeline of the possible points at which testing can occur:
Line 286: Figure 12.5 – Testing timeline
Line 287: Test-first approaches shift the testing to be as early as possible – an approach called shift-left – where 
Line 288: defects can be corrected cheaply and easily. Thinking that we won’t test merely pushes testing all the 
Line 289: way to the right – after users start using features live.
Line 290: Ultimately, all code that users care about gets tested eventually. Maybe developers don’t test it. Maybe 
Line 291: testing will fall to another specialist testing team, who will write defect reports. Maybe defects will 
Line 292: be found during the operation of the software. Most commonly of all, we end up outsourcing testing 
Line 293: to the users themselves.
Line 294: Having users test our code for us is generally a bad idea. Users trust us to give them software that solves 
Line 295: their problems. Whenever a defect in our code prevents that from happening, we lose that trust. A 
Line 296: loss of trust damages the 3 Rs of a business: revenue, reputation, and retention. Users may well switch 
Line 297: to another supplier, whose better-tested code actually solves the user’s problem.
Line 298: If there is any possibility at all to test our work before we ship it, we should take that opportunity. The 
Line 299: sooner we build test-driven feedback loops into our work, the easier it will be to improve the quality 
Line 300: of that work.
Line 301: Having looked at when we test our software, let’s turn to where we test it. Given the overall design of 
Line 302: a piece of software, where should we start testing? The next section reviews a test approach that starts 
Line 303: from the inside of a design and works its way out.
Line 304: Testing from the inside out
Line 305: In this section, we’re going to review our choice of starting point for our TDD activities. The first place 
Line 306: to look at is inside our software system, starting with details.
Line 307: When starting to build software, we obviously need some place to start from. One place to start is 
Line 308: with some of the details. Software is made up of small interconnecting components, each of which 
Line 309: 
Line 310: --- 페이지 246 ---
Line 311: Testing from the inside out
Line 312: 223
Line 313: performs a portion of the whole task. Some components come from library code. Many components 
Line 314: are custom-made to provide the functionality our application needs.
Line 315: One place to start building, then, is on the inside of this software system. Starting with an overall 
Line 316: user story, we can imagine a small component that is likely to be of use to us. We can begin our TDD 
Line 317: efforts around this component and see where that leads us. This is a bottom-up approach to the design, 
Line 318: composing the whole from smaller parts.
Line 319: If we consider a simplified version of our Wordz application structure, we can illustrate the inside-out 
Line 320: approach as follows:
Line 321: Figure 12.6 – Inside-out development
Line 322: The diagram shows the Score component highlighted, as that is where we will start development using 
Line 323: an inside-out approach. The other software components are grayed-out. We are not designing those 
Line 324: pieces yet. We would start with a test for some behavior we wanted the Score component to have. We 
Line 325: would work our way outward from that starting point.
Line 326: This style of inside-out TDD is also known as Classicist TDD or Chicago TDD. It is the approach 
Line 327: originally described by Kent Beck in his book Test-Driven Development by Example. The basic idea is 
Line 328: to start anywhere to create any useful building block for our code. We then develop a progressively 
Line 329: larger unit that incorporates the earlier building blocks.
Line 330: The inside-out approach has a few advantages:
Line 331: •	 Quick start to development: We test pure Java code first in this approach, using the familiar 
Line 332: tools of JUnit and AssertJ. There is no setup for user interfaces, web service stubs, or databases. 
Line 333: There is no setup of user interface testing tools. We just dive right in and code using Java.
Line 334: 
Line 335: --- 페이지 247 ---
Line 336: Test First, Test Later, Test Never
Line 337: 224
Line 338: •	 Good for known designs: As we gain experience, we recognize some problems as having 
Line 339: known solutions. Perhaps we have written something similar before. Maybe we know a useful 
Line 340: collection of design patterns that will work. In these cases, starting from the interior structure 
Line 341: of our code makes sense.
Line 342: •	 Works well with hexagonal architecture: Inside-out TDD starts work inside the inner hexagon, 
Line 343: the domain model of our application. The adapter layer forms a natural boundary. An inside-
Line 344: out design is a good fit for this design approach.
Line 345: Naturally, nothing is perfect and inside-out TDD is no exception. Some challenges include the following:
Line 346: •	 Possibility of waste: We begin inside-out TDD with our best guess of some components that 
Line 347: will be needed. Sometimes, it emerges later that either we don’t need these components, or we 
Line 348: should refactor the features somewhere else. Our initial effort is in some sense wasted – although 
Line 349: it will have helped us progress to this point.
Line 350: •	 Risk of implementation lock-in: Related to the previous point, sometimes we move on from 
Line 351: an initial design having learned more about the problem we’re solving, but we don’t always 
Line 352: recognize a sunk cost. There is always a temptation to keep using a component we wrote earlier 
Line 353: even if it no longer fits as well, just because we invested that time and money into creating it.
Line 354: Inside-out TDD is a useful approach and was first popularized by Kent Beck’s book. However, if we can 
Line 355: start inside-out, what about turning that around? What if we started from the outside of the system 
Line 356: and worked our way in? The next section reviews this alternative approach.
Line 357: Testing from the outside in
Line 358: Given that inside-out TDD has some challenges as well as strengths, what difference does outside-in 
Line 359: TDD make? This section reviews the alternative approach of starting from outside the system.
Line 360: Outside-in TDD begins with the external users of the system. They may be human users or machines, 
Line 361: consuming some API offered by our software. This approach to TDD begins by simulating some 
Line 362: external input, such as the submission of a web form.
Line 363: The test will typically use some kind of test framework – such as Selenium or Cypress for web applications 
Line 364: – that allows the test to call up a specific web view, and simulate typing text into fields, then clicking 
Line 365: a submit button. We can then make this test pass in the normal way, only we will have written some 
Line 366: code that directly deals with the input from a user this time. In our hexagonal architecture model, we 
Line 367: will end up writing the user input adapter first.
Line 368: 
Line 369: --- 페이지 248 ---
Line 370: Testing from the outside in
Line 371: 225
Line 372: We can illustrate the outside-in approach as follows:
Line 373: Figure 12.7 – Outside-in view
Line 374: We can see that a component called Web API is the focus of our attention here. We will write a test 
Line 375: that sets up enough of our application to run a component that handles web requests. The test will 
Line 376: form a web request, send it to our software, and then assert that the correct web response is sent. The 
Line 377: test may also instrument the software itself to verify it takes the expected actions internally. We start 
Line 378: testing from the outside, and as development progresses, we move inwards.
Line 379: This approach to TDD is described in the book, Growing Object-Oriented Software, Guided by Tests, 
Line 380: by Steve Freeman and Nat Pryce. The technique is also known as the London or Mockist school of 
Line 381: TDD. The reasons for that are the location where it was first popularized and its use of mock objects, 
Line 382: respectively. To test drive the user input adapter as the first component we tackle, we need a test 
Line 383: double in place of the rest of the software. Mocks and stubs are an inherent part of outside-in TDD.
Line 384: Outside-in TDD, predictably enough, has some strengths and weaknesses. Let’s take a look at the 
Line 385: strengths first:
Line 386: •	 Less waste: Outside-in TDD encourages a quite minimal approach to satisfying external 
Line 387: behavior. The code produced tends to be highly customized to the application at hand. In 
Line 388: contrast, inside-out TDD focuses on building a robust domain model, perhaps providing more 
Line 389: functionality than will end up in use by users.
Line 390: •	 Delivers user value quickly: Because we start from a test that simulates a user request, the 
Line 391: code we write will satisfy a user request. We can deliver value to users almost immediately.
Line 392: 
Line 393: --- 페이지 249 ---
Line 394: Test First, Test Later, Test Never
Line 395: 226
Line 396: Outside-in TDD also has some weaknesses, or at least limitations:
Line 397: •	 Fewest abstractions: On a related note, when writing the minimum code necessary to make 
Line 398: a test pass, outside-in TDD may lead to application logic being present in the adapter layer. 
Line 399: This can be refactored later but can lead to a less organized code base.
Line 400: •	 Inverted test pyramid: If all our TDD test efforts focus on the external responses, they are, 
Line 401: in fact, end-to-end tests. This opposes the recommended pattern of the test pyramid, which 
Line 402: prefers faster unit tests inside the code base. Having only slower, less repeatable end-to-end 
Line 403: tests can slow development.
Line 404: The two traditional schools of TDD both offer certain advantages in terms of how they affect the 
Line 405: software design we will produce. The next section looks at the impact of hexagonal architecture. By 
Line 406: starting from the idea that we will use a hexagonal approach, we can combine the advantages of both 
Line 407: schools of TDD. We end up defining a natural test boundary between the inside-out and outside-in 
Line 408: approaches to TDD.
Line 409: Defining test boundaries with hexagonal architecture
Line 410: The topic for this section is how using a hexagonal architecture impacts TDD. Knowing that we are using 
Line 411: hexagonal architecture presents useful boundaries for the different kinds of tests in the test pyramid.
Line 412: In one sense, how we organize our code base does not affect our use of TDD. The internal structure 
Line 413: of the code is simply an implementation detail, one of many possibilities that will make our tests 
Line 414: pass. That being said, some ways of structuring our code are easier to work with than others. Using 
Line 415: hexagonal architecture as a foundational structure does offer TDD some advantages. The reason why 
Line 416: lies with the use of ports and adapters.
Line 417: We’ve learned from previous chapters that it is easier to write tests for code where we can control 
Line 418: the environment in which the code runs. We’ve seen how the test pyramid gives a structure to the 
Line 419: different kinds of tests we write. Using the ports and adapters approach provides clean boundaries 
Line 420: for each kind of test in the code. Better yet, it provides us with an opportunity to bring even more 
Line 421: tests to the unit test level.
Line 422: Let’s review what kinds of tests best fit each layer of software written using hexagonal architecture.
Line 423: Inside-out works well with the domain model
Line 424: Classic TDD uses an inside-out development approach, where we choose a certain software component 
Line 425: to test-drive. This component may be a single function, a single class, or a small cluster of classes 
Line 426: that collaborate with each other. We use TDD to test this component as a whole given the behaviors 
Line 427: it offers to its consumers.
Line 428: 
Line 429: --- 페이지 250 ---
Line 430: Defining test boundaries with hexagonal architecture
Line 431: 227
Line 432: This kind of component resides in the domain model – the inner hexagon:
Line 433: Figure 12.8 – Testing the domain logic
Line 434: The key advantage is that these components are easy to write tests for and those tests run very quickly. 
Line 435: Everything lives in computer memory and there are no external systems to contend with.
Line 436: A further advantage is that complex behaviors can be unit-tested here at a very fine granularity. An 
Line 437: example would be testing all the state transitions within a finite state machine used to control a workflow.
Line 438: One disadvantage is that these fine-grained domain logic tests can get lost if a larger refactoring takes 
Line 439: place. If the component under fine-grained tests gets removed during refactoring, its corresponding 
Line 440: test will be lost – but the behavior will still exist somewhere else as a result of that refactoring. One 
Line 441: thing refactoring tools cannot do is figure out what test code relates to the production code being 
Line 442: refactored, and automatically refactor the test code to fit the new structure.
Line 443: Outside-in works well with adapters
Line 444: Mockist-style TDD approaches development from an outside-in perspective. This is a great match for 
Line 445: our adapter layer in a hexagonal architecture. We can assume that the core application logic resides 
Line 446: in the domain model and has been tested there with fast unit tests. This leaves adapters in the outer 
Line 447: hexagon to be tested by integration tests.
Line 448: 
Line 449: --- 페이지 251 ---
Line 450: Test First, Test Later, Test Never
Line 451: 228
Line 452: These integration tests only need to cover the behavior provided by the adapter. This should be very 
Line 453: limited in scope. The adapter code maps from the formats used by the external system only to what 
Line 454: is required by the domain model. It has no other function.
Line 455: This structure naturally follows the test pyramid guidelines. Fewer integration tests are required. Each 
Line 456: integration test has only a small scope of behavior to test:
Line 457: Figure 12.9 – Testing adapters
Line 458: This style of testing verifies the adapter in isolation. It will require some end-to-end happy-path testing 
Line 459: to show that the system as a whole has used the correct adapters.
Line 460: User stories can be tested across the domain model
Line 461: One benefit of having a domain model containing all the application logic is that we can test the logic 
Line 462: of complete user stories. We can replace the adapters with test doubles to simulate typical responses 
Line 463: from the external systems. We can then use FIRST unit tests to exercise complete user stories:
Line 464: 
Line 465: --- 페이지 252 ---
Line 466: Defining test boundaries with hexagonal architecture
Line 467: 229
Line 468: Figure 12.10 – Testing user stories
Line 469: The advantages are the speed and repeatability of FIRST unit tests. In other approaches to structuring 
Line 470: our code, we might only be able to exercise a user story as an end-to-end test in a test environment, 
Line 471: with all associated disadvantages. Having the ability to test user story logic at the unit level – across 
Line 472: the whole domain model – gives us a high degree of confidence that our application will satisfy the 
Line 473: users’ needs.
Line 474: To ensure this confidence, we need the integration tests of the adapter layer, plus some end-to-end 
Line 475: tests across selected user stories, confirming the application is wired and configured correctly as a 
Line 476: whole. These higher-level tests do not need to be as detailed as the user story tests performed around 
Line 477: the domain model.
Line 478: Having a good set of user story tests around the domain model also enables large-scale refactoring 
Line 479: within the domain model. We can have the confidence to restructure the inner hexagon guided by 
Line 480: these broadly scoped user story tests.
Line 481: This section has shown us how to relate the different kinds of tests in the test pyramid to the different 
Line 482: layers in a hexagonal architecture.
Line 483: 
Line 484: --- 페이지 253 ---
Line 485: Test First, Test Later, Test Never
Line 486: 230
Line 487: Summary
Line 488: This chapter has discussed the various stages at which we can write tests – before we write code, after 
Line 489: we write code, or possibly even never. It has made a case for writing tests before code as providing the 
Line 490: most value in terms of valid execution path coverage and developer ease. We went on to review how 
Line 491: hexagonal architecture interacts with both TDD and the test pyramid, leading to an opportunity to 
Line 492: bring user story testing into the realm of FIRST unit tests. This allows the fast and repeatable validation 
Line 493: of the core logic driving our user stories.
Line 494: In the next chapter – and throughout the third part of the book – we will return to building our Wordz 
Line 495: application. We will be making full use of all the techniques we’ve learned so far. We will begin inside-
Line 496: out with Chapter 13, Driving the Domain Layer.
Line 497: Questions and answers
Line 498: 1.	
Line 499: Is writing tests shortly after code just as good as writing test-first TDD?
Line 500: Some research seems to suggest that, although it is very difficult to set up a controlled experiment 
Line 501: with statistically significant results in this area. One factor we can consider concerns our own 
Line 502: personal discipline. If we write tests later, are we sure we will cover everything necessary? I 
Line 503: personally have concluded that I would not remember all I needed to cover and would need 
Line 504: to make notes. Those notes are perhaps best captured in the form of test code, leading to a 
Line 505: preference for test-first TDD.
Line 506: 2.	
Line 507: How does hexagonal architecture affect TDD?
Line 508: Hexagonal architecture provides a clean separation between a pure, inner core of domain logic 
Line 509: and the outside world. This allows us to mix and match the two schools of TDD knowing that 
Line 510: there is a firm boundary in the design up to which we can code. The inner domain model 
Line 511: supports entire use cases being unit-tested, as well as any fine-grained unit tests for detailed 
Line 512: behavior we feel are necessary. External adapters naturally suit integration tests, but these tests 
Line 513: don’t have to cover much, as the logic relates to our domain lives in the inner domain model.
Line 514: 3.	
Line 515: What happens if we abandon testing completely?
Line 516: We export the responsibility to the end user who will test it for us. We risk loss in revenue, 
Line 517: reputation, and user retention. Sometimes, we cannot perfectly recreate the final environment 
Line 518: in which the system will be used. In this case, making sure we have fully characterized and 
Line 519: tested our system as closely as we can seems wise. We can at least minimize the known risks.
Line 520: 
Line 521: --- 페이지 254 ---
Line 522: Further reading
Line 523: 231
Line 524: Further reading
Line 525: •	 An explanation of the Cyclomatic Complexity metric: https://en.wikipedia.org/
Line 526: wiki/Cyclomatic_complexity
Line 527: •	 Continuous Delivery, Jez Humble and Dave Farley, ISBN 978-0321601919
Line 528: •	 Working Effectively with Legacy Code, Michael Feathers, ISBN 978-0131177055
Line 529: •	 Test-Driven Development by Example, Kent Beck, ISBN 978-0321146533
Line 530: •	 Growing Object-Oriented Software, Guided by Tests, Steve Freeman and Nat Pryce, 
Line 531: ISBN 9780321503626
Line 532: •	 https://arxiv.org/pdf/1611.05994.pdf
Line 533: •	 Why Research on Test-Driven Development is Inconclusive?, Ghafari, Gucci, Gross, and 
Line 534: Felderer: https://arxiv.org/pdf/2007.09863.pdf
Line 535: 
Line 536: --- 페이지 255 ---