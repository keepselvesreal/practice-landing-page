Line 1: 
Line 2: --- 페이지 232 ---
Line 3: Chapter 25 
Line 4: Retrospective and Perspective 
Line 5: “There are those who look at things the way they are, and ask why... I 
Line 6: dream of things that never were, and ask why not?”
Line 7: Robert Kennedy 
Line 8: We’ve looked at acceptance tests from many different viewpoints. Here is a look 
Line 9: back at of some of the salient points and a look-forward to see how you can 
Line 10: apply it. 
Line 11: Recap
Line 12:  
Line 13: Now that the details of acceptance testing have been explored, it’s time for a 
Line 14: recap of how acceptance testing ﬁts into the overall development process, as well 
Line 15: as a few overall facets. The tale in this book of Debbie the developer, Tom the 
Line 16: tester, and Cathy the customer has been a narrative one, with the goals and ben-
Line 17: eﬁts of acceptance test-driven development (ATDD) woven in. ATDD is a com-
Line 18: munication tool between the customer, developer, and tester. It is about writing 
Line 19: the right code (fulﬁlling the requirements), rather than writing the code right 
Line 20: (design of the implementation). To summarize, the primary goals are as follows: 
Line 21: • Discover ambiguous requirements and gaps in requirements early on. 
Line 22: • Create a record of business/development understanding. 
Line 23: • Give feedback on quality. 
Line 24: 209
Line 25: 
Line 26: --- 페이지 233 ---
Line 27: Chapter 25 Retrospective and Perspective
Line 28: 210
Line 29: The secondary goals are these: 
Line 30: • Use acceptance tests as an executable regression test. 
Line 31: • Measure your progress toward completeness. 
Line 32: • Measure the complexity of requirements. 
Line 33: • Use the tests as a basis for user documentation. 
Line 34: Passing the functional acceptance tests is necessary, but it’s insufﬁcient for 
Line 35: verifying a system. The system must pass other tests, such as those for quality 
Line 36: attributes (performance and reliability) and usability. 
Line 37: The Process 
Line 38: The project started with a charter that included objectives—acceptance tests 
Line 39: for the whole project. Features with acceptance criteria were developed. The 
Line 40: features gave an overall picture of what the system was going to do. Then the 
Line 41: features were broken into stories, each with its own acceptance criteria. The sto-
Line 42: ries were detailed in use cases or alternatively in event/response tables. Speciﬁc 
Line 43: acceptance tests were written for the scenarios in the use cases, for individual 
Line 44: events, or for individual state transitions. Workﬂow tests could be created that 
Line 45: exercised more than a single use case. 
Line 46: Testing Layers 
Line 47: Acceptance tests, as used in this book, are customer-deﬁned tests created prior 
Line 48: to implementation. You can use many of these acceptance tests at multiple levels 
Line 49: both as implementation validation tests and design veriﬁcation tests. For exam-
Line 50: ple, you can run the check-out and check-in tests as follows: 
Line 51: • Run manually as full integration tests through the user interface. The rent-
Line 52: al contract values are checked on the printer output, and the credit charge 
Line 53: output is checked on the bank statement. 
Line 54: • Used as the basis for usability tests. As a user runs the test, he may see how 
Line 55: usable the system is. 
Line 56: • Run beneath the user interface with real databases in an almost-full inte-
Line 57: gration test. 
Line 58: • Run with an in-memory database to run faster in a partial integration test. 
Line 59: • Run automatically as regression tests. 
Line 60: 
Line 61: --- 페이지 234 ---
Line 62: Recap 
Line 63: 211
Line 64: As another example, an almost-complete integration test might use a mock 
Line 65: mail server to which it sends mail. A complete integration test involves using 
Line 66: a real mail server (and appropriate e-mail addresses so that the tests aren’t a 
Line 67: source of spam). 
Line 68: The information in the acceptance tests provides information to all the 
Line 69: developers in a project. For example, the ﬂow associated with the tests and 
Line 70: the actions performed give a framework that the user interface developers can 
Line 71: employ in designing the user experience. The database developers can design the 
Line 72: database structure based on the relationships between data, as shown in rows 
Line 73: and columns of the tests. 
Line 74: The Tests 
Line 75: Acceptance tests are customer-understood tests. They come from user stories, 
Line 76: business rules, or event/response tables. They exercise different scenarios in use 
Line 77: cases—the happy path and every exception path. A passing acceptance test is 
Line 78: a speciﬁcation of how the system works. A  failing acceptance test is a require-
Line 79: ment that the system has not yet implemented. Initially, all acceptance tests for 
Line 80: a new system should fail. Otherwise, the system is already doing what has been 
Line 81: requested. An acceptance test failure may not help diagnose what caused the 
Line 82: problem. It simply indicates that there is a problem. 
Line 83: Unit tests are employed by the developers to help maintain and design the 
Line 84: implementation. A developer can use the acceptance tests as a basis for develop-
Line 85: ing unit tests. If there is a test at the outer layer, some module inside must help to 
Line 86: pass that test. The unit tests can diagnose where the problem exists that causes 
Line 87: a failing acceptance test. 
Line 88: Architects or developers create component or module tests. These tests work 
Line 89: as internal acceptance tests to ensure that the individual pieces of a system cor-
Line 90: rectly perform their responsibilities. 
Line 91: Acceptance tests suggest ways that a system might be controlled or observed 
Line 92: at levels lower than the user interface. For example, a business rule test may 
Line 93: connect directly with a module that implements it. A data lookup test may go 
Line 94: to a data access layer to retrieve information to ensure that the data has been 
Line 95: properly stored. Many tests are round-trip on the same layer. For example, they 
Line 96: perform actions on the middle tier and check the results at the middle-tier level. 
Line 97: Other acceptance tests may cross layers, such as input through the user interface 
Line 98: layer and output checking from the data access layer. Having an implementa-
Line 99: tion required to meet the needs of acceptance tests for inputs and outputs makes 
Line 100: the system more testable. The proof of testability is that a system can be tested. 
Line 101: If the system provides a way to run the acceptance tests, the system is testable. 
Line 102: Implementing an acceptance test may require additional output that is not 
Line 103: part of the set of requirements. For example, a CD status report might show the 
Line 104: 
Line 105: --- 페이지 235 ---
Line 106: Chapter 25 Retrospective and Perspective
Line 107: 212
Line 108: status of every CD (rented or not rented). Such a report could be used to view 
Line 109: the results of a check-out or check-in test. Bret Pettichord calls the additional 
Line 110: control points and reporting points touch-points in the code [Pettichord01]. 
Line 111: Communication
Line 112: There are two points to remember about communication: 
Line 113: •  Acceptance tests are not a substitute for interactive communication. 
Line 114: •  Acceptance tests can provide focus for that communication. 
Line 115: What’s the Block? 
Line 116: Each member of the triad has read this book on ATDD. Okay, one hasn’t. 
Line 117: That’s a block. You need to be on the same page to collaborate. Just one party 
Line 118: such as the developer raving about how wonderful ATDD is may not help with 
Line 119: the change. All members of the triad have to realize the beneﬁts of ATDD and 
Line 120: be in a position to implement it. 
Line 121: Often, customers feel they do not have the knowledge to give the speciﬁcs 
Line 122: necessary for the tests. They do not have to have all the information. The people 
Line 123: who have it need to be identiﬁed and brought into the collaboration process. 
Line 124: Customers may not have the time, or they may not be used to working at the 
Line 125: level of precision that acceptance tests require. Once again, they need to identify 
Line 126: someone—such as a business analyst or subject matter expert—who has the 
Line 127: time and can work at that level of precision. Just because the triad includes the 
Line 128: customer doesn’t mean that she has to be present; her designated representative 
Line 129: with the authority to make decisions can ﬁll the chair. 
Line 130: Monad
Line 131: Are you a monad? You get requirements without tests. You have no commu-
Line 132: nication with the customer. You have no tester to help you. If you have no ac-
Line 133: ceptance tests, you have no requirements. Why are you writing code if there are 
Line 134: no requirements? If the situation is such that it is absolutely necessary to start 
Line 135: developing, write the acceptance tests from what you understand the require-
Line 136: ments to be, and code to them. 
Line 137: 
Line 138: --- 페이지 236 ---
Line 139: What’s the Block? 
Line 140: 213
Line 141: Unavailable Customer 
Line 142: The customer says, “Go away and work. I’ve given you all the information.” 
Line 143: Now if it’s an internal customer, you can appeal to shareholder ﬁduciary re-
Line 144: sponsibility. You waste shareholder resources if you create a program that does 
Line 145: not provide business value or one that does not meet the real needs of the cus-
Line 146: tomer. Don’t work on that project until the customer provides speciﬁc accept-
Line 147: ance tests. If you are assigned to two projects, work on the other project or 
Line 148: spend some time learning a new skill. Alternatively, you can investigate who 
Line 149: else has the subject matter expertise to create the tests and request that person 
Line 150: be assigned to the project. 
Line 151: If it’s an external customer, be sure you are on a time-and-materials basis, not 
Line 152: ﬁxed price. You may make money in reworking the implementation of unclear 
Line 153: requirements, but you may get an unsatisﬁed customer who never comes back. 
Line 154: Change
Line 155: Virginia Satir [Satir01] developed a change model that describes how people 
Line 156: adapt to change. When a foreign element, such as ATDD, is introduced into 
Line 157: an organization, it upsets the status quo, which may cause chaos. Chaos comes 
Line 158: from the change in peoples’ roles. The customer unit is more involved with 
Line 159: providing examples. Testers create tests for an application that has not yet been 
Line 160: written instead of seeing a user interface. Developers test more. 
Line 161: Exiting the chaos comes from a transforming idea—“a sudden awareness of 
Line 162: and understanding of new possibilities.” In this book, you’ve seen examples of 
Line 163: the possibilities for ATDD. When you integrate the practice of ATDD into your 
Line 164: process, you will be in a new status quo—a more effective software development 
Line 165: organization. How to exit the chaos involves many aspects that are covered in 
Line 166: [Rising01].1
Line 167:   1.  See [Koskela02] and [Adzic01] for other change issues. 
Line 168: What Will It Take? 
Line 169: I was teaching a course a few years ago on being lean and agile. I always 
Line 170: ask why the students are in the course and what their backgrounds are. 
Line 171: One student said that he had completed an agile project. The customer 
Line 172: was more satisﬁed than with previous waterfall projects. The project was 
Line 173: completed under budget and in less time. He wanted more ammunition he 
Line 174: could present to management as to why the company should do another 
Line 175: agile project. I said that the points he raised were the best shot. I could give 
Line 176: conﬁrming information, but if someone isn’t satisﬁed with those results, 
Line 177: I’m not sure I could convince him otherwise. 
Line 178: 
Line 179: --- 페이지 237 ---
Line 180: Chapter 25 Retrospective and Perspective
Line 181: 214
Line 182: Risks
Line 183: There are risks associated with acceptance tests—particularly automated accept-
Line 184: ance testing. Tests require maintenance, and changing requirements cause tests 
Line 185: to break. If the number of broken tests is large, there may not be time to ﬁx all 
Line 186: of them before a release. If the broken tests are not ﬁxed, their failure may start 
Line 187: to be ignored or signal that it’s okay to have a broken test. (See Broken Window 
Line 188: Syndrome [Wiki10].) 
Line 189: ATDD veriﬁes that a system delivers what the requirements and tests specify. 
Line 190: It does not validate that the system is actually what the user needs. Having the 
Line 191: user, such as Cary, the clerk, is involved in the development process can reduce 
Line 192: the issues in delivering a useful system. 
Line 193: Beneﬁts 
Line 194: A common complaint against acceptance testing is that it’s too expensive. If 
Line 195: you are going to test something and document these tests, it costs no more to 
Line 196: document the tests up front than it does to document them at the end. Adding 
Line 197: automation to the tests up front does add a little bit of work, but it can pay off 
Line 198: in reduced time for changes and the courage to refactor code to make it more 
Line 199: maintainable.
Line 200: What have been the results of ATDD? The Epilogue contains success stories 
Line 201: from teams that have adopted ATDD. These stories give concrete examples of 
Line 202: how ATDD improves quality, maintainability, and the development process in 
Line 203: general.
Line 204: ATDD produces improved quality as the triad gains a better awareness 
Line 205: of the system. Creating the tests forces the conversation of what the system 
Line 206: should do. The translation errors between requirements and implementation 
Line 207: are reduced because the tests form the common understanding between them. 
Line 208: Thinking through scenarios for tests identiﬁes unclear requirements and can 
Line 209: identify where cases might have been missed. There is a reduced risk of deliver-
Line 210: ing a system that does not meet the requirements, because it is not delivered until 
Line 211: it passes all the tests. 
Line 212: ATDD can create a more maintainable system. The terms used in the test 
Line 213: form a common language between customers and developers/testers. If the same 
Line 214: terms are followed in the implementation, it can be easier to understand the rela-
Line 215: tionship of the code to the requirement. Writing the tests acts as a domain mod-
Line 216: eling process. The relationships between the entities are captured in the tests. 
Line 217: Having the tests prior to implementation requires the code to pass those tests. 
Line 218: In the process, the code becomes more testable. The tests document how the 
Line 219: system works. Developer acceptance tests specify how a module works. Because 
Line 220: 
Line 221: --- 페이지 238 ---
Line 222: Summary 
Line 223: 215
Line 224: passing the tests shows how the system or module works, the tests are execut-
Line 225: able speciﬁcations that, if run, will not become outdated. 
Line 226: In development, the tests provide a focus on what the developers should 
Line 227: implement. They write the code that needs to be written to pass a test. If the 
Line 228: code is not executed by a test, why is the code present? 
Line 229: Summary
Line 230: •  ATDD makes a system testable, which drives it to be of higher quality. 
Line 231: •  The bottom line is that ATDD provides beneﬁts to an organization. 
Line 232: 
Line 233: --- 페이지 239 ---
Line 234: This page intentionally left blank 