Line 1: 
Line 2: --- 페이지 46 ---
Line 3: Chapter 3 
Line 4: Testing Strategy 
Line 5: “How do I test thee? Let me count the ways.”
Line 6: Elizabeth Barrett Browning (altered) 
Line 7: The different types of testing that occur during development are explained to 
Line 8: give the context in which acceptance tests are developed. The tests that the cus-
Line 9: tomer provides are only one part of the testing process. 
Line 10: Types of Tests 
Line 11: Acceptance tests are one part of the testing strategy for a program. The easiest 
Line 12: way to describe the full set of tests for an application is to use the testing matrix 
Line 13: from Gerard Meszaros [Meszaros01]. The matrix in Figure 3.1 shows how ac-
Line 14: ceptance tests ﬁt into the overall picture. 
Line 15: Customer tests encompass the business facing functional tests that ensure the 
Line 16: product is acceptable to the customer. These functional tests are the acceptance 
Line 17: tests described in this book. The result of almost every acceptance test can be 
Line 18: expressed in yes or no terms. Examples are, “When a customer places an order 
Line 19: of $100, does the system give a 5% discount?” and, “Is the Edit button disabled 
Line 20: if the account is inactive?” 
Line 21: As shown in lower right of the matrix, there are other requirements for a soft-
Line 22: ware system checked by the property tests. These include nonfunctional require-
Line 23: ments (often called the ilities or quality attributes) such as scalability, reliability, 
Line 24: security, and performance. 1 Some of the tests for these requirements can be 
Line 25: expressed in questions with yes or no answers. For example, “If there are 100 
Line 26: 23
Line 27:   1 . Some people separate performance (and security for that matter) because it does not 
Line 28: end in ility.
Line 29: 
Line 30: --- 페이지 47 ---
Line 31: Chapter 3 Testing Strategy
Line 32: 24
Line 33: users on the system and they are placing orders at the same time, does the system 
Line 34: respond to each one of them in less than 5 seconds?” However, for other quality 
Line 35: attributes, the question can be asked, but the answer is unknowable, such as, “Is 
Line 36: the system secure from all threats?” For the user to accept the system, the sys-
Line 37: tem needs to pass these nonfunctional tests. So the property tests are sometimes 
Line 38: referred to as nonfunctional acceptance tests.
Line 39: Usability tests are in a separate category. You might create some factual tests, 
Line 40: such as, “Given a certain level of user, can he pay for an order in less than 30 
Line 41: seconds?” or, “Given 100 users ranking the system usability on a scale from 
Line 42: 1 to 10, is the average greater than 8?” But often, usability is more subjective: 
Line 43: “Does this screen feel right to me?” or, “Does this workﬂow match the way I do 
Line 44: things?” Usability testing is strictly manual. No robot program can measure the 
Line 45: usability of a system. Often the customer is of the mind, “I’m not sure what I’d 
Line 46: like, but I’ll know it when I see it.” It’s difﬁcult to write a test for that [Constan-
Line 47: tine01], [Nielsen01], [Aston01]. 
Line 48: Exploratory tests are tests whose ﬂow is not described in advance [Petti-
Line 49: chord01]. An exploratory tester does parallel test design, execution, result inter-
Line 50: pretation, and learning. Exploratory testing may disclose defects undiscovered 
Line 51: by other forms of testing [Whittaker01], [Bach01]. 
Line 52: The term has also been applied to a situation in which all team members—
Line 53: Tom, Cathy, and Debbie—take on the persona of a user and go through the 
Line 54: Customer
Line 55: Tests
Line 56: Business Intent
Line 57: (Executable  Specification)
Line 58: Unit
Line 59: Tests
Line 60: Developer Intent
Line 61: (Design of the Code)
Line 62: Property
Line 63: Testing
Line 64: Is it responsive,
Line 65: secure, scalable?
Line 66: Manual
Line 67: Technology
Line 68: Facing
Line 69: Business
Line 70: Facing
Line 71: Support
Line 72: Development
Line 73: Critique
Line 74: Product
Line 75: Purpose of Tests
Line 76: Component
Line 77: Tests
Line 78: Architect Intent
Line 79: (Design of the System)
Line 80: Manual
Line 81: Per Functionality 
Line 82: Cross-Functional
Line 83: Kind of Behavior
Line 84: Diagram adapted
Line 85: from Mary
Line 86: Poppendieck and
Line 87: Brian Marick
Line 88: Automated
Line 89: various
Line 90: Automated
Line 91: xUnit
Line 92: Special-Purpose
Line 93: Tool-Based
Line 94: Automated
Line 95: xUnit
Line 96: Usability
Line 97: Testing
Line 98: Exploratory
Line 99: Testing
Line 100: Is it pleasurable?
Line 101: Is it self-consistent?
Line 102: Figure 3.1 The Testing Matrix (Source: Meszaros, Xunit Test Patterns: Refactoring 
Line 103: Test Code, Fig 6.1 “Purpose of Tests” p. 51, © 2007 Pearson Education, Inc. Repro-
Line 104: duced by permission of Pearson Education, Inc.) 
Line 105: 
Line 106: --- 페이지 48 ---
Line 107: Where Tests Run 
Line 108: 25
Line 109: system based on the needs and abilities of that user. Because a system has to be 
Line 110: working to be explored, these tests cannot be created up front. But they can be 
Line 111: performed whenever the program is in a working condition. 
Line 112: Unit tests are created by Debbie and other developers in conjunction with 
Line 113: writing code. They aid in creating a design that is testable, a measure of high 
Line 114: technical quality. Unit tests also serve as documentation for the way the internal 
Line 115: code works. 
Line 116: Component tests verify that units and combinations of units work together 
Line 117: to perform the desired operations. As we will see later, many of the unit and 
Line 118: component tests are derived from the acceptance tests [Wiki03]. 
Line 119: All types of testing are important to ensure delivery of a quality product. 2
Line 120: This book discusses mainly acceptance tests—the functional tests that involve 
Line 121: collaboration between the business customer, the developer, and the tester. 
Line 122: Where Tests Run 
Line 123: Acceptance tests, as deﬁned in this book, can be run on multiple platforms at 
Line 124: multiple times. An example of some of the platforms is shown in Figure 3.2.
Line 125: Debbie runs unit tests on her machine. She can also run many acceptance tests, 
Line 126: particularly if they don’t require external resources. For example, any business 
Line 127: rule test can usually run on her machine. In some instances, she may create test 
Line 128: doubles for external resources to avoid having tests depend on them. The topic 
Line 129: of test doubles will be covered in Chapter 11, “System Boundary.” 
Line 130: On a larger project, Debbie and the other developers would merge their code 
Line 131: to a build or integration platform. The unit tests of all the developers would be 
Line 132: run on this platform to make sure that the changes one developer makes in his 
Line 133: code would not affect the changes that other developers make. The acceptance 
Line 134: tests would be run on this platform if the external resources or their test doubles 
Line 135: are available. In Sam’s project, Debbie’s machine acts as both the developer 
Line 136: platform and the integration platform because she has no other developers on 
Line 137: the project. 
Line 138: Once all tests pass on the build/integration platform, the application is 
Line 139: deployed to the test platform. On this platform, the full external resources, such 
Line 140: as a working database, are available. All types of tests can be run here. But often 
Line 141: the unit tests are not run, particularly if the application is deployed as a whole 
Line 142: and not rebuilt for the test platform. 
Line 143: Cathy, the customer, and other users try out the user interface to see how 
Line 144: well it works. Tom can do some exploratory testing. If this were a system that 
Line 145:   2 . See [Crispin02] for a discussion of how to implement the other testing types. 
Line 146: 
Line 147: --- 페이지 49 ---
Line 148: Chapter 3 Testing Strategy
Line 149: 26
Line 150: required it, the security testers and the performance testers could have their ﬁrst 
Line 151: go at the application. 
Line 152: Once the customer is satisﬁed with the outcome of all tests, the application 
Line 153: is deployed to the production platform. There is still a possibility that bugs 
Line 154: may show up. Users may do entirely unexpected things, or there may be some 
Line 155: conﬁguration that causes problems for the application. Debbie and Tom have 
Line 156: a measure of quality that is the number of bugs in production. They are called 
Line 157: escaped bugs because they escaped discovery from all other testing. 
Line 158: Test Facets 
Line 159: Figure 3.3 shows examples of positive and negative testing. Positive tests ensure 
Line 160: that the program works as expected. Negative testing checks to see that the 
Line 161: program does not create unexpected results. Acceptance tests that the customer 
Line 162: thinks about are mostly in the “Speciﬁed Effect” box. The ones that Tom and 
Line 163: Developer’s
Line 164: Platform
Line 165: Build /
Line 166: Integration
Line 167: Platform
Line 168: Test Platform
Line 169: Property Tests
Line 170: Exploratory
Line 171: Tests
Line 172: Unit
Line 173: Tests
Line 174: Acceptance Tests
Line 175: (Customer
Line 176: Tests)
Line 177: Component
Line 178: Tests
Line 179: Usability
Line 180: Tests
Line 181: Figure 3.2 Where Tests Run 
Line 182: 
Line 183: --- 페이지 50 ---
Line 184: Test Facets 
Line 185: 27
Line 186: Debbie come up with are in the other three boxes. Tom, as the tester, has a par-
Line 187: ticular focus on ﬁnding unexpected results. 
Line 188: Valid Input
Line 189: Invalid Input
Line 190: Expected Result
Line 191: Specified effect
Line 192: Any effects
Line 193: Specified error handling
Line 194: Unspecified effect
Line 195: Unexpected Result
Line 196: Figure 3.3 Positive and Negative Testing 
Line 197: Control and Observation Points 
Line 198: Tests are often run from the external view of the system. Bret Pettichord talks 
Line 199: about control points and observation points [Pettichord01]. A control point is 
Line 200: the part of the system where the tester inputs values or commands to the system. 
Line 201: The observation point is where the system response is checked to see that it is 
Line 202: performing properly. Often the control point is the user interface and the output 
Line 203: is observed on the user interface, a printed report, or a connection to an external 
Line 204: platform. As seen in the next chapter, it is often easier to run many tests if you 
Line 205: have control and observation points within the system. 
Line 206: New Test Is a New Requirement 
Line 207: Requirements and tests are linked. You can’t have one without the other. They 
Line 208: are like Abbott and Costello, Calvin and Hobbes, nuts and bolts, or another 
Line 209: favorite duo. The tests clarify and amplify the requirements [Melnik01]. A test 
Line 210: that fails shows that the system does not properly implement a requirement. A 
Line 211: test that passes is a speciﬁcation of how the system works. Any test created after 
Line 212: the code is written is a new requirement or a new detail on an existing require-
Line 213: ment.3
Line 214: If Cathy comes across a new detail after Debbie has implemented the code, 
Line 215: the triad needs to create a new test for that detail. For example, suppose there 
Line 216: is an input ﬁeld that doesn’t have limits on what can go in it. Then Cathy real-
Line 217: izes that there needs to be a limit. The triad would create tests to ensure that 
Line 218: the limit is checked on input. The requirement that there is a limit and the tests 
Line 219: that ensure it is checked are linked. Because the tests did not exist before Debbie 
Line 220: ﬁnished the code, it is not a developer bug that the limit was not checked. It is 
Line 221: 3. Thanks to Scott Bain and Amir Kolsky for the discussion where this idea occurred. 
Line 222: 
Line 223: --- 페이지 51 ---
Line 224: Chapter 3 Testing Strategy
Line 225: 28
Line 226: just a new requirement that needs to be implemented. Some people might call 
Line 227: it an analysis bug or a missed requirement. Or you can simply say, “You can’t 
Line 228: think of everything” and call it a new requirement. 
Line 229: Summary
Line 230: •  Testing areas include 
Line 231: • Acceptance tests that are business-facing functionality tests 
Line 232: • Tests that check component and module functionality 
Line 233: • Unit tests that developers use to drive the design 
Line 234: • Usability, exploratory, and quality attribute (reliability, scalability, 
Line 235: performance)
Line 236: • Functionality tests should be run frequently on developer, build/
Line 237: integration, and test platforms. 
Line 238: • Tests and requirements are linked together. 