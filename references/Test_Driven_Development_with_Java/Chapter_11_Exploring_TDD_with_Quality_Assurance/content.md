Line 1: 
Line 2: --- 페이지 222 ---
Line 3: 11
Line 4: Exploring TDD with 
Line 5: Quality Assurance
Line 6: Previous chapters have covered the technical practices needed to design and test well-engineered 
Line 7: code. The approach presented has been primarily for developers to gain rapid feedback on software 
Line 8: design. Testing has been almost a byproduct of these efforts.
Line 9: The combination of TDD, continuous integration, and pipelines provides us with a high level of confidence 
Line 10: in our code. But they are not the whole picture when it comes to software Quality Assurance (QA). 
Line 11: Creating the highest-quality software needs additional processes, featuring the human touch. In this 
Line 12: chapter, we will highlight the importance of manual exploratory testing, code reviews, user experience, 
Line 13: and security testing, together with approaches to adding a human decision point to a software release.
Line 14: In this chapter, we’re going to cover the following main topics:
Line 15: •	 TDD – its place in the bigger quality picture
Line 16: •	 Manual exploratory testing – discovering the unexpected
Line 17: •	 Code review and ensemble programming
Line 18: •	 User interface and user experience testing
Line 19: •	 Security testing and operations monitoring
Line 20: •	 Incorporating manual elements into CI/CD workflows
Line 21: TDD – its place in the bigger quality picture
Line 22: In this section, we will take a critical look at what TDD has brought to the testing table, and what 
Line 23: remains human activities. While TDD undoubtedly has advantages as part of a test strategy, it can 
Line 24: never be the entire strategy for a successful software system.
Line 25: 
Line 26: --- 페이지 223 ---
Line 27: Exploring TDD with Quality Assurance
Line 28: 200
Line 29: Understanding the limits of TDD
Line 30: TDD is a relatively recent discipline as far as mainstream development goes. The modern genesis 
Line 31: of TDD lies with Kent Beck in the Chrysler Comprehensive Compensation System (see the Further 
Line 32: reading section, where the idea of test-first unit testing came from). The project began in 1993 and 
Line 33: Kent Beck’s involvement commenced in 1996.
Line 34: The Chrysler Comprehensive Compensation project was characterized by extensive use of unit tests 
Line 35: driving small iterations and frequent releases of code. Hopefully, we recognize those ideas from the 
Line 36: preceding chapters in this book. Much has changed since then – the deployment options are different, 
Line 37: the number of users has increased, and agile approaches are more common – but the goals of testing 
Line 38: remain the same. Those goals are to drive out correct, well-engineered code and ultimately satisfy users.
Line 39: The alternative to test automation is to run tests without automation – in other words, run them 
Line 40: manually. A better term might be human-driven. Before test automation became commonplace, an 
Line 41: important part of any development plan was a test strategy document. These lengthy documents 
Line 42: defined when testing would be done, how it would be done, and who would be doing that testing.
Line 43: This strategy document existed alongside detailed test plans. These would also be written documents, 
Line 44: describing each test to be performed – how it would be set up, what steps exactly were to be tested, 
Line 45: and what the expected results should be. The traditional waterfall-style project would spend a lot of 
Line 46: time defining these documents. In some ways, these documents were similar to our TDD test code, 
Line 47: only written on paper, rather than source code.
Line 48: Executing these manual test plans was a large effort. Running a test needs us to set up test data by hand, 
Line 49: run the application, then click through user interfaces. Results must be documented. Defects found 
Line 50: must be recorded in defect reports. These must be fed back up the waterfall, triggering redesigns and 
Line 51: recoding. This must happen with every single release. Human-driven testing is repeatable, but only 
Line 52: at the great cost of preparing, updating, and following test documents. All of this took time – and a 
Line 53: lot of time at that.
Line 54: Against this background, Beck’s TDD ideas seemed remarkable. Test documents became executable 
Line 55: code and could be run as often as desired, for a fraction of the cost of human testing. This was a 
Line 56: compelling vision. The responsibility of testing code was part of the developer’s world now. The tests 
Line 57: were part of the source code itself. These tests were automated, capable of being run in full on every 
Line 58: build, and kept up to date as the code changed.
Line 59: No more need for manual testing?
Line 60: It’s tempting to think that using TDD as described in this book might eliminate manual testing. It 
Line 61: does eliminate some manual processes, but certainly not all. The main manual steps we replace with 
Line 62: automation are feature testing during development and regression testing before release.
Line 63: As we develop a new feature with TDD, we start by writing automated tests for that feature. Every 
Line 64: automated test we write is a test that does not need to be run by hand. We save all that test setup time, 
Line 65: 
Line 66: --- 페이지 224 ---
Line 67: Manual exploratory – discovering the unexpected
Line 68: 201
Line 69: together with the often lengthy process to click through a user interface to trigger the behavior we’re 
Line 70: testing. The main difference TDD brings is replacing test plans written in a word processor with test 
Line 71: code written in an IDE. Development feature manual testing is replaced by automation.
Line 72: TDD also provides us with automated regression testing, for free:
Line 73: Figure 11.1 – Regression testing
Line 74: Using TDD, we add one or more tests as we build out each feature. Significantly, we retain all those 
Line 75: tests. We naturally build up a large suite of automated tests, captured in source control and executed 
Line 76: on every build automatically. This is known as a regression test suite. Regression testing means that we 
Line 77: re-check all the tests run to date on every build. This ensures that as we make changes to the system, 
Line 78: we don’t break anything. Moving fast and not breaking things might be how we describe this approach.
Line 79: Regression tests also include tests for previously reported defects. These regression tests confirm that 
Line 80: they have not been re-introduced. It bears repeating that the regression suite saves on all the manual 
Line 81: effort required by non-automated tests each and every time the suite gets executed. This adds up over 
Line 82: the full software life cycle to a huge reduction.
Line 83: Test automation is good, but an automated test is a software machine. It cannot think for itself. It 
Line 84: cannot visually inspect code. It cannot assess the appearance of a user interface. It cannot tell whether 
Line 85: the user experience is good or bad. It cannot determine whether the overall system is fit for purpose.
Line 86: This is where human-driven manual testing comes in. The following sections will look at areas where 
Line 87: we need human-led testing, starting with an obvious one: finding bugs that our tests missed.
Line 88: Manual exploratory – discovering the unexpected
Line 89: In this section, we will appreciate the role of manual exploratory testing as an important line of defense 
Line 90: against defects where TDD is used.
Line 91: The biggest threat to our success with TDD lies in our ability to think about all the conditions our 
Line 92: software needs to handle. Any reasonably complex piece of software has a huge range of possible input 
Line 93: combinations, edge cases, and configuration options.
Line 94: 
Line 95: --- 페이지 225 ---
Line 96: Exploring TDD with Quality Assurance
Line 97: 202
Line 98: Consider using TDD to write code to restrict the sales of a product to buyers who are 18 years old and 
Line 99: above. We must first write a happy-path test to check whether the sale is allowed, make it pass, then write 
Line 100: a negative test, confirming that the sale can be blocked based on age. This test has the following form:
Line 101: public class RestrictedSalesTest {
Line 102:     @Test
Line 103:     void saleRestrictedTo17yearOld() {
Line 104:         // ... test code omitted
Line 105:     }
Line 106:     @Test
Line 107:     void salePermittedTo19yearOld() {
Line 108:         // ... test code omitted
Line 109:     }
Line 110: }
Line 111: The error is obvious when we’re looking for it: what happens at the boundary between the ages of 17 
Line 112: and 18? Can an 18-year-old buy this product or not? We don’t know, because there is no test for that. 
Line 113: We tested for 17 and 19 years old. For that matter, what should happen on that boundary? In general, 
Line 114: that’s a stakeholder decision.
Line 115: Automated tests cannot do two things:
Line 116: •	 Ask a stakeholder what they want the software to do
Line 117: •	 Spot a missing test
Line 118: This is where manual exploratory testing comes in. This is an approach to testing that makes the 
Line 119: most of human creativity. It uses our instincts and intelligence to work out what tests we might be 
Line 120: missing. It then uses scientific experimentation to discover whether our predictions of a missing test 
Line 121: were correct. If proven true, we can provide feedback on these findings and repair the defect. This 
Line 122: can be done either as an informal discussion or using a formal defect tracking tool. In due course, we 
Line 123: can write new automated tests to capture our discoveries and provide regression tests for the future.
Line 124: This kind of exploratory testing is a highly technical job, based on knowledge of what kinds of 
Line 125: boundaries exist in software systems. It also requires extensive knowledge of local deployment and 
Line 126: setup of software systems, together with knowing how software is built, and where defects are likely 
Line 127: to appear. To an extent, it relies on knowing how developers think and predicting the kinds of things 
Line 128: they may overlook.
Line 129: Some key differences between automated testing and exploratory testing can be summarized as follows:
Line 130: 
Line 131: --- 페이지 226 ---
Line 132: Code review and ensemble programming
Line 133: 203
Line 134: Automated Testing
Line 135: Manual Exploratory Testing
Line 136: Repeatable
Line 137: Creative
Line 138: Tests for known outcomes
Line 139: Finds unknown outcomes
Line 140: Possible by machine
Line 141: Requires human creativity
Line 142: Behavior verification
Line 143: Behavior investigation
Line 144: Planned
Line 145: Opportunistic
Line 146: Code is in control of the testing
Line 147: Human minds control the testing
Line 148: Table 11.1 – Automated versus manual exploratory testing
Line 149: Manual exploratory testing will always be needed. Even the best developers get pressed for time, 
Line 150: distracted, or have yet another meeting that should have been an email. Once concentration is lost, 
Line 151: it’s all too easy for mistakes to creep in. Some missing tests relate to edge cases that we cannot see 
Line 152: alone. Another human perspective often brings a fresh insight we would simply never have unaided. 
Line 153: Manual exploratory testing provides an important extra layer of defense in depth against defects 
Line 154: going unnoticed.
Line 155: Once exploratory testing identifies some unexpected behavior, we can feed this back into development. 
Line 156: At that point, we can use TDD to write a test for the correct behavior, confirm the presence of the 
Line 157: defect, then develop the fix. We now have a fix and a regression test to ensure the bug remains fixed. 
Line 158: We can think of manual exploratory testing as the fastest possible feedback loop for a defect we missed. 
Line 159: An excellent guide to exploratory testing is listed in the Further reading section.
Line 160: Seen in this light, automation testing and TDD do not make manual efforts less important. Instead, 
Line 161: their value is amplified. The two approaches work together to build quality into the code base.
Line 162: Manual testing for things we missed isn’t the only development time activity of value that cannot be 
Line 163: automated. We also have the task of checking the quality of our source code, which is the subject of 
Line 164: the next section.
Line 165: Code review and ensemble programming
Line 166: This section reviews another area surprisingly resistant to automation: checking code quality.
Line 167: As we’ve seen throughout this book, TDD is primarily concerned with the design of our code. As we 
Line 168: build up a unit test, we define how our code will be used by its consumers. The implementation of 
Line 169: that design is of no concern to our test, but it does concern us as software engineers. We want that 
Line 170: implementation to perform well and to be easy for the next reader to understand. Code is read many 
Line 171: more times than it is written over its life cycle.
Line 172: Some automated tools exist to help with checking code quality. These are known as static code analysis 
Line 173: tools. The name comes from the fact that they do not run code; instead, they perform an automated 
Line 174: 
Line 175: --- 페이지 227 ---
Line 176: Exploring TDD with Quality Assurance
Line 177: 204
Line 178: review of the source code. One popular tool for Java is Sonarqube (at https://www.sonarqube.
Line 179: org/), which runs a set of rules across a code base.
Line 180: Out of the box, tools like this give warnings about the following:
Line 181: •	 Variable name conventions not being followed
Line 182: •	 Uninitialized variables leading to possible NullPointerException problems
Line 183: •	 Security vulnerabilities
Line 184: •	 Poor or risky use of programming constructs
Line 185: •	 Violations of community-accepted practices and standards
Line 186: These rules can be modified and added to, allowing customization to be made to the local project 
Line 187: house style and rules.
Line 188: Of course, such automated assessments have limitations. As with manual exploratory testing, there 
Line 189: are simply some things only a human can do (at least at the time of writing). In terms of code analysis, 
Line 190: this mainly involves bringing context to the decisions. One simple example here is preferring longer, 
Line 191: more descriptive variable names to a primitive such as int, compared to a more detailed type such 
Line 192: as WordRepository. Static tools lack that understanding of the different contexts.
Line 193: Automated code analysis has its benefits and limitations, as summarized here:
Line 194: Automated Analysis
Line 195: Human Review
Line 196: Rigid rules (for example, variable name length)
Line 197: Relaxes rules based on context
Line 198: Applies a fixed set of assessment criteria
Line 199: Applies experiential learning
Line 200: Reports pass/fail outcomes
Line 201: Suggests alternative improvements
Line 202: Table 11.2 – Automated analysis versus human review
Line 203: Google has a very interesting system called Google Tricorder. This is a set of program analysis tools 
Line 204: that combines the creativity of Google engineers in devising rules for good code with the automation 
Line 205: to apply them. For more information, see https://research.google/pubs/pub43322/.
Line 206: Manually reviewing code can be done in various ways, with some common approaches:
Line 207: •	 Code review on pull requests:
Line 208: A pull request, also known as a merge request, is made by a developer when they wish to 
Line 209: integrate their latest code changes into the main code base. This provides an opportunity for 
Line 210: another developer to review that work and suggest improvements. They may even visually 
Line 211: spot defects. Once the original developer makes agreed changes, the request is approved and 
Line 212: the code is merged.
Line 213: 
Line 214: --- 페이지 228 ---
Line 215: User interface and user experience testing
Line 216: 205
Line 217: •	 Pair programming:
Line 218: Pair programming is a way of working where two developers work on the same task at the 
Line 219: same time. There is a continuous discussion about how to write the code in the best way. It is 
Line 220: a continuous review process. As soon as either developer spots a problem, or has a suggested 
Line 221: improvement, a discussion happens and a decision is made. The code is continuously corrected 
Line 222: and refined as it is developed.
Line 223: •	 Ensemble (mob) programming:
Line 224: Like pair programming, only the whole team takes part in writing the code for one task. The 
Line 225: ultimate in collaboration, which continuously brings the expertise and opinions of an entire 
Line 226: team to bear on every piece of code written.
Line 227: The dramatic difference here is that a code review happens after the code is written, but pair programming 
Line 228: and mobbing happen while the code is being written. Code reviews performed after the code is written 
Line 229: frequently happen too late to allow meaningful changes to be made. Pairing and mobbing avoid this 
Line 230: by reviewing and refining code continuously. Changes are made the instant they are identified. This 
Line 231: can result in higher quality output delivered sooner compared to the code-then-review workflow.
Line 232: Different development situations will adopt different practices. In every case, adding a second pair of 
Line 233: human eyes (or more) provides an opportunity for a design-level improvement, not a syntax-level one.
Line 234: With that, we’ve seen how developers can benefit from adding manual exploratory testing and code review 
Line 235: to their TDD work. Manual techniques benefit our users as well, as we will cover in the next section.
Line 236: User interface and user experience testing
Line 237: In this section, we will consider how we evaluate the impact of our user interface on users. This is another 
Line 238: area where automation brings benefits but cannot complete the job without humans being involved.
Line 239: Testing the user interface
Line 240: User interfaces are the only part of our software system that matters to the most important people of 
Line 241: all: our users. They are – quite literally – their windows into our world. Whether we have a command-
Line 242: line interface, a mobile web application, or a desktop GUI, our users will be helped or hindered in 
Line 243: their tasks by our user interface.
Line 244: The success of a user interface rests on two things being done well:
Line 245: •	 It provides all the functionality a user needs (and wants)
Line 246: •	 It allows a user to accomplish their end goals in an effective and efficient manner
Line 247: The first of these, providing functionality, is the more programmatic of the two. In the same way that we 
Line 248: use TDD to drive a good design for our server-side code, we can use it in our frontend code as well. If 
Line 249: our Java application generates HTML – called server-side rendering – TDD is trivial to use. We test the 
Line 250: 
Line 251: --- 페이지 229 ---
Line 252: Exploring TDD with Quality Assurance
Line 253: 206
Line 254: HTML generation adapter and we’re done. If we are using a JavaScript/Typescript framework running 
Line 255: in the browser, we can use TDD there, with a test framework such as Jest (https://jestjs.io/).
Line 256: Having tested we’re providing the right functions to the user, automation then becomes less useful. 
Line 257: With TDD, we can verify that all the right sorts of graphical elements are present in our user interface. 
Line 258: But we can’t tell whether they are meeting the needs of the user.
Line 259: Consider this fictional user interface for buying merchandise relating to our Wordz application:
Line 260: Figure 11.2 – Example user interface
Line 261: We can use TDD to test that all those interface elements – the boxes and buttons – are present and 
Line 262: working. But will our users care? Here are the questions we need to ask:
Line 263: •	 Does it look and feel good?
Line 264: •	 Does it align with corporate branding and house style guides?
Line 265: •	 For the task of buying a T-shirt, is it easy to use?
Line 266: •	 Does it present a logical flow to the user, guiding them through their task?
Line 267: Quite deliberately for this example, the answer is no to all these questions. This is, quite frankly, a 
Line 268: terrible user interface layout. It has no style, no feeling, and no brand identity. You have to type in 
Line 269: the product name in the text field. There is no product image, no description, and no price! This user 
Line 270: interface is truly the worst imaginable for an e-commerce product sales page. Yet it would pass all 
Line 271: our automated functionality tests.
Line 272: Designing effective user interfaces is a very human skill. It involves a little psychology in knowing 
Line 273: how humans behave when presented with a task, mixed with an artistic eye, backed by creativity. 
Line 274: These qualities of a user interface are best assessed by humans, adding another manual step to our 
Line 275: development process.
Line 276: 
Line 277: --- 페이지 230 ---
Line 278: User interface and user experience testing
Line 279: 207
Line 280: Evaluating the user experience
Line 281: Closely related to user interface design is user experience design.
Line 282: User experience goes beyond any individual element or view on a user interface. It is the entire 
Line 283: experience our users have, end to end. When we want to order the latest Wordz T-shirt from our 
Line 284: e-commerce store, we want the entire process to be easy. We want the workflow across every screen 
Line 285: to be obvious, uncluttered, and easier to get right than to get wrong. Going further, service design is 
Line 286: about optimizing the experience from wanting a T-shirt to wearing it.
Line 287: Ensuring users have a great experience is the job of a user experience designer. It is a human activity 
Line 288: that combines empathy, psychology, and experimentation. Automation is limited in how it can help 
Line 289: here. Some mechanical parts of this can be automated. Obvious candidates are applications such as 
Line 290: Invision (https://www.invisionapp.com/), which allows us to produce a screen mockup 
Line 291: that can be interacted with, and Google Forms, which allows us to collect feedback over the web, with 
Line 292: no code to set that up.
Line 293: After creating a candidate user experience, we can craft experiments where potential users are given 
Line 294: a task to complete, then asked to provide feedback on how they found the experience.
Line 295: A simple, manual form is more than adequate to capture this feedback:
Line 296: Experience
Line 297: Rating of 1 (Poor) – 5 (Good)
Line 298: Comments
Line 299: My task was easy 
Line 300: to complete
Line 301: 4
Line 302: I completed the task ok after being 
Line 303: prompted by your researcher.
Line 304: I felt confident 
Line 305: completing my task 
Line 306: without instructions
Line 307: 2
Line 308: The text entry field about T-shirt size 
Line 309: confused me. Could it be a dropdown of 
Line 310: available options instead?
Line 311: The interface guided 
Line 312: me through the task
Line 313: 3
Line 314: It was ok in the end – but that text field 
Line 315: was an annoyance, so I scored this 
Line 316: task lower.
Line 317: Table 11.3 – User experience feedback form
Line 318: User experience design is primarily a human activity. So is the evaluation of test results. These tools 
Line 319: only go as far as allowing us to create a mockup of our visions and collect experimental results. We 
Line 320: must run sessions with real users, solicit their opinions on how their experience was, then feed back 
Line 321: the results in an improved design.
Line 322: While user experience is important, the next section deals with a mission-critical aspect of our code: 
Line 323: security and operations.
Line 324: 
Line 325: --- 페이지 231 ---
Line 326: Exploring TDD with Quality Assurance
Line 327: 208
Line 328: Security testing and operations monitoring
Line 329: This section reflects on the critical aspects of security and operations concerns.
Line 330: So far, we have created an application that is well-engineered and has very low defects. Our user 
Line 331: experience feedback has been positive – it is easy to use. But all that potential can be lost in an instant 
Line 332: if we cannot keep the application running. If hackers target our site and harm users, the situation 
Line 333: becomes even worse.
Line 334: An application that is not running does not exist. The discipline of operations – often called DevOps 
Line 335: these days – aims to keep applications running in good health and alert us if that health starts to fail.
Line 336: Security testing – also called penetration testing (pentesting) – is a special case of manual exploratory 
Line 337: testing. By its nature, we are looking for new exploits and unknown vulnerabilities in our application. 
Line 338: Such work is not best served by automation. Automation repeats what is already known; to discover 
Line 339: the unknown requires human ingenuity.
Line 340: Penetration testing is the discipline that takes a piece of software and attempts to circumvent its 
Line 341: security. Security breaches can be expensive, embarrassing, or business-ending for a company. The 
Line 342: exploits used to create the breach are often very simple.
Line 343: Security risks can be summarized roughly as follows:
Line 344: •	 Things we shouldn’t see
Line 345: •	 Things we shouldn’t change
Line 346: •	 Things we shouldn’t use as often
Line 347: •	 Things we should not be able to lie about
Line 348: This is an oversimplification, of course. But the fact remains that our application may be vulnerable 
Line 349: to these damaging activities – and we need to know whether that is the case or not. This requires 
Line 350: testing. This kind of testing must be adaptive, creative, devious, and continually updated. An automated 
Line 351: approach is none of those things, meaning security testing must take its place as a manual step in our 
Line 352: development process.
Line 353: A great starting point is to review the latest OWASP Top 10 Web Application Security Risks 
Line 354: (https://owasp.org/www-project-top-ten/) and begin some manual exploratory 
Line 355: testing based on the risks listed. Further information on threat models such as Spoofing, Tampering, 
Line 356: Repudiation, Information Disclosure, Denial of Service, and Elevation of Privilege (STRIDE) can 
Line 357: be found at https://www.eccouncil.org/threat-modeling/. OWASP also has some 
Line 358: excellent resources on useful tools at https://owasp.org/www-community/Fuzzing. 
Line 359: Fuzzing is an automated way of discovering defects, although it requires a human to interpret the 
Line 360: results of a failed test.
Line 361: As with other manual exploratory tests, these ad hoc experiments may lead to some future test 
Line 362: automation. But the real value lies in the creativity applied to investigating the unknown.
Line 363: 
Line 364: --- 페이지 232 ---
Line 365: Incorporating manual elements into CI/CD workflows
Line 366: 209
Line 367: The preceding sections have made a case for the importance of manual interventions to complement 
Line 368: our test automation efforts. But how does that fit in with a continuous integration/continuous 
Line 369: delivery (CI/CD) approach? That’s the focus of the next section.
Line 370: Incorporating manual elements into CI/CD workflows
Line 371: We’ve seen that not only are manual processes important in our overall workflow but for some things, 
Line 372: they are irreplaceable. But how do manual steps fit into heavily automated workflows? That’s the 
Line 373: challenge we will cover in this section.
Line 374: Integrating manual processes into an automated CI/CD pipeline can be difficult. The two approaches 
Line 375: are not natural partners in terms of a linear, repeatable sequence of activities. The approach we take 
Line 376: depends on our ultimate goal. Do we want a fully automated continuous deployment system, or are 
Line 377: we happy with some manual interruptions?
Line 378: The simplest approach to incorporating a manual process is to simply stop the automation at a suitable 
Line 379: point, begin the manual process, then resume automaton once the manual process completes. We can 
Line 380: think of this as a blocking workflow, as all further automated steps in the pipeline must stop until the 
Line 381: manual work is completed. This is illustrated in the following diagram:
Line 382: Figure 11.3 – Blocking workflow
Line 383: By organizing our development process as a series of stages, some being automated and some being 
Line 384: manual, we create a simple blocking workflow. Blocking here means that the flow of value is blocked 
Line 385: by each stage. The automation stages typically run more quickly than the manual stages.
Line 386: This workflow has some advantages in that it’s simple to understand and operate. Each iteration of 
Line 387: software we deliver will have all automated tests run as well as all the current manual processes. In 
Line 388: one sense, this release is of the highest quality we know how to make at that time. The disadvantage 
Line 389: is that each iteration must wait for all manual processes to complete:
Line 390: Figure 11.4 – Dual track workflow
Line 391: 
Line 392: --- 페이지 233 ---
Line 393: Exploring TDD with Quality Assurance
Line 394: 210
Line 395: One enabler for very smooth dual-track workflows is to use a single main trunk for the whole code 
Line 396: base. All developers commit to this main trunk. There are no other branches. Any features in active 
Line 397: development are isolated by feature flags. These are Boolean values that can be set to true or 
Line 398: false at runtime. The code inspects these flags and decides whether to run a feature or not. Manual 
Line 399: testing can then happen without having to pause deployments. During testing, the features in progress 
Line 400: are enabled via the relevant feature flags. For the general end users, features in progress are disabled.
Line 401: We can select the approach that fits our delivery goals the best. The blocking workflow trades off 
Line 402: less rework for an extended delivery cycle. The dual-track approach allows for more frequent feature 
Line 403: delivery, with a risk of having defects in production before they are discovered by a manual process 
Line 404: and, subsequently, repaired.
Line 405: Selecting the right process to use involves a trade-off between feature release cadence and tolerating 
Line 406: defects. Whatever we choose, the goal is to focus the expertise of the whole team on creating software 
Line 407: with a low defect rate.
Line 408: Balancing automated workflows with manual, human workflows isn’t easy, but it does result in getting 
Line 409: the most human intuition and experience into the product. That’s good for our development teams and 
Line 410: it is good for our users. They benefit from improved ease of use and robustness in their applications. 
Line 411: Hopefully, this chapter has shown you how we can combine these two worlds and cross that traditional 
Line 412: developer-tester divide. We can make one great team, aiming at one excellent outcome.
Line 413: Summary
Line 414: This chapter discussed the importance of various manual processes during development.
Line 415: Despite its advantages, we’ve seen how TDD cannot prevent all kinds of defects in software. First, we 
Line 416: covered the benefits of applying human creativity to manual exploratory testing, where we can uncover 
Line 417: defects that we missed during TDD. Then, we highlighted the quality improvements that code reviews 
Line 418: and analysis bring. We also covered the very manual nature of creating and verifying excellent user 
Line 419: interfaces with satisfying user experiences. Next, we emphasized the importance of security testing 
Line 420: and operations monitoring in keeping a live system working well. Finally, we reviewed approaches to 
Line 421: integrating manual steps into automation workflows, and the trade-offs we need to make.
Line 422: In the next chapter, we’ll review some ways of working related to when and where we develop tests, 
Line 423: before moving on to Part 3 of this book, where we will finish building our Wordz application.
Line 424: 
Line 425: --- 페이지 234 ---
Line 426: Questions and answers
Line 427: 211
Line 428: Questions and answers
Line 429: The following are some questions and answers regarding this chapter’s content:
Line 430: 1.	
Line 431: Have TDD and CI/CD pipelines eliminated the need for manual testing?
Line 432: No. They have changed where the value lies. Some manual processes have become irrelevant, 
Line 433: whereas others have increased in importance. Traditionally, manual steps, such as following test 
Line 434: documents for feature testing and regression testing, are no longer required. Running feature 
Line 435: and regression tests has changed from writing test plans in a word processor to writing test 
Line 436: code in an IDE. But for many human-centric tasks, having a human mind in the loop remains 
Line 437: vital to success.
Line 438: 2.	
Line 439: Will artificial intelligence (AI) automate away the remaining tasks?
Line 440: This is unknown. Advances in AI at this time (the early 2020s) can probably improve visual 
Line 441: identification and static code analysis. It is conceivable that AI image analysis may one day be 
Line 442: able to provide a good/bad analysis of usability – but that is pure speculation, based on AI’s 
Line 443: abilities to generate artworks today. Such a thing may remain impossible. In terms of practical 
Line 444: advice now, assume that the recommended manual processes in this chapter will remain 
Line 445: manual for some time.
Line 446: Further reading
Line 447: To learn more about the topics that were covered in this chapter, take a look at the following resources:
Line 448: •	 https://dl.acm.org/doi/pdf/10.1145/274567.274574:
Line 449: An overview of the modern genesis of TDD by Kent Beck. While the ideas certainly predate 
Line 450: this project, this is the central reference of modern TDD practice. This paper contains many 
Line 451: important insights into software development and teams – including the quote make it run, make 
Line 452: it right, make it fast, and the need to not feel like we are working all the time. Well worth reading.
Line 453: •	 Explore It, Elizabeth Hendrickson, ISBN 978-1937785024.
Line 454: •	 https://trunkbaseddevelopment.com/.
Line 455: •	 https://martinfowler.com/articles/feature-toggles.html.
Line 456: •	 Inspired: How to create tech products customers love, Marty Cagan, ISBN 978-1119387503:
Line 457: An interesting book that talks about product management. While this may seem strange in a 
Line 458: developer book on TDD, a lot of the ideas in this chapter came from developer experience in 
Line 459: a dual-track agile project, following this book. Dual agile means that fast feedback loops on 
Line 460: feature discovery feed into fast feedback agile/TDD delivery. Essentially, manual TDD is done 
Line 461: at the product requirements level. This book is an interesting read regarding modern product 
Line 462: management, which has adopted the principles of TDD for rapid validation of assumptions 
Line 463: about user features. Many ideas in this chapter aim to improve the software at the product level.
Line 464: 
Line 465: --- 페이지 235 ---