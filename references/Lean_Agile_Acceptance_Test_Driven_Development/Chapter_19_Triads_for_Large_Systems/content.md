Line 1: 
Line 2: --- 페이지 190 ---
Line 3: Chapter 19 
Line 4: Triads for Large Systems 
Line 5: “It always takes longer than you expect, even if you take Hofstadter’s Law 
Line 6: into account.”
Line 7: Douglas Hofstadter 
Line 8: This chapter shows how larger systems can have more and different triads. Some 
Line 9: projects do not require new customer acceptance tests. This chapter also exam-
Line 10: ines a lack of acceptance tests. 
Line 11: Large Systems 
Line 12: Sam’s system had just two people, Debbie and Tom, as developer and tester. 
Line 13: Debbie was an omnipotent developer. She did everything from creating the over-
Line 14: all architecture to designing the user interface to administering the database. 
Line 15: Tom did all sorts of testing, from helping with acceptance test development to 
Line 16: running performance testing tools to checking usability and performing explora-
Line 17: tory testing. Teams for larger projects are sometimes composed of such ambi-
Line 18: dextrous individuals. But often the range of technology involved and the scope 
Line 19: of the project do not allow individuals to cover the entire gamut of development 
Line 20: and testing. Nor does a single customer, such as Cathy, know every detail about 
Line 21: what needs to go into the system. Subject matter experts specify the require-
Line 22: ments in their own particular area of expertise. 
Line 23: The triad still exists, just with different people. It becomes the subject matter 
Line 24: expert, the developer (or developers if you are doing pair programming), and 
Line 25: the functional tester (or people whose focus is one of these roles). They develop 
Line 26: acceptance tests for the particular stories or requirements with which the expert 
Line 27: is familiar. 
Line 28: For projects with larger implementations, teams often have an architect or 
Line 29: technical lead focus on the overall structure of a system to keep it consistent 
Line 30: 167
Line 31: 
Line 32: --- 페이지 191 ---
Line 33: Chapter 19 Triads for Large Systems
Line 34: 168
Line 35: with other systems. The system may encompass a single application or multiple 
Line 36: applications.
Line 37: For teams like this, you have another triad: the architect, developer, and 
Line 38: tester (see Figure 19.1). The architect, Al, helps the developer unit make design 
Line 39: decisions that are consistent with the larger picture. The three work together to 
Line 40: determine a system’s modules and their interrelationships. The responsibilities 
Line 41: of each module are speciﬁed with acceptance tests, like the ones Debbie created 
Line 42: in Chapter 16, “Developer Acceptance Tests.” The triad develops these tests 
Line 43: collaboratively. Because all involved people are of a technical bent, the tests may 
Line 44: incorporate many non-customer-related terms. But everyone in the triad needs 
Line 45: to understand the terms and their implications. 
Line 46: Al
Line 47: the
Line 48: Architect
Line 49: Tom
Line 50: the
Line 51: Tester
Line 52: Debbie
Line 53: the
Line 54: Developer
Line 55: Figure 19.1 The Technical Triad 
Line 56: Some tests for the modules are derived from the customer acceptance tests, 
Line 57: just as unit tests are derived from them. The process of deciding how many mod-
Line 58: ules are required and which modules are responsible for fulﬁlling which parts 
Line 59: of the acceptance tests is a major facet of the architectural design process. This 
Line 60: process is covered in other books, such as [Fowler01]. 
Line 61: One key that the team should focus on is getting an end-to-end system work-
Line 62: ing soon after the start of the project. One customer acceptance test should be 
Line 63: demonstrated on the entire system. The feedback from the ease or non-ease of 
Line 64: developing for that test can yield helpful information to the triad as to whether 
Line 65: a particular architecture is suitable for the project. It also gives a baseline against 
Line 66: which to measure additions. When a new story is implemented, a customer 
Line 67: acceptance test may fail because an implementation changed its behavior. If the 
Line 68: behavior represented by the test is still required, the triad can review and pos-
Line 69: sibly revise the architecture. This is before much work has been spent writing 
Line 70: code dependent on the architecture. 
Line 71: 
Line 72: --- 페이지 192 ---
Line 73: When a Customer Test May Not Be Required 
Line 74: 169
Line 75: With larger systems, you may have a database architect, Dana. Dana creates 
Line 76: the persistent storage that multiple applications require. She ensures that there is 
Line 77: no redundancy of information, such as storing a customer’s address in two dif-
Line 78: ferent places. A different triad—the developer, the tester, and Dana (see Figure
Line 79: 19.2)—works to ensure that the developer has a way to make persistent all the 
Line 80: information needed to solve the story that the developer is working on. This col-
Line 81: laboration operates the same way as the customer-developer-tester triad. Debbie 
Line 82: states what she needs and creates an acceptance test. Dana delivers the persist-
Line 83: ence methods required. Tom may suggest additional tests. Again, the three peo-
Line 84: ple in the triad may not have these titles; they are just the roles they play. 
Line 85: Debbie
Line 86: the
Line 87: Developer
Line 88: Tom
Line 89: the
Line 90: Tester
Line 91: Dana
Line 92: the
Line 93: Database
Line 94: Architect
Line 95: Figure 19.2 Another Technical Triad 
Line 96: As we have seen, the triad concept can work all the way up and down the 
Line 97: chain, from an overall software application down to the individual modules. The 
Line 98: triad consists of the requester, the implementer, and the tester who ensures that 
Line 99: all bases are covered. The triad is meant as a minimum for the number of people 
Line 100: in collaboration. You may have a quad, a penta, or a larger group as required. 
Line 101: However, it is often the case that the larger the group, the less members interact 
Line 102: and the less effective they are. So limit the number to those actually required 
Line 103: rather than those who just have a possible “want to know what’s happening.” 
Line 104: When a Customer Test May Not Be Required 
Line 105: Sam’s business is booming. He now rents not just CDs, but electronic books, 
Line 106: videos, and games. He has bought up a number of competitors. So now Al, 
Line 107: the architect, has the work of keeping a large set of diverse programs working 
Line 108: together. Al needs to combine systems so that the counter clerks use the same 
Line 109: system if they switch stores. The combination involves taking the data, such as 
Line 110: 
Line 111: --- 페이지 193 ---
Line 112: Chapter 19 Triads for Large Systems
Line 113: 170
Line 114: customers, from one system, and converting it to another. There are projects like 
Line 115: these that may not necessarily involve new customer acceptance tests. 
Line 116: Data Conversion 
Line 117: Al and Dana work together on the data conversion project. This conversion is a 
Line 118: mostly technical project, not a customer project. Al will be the one to write the 
Line 119: acceptance tests for the conversion. He will specify the measures of the cleanli-
Line 120: ness of the conversion. For example, he may create the rules to determine that 
Line 121: a customer who resides on two systems is a duplicate. Al knows that Sam does 
Line 122: not want a customer showing up twice on the converted system. 
Line 123: There may be some business issues, such as differences in customer status 
Line 124: from one system to another. For example, Sam’s business rule for allowing 
Line 125: someone to reserve may be different from the business rule for an acquired 
Line 126: competitor. You can keep track of where a customer came from and incorporate 
Line 127: both rules. But that is Sam’s call. 
Line 128: There should be no new customer acceptance tests, because they have already 
Line 129: been created for the working system. The only exceptions would be tests that 
Line 130: check that the business issues, such as customer status, have been appropriately 
Line 131: handled.
Line 132: Database Conversions 
Line 133: Dana has been informed that there is not going to be support for the current 
Line 134: database version that Sam’s systems use. Dana needs to convert to the next ver-
Line 135: sion, or perhaps to a different system. This is not a customer need, but a tech-
Line 136: nical issue. There are no new customer acceptance tests because the behavior 
Line 137: of the system should not change. All acceptance tests can work as a regression 
Line 138: suite. When the conversion is complete, the tests should still run as before. 
Line 139: If a project involves lots of stories for which there are no customer accept-
Line 140: ance tests, it may well be a technical project. Often, large technical issues such 
Line 141: as database conversion are incorporated into customer-focused projects. The 
Line 142: customer often does not have knowledge of the underlying issues and therefore 
Line 143: has no ability to provide acceptance tests. If this is the case, the technical parts 
Line 144: should be broken into a technical project with a technical lead playing the part 
Line 145: of the customer. Projects such as an upgrade to a new database, a new version of 
Line 146: a language, or a new operating system are technical infrastructure issues. 
Line 147: What If There Are No Tests? 
Line 148: You have a system that has been acquired and for which there are no accept-
Line 149: ance tests: no manual ones, and no automated ones. You need to make some 
Line 150: 
Line 151: --- 페이지 194 ---
Line 152: What If There Are No Tests? 
Line 153: 171
Line 154: changes, but what can you do? Let’s look at a couple of conditions. In one, you 
Line 155: may acquire the system from a vendor; in the other, you may inherit it from an 
Line 156: acquisition.
Line 157: When you buy a vendor application, it may be conﬁgurable or customizable. 
Line 158: Conﬁgurable means that you set up values to make the application run in your 
Line 159: environment or with your set of data. The logic in the application uses this con-
Line 160: ﬁguration information to alter its operation in predetermined ways. You may 
Line 161: be able to add some additional features, such as a Microsoft Word macro, but 
Line 162: these macros use existing operations. Because the vendor should have tested all 
Line 163: operations, having acceptance tests is less critical. 
Line 164: Customizable means that you are provided with some source code for the 
Line 165: system that you alter to make a system work for your particular purpose. The 
Line 166: code provides some existing behavior that you are changing. In this case, you 
Line 167: should ask the vendor for acceptance tests—either manual or automatic. The 
Line 168: vendor response might be as follows: 1
Line 169: • Don’t have any 
Line 170: • Have some, but all manual 
Line 171: • Have full set, but all manual 
Line 172: • Have full set: some manual, some automated 
Line 173: • Have full set, completely automated 
Line 174: If a vendor doesn’t have a full set, ask him how he knows the system works. 
Line 175: It could be that he has a full set, but contractually he is not required to provide 
Line 176: them to you. If you can’t ﬁnd another vendor that will provide acceptance tests, 
Line 177: you are in the same situation as from an acquisition. 
Line 178: You have to change an acquired system that has few or no acceptance tests 
Line 179: in the area that you want to change. Chances are that the system has not been 
Line 180: designed to be tested [Feathers01]. 
Line 181: First, create acceptance tests for the functionality you are going to change. 
Line 182: Inject the tests beneath the user interface if you can. Otherwise, run the tests 
Line 183: through the user interface, and automate the tests if possible. Every test should 
Line 184: pass as it documents the current working of the system. These tests will now run 
Line 185: as a regression test. Create an acceptance test for the change you are going to 
Line 186: make. Determine which of the current tests, if any, should fail once the change 
Line 187: is made. Then implement the change and test. 
Line 188: 1. There are some gray areas that might be considered either conﬁgurable or
Line 189: customizable.
Line 190: 
Line 191: --- 페이지 195 ---
Line 192: Chapter 19 Triads for Large Systems
Line 193: 172
Line 194: Legacy Systems 
Line 195: One common issue with legacy systems is the lack of tests: both external accept-
Line 196: ance tests and internal unit tests. 2 And often when there are external acceptance 
Line 197: tests, they are not automated. Making changes in the system and ensuring that 
Line 198: the changes do not have unintended effects is difﬁcult. 
Line 199: Just as for an acquired system without tests, before making a change, cre-
Line 200: ate acceptance tests around the portion of the system that is involved with the 
Line 201: change. The acceptance tests document how the system currently works. You 
Line 202: sometimes have more control over legacy systems, then those acquired from a 
Line 203: vendor. So the acceptance tests you write may be able to be run beneath the user 
Line 204: interface.
Line 205: Then write acceptance tests for how the system should work once the change 
Line 206: is implemented. Initially, they should fail. Otherwise, the system is already doing 
Line 207: what the change request asks for. The feature was just not documented. 
Line 208: In many instances, you may have to write the tests as user interface tests. If 
Line 209: it’s possible, automate these tests. If the system design allows it, write the tests to 
Line 210: the middle-tier layer and automate them. Then proceed with the change. When 
Line 211: your new tests pass and any identiﬁed as “should break” fail, the system has 
Line 212: been changed correctly. 
Line 213: Suppose you don’t have tests around every functional piece of the system. 
Line 214: With the tests around the part of the system you are changing, you ensure there 
Line 215: are no side effects in that part. But you cannot be sure that the change has not 
Line 216: affected anything else. 
Line 217:   2.  Michael’s Feather’s deﬁnition of a legacy code is anything without tests 
Line 218: [Feathers01].
Line 219: Lack of Acceptance Tests Is a Debt 
Line 220: An acquaintance of mine asked me to estimate the cost of converting a web 
Line 221: application from a commercial application server to an open-source one 
Line 222: to save licensing fees. The application had been coded by a third party. I 
Line 223: examined the code and determined that there were only a very few vendor-
Line 224: speciﬁc methods that would need to be changed. I gave him the estimate, 
Line 225: and he said it seemed reasonable. 
Line 226: I said that the estimate did not include ﬁxing bugs that currently existed in 
Line 227: the system. He agreed to that. I suggested that my responsibility would be 
Line 228: over when the converted system passed all the automated acceptance tests. 
Line 229: He hesitated and replied that there were no automated acceptance tests. 
Line 230: I said then my responsibility would end when the system passed all the 
Line 231: 
Line 232: --- 페이지 196 ---
Line 233: Summary 
Line 234: 173
Line 235: Summary
Line 236: • Larger teams have more triads consisting of the requester, the implementer, 
Line 237: and the tester. 
Line 238: • Focus on getting an end-to-end system passing the simplest tests. 
Line 239: • Some projects are developer related and should have developer-created 
Line 240: acceptance tests. 
Line 241: • If there are no acceptance tests for the portion of a system that needs to 
Line 242: change, create acceptance tests before making the change. 
Line 243: manual acceptance tests. He again paused and acknowledged that there 
Line 244: were no acceptance tests for the system. 
Line 245: I looked at him and stated that I could then have a converted system that 
Line 246: passed all the acceptance tests that afternoon for half the price. He smiled. 
Line 247: I then proposed that I would help develop acceptance tests for the current 
Line 248: system, because his staff did not have time to do so. That was agreed to. 
Line 249: In the end, the total cost of creating the tests and doing the conversion far 
Line 250: exceeded the license fees, so the project never got off the ground. 
Line 251: Projects such as conversions cost more due to the technical debt repre-
Line 252: sented by the lack of acceptance tests. 
Line 253: Manual Testing 
Line 254: In one instance, a legacy system had acceptance tests, but they were severely 
Line 255: out of date. They were mostly manual tests, so they were executed infre-
Line 256: quently (if at all). In addition, the developers could not be sure whether 
Line 257: the results were correct. A situation like this could become a nightmare, 
Line 258: because it appeared that the tests were available, but they really were not. 
Line 259: Sometimes with manual tests, the entire team participates in manual 
Line 260: regression testing. The testers provide scripts, and everyone devotes a day 
Line 261: or two every iteration to testing. This motivates the team to automate the 
Line 262: regression testing. With automation, the tests are run frequently. 
Line 263: 
Line 264: --- 페이지 197 ---
Line 265: This page intentionally left blank 