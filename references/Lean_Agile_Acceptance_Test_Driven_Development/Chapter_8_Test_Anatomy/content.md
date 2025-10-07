Line 1: 
Line 2: --- 페이지 92 ---
Line 3: Chapter 8 
Line 4: Test Anatomy 
Line 5: “Whoever named it necking was a poor judge of anatomy.”
Line 6: Groucho Marx 
Line 7: Tests for scenarios are now developed (see Figure 8.1). The basic structure of 
Line 8: tests—given, when, then—is explained. Examples are shown in tables and text. 
Line 9: Charter 
Line 10: Scenario 
Line 11: Test
Line 12: Story
Line 13: Feature
Line 14: Focus
Line 15: Figure 8.1 Creating Tests 
Line 16: Triad Creates Tests 
Line 17: All three members of the triad create tests. The customer usually leads with 
Line 18: examples for the basic workﬂow tests, and the developers and testers come up 
Line 19: with ones from their training and experience. Testers are responsible for en-
Line 20: suring that there is a set of tests that is as complete as practical. For example, 
Line 21: Tom might envision more tests that can be run for the use case in the previous 
Line 22: chapter:
Line 23: 69
Line 24: 
Line 25: --- 페이지 93 ---
Line 26: Chapter 8 Test Anatomy
Line 27: 70
Line 28: Ideally, the triad should come up with all tests prior to Debbie starting to 
Line 29: implement the story. But sometimes, they may discover a test during imple-
Line 30: mentation or later. During exploratory testing, Tom or the team may discover 
Line 31: missed conditions or other issues that suggest new tests. If the need to create 
Line 32: tests post-implementation occurs frequently, the team should investigate the 
Line 33: root cause. 
Line 34: Test Context 
Line 35: A system’s operation is deﬁned by its inputs and its outputs, as shown in  Figure
Line 36: 8.2. This is a context diagram. What is external to a system is outside the circle. 
Line 37: These externalities deﬁne the context in which the system operates. An input or 
Line 38: sequence of inputs should result in a determinable output. For example, if the 
Line 39: clerk inputs a rental for a particular customer and a particular CD, the output 
Line 40: should be a rental contract. If the clerk inputs another rental for the same CD 
Line 41: without its being checked in, he should get an error. 
Line 42: The response of the system is different the second time someone tries to rent 
Line 43: the CD, because the system has stored (that is, made persistent) the rental infor-
Line 44: mation for the ﬁrst check-out. 
Line 45: A system can store the rental data internally or externally. If it stores the data 
Line 46: internally, it changes the internal state of the system. If it stores the data exter-
Line 47: nally, the data is simply another output and input to the system. 
Line 48: For Sam’s system, the data will be treated as internally persistent. Renting a 
Line 49: CD the second time causes a different output because the state of the system is 
Line 50: different. Part of a test involves specifying what the current state of the system is. 
Line 51: Output
Line 52: Persistent Storage 
Line 53: Input
Line 54: Output
Line 55: Input
Line 56: System
Line 57: External
Line 58: Persistence
Line 59: System
Line 60: Internal
Line 61: Persistence
Line 62: Figure 8.2 Context Diagram 
Line 63: Check Out Rented CD—Customer attempts to rent a CD that is already 
Line 64: rented.
Line 65: CD ID Not Recognized—The system does not recognize the CD ID. 
Line 66: 
Line 67: --- 페이지 94 ---
Line 68: Test Structure 
Line 69: 71
Line 70: Test Structure 
Line 71: There is a basic ﬂow to a test, shown in  Figure 8.3. The test starts with setting 
Line 72: up the state of the system. Then a trigger occurs—an event or action is made to 
Line 73: happen. The test has an expected outcome of that event—a change in the state 
Line 74: of the system or an output from the system. The test compares that expected 
Line 75: outcome to the actual outcome of the system under test. If the two are equal, the 
Line 76: test succeeds; otherwise, it fails. The ﬂow is often shown in text like this: 
Line 77: Given <setup> 
Line 78: When <event or action> 
Line 79: Then <expected outcome> 
Line 80: Setup
Line 81: (Given)
Line 82: Initial
Line 83: System
Line 84: State
Line 85: Verify
Line 86: (Then)
Line 87: Trigger
Line 88: (When)
Line 89: Event or Action 
Line 90: Final System
Line 91: State and
Line 92: Output
Line 93: Expected
Line 94: System State
Line 95: and Output
Line 96: Figure 8.3 Test Flow 
Line 97: For simple calculations, like the discount in Chapter 4, “An Introductory 
Line 98: Acceptance Test,” the action is just calling some module to perform a calcula-
Line 99: tion. So the form could look like this: 
Line 100: Given <inputs> 
Line 101: When <computation occurs> 
Line 102: Then <expected results> 
Line 103: 
Line 104: --- 페이지 95 ---
Line 105: Chapter 8 Test Anatomy
Line 106: 72
Line 107: The computations looked like this. 
Line 108: Discount Calculation 
Line 109: Item Total 
Line 110: Customer Rating 
Line 111: Discount Percentage? 
Line 112: $10.00 
Line 113: Good 
Line 114: 0%
Line 115: $10.01 
Line 116: Good 
Line 117: 1%
Line 118: $50.01 
Line 119: Good 
Line 120: 1%
Line 121: $.01 
Line 122: Excellent 
Line 123: 1%
Line 124: $50.00 
Line 125: Excellent 
Line 126: 1%
Line 127: $50.01 
Line 128: Excellent 
Line 129: 5%
Line 130: So a single test case could be as follows: 
Line 131: Given Item Total of $10.00 and a Customer Rating of Good 
Line 132: When computing the discount percentage 
Line 133: Then the output should be 0% 
Line 134: In the discount example, there are six combinations of values for the input. 
Line 135: Each combination (or row in the table) is a test case. For something like a cal-
Line 136: culation, the group of these test cases can be referred to as a calculation test or 
Line 137: a business rule test.
Line 138: The ﬂow for the tests for Check Out CD would be something like this: 
Line 139: Given (Setup) 
Line 140: Customer has ID (initial system state) 
Line 141: CD has ID (initial system state) 
Line 142: CD is not currently rented (initial system state) 
Line 143: When (Trigger) 
Line 144: Clerk checks out CD (action) 
Line 145: Then (Verify) 
Line 146: CD recorded as rented (ﬁnal system state) 
Line 147: Rental contract printed (output) 
Line 148: 
Line 149: --- 페이지 96 ---
Line 150: Test Structure 
Line 151: 73
Line 152:  
Line 153: There can be multiple ways to ﬂow through a use case. Each exception or 
Line 154: alternative in a use case is called a scenario, because there is a different ﬂow. 
Line 155: For each scenario, a different test scenario is needed that has a different setup 
Line 156: or a different action. A test case is a test scenario with the actual data. The term 
Line 157: acceptance test, as used in this book, may refer to a single test case or a group of 
Line 158: test cases for either calculations or scenarios. 
Line 159: Business rule tests are usually not as complicated as test scenarios. The busi-
Line 160: ness rules often have no initial state setup, and the veriﬁcation is simply compar-
Line 161: ing a single result to the expected result. 
Line 162: Because a test scenario is more complicated, you should not duplicate it just 
Line 163: for a different business rule case. Separately testing the business rule can reduce 
Line 164: the number of test scenarios that need to be written. 
Line 165: When writing a test, use the same domain language you use to write up the 
Line 166: stories. The consistency reduces misunderstandings. If you discover during 
Line 167: the test writing that the terms are ambiguous, go back and ﬁx the glossary and 
Line 168: the stories. 
Line 169: To complete a test case, the case needs values that are setup, input, and out-
Line 170: put. These values can be speciﬁed in tables or in text, whichever way the cus-
Line 171: tomer prefers. 
Line 172: Customers who have experience with spreadsheets may like having the values 
Line 173: in tables because that is more familiar. Tables come in many forms. Three com-
Line 174: mon ones are the calculation table, the data table, and the action table. 
Line 175: Calculation Table 
Line 176: The table structure used in the previous discount calculation example in Chapter
Line 177: 4 followed this form. 
Line 178: Title
Line 179: Input Name 1 
Line 180: Input Name 2 
Line 181: Result Name? 
Line 182: Notes
Line 183: Value for input 1 
Line 184: Value for input 2 
Line 185: Expected output 
Line 186: Anything that
Line 187: describes scenario 
Line 188: Another value for 
Line 189: input 1 
Line 190: Another value for 
Line 191: input 2 
Line 192: Another expected 
Line 193: output
Line 194: This structure is used primarily for calculations. 1 A question mark (?) appears 
Line 195: after names that represent outputs. Following is an example of this table with 
Line 196: only one input and one output. 
Line 197:   1 . The structure is sometimes used for actions, such as recording that a CD is rented, 
Line 198: particularly for lots of test cases for the same action. There is another structure used 
Line 199: speciﬁcally for actions, which will be described shortly. 
Line 200: 
Line 201: --- 페이지 97 ---
Line 202: Chapter 8 Test Anatomy
Line 203: 74
Line 204: CD Rentals 
Line 205: CD ID 
Line 206: Rented?
Line 207: CD2 
Line 208: No
Line 209: CD3 
Line 210: Yes
Line 211: The name of the input is CD ID, and the name of the result is Rented. The 
Line 212: value for the input is CD2, and the expected output is No. 
Line 213: Another example of this table is the one that was used for discounts. The two 
Line 214: input names are Item Total and Customer Rating. The result is Discount Per-
Line 215: centage. The input values are $10.00 and Good, and the expected output is 0%. 
Line 216: Discount Calculation 
Line 217: Item Total 
Line 218: Customer Rating 
Line 219: Discount Percentage? 
Line 220: $10.00 
Line 221: Good 
Line 222: 0%
Line 223: Data Table 
Line 224: Another table structure declares that information in the system exists (or should 
Line 225: exist). Part of the name of the table can indicate that it is a data table rather than 
Line 226: a calculation table. 
Line 227: Title
Line 228: Value Name 1 
Line 229: Value Name 2 
Line 230: Value for 1 
Line 231: Value for 2 
Line 232: Another value for 1 
Line 233: Another value for 2 
Line 234: Here’s an example for customer data. This shows that there should be a 
Line 235: customer whose name is James and whose customer ID is 007 and a customer 
Line 236: named Maxwell whose customer ID is 86. 
Line 237: Customer Data 
Line 238: Name 
Line 239: ID
Line 240: James 
Line 241: 007
Line 242: Maxwell 
Line 243: 86
Line 244: The columns represent different ﬁelds in a data record, and each row repre-
Line 245: sents a data record. But the table does not have to correspond to any speciﬁc 
Line 246: database table. It can represent any collection of the data items. It is the user’s 
Line 247: 
Line 248: --- 페이지 98 ---
Line 249: Test Structure 
Line 250: 75
Line 251: view of how the data elements are related, regardless of how they are stored. If 
Line 252: the table is used for the setup part of a test, the data is put into the collection, if 
Line 253: it does not already exist. If the table is used as expected values, the test fails if the 
Line 254: data items do not exist in the collection or have different values. 
Line 255: There is a variation of the data table that shows only rows that meet certain 
Line 256: criteria. The criteria are speciﬁed after the name. For example, if you only want 
Line 257: to see customers whose names begin with J, you could have the following. 
Line 258: Customer Data 
Line 259: Name Begins with=“’J” 
Line 260: Name 
Line 261: ID
Line 262: James 
Line 263: 007
Line 264: Action Table 
Line 265: The third table structure is an action table. The easiest way to describe the table 
Line 266: is that it works like a dialog box, although it can be used for other purposes. If 
Line 267: a team member needs to visualize a system through a user interface, an action 
Line 268: table can often stand in for a dialog box. 
Line 269: The table starts with a title that represents a procedure or the name of a dia-
Line 270: log box. The ﬁrst column has one of three verbs:  enter, press, and check. Each 
Line 271: verb has an object that it uses. Enter enters data into an entry ﬁeld;  press initi-
Line 272: ates a process, such as a Submit button on a dialog box; check sees if a result is 
Line 273: equal to an expected value. 
Line 274: Action Name 
Line 275: Enter 
Line 276: Value Name 1 
Line 277: Value for 1 
Line 278: Enter 
Line 279: Value Name 2 
Line 280: Value for 2 
Line 281: Press 
Line 282: Submit
Line 283: Check 
Line 284: Value Name 3 
Line 285: Expected value for 3 
Line 286: Following is an example for Check Out CD. 
Line 287: Check Out CD 
Line 288: Enter 
Line 289: Customer ID 
Line 290: 007
Line 291: Enter 
Line 292: CD ID 
Line 293: CD2
Line 294: Press 
Line 295: Submit
Line 296: Check 
Line 297: Rented 
Line 298: True
Line 299: 
Line 300: --- 페이지 99 ---
Line 301: Chapter 8 Test Anatomy
Line 302: 76
Line 303: Some people are horizontally oriented. Others are vertically oriented. The 
Line 304: action table can be represented horizontally. If there is a repeated set of actions, 
Line 305: using the previous layouts requires repeating the value names. So sometimes a 
Line 306: table that looks like a calculation table is used for actions. For example, if a 
Line 307: customer checked out two CDs, it could look like this. 
Line 308: Check Out CD 
Line 309: Customer ID 
Line 310: CD ID 
Line 311: Rented?
Line 312: 007 
Line 313: CD2 
Line 314: True
Line 315: 007 
Line 316: CD1 
Line 317: True
Line 318: Tests with Example Values 
Line 319: Tom starts off, “Let’s put some data into the test structure. Cathy, can you give 
Line 320: me an example of a rental?” 
Line 321: Cathy puts up some values on the whiteboard. After the triad discusses them, 
Line 322: they come up with this test: 
Line 323: Check Out CD 
Line 324: Given Customer has ID 
Line 325: and CD has ID 
Line 326: and CD is not currently rented 
Line 327: Customer Data 
Line 328: Name 
Line 329: ID
Line 330: James 
Line 331: 007
Line 332: CD Data 
Line 333: ID 
Line 334: Title 
Line 335: Rented
Line 336: CD2 
Line 337: Beatles Greatest Hits 
Line 338: No
Line 339: When a clerk checks out a CD: 
Line 340: Check Out CD 
Line 341: Enter 
Line 342: Customer ID 
Line 343: 007
Line 344: Enter 
Line 345: CD ID 
Line 346: CD2
Line 347: Press 
Line 348: Submit
Line 349: 
Line 350: --- 페이지 100 ---
Line 351: Tests with Example Values 
Line 352: 77
Line 353: Tom says, “The rental contract shows the information that will be printed on 
Line 354: the form, but not all the surrounding text. This way, you can be sure that the 
Line 355: correct information is on the contract. Later on, you can decide with Sam how 
Line 356: the rental contract should be worded.” 
Line 357: Requirements Revised 
Line 358: “Now that you can see how the test is structured, does it look like anything is 
Line 359: missing?,” Tom asked. 
Line 360: “Yes,” Cathy replied. “The tables deﬁnitely make things more apparent. 
Line 361: Every CD has a rental period. If the customer returns the CD after the end of the 
Line 362: rental period, we charge him a late fee. The rental contract should have the date 
Line 363: of the end of the rental period. We also want the rental fee itself on this contract, 
Line 364: but I think we covered that in another story.” 
Line 365: “Okay,” said Tom. “Let’s revise the tables to include this rental period. Let 
Line 366: me make sure of something. To get the date for the rental period end date, you 
Line 367: add the rental period to the start date. Is that right?” 
Line 368: “Sure,” said Cathy. 
Line 369: “Okay, so let’s make up a quick table to check out both the calculation and 
Line 370: our terminology,” Tom stated. The triad came up with this. 
Line 371: Calculate Rental End 
Line 372: Start Date 
Line 373: Rental Period (Days) 
Line 374: Rental Due? 
Line 375: Notes
Line 376: 1/21/2011 
Line 377: 2 
Line 378: 1/23/2011
Line 379: 2/28/2012 
Line 380: 3 
Line 381: 3/2/2012 
Line 382: Leap Year 
Line 383: 12/31/2010 
Line 384: 4 
Line 385: 1/4/2011 
Line 386: New Year 
Line 387: Then the CD is recorded as rented and a rental contract is printed: 
Line 388: CD Data 
Line 389: ID 
Line 390: Title 
Line 391: Rented 
Line 392: Customer ID 
Line 393: CD2 
Line 394: Beatles Greatest Hits 
Line 395: Yes 
Line 396: 007
Line 397: Rental Contract 
Line 398: Customer ID 
Line 399: Customer Name 
Line 400: CD ID 
Line 401: CD Title 
Line 402: 007 
Line 403: James 
Line 404: CD2 
Line 405: Beatles Greatest Hits 
Line 406: 
Line 407: --- 페이지 101 ---
Line 408: Chapter 8 Test Anatomy
Line 409: 78
Line 410: Cathy says, “It looks like Tom came up with some odd cases. Thinking about 
Line 411: leap years is not something I would normally consider.” 
Line 412: Tom continues, “So you want the rental due date on the rental contract. 
Line 413: I guess we should keep it with the CD as well so we know when it’s due. I 
Line 414: just have a feeling from the bigger picture—the Inventory Report story—that it 
Line 415: would be a good idea. Because that story is coming up soon, it’s okay to con-
Line 416: sider it now as part of our big picture scope. “ 
Line 417: Acceptance Test Revised 
Line 418: Tom continues, “So given that we have that simple calculation correct, what 
Line 419: our tests need to do is set the current date. We do not want to have to change 
Line 420: our test just because the date has changed. I’ll show how we set a date here and 
Line 421: talk about it more when we discuss test doubles [see Chapter 11, “User Story 
Line 422: Breakup”]. So the test could now read:” 
Line 423: Check Out CD 
Line 424: Given Customer has ID 
Line 425: and CD has ID 
Line 426: and CD is not currently rented 
Line 427: Customer Data 
Line 428: Name 
Line 429: ID
Line 430: James 
Line 431: 007
Line 432: CD Data 
Line 433: ID 
Line 434: Title 
Line 435: Rented 
Line 436: Rental Period 
Line 437: CD2 
Line 438: Beatles Greatest Hits 
Line 439: No 
Line 440: 2
Line 441: When the clerk checks out the CD: 
Line 442: Test Date 
Line 443: Date
Line 444: 1/21/2011
Line 445: 
Line 446: --- 페이지 102 ---
Line 447: Test with Values in Text 
Line 448: 79
Line 449: The example tables have been presented with formatting that distinguishes 
Line 450: between the column headers and the data. The formatting is not mandatory. 
Line 451: When coming up with these on the whiteboard, headers are not bolded. Teams 
Line 452: take pictures of the whiteboard, transcribe the information into tables, and have 
Line 453: the customers review them to make sure no errors crept in. 
Line 454: Test with Values in Text 
Line 455: Some triads use what looks like regular text to specify the tests. So they might 
Line 456: write something that looks like this: 
Line 457: Check Out CD 
Line 458: Enter 
Line 459: Customer ID 
Line 460: 007
Line 461: Enter 
Line 462: CD ID 
Line 463: CD2
Line 464: Press 
Line 465: Submit
Line 466: Then the CD is recorded as rented and a rental contract is printed: 
Line 467: CD Data 
Line 468: ID 
Line 469: Title 
Line 470: Rented 
Line 471: Customer ID 
Line 472: Rental Due 
Line 473: CD2 
Line 474: Beatles Greatest Hits 
Line 475: Yes 
Line 476: 007 
Line 477: 1/23/2011
Line 478: Rental Contract 
Line 479: Customer ID 
Line 480: Customer Name 
Line 481: CD ID 
Line 482: CD Title 
Line 483: Rental
Line 484: Due
Line 485: 007 
Line 486: James 
Line 487: CD2 
Line 488: Beatles Greatest Hits 
Line 489: 1/23/2011
Line 490: Given
Line 491: Customer “James” with ID 007 
Line 492: and CD with ID CD2, title “Beatles Greatest Hits,” 
Line 493: a rental period of 2 days,
Line 494: and is not currently rented: 
Line 495: When
Line 496: The clerk checks out the CD with ID CD2 
Line 497: to customer with ID 007 on 1/21/2011 
Line 498: 
Line 499: --- 페이지 103 ---
Line 500: Chapter 8 Test Anatomy
Line 501: 80
Line 502: There is a table form that is halfway between the text and a table [Martin02]. 
Line 503: The entry ﬁeld names and the values are in a single row. An example of this 
Line 504: layout for the When part of the test looks like this. 
Line 505: Check Out 
Line 506: CD with ID 
Line 507: CD2 
Line 508: to Customer with ID 
Line 509: 007 
Line 510: On 
Line 511: 1/21/2011
Line 512: The examples of tests in this book are presented with tables. It is usually 
Line 513: easier to translate a table into narrative text than it is to do the reverse. For busi-
Line 514: ness rules, such as discount percentage, that have multiple test cases, it is usu-
Line 515: ally less repetitive to express these cases in a table, rather than in free text. The 
Line 516: names and column headers, which represent the domain language [see Chapter
Line 517: 24, “Context and Domain Language”], are separate from the values. This can 
Line 518: make it easier to check for consistency. 
Line 519: When and Where Tests Are Run 
Line 520: The acceptance test for the Check Out CD test can be on multiple levels. It can 
Line 521: be run as a user acceptance test through the user interface. It can also be tested 
Line 522: though the middle tier by simulating the input from the user interface. 2 Or a 
Line 523: unit test can be written to ensure that the rented value is changed to Yes when 
Line 524: the check out occurs. 
Line 525: Then
Line 526: CD with ID CD2 is recorded as rented 
Line 527: and rental is contract printed with customer ID 007, customer name 
Line 528: “James,” CD ID CD2, CD title “Beatles Greatest Hits,” 
Line 529: and rental due on 1/23/2011 
Line 530: 2. See [Koskela02] for other ways to run acceptance tests. 
Line 531: 
Line 532: --- 페이지 104 ---
Line 533: Summary 
Line 534: 81
Line 535: Summary
Line 536: • The structure of a test is 
Line 537: • Given <setup> 
Line 538: • When <action or event> 
Line 539: • Then <expected results> 
Line 540: • For calculation tests, the structure is 
Line 541: • Given <input> 
Line 542: • When <computation occurs> 
Line 543: • Then <expected results> 
Line 544: • Following are three types of tables: 
Line 545: • Calculation—Gives result for particular input 
Line 546: • Data—Gives data that should exist (or be created if necessary) 
Line 547: • Action—Performs some action 
Line 548: 
Line 549: --- 페이지 105 ---
Line 550: This page intentionally left blank 