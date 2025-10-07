Line 1: 
Line 2: --- 페이지 214 ---
Line 3: Chapter 22 
Line 4: Test Evaluation 
Line 5: “Program testing can be a very effective way to show the presence of bugs, 
Line 6: but it is hopelessly inadequate for showing their absence.”
Line 7: Edsger Dijkstra 
Line 8: This chapter describes the characteristics of good tests. These characteristics 
Line 9: include being understandable to customers, not fragile, and test a single concept. 
Line 10: Test Facets 
Line 11: The following discussion of things to look for in tests came partly from Gerard 
Line 12: Meszaros [Meszaros01], Ward Cunningham, and Rick Mugridge [Cunning-
Line 13: ham01]. Overall, remember that the tests represent a shared understanding be-
Line 14: tween the triad. 
Line 15: Understandable to Customers 
Line 16: The test should be written in customer terms (ubiquitous language) ( Chapter 24,
Line 17: “Context and Domain Language”). The tables should represent the application 
Line 18: domain. If the standard tables shown in the examples are not sufﬁcient, cre-
Line 19: ate tables that the user can understand ( Chapter 21, “Test Presentation”). Use 
Line 20: whatever way of expressing the test most closely matches the customer’s way 
Line 21: of looking at things. Try multiple ways to see which way is most suitable to the 
Line 22: customer.
Line 23: The bottom line is to use what is easiest for the customer. If a basic action 
Line 24: table is not as understandable, add graphics to make it look like a dialog box. If 
Line 25: the customer needs something that looks like a printed form to understand the 
Line 26: material, rather than just the data, use that as expected output. You can also 
Line 27: 191
Line 28: 
Line 29: --- 페이지 215 ---
Line 30: Chapter 22 Test Evaluation
Line 31: 192
Line 32: have a simple test for the data to more easily debug what might be wrong with 
Line 33: the printed form ( Chapter 12, “Development Review”). 
Line 34: Unless the customer wants values, use names. For example, use Good and 
Line 35: Excellent as customer types, not customer types 1 and 2. 
Line 36: As presented in this book, acceptance tests are customer-deﬁned tests that are 
Line 37: created prior to implementation (see the book’s Introduction). You can execute 
Line 38: them as unit tests, integration tests, or user interface tests. Make the acceptance 
Line 39: tests written in unit testing frameworks readable, as shown in the example in 
Line 40: Chapter 4, “An Introductory Acceptance Test,” so that you can match them 
Line 41: with the customer’s expectations. 
Line 42: Spell Checked 
Line 43: Spell-check your tests. Tests are meant for communication, and misspelled 
Line 44: words hinder communication. The spell-check dictionary can contain triad-
Line 45: agreed-upon acronyms and abbreviations. Deﬁne these acronyms and abbrevia-
Line 46: tions in a glossary. 
Line 47: Idempotent
Line 48: Tests should be idempotent. They should work the same way all the time. Either 
Line 49: they consistently pass or they consistently fail. A non-idempotent test is erratic; 
Line 50: it does not work the same way all the time. Causes of erratic tests are interact-
Line 51: ing tests that share data and tests for which ﬁrst and following executions are 
Line 52: different because something in the state has changed. Paying attention to setup 
Line 53: (Chapter 31, “Test Setup”) can usually resolve erratic tests. 
Line 54: Not Fragile 
Line 55: Fragile tests are sensitive to changes in the state of the system and with the inter-
Line 56: faces they interact with. The state of the system includes all code in the system 
Line 57: and any internal data repositories. 
Line 58: Handle sensitivity to external interfaces by using test doubles as necessary 
Line 59: (Chapter 11, “System Boundary”). In particular, functionality that depends on 
Line 60: the date or time will most likely need a clock that can be controlled through a 
Line 61: test double. For example, testing an end-of-the-month report may require the 
Line 62: date to be set to the end of the month. Random events should be simulated so 
Line 63: that they occur in the same sequence for testing. 
Line 64: Changes to a common setup can cause a test to fail. If there is something 
Line 65: particular that is required for the test, the test could check for the assumptions it 
Line 66: makes about the condition of the system. If the condition is not satisﬁed, the test 
Line 67: 
Line 68: --- 페이지 216 ---
Line 69: Test Sequence 
Line 70: 193
Line 71: fails in setup, rather than in the conﬁrmation of expected outcome. This makes 
Line 72: it easier to diagnose why the failure occurred. 
Line 73: Tests should only check for the minimum amount of expected results. This 
Line 74: makes them less sensitive to side effects from other tests. 
Line 75: Conﬁrm the Environment 
Line 76: Many programs require that the platform they are installed upon meet a 
Line 77: particular requirement, such as a particular version of an operating sys-
Line 78: tem. When the program is installed, the installation process veriﬁes that 
Line 79: these requirements are met. If they are not, the installation terminates. 
Line 80: This approach is more user friendly than letting a program be installed 
Line 81: and then having the program fail because the environment is wrong. How-
Line 82: ever, the program assumes that the environment does not change after it 
Line 83: is installed. Sometimes the installation of another program changes the 
Line 84: environment and causes the ﬁrst program to fail. 
Line 85: To be less fragile, the program should conﬁrm the required environment 
Line 86: every time it starts up. If the environment is not as expected, the program 
Line 87: should notify the user with an error message. That makes it much easier 
Line 88: for a user to determine what the problem is than a “This program had a 
Line 89: problem” message. 
Line 90: Test Sequence 
Line 91: Ideally, tests should be independent so they can run in any sequence without 
Line 92: dependencies on other tests. To ensure that tests are as independent as possible, 
Line 93: use a common setup ( Chapter 31) only when necessary. As noted in that chap-
Line 94: ter, the setup part of a test (“Given”) should ensure that the state of the system 
Line 95: is examined to see that it matches what the test requires. Internally, this can be 
Line 96: done by either checking that the condition is as described or making the condi-
Line 97: tion be that which is described. 
Line 98: Workﬂow Tests 
Line 99: Often, there are workﬂows: sequences of operations that are performed to reach 
Line 100: a goal. You should test each operation separately. Then you might have a work-
Line 101: ﬂow test. A workﬂow tests includes multiple operations that need to be run in a 
Line 102: particular order to demonstrate that the system processes the sequence correctly. 
Line 103: Use case tests should have a single action table in them. Workﬂows that have 
Line 104: multiple use cases within them may have multiple action tables in their tests. Try 
Line 105: 
Line 106: --- 페이지 217 ---
Line 107:  
Line 108: Chapter 22 Test Evaluation
Line 109: 194
Line 110: not to have too many complicated workﬂow tests. They can be fragile or hard to 
Line 111: maintain. See Chapter 28, “Case Study: A Library Print Server,” for an example 
Line 112: of a workﬂow test. 
Line 113: Test Conditions 
Line 114: A set of tests should abide by these three conditions: 1
Line 115: 1. A test should fail for a well-deﬁned reason. (That is what the test is check-
Line 116: ing.) The reason should be speciﬁc and easy to diagnose. Each test case has 
Line 117: a scope and a purpose. The failure reason relates to the purpose. 
Line 118: 2. No other test should fail for the same reason. Otherwise, you may have a 
Line 119: redundant test. You may have a test fail at each level—an internal business 
Line 120: rule test and a workﬂow test that uses one case of the business rule. If the 
Line 121: business rule changes and the result for that business rule changes, you will 
Line 122: have two failing tests. You want to minimize overlapping tests. But if the 
Line 123: customer wants to have more tests because they are familiar or meaningful 
Line 124: to him, do it. Remember: The customer is in charge of the tests. 
Line 125: 3. A test should not fail for any other reason. This is the ideal, but it is often 
Line 126: hard to achieve. Each test has a three part sequence: setup, action/trigger, 
Line 127: and expected result. The purpose of the test is to ensure that the actual 
Line 128: result is equal to the expected result. A test may fail because the setup did 
Line 129: not work or the action/trigger did not function properly. 
Line 130: Separation of Concerns 
Line 131: The more that you can separate concerns, the easier it can be to maintain the 
Line 132: tests. With separation, changes in the behavior of one aspect of the application 
Line 133: do not affect other aspects. Here are some parts that can be separated, as shown 
Line 134: earlier in this book: 
Line 135: •  Separate business rules from the way the results of business rules are dis-
Line 136: played ( Chapter 14, “Separate View from Model”). 
Line 137:   1 . These came from Amir Kolsky. 
Line 138: 
Line 139: --- 페이지 218 ---
Line 140: Test Conditions 
Line 141: 195
Line 142: • Separate the calculation of a business rule, such as a rating, from the use 
Line 143: of that business rule ( Chapter 13, “Simpliﬁcation by Separation”). 
Line 144: • Separate each use case or step in a workﬂow ( Chapter 8, “Test Anatomy”). 
Line 145: • Separate validation of an entity from use of that entity ( Chapter 16, “De-
Line 146: veloper Acceptance Tests”). 
Line 147: You can have separate tests for the simplest things. For example, the customer 
Line 148: ID formatting functionality needs to be tested. The test can show the kinds of 
Line 149: issues that the formatting deals with. If the same module is used anywhere a cus-
Line 150: tomer ID is used, other tests do not have to perform checks for invalid customer 
Line 151: IDs. And if the same module is not used, you have a design issue. A test of ID 
Line 152: might be as follows. 
Line 153: Customer ID Format 
Line 154: ID 
Line 155: Valid? 
Line 156: Notes
Line 157: 007 
Line 158: Y
Line 159: 1 
Line 160: N 
Line 161: Too few characters 
Line 162: 0071 
Line 163: N 
Line 164: Too many characters 
Line 165: Test Failure 
Line 166: As noted before in Chapter 3, “Testing Strategy,” a passing test is a speciﬁcation 
Line 167: of how the system works. A failing test indicates that a requirement has not been 
Line 168: met. Initially, before an implementation is created, every acceptance test should 
Line 169: fail. If a test passes, you need to determine why it passed. 
Line 170: • Is the desired behavior that the test checks already covered by another test? 
Line 171: If so, the new test is redundant. 
Line 172: • Does the implementation already cover the new requirement? 
Line 173: • Is the test really not testing anything? For example, the expected result 
Line 174: may be the default output of the implementation. 2
Line 175:   2. Any new test that passes the ﬁrst time without a change in the implementation 
Line 176: should be made to fail by brieﬂy changing the implementation. This ensures that the 
Line 177: test is actually testing something. 
Line 178: 
Line 179: --- 페이지 219 ---
Line 180: Chapter 22 Test Evaluation
Line 181: 196
Line 182: Test Redundancy 
Line 183: You want to avoid test redundancy. Redundancy often occurs when you have 
Line 184: data-dependent calculations. For example, here are the rental fees for different 
Line 185: category CDs that were shown in Chapter 10, “User Story Breakup.” 
Line 186: CD Rental Fees 
Line 187: Category
Line 188: Standard Rental 
Line 189: Days
Line 190: Standard Rental 
Line 191: Charge
Line 192: Extra Day 
Line 193: Rental Charge 
Line 194: Regular 
Line 195: 2 
Line 196: $2 
Line 197: $1
Line 198: Golden Oldie 
Line 199: 3 
Line 200: $1 
Line 201: $.50
Line 202: Hot Stuff 
Line 203: 1 
Line 204: $4 
Line 205: $2
Line 206: Here were the tests that were created. 
Line 207: Rental Charges 
Line 208: Type 
Line 209: Days 
Line 210: Cost?
Line 211: Regular 
Line 212: 3 
Line 213: $3
Line 214: Golden Oldie 
Line 215: 3 
Line 216: $1
Line 217: Hot Stuff 
Line 218: 3 
Line 219: $8
Line 220:  
Line 221: Do you need all these tests? Are they equivalent? They all use the same under-
Line 222: lying formula (Cost = Standard Rental Charge + (Number Rental Days – Stand-
Line 223: ard Rental Days) * Extra Day Rental Charge). 3 When the ﬁrst test passes, the 
Line 224: other tests also pass. 
Line 225: What if there are lots of categories? Say there are 100 different ones that all 
Line 226: use this same formula. That would be a lot of redundant tests. If there was an 
Line 227: identiﬁed risk in not running them, then they may be necessary. 4 A collaborative 
Line 228: triad should be able to cut down these tests to the essential ones. 
Line 229: Test variations of business rules or calculations separately, unless they affect 
Line 230: the ﬂow through a use case or user story. 
Line 231: In an effort to avoid redundancy, don’t shortcut tests. Have at least one posi-
Line 232: tive and one negative test. For example, there should be a test with a customer 
Line 233:   3.  Depending on how the code is written, a single test might provide 100% code cover-
Line 234: age. If you have that coverage, do you need more tests? 
Line 235:   4.  These tests may not be performed during the standard build-test cycle if they take 
Line 236: excessive time. 
Line 237: 
Line 238: --- 페이지 220 ---
Line 239: Points to Remember 
Line 240: 197
Line 241: ID that is valid and one that is not valid. Be sure to test each exception. For 
Line 242: example, with the CD rental limit of three, have a test for renting three CDs (the 
Line 243: happy path) and four CDs (the exception path). 
Line 244: No Implementation Issues 
Line 245: Tests should be minimally maintainable. Make them depend on the behavior 
Line 246: being tested, not the implementation underneath. This way they require little 
Line 247: maintenance work. Unless the desired behavior has changed, the test should 
Line 248: not have to change, regardless of any implementation changes underneath. To 
Line 249: achieve this, design tests as if they had to work with multiple implementations. 
Line 250: Tests should not imply that you need a database underneath. You can have a 
Line 251: slew of ﬁle clerks who took down the data, ﬁled it away in folders, and retrieved 
Line 252: it when requested. Of course, the system would take a little bit longer. The 
Line 253: tables in the tests such as CD Data represent the business view of the objects, 
Line 254: not the persistence layer view. They will be used to create the database tables, 
Line 255: so there will be similarities. 
Line 256: Points to Remember 
Line 257: When creating and implementing tests, consider the following: 
Line 258: • Develop tests and automation separately. Understand the test ﬁrst, and 
Line 259: then explore how to automate it. 
Line 260: • Automate the tests so that they can be part of a continuous build. See 
Line 261: Appendix C, “Test Framework Examples,” for examples of automation. 
Line 262: • Don’t put test logic in the production code. Tests should be completely 
Line 263: separate from the production code. 5
Line 264: • As much as practical, cover 100% of the functional requirements in the 
Line 265: acceptance tests. 
Line 266:   5.  In some cases, such as hardware chip design, it is acceptable for production code to 
Line 267: have a built-in self-test to conﬁrm that assumptions about the system’s environment 
Line 268: still hold and all elements of the system are functioning correctly. 
Line 269: 
Line 270: --- 페이지 221 ---
Line 271: Chapter 22 Test Evaluation
Line 272: 198
Line 273: In structuring tests, remember the following: 
Line 274: •  Tests should follow the Given-When-Then or the Arrange-Act-Assert form 
Line 275: [AAA01].
Line 276: •  Keep tests simple. 
Line 277: • Only have the essential detail in a test. 
Line 278: • Avoid lots of input and output columns. Break large tables into smaller 
Line 279: ones, or show common values in the headers ( Chapter 18, “Entities and 
Line 280: Relationships”).
Line 281: • Avoid logic in tests. 
Line 282: •  Describe the intent of the test, not just a series of steps. 
Line 283: A test has several costs involved in writing and testing it, executing it, and main-
Line 284: taining it. The tests deliver the beneﬁts of communicating requirements and 
Line 285: identifying defects. The incremental cost of a new test should be less than the 
Line 286: incremental beneﬁt that that test delivers. 
Line 287: Summary
Line 288: • Make acceptance tests readable to customers. 
Line 289: • Separate concerns—test one concept with each test. 
Line 290: • Avoid test redundancy. 