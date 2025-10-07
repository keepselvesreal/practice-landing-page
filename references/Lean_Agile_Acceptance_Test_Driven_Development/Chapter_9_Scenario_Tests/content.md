Line 1: 
Line 2: --- 페이지 106 ---
Line 3: Chapter 9 
Line 4: Scenario Tests 
Line 5: “I did then what I knew how to do. Now that I know better, I do better.”
Line 6: Maya Angelou 
Line 7: The triad creates tests for the exceptions in a use case. Tom explains the levels at 
Line 8: which the tests are run. Debbie shows how early implementation can give quick 
Line 9: feedback on meeting the charter’s objectives. 
Line 10: Tests for Exception Scenarios 
Line 11: Cathy starts off, “We’ve ﬁnished the test for the main course of the Check Out 
Line 12: CD use case. I suppose we should do tests for the other scenarios, because we’re 
Line 13: focused on that use case. Where should we start?” 
Line 14: Tom replies, “If you had limited time, Debbie and I would create tests for the 
Line 15: exceptions and alternatives and then review them with you. You’ve already told 
Line 16: us how the system should respond to many of the exceptions and given us an 
Line 17: example for the main course. But because you have the time and interest, let’s 
Line 18: create a test for the scenario Check Out Rented CD. The customer attempts to 
Line 19: rent a CD that is already rented. The change is in the setup. What do you want 
Line 20: to see as a result?” 
Line 21: Cathy replies, “I think the clerk should see an error message.” 
Line 22: 83
Line 23: 
Line 24: --- 페이지 107 ---
Line 25: Chapter 9 Scenario Tests
Line 26: 84
Line 27: Tom states, “So the test looks like the following:” 
Line 28: CD Already Rented 
Line 29: Given a CD that has already been rented: 
Line 30: CD Data 
Line 31: ID 
Line 32: Title 
Line 33: Rented 
Line 34: Rental Period 
Line 35: CD2 
Line 36: Beatles Greatest Hits 
Line 37: Yes 
Line 38: 2
Line 39: Customer Data 
Line 40: Name 
Line 41: ID
Line 42: Maxwell 
Line 43: 86
Line 44: When a customer attempts to rent the CD, an error message is displayed. 
Line 45: Check Out CD 
Line 46: Enter 
Line 47: Customer ID 
Line 48: 86
Line 49: Enter 
Line 50: CD ID 
Line 51: CD2
Line 52: Press 
Line 53: Submit
Line 54: Check 
Line 55: Error Message 
Line 56: CD_Already_Rented
Line 57: Tom continues, “You can see that the customer data is the same. We could 
Line 58: put the Customer Data table into a common location and reference it from the 
Line 59: other tests. There is a trade-off between using a common setup and redoing the 
Line 60: setup for every test. We’ll talk about that later [see Chapter 31, “Test Setup”]. 
Line 61: The difference in the setup in this case is that the CD is already rented. The 
Line 62: difference in the result, which we put as the ﬁnal step in the action, is that an 
Line 63: error is produced. The Check in the last table veriﬁes that the error message is 
Line 64: reported as CD_Already_Rented. This name could be what is output, or it could 
Line 65: represent text that is determined later. No contract is printed out since the error 
Line 66: occurred.”
Line 67: “Another test scenario is CD Rental Limit. This is when a customer who has 
Line 68: three CDs rented tries to rent another one. We need to setup the situation where 
Line 69: a customer has rented three CDs. Without repeating the Customer Data, the 
Line 70: setup looks like this:” 
Line 71: 
Line 72: --- 페이지 108 ---
Line 73: Tests for Exception Scenarios 
Line 74: 85
Line 75: “We included one additional aspect in this setup. It’s customer ID = 007. This 
Line 76: table reﬂects the rentals for which the customer ID is 007 or James. That way, 
Line 77: we do not have to duplicate the 007 in every row for the Customer ID column. 
Line 78: Also, if the CD data in the system has rentals for customers other than 007, this 
Line 79: table only reﬂects those for 007. Now, you might notice that Rented is Yes for 
Line 80: every row. So we could move that up to the ﬁrst line. 
Line 81: Given a customer who has rented the CD limit of three: 
Line 82: CD Data 
Line 83: Customer ID = 007 
Line 84: ID 
Line 85: Title 
Line 86: Rented 
Line 87: Rental Due 
Line 88: CD2 
Line 89: Beatles Greatest Hits 
Line 90: Yes 
Line 91: 1/23/2011
Line 92: CD3 
Line 93: Lucy Michelle Hits 
Line 94: Yes 
Line 95: 1/24/2011
Line 96: CD4 
Line 97: Janet Jackson Hits 
Line 98: Yes 
Line 99: 1/25/2011
Line 100: CD Limit Reached 
Line 101: Given a customer who has rented the CD limit of three: 
Line 102: CD Data 
Line 103: Rented = Yes 
Line 104: Customer ID = 007 
Line 105: ID 
Line 106: Title 
Line 107: Rental Due 
Line 108: CD2 
Line 109: Beatles Greatest Hits 
Line 110: 1/23/2011
Line 111: CD3 
Line 112: Lucy Michelle Hits 
Line 113: 1/24/2011
Line 114: CD4 
Line 115: Janet Jackson Hits 
Line 116: 1/25/2011
Line 117: When James attempts to rent another CD, an error message is displayed. 
Line 118: Checkout CD 
Line 119: Enter 
Line 120: Customer ID 
Line 121: 007
Line 122: Enter 
Line 123: CD ID 
Line 124: CD5
Line 125: Press 
Line 126: Submit
Line 127: Check 
Line 128: Error Message 
Line 129: CD_Rental_Limit_Exceeded
Line 130: “In this case, the error message is different from the previous test. To check 
Line 131: that the CD limit was applied correctly, we should make up a test where two 
Line 132: CDs are currently rented. If this story was critical, I might try more conditions. 
Line 133: 
Line 134: --- 페이지 109 ---
Line 135: Chapter 9 Scenario Tests
Line 136: 86
Line 137: For example, I could try to rent lots of CDs and make sure that the error occurs 
Line 138: on every attempt after the third CD.” 
Line 139: “The given part of this test could be simpliﬁed. In this case, the title of the 
Line 140: CD and the rental due dates are not needed by the test. So it could be shown as 
Line 141: the following:” 
Line 142: CD Data 
Line 143: Rented = Yes 
Line 144: Customer ID = 007 
Line 145: ID
Line 146: CD2
Line 147: CD3
Line 148: CD4
Line 149: “This test scenario might be further condensed into a single table, such as 
Line 150: this one:” 
Line 151: CD Limit Reached 
Line 152: Given a customer who has rented a number of CDs, is he allowed to rent 
Line 153: another one? 
Line 154: CD Limit Business Rule 
Line 155: Current Rentals for Customer 
Line 156: Allowed?
Line 157: CD2, CD3 
Line 158: Yes
Line 159: CD2, CD3, CD4 
Line 160: No
Line 161: Tom continues, “This is a simple business rule test. You can test it by con-
Line 162: necting to the module that implements the rule. Then you need to create a test 
Line 163: that ensures the business rule is correctly connected to the check-out process. 
Line 164: That test would look like the uncondensed one.” 
Line 165: A Couple More Scenarios 
Line 166: In a ﬁnancial application, one customer wanted the tester to add an addi-
Line 167: tional test scenario. In the application, the net worth of the corporation 
Line 168: was computed every day. The net worth calculation depended on the cur-
Line 169: rent Federal Reserve inter-bank rate. The developer asked what rate to use 
Line 170: if the inter-bank rate was unavailable due to a server or network issue. The 
Line 171: customer replied that he wanted a way to input the rate manually. 
Line 172: 
Line 173: --- 페이지 110 ---
Line 174: Tests for Business Rules 
Line 175: 87
Line 176: Tests for Business Rules 
Line 177: Cathy states, “I think I’ve gotten the idea now. Sam and I were thinking of 
Line 178: another business rule. We won’t let a customer rent another CD if he has one 
Line 179: that is late. So, based on your examples, here’s what I think the test should look 
Line 180: like:”
Line 181: The tester then asked what the rate should be if the Federal Reserve goes 
Line 182: broke and has no rate. The customer answered, “Then I think we’ll have a 
Line 183: few other things to worry about in that case. Without the Federal Reserve, 
Line 184: our net worth would be zero.” 
Line 185: Current Late Rental When Renting 
Line 186: Given a customer who has a rental that has not been returned by the due 
Line 187: date:
Line 188: Test Date 
Line 189: Date
Line 190: 1/24/2011
Line 191: CD Data 
Line 192: Rented = Yes 
Line 193: Customer ID = 007 
Line 194: ID 
Line 195: Rental Due 
Line 196: CD2 
Line 197: 1/23/2011
Line 198: When he attempts to rent another CD, notify him that he has a late rental 
Line 199: and he cannot rent the CD. 
Line 200: Check Out CD 
Line 201: Enter 
Line 202: Customer ID 
Line 203: 007
Line 204: Enter 
Line 205: CD ID 
Line 206: CD3
Line 207: Press 
Line 208: Submit
Line 209: Check 
Line 210: Error Message 
Line 211: Customer_Has_Late_Rental
Line 212: 
Line 213: --- 페이지 111 ---
Line 214: Chapter 9 Scenario Tests
Line 215: 88
Line 216: Cross-Story Issues 
Line 217: Tom notes, “It’s possible that both the CD Limit and the Late Rental conditions 
Line 218: occur at the same time. For example:” 
Line 219: CD Limit Reached and Late Rental 
Line 220: Given a customer who has a rental that has not been returned by the due 
Line 221: date:
Line 222: Test Date
Line 223: Date
Line 224: 1/24/2011
Line 225: and who has reached the CD limit of three: 
Line 226: CD Data 
Line 227: Rented = Yes 
Line 228: Customer ID = 007 
Line 229: ID 
Line 230: Rental Due 
Line 231: CD2 
Line 232: 1/23/2011
Line 233: CD3 
Line 234: 1/24/2011
Line 235: CD4 
Line 236: 1/25/2011
Line 237: When the customer attempts to rent another CD, an error message is 
Line 238: displayed.
Line 239: Checkout CD 
Line 240: Enter 
Line 241: Customer ID 
Line 242: 007
Line 243: Enter 
Line 244: CD ID 
Line 245: CD5
Line 246: Press 
Line 247: Submit
Line 248: Check 
Line 249: Error Message 
Line 250: CD_Rental_Limit_Exceeded
Line 251: Cathy interrupts, “I can see from the test what the issue is. Should the sys-
Line 252: tem report Customer_Has_Late_Rental or CD_Rental_Limit_Exceeded? In this 
Line 253: case, even if the customer returns the two CDs that are not late, he cannot rent 
Line 254: a CD. So I’d have the system report as Customer_Has_Late_Rental. When the 
Line 255: customer return the late CD, the CD limit will not be reached.” 
Line 256: Tom resumes, “This is an example of cross-story issues. As best as we try, 
Line 257: some stories have issues with other stories. Many times, we can identify these in 
Line 258: advance. At other times, we may not discover the issues until later.” 
Line 259: 
Line 260: --- 페이지 112 ---
Line 261: Don’t Automate Everything 
Line 262: 89
Line 263: Disk Monitor
Line 264: Report Error If Disk
Line 265: Does Not Respond
Line 266: Within 1 Second
Line 267: Power Saver
Line 268: Spin Down Disk If Not
Line 269: Accessed in Past Minute
Line 270: Figure 9.1 Cross-Story Interaction 
Line 271: Don’t Automate Everything 
Line 272: Tom starts off, “Cvathy, we’ve created a couple of exceptions for entering a bad 
Line 273: customer ID.” Debbie could program this into the system. She could track the 
Line 274: number of times a bad customer ID was entered and put up an appropriate error 
Line 275: message. I’d have to write some tests to ensure that was coded correctly.” Cathy 
Line 276: replies, “It seems like this exception could be handled by manual instructions to 
Line 277: the clerk. It could be:” 
Line 278: Unit Tests Are Not Enough 
Line 279: Several companies make highly available disk storage systems. As part of 
Line 280: the system, there is a monitoring module that checks to see if each disk has 
Line 281: problems (see Figure 9.1). One measurement it uses is the response time 
Line 282: for a disk. If a disk does not return requested data in a certain amount 
Line 283: of time, such as 1 second, the monitor reports a failure. Tests are run to 
Line 284: ensure that the monitor operates properly. 
Line 285: A second requirement has been added to make the system green. To 
Line 286: save power, a power saver monitor turns a disk off if it is not accessed for 
Line 287: a certain amount of time. The tests for that requirement also passed. 
Line 288: Testing the individual pieces is insufﬁcient to verify the entire system. 
Line 289: When the new feature was tested in an integrated environment, the disk 
Line 290: monitor signaled failures at random times. The power saver was turning 
Line 291: off disks when they had not been accessed in the recent past. The next time 
Line 292: a powered-down disk was accessed, it sometimes took more than a second 
Line 293: to respond, because it had to be powered up. So the disk monitor reported 
Line 294: an error. When the operator checked the disk, it was perfectly ﬁne. 
Line 295: If the system responds with a bad customer ID, try re-entering the ID. If 
Line 296: you try the ID a second time and it does not work, make a copy of the 
Line 297: customer’s driver’s license and manually ﬁll out a rental contract for the 
Line 298: customer to sign. 
Line 299: 
Line 300: --- 페이지 113 ---
Line 301: Chapter 9 Scenario Tests
Line 302: 90
Line 303: Tom continues, “Then we just have to write a test for one bad customer ID.” 
Line 304: Bad Customer ID 
Line 305: Given that we have all valid customers in our customer data: 
Line 306: Customer Data 
Line 307: Name 
Line 308: ID
Line 309: James 
Line 310: 007
Line 311: Maxwell 
Line 312: 86
Line 313: When a customer ID is entered that is not valid, inform the clerk. 
Line 314: Check Out CD 
Line 315: Enter 
Line 316: Customer ID 
Line 317: 99
Line 318: Enter 
Line 319: CD ID 
Line 320: CD3
Line 321: Press 
Line 322: Submit
Line 323: Check 
Line 324: Error Message 
Line 325: Customer_ID_Invalid
Line 326: “The cost of implementing and testing for the number of bad entries is prob-
Line 327: ably not justiﬁed by a business value. But that’s your call. Part of our job is not 
Line 328: just to deliver software to you, but to deliver software that delivers business 
Line 329: value.”
Line 330: Multi-Level Tests 
Line 331: Tom starts off, “The tests we created can be used on multiple levels within the 
Line 332: system. For example, the CD Check Out Test can be applied at the user inter-
Line 333: face level or the middle tier (see Figure 9.2). If we apply the test at the middle 
Line 334: tier, we check that the functionality works in Debbie’s code. Once we design the 
Line 335: user interface, we test that the user interface is coupled properly to the correct 
Line 336: functionality in the middle tier.” 
Line 337: “As a side note, running the test at the middle-tier level ensures that busi-
Line 338: ness rules are not coded in the user interface. This makes a clean separation of 
Line 339: responsibilities between the two levels.” 
Line 340: “We may run some tests just against the middle tier, such as Calculate Rental 
Line 341: End [see Chapter 8, “Test Anatomy”]. To clarify the context, I created a dia-
Line 342: gram (see Figure 9.3). The results of that calculation show up in an output in 
Line 343: 
Line 344: --- 페이지 114 ---
Line 345: Multi-Level Tests 
Line 346: 91
Line 347: the rental contract. I’ve added an additional screen, CD Data Screen, to allow 
Line 348: viewing of CD data for setup and expected outcomes. We will use this addi-
Line 349: tional screen just during testing, not in the deployed system. It is not a good idea 
Line 350: to keep test-related functionality in production. It can cause security problems 
Line 351: and other issues.” 
Line 352: CD Check Out
Line 353: Test
Line 354: User Interface
Line 355: Middle Tier or
Line 356: Interior of 
Line 357: Application
Line 358: Persistence
Line 359: Figure 9.2 Multi-Level Tests 
Line 360: Check Out
Line 361: CD
Line 362: Screen
Line 363: CD Data
Line 364: Screen
Line 365: Rental
Line 366: Contract
Line 367: Set Date
Line 368: Screen
Line 369: Calculate Rental End
Line 370: Interior of
Line 371: Application,
Line 372: Rental
Line 373: Calculator
Line 374: User Interface
Line 375: Figure 9.3 Tests for Different Layers 
Line 376: Cathy states, “If this screen shows all the data on a CD, we could use it on 
Line 377: a regular basis. It made me think of a situation where the clerk might want to 
Line 378: know whether a particular CD was rented. Let’s make it into a requirement. 
Line 379: What will it look like?” 
Line 380: 
Line 381: --- 페이지 115 ---
Line 382: Chapter 9 Scenario Tests
Line 383: 92
Line 384: Tom displays the screen in Figure 9.4.
Line 385: ID 
Line 386: CD2
Line 387: Title 
Line 388: Beatles Greatest Hits
Line 389: Rented 
Line 390: Yes
Line 391: CD Data
Line 392: Customer ID 
Line 393: 007
Line 394: Rental Due 
Line 395: 1/23/2011
Line 396: Rental Period 
Line 397: 2
Line 398: OK
Line 399: Figure 9.4 The CD Screen 
Line 400: “The Calculate Rental End test goes into the heart of the application. You 
Line 401: probably would not use it in regular operations, so we are not going to create 
Line 402: a user interface for it. Just use a test that goes to the middle tier. However, we 
Line 403: do need the ability to set the date for the application, not for the entire compu-
Line 404: ter. Otherwise, other programs may be affected. So we could either have a Set 
Line 405: Date screen that allows the tester to manually set the date, or we could have an 
Line 406: input at the start of the program (called a command-line parameter) that sets 
Line 407: the date.” 
Line 408: “Another reason that we run Calculate Rental End to the middle tier is that 
Line 409: we can run many test cases on this business rule without the user interface. As 
Line 410: we talked about earlier [see Chapter 4, “An Introductory Acceptance Test”], 
Line 411: tests run directly to the middle tier allow execution of lots of test cases without 
Line 412: getting carpal tunnel syndrome.” 
Line 413: “All the test scenarios from the use case should be run through the user inter-
Line 414: face. But sometimes the business rules are so numerous that it could take a long 
Line 415: time to create test scenarios. For example, if there were hundreds of discount 
Line 416: levels, creating an order to test every one of them would be onerous. In cases like 
Line 417: that, if Debbie, you, and I agree that there is little risk for a particular aspect of 
Line 418: a story, it makes more sense for us to concentrate our time elsewhere. We will 
Line 419: 
Line 420: --- 페이지 116 ---
Line 421: Check the Objectives 
Line 422: 93
Line 423: run at least one case for each scenario that causes the user interface to generate 
Line 424: a different display, such as an error message.” 
Line 425: User Interface Tests 
Line 426: Tom starts off, “If you need a more visual representation of how the user in-
Line 427: terface works, we could work together to create a prototype. We might come 
Line 428: up with something like this display [see Figure 9.5]. We could get preliminary 
Line 429: feedback from you and the clerks. After Debbie implements the ﬁrst version of 
Line 430: the user interface and tests it against the acceptance tests, you and the clerks can 
Line 431: start using it. The interface may change dramatically based on your comments. 
Line 432: For example, the order and position of the two input ﬁelds might change. Or we 
Line 433: might not have a Submit button on the check-out screen. When both ﬁelds are 
Line 434: ﬁlled in, the rest of the rental process would commence.” 
Line 435: CD ID 
Line 436: CD2
Line 437: Check-Out CD
Line 438: Customer ID 
Line 439: 007
Line 440: Cancel 
Line 441: OK
Line 442: Figure 9.5 Check-Out Screen 
Line 443: “For each of the error messages that appeared during the Check Out tests 
Line 444: (such as Customer_Has_Late_Rental), Debbie will create an indication on the 
Line 445: display. The message could appear on the entry screen or in a separate dialog 
Line 446: box. The error could create a loud beep or just a quiet ding.” Cary, Mary, 
Line 447: and Harry will tell Debbie what they want. We will talk later [see Chapter 14,
Line 448: “Separate View from Model”] about ways to capture tests for displays.” 
Line 449: Check the Objectives 
Line 450: Tom continues, “Once we have a user interface for the Check Out CD story, we 
Line 451: can see how the check-out time compares to the objective stated in the project 
Line 452: 
Line 453: --- 페이지 117 ---
Line 454: Chapter 9 Scenario Tests
Line 455: 94
Line 456: charter. Remember that the measure is to achieve 50% less time [see Chapter
Line 457: 5, “The Example Project”]. We are going to start with the easiest way to imple-
Line 458: ment the check-out screen. The beneﬁt of this approach is that it requires no 
Line 459: hardware. However, it does take more clerk time and introduces the possibility 
Line 460: of errors, even if appropriate check digits are incorporated in the IDs. If we meet 
Line 461: the objective, we are done.” 
Line 462: “If we come shy of the 50%, we have a system that is faster than before. You 
Line 463: and Sam can decide whether there is a business reason for spending more money 
Line 464: to reach the 50% measure. If there is little ﬁnancial justiﬁcation, you may want 
Line 465: to revise the objective.” 
Line 466: “If the measured time is far off, we could investigate ways to cut it down. 
Line 467: We could add a handheld barcode scanner for either or both IDs. A customer 
Line 468: might forget to bring his customer card with a bar code, so we might have to 
Line 469: ﬁgure the potential time savings for just scanning the CD. And we need to take 
Line 470: into account unreadable bar codes. If the handheld scanner isn’t fast enough, we 
Line 471: could look at an in-counter scanner.” 
Line 472: “If the bar code scanner doesn’t look like it will be fast enough, well, Deb-
Line 473: bie has been dying for an opportunity to try out those new radio frequency ID 
Line 474: (RFID) microchips. With an RFID embedded in the CD case and one in the 
Line 475: customer identiﬁcation card, you could check out the customer as he walked 
Line 476: past the clerk’s desk.” 
Line 477: Debbie’s responds to the mention of RFID, “I’m pretty sure that’s overkill for 
Line 478: this size operation. But when Sam ramps up the marketing for this place after 
Line 479: the software is developed, it might be a thing to try.” 
Line 480: Tom resumes, “If we had a larger system to measure, we might record a log 
Line 481: ﬁle that monitors the speed and correctness of entries. The time delay due to 
Line 482: errors or slowness could be converted to dollars based on some conversion ratio. 
Line 483: Unfortunately, the negatives caused by the delay or customer impatience are 
Line 484: harder to measure. When the dollars that are lost due to delay justify the cost of 
Line 485: additional hardware, we can upgrade the system.” 
Line 486: Summary
Line 487: • Create a test for each exception and alternative in a use case. 
Line 488: • Do not automate everything. 
Line 489: • Run tests at multiple levels. 
Line 490: • Create a working system early to check against objectives. 