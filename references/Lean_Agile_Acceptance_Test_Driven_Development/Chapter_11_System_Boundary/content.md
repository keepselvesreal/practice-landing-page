Line 1: 
Line 2: --- 페이지 126 ---
Line 3: Chapter 11 
Line 4: System Boundary 
Line 5: “You cannot always control what goes on outside. But you can always 
Line 6: control what goes on inside.”
Line 7: Wayne Dyer 
Line 8: The triad works on stories that involve interfaces to external systems. Tom 
Line 9: explicates on test doubles and mocks. 
Line 10: External Interfaces 
Line 11: Debbie starts off, “Now that we’ve determined correctly how much to charge 
Line 12: the customer, let’s move on to the Submit Charge story. I see the high-level tests 
Line 13: for this were as follows.” 
Line 14: Submit Charge 
Line 15: •  Submit the charge to the credit card company. Check that the bank 
Line 16: account receives money from the charge. 
Line 17: “Cathy, would you explain how charging works,” Debbie asked. 
Line 18: Cathy answers. “I’ve talked with my bank and the credit-card processing 
Line 19: company. The rental system needs to send a charge to the credit-card processor, 
Line 20: like our current charge card reader does. The processor returns a message that 
Line 21: the charge is accepted or declined. At the end of the day, the processor makes 
Line 22: a bank transfer for all the charges during a day less any charge-backs and the 
Line 23: processing fee. Don’t get me started on the size of that processing fee. Anyway, 
Line 24: I can go online and see the transfers that were made during the previous days. 
Line 25: 103
Line 26: 
Line 27: --- 페이지 127 ---
Line 28: Chapter 11 System Boundary
Line 29: 104
Line 30: 104
Line 31: If I need to, I can get a listing of all the charges that were made from the credit-
Line 32: card processor. I can also conﬁrm with my bank to see that the transfer was 
Line 33: received.”
Line 34: Debbie draws a diagram (see Figure 11.1). She says, “This is my understand-
Line 35: ing of what you said. Am I right?” 
Line 36: Charge 
Line 37: CD Rental
Line 38: System
Line 39: Credit Card
Line 40: Processor
Line 41: Sam’s
Line 42: Bank
Line 43: Bank
Line 44: Statement
Line 45: Accepted or 
Line 46: Declined
Line 47: Transfer To
Line 48: Figure 11.1 Credit-Card Charge Processing 
Line 49: “That looks good to me,” Cathy replies. 
Line 50: Tom states, “Do you have in mind some acceptance tests for this workﬂow?” 
Line 51: “Yes,” Cathy replies. “It seems like there are two acceptance tests. The ﬁrst 
Line 52: is to verify that the credit-card processor got all the transactions that the rental 
Line 53: system said it sent. And the second makes sure the bank got all the transfers that 
Line 54: the processor said it sent. So the ﬁrst one would be this.” 
Line 55: Card Processor Charges Matches Rental Charges 
Line 56: Given a list of credit-card charges that the rental system sent for a day: 
Line 57: Credit-Card Charges from Rental System 
Line 58: Day = 1/21/2011 
Line 59: Card Number 
Line 60: Customer Name 
Line 61: Amount 
Line 62: Time
Line 63: 4005550000000019 
Line 64: James 
Line 65: $2 
Line 66: 10:53 a.m. 
Line 67: 4111111111111111 
Line 68: Maxwell 
Line 69: $10 
Line 70: 10:59 a.m. 
Line 71: When I request a list of charges for the day from the credit-card processor: 
Line 72: 
Line 73: --- 페이지 128 ---
Line 74: External Interfaces 
Line 75: 105
Line 76: Request Rental Charges from Processor 
Line 77: Enter 
Line 78: Date 
Line 79: 1/21/2011
Line 80: Press 
Line 81: Submit
Line 82: Then the charges should match the list from the rental system. 
Line 83: Credit-Card Charges from Processor 
Line 84: Day = 1/21/2011 
Line 85: Card Number 
Line 86: Customer Name 
Line 87: Amount 
Line 88: Time
Line 89: 4005550000000019 
Line 90: James 
Line 91: $2 
Line 92: 10:53 a.m. 
Line 93: 4111111111111111 
Line 94: Maxwell 
Line 95: $10 
Line 96: 10:59 a.m. 
Line 97: Cathy continues, “As ﬁnance manager, I’ve gotten this report of credit-card 
Line 98: charges many times, but I’ve only been concerned with the dollar numbers. The 
Line 99: three of us should see if you two need to know about anything else on the report. 
Line 100: For example, there is a column for transaction ID on the report. That might be 
Line 101: useful.”
Line 102: Tom replies, “That would be great. We could run this test as an acceptance 
Line 103: test for the system. In that case, we would do a manual comparison of the two 
Line 104: lists, and we could incorporate the comparison into part of daily process. If we 
Line 105: did that, Debbie could create a way to compare the information you down-
Line 106: loaded to the list that the rental system generates. We could create a story to do 
Line 107: that. Have you ever had a problem with a charge not showing up?” 
Line 108: Cathy answers, “There may have been one or two, but it’s never been an issue 
Line 109: that crossed my mind. The effort of calling up the credit-card processor to check 
Line 110: on a $2 charge isn’t really worth it. So I think we can put that story on hold.” 
Line 111: “Oh, I forgot,” Cathy exclaimed. “What about charge-backs? How should 
Line 112: we handle those?” 
Line 113: Debbie replied, “We can give it to you in whatever form is easiest for you to 
Line 114: match up. If the transactions from the credit-card processor are listed separately 
Line 115: as charges and charge-backs, we’ll give you two lists. If they are listed on one 
Line 116: list, say sorted by the time, we’ll give you one list. Our job is to create a system 
Line 117: that makes it easy for you to do your job.” 
Line 118: Tom queries, “Cathy, is there another test you apply to the ﬂow?” 
Line 119: Cathy replies, “There should be one to verify that a transfer was made each 
Line 120: day and that the bank received it. This step follows after the ﬁrst one. So the test 
Line 121: would be this.” 
Line 122: 
Line 123: --- 페이지 129 ---
Line 124: Chapter 11 System Boundary
Line 125: 106
Line 126: Cathy continues, “I do this every now and then for a whole set of days. In the 
Line 127: past few years, I’ve never seen a transfer for the amount absent from the bank 
Line 128: statement. There was one time it was off by a day, so there were two transfers on 
Line 129: the same day. I’ll continue to do so for the present. We can put off automating 
Line 130: this process until later.” 
Line 131: Cathy concludes, “This whole idea of charging our customers automatically 
Line 132: instead of handling cash is appealing. Of course, we may lose a few customers 
Line 133: who don’t want to have their rentals appear on their credit-card statements. I 
Line 134: know of one whose spouse would become really angry, to put it mildly, if the 
Line 135: amount of money spent on CD rentals became known. But the savings in the 
Line 136: clerk’s time in collecting money and balancing a cash drawer, my time in tak-
Line 137: ing deposits to the bank, and the insurance costs of not having money on the 
Line 138: premises will more than make up for any lost rentals. Please get going on Submit 
Line 139: Charge pronto.” 
Line 140: Charges Agree with Transfer 
Line 141: Given the charges processed by the credit-card processor: 
Line 142: Credit-Card Charges from Processor 
Line 143: Day = 1/21/2011 
Line 144: Card Number 
Line 145: Customer Name 
Line 146: Amount 
Line 147: Time
Line 148: 4005550000000019 
Line 149: James 
Line 150: $2 
Line 151: 10:53 a.m. 
Line 152: 4111111111111111 
Line 153: Maxwell 
Line 154: $10 
Line 155: 10:59 a.m. 
Line 156: When the bank statement is checked the next day for transfers made: 
Line 157: Request Transfers from Bank 
Line 158: Enter 
Line 159: Day 
Line 160: 1/21/2011
Line 161: Press 
Line 162: Submit
Line 163: Then there should be a transfer for the total of the charges less the process-
Line 164: ing fee. 
Line 165: Transfers Received by Bank 
Line 166: Day = 1/21/2011 
Line 167: From 
Line 168: Amount 
Line 169: Notes
Line 170: Credit-Card Processor 
Line 171: $10.80 
Line 172: 10% fee 
Line 173: 
Line 174: --- 페이지 130 ---
Line 175: External Interfaces 
Line 176: 107
Line 177: More Details 
Line 178: Debbie says, “I think we’ve got the big picture for this story. Let’s take a look 
Line 179: at more details. From the results of the Check-In story [ Chapter 10, “User Story 
Line 180: Breakup”], we have a rentals fee to be charged for a particular day. This fee 
Line 181: becomes the input for the next step: Submit a charge to the credit-card proces-
Line 182: sor. An additional test for Check-In appears as follows.” 
Line 183: Charge Submitted During Check-In 
Line 184: Given that the customer has a credit-card number and has a CD rented: 
Line 185: Customer Data 
Line 186: Name 
Line 187: ID 
Line 188: Credit-Card Number 
Line 189: James 
Line 190: 007 
Line 191: 4005550000000019
Line 192: CD Data 
Line 193: ID 
Line 194: Title 
Line 195: Rented
Line 196: CD
Line 197: Category 
Line 198: Customer ID 
Line 199: Rental Due 
Line 200: CD3 
Line 201: Janet Jackson 
Line 202: Number Ones 
Line 203: Yes 
Line 204: Regular 
Line 205: 007 
Line 206: 1/23/2011
Line 207: When the CD is returned and the rental fee computed: 
Line 208: Test Date 
Line 209: Date
Line 210: 1/23/2011
Line 211: Check-In CD 
Line 212: Enter 
Line 213: CD ID 
Line 214: CD3
Line 215: Press 
Line 216: Submit
Line 217: Rental Fee 
Line 218: Customer
Line 219: ID 
Line 220: Name 
Line 221: Title 
Line 222: Rental Fee 
Line 223: Return
Line 224: Day
Line 225: Return
Line 226: Time
Line 227: 007 
Line 228: James 
Line 229: Janet Jackson 
Line 230: Number Ones 
Line 231: $2 
Line 232: 1/23/2011 
Line 233: 10:53 a.m. 
Line 234: 
Line 235: --- 페이지 131 ---
Line 236: Chapter 11 System Boundary
Line 237: 108
Line 238: Then submit a charge to the credit-card processor at that time. 
Line 239: Credit-Card Charge 
Line 240: Card Number 
Line 241: Customer Name 
Line 242: Amount 
Line 243: Date 
Line 244: Time
Line 245: 4005550000000019 
Line 246: James 
Line 247: $2 
Line 248: 1/23/2011 
Line 249: 10:53 a.m. 
Line 250: External Interface Tests 
Line 251: Debbie starts off, “So far, we can create the values for a card charge and conﬁrm 
Line 252: that the charge is received by the credit-card processor. However, there is still 
Line 253: one missing piece: having the rental system actually submit the charge. Cathy, 
Line 254: can you go through the possibilities from the business side? How do you submit 
Line 255: a card charge now?” 
Line 256: Cathy replies, “The clerk enters the amount and swipes the card. Either a 
Line 257: card charge is conﬁrmed, or it is declined. Based on how we’ve been expressing 
Line 258: tests, I can see two cases.” 
Line 259: Given a valid credit-card charge: 
Line 260: When the charge is submitted to the credit-card processor.
Line 261: Then a charge accepted status is received. 
Line 262: Given an invalid credit-card charge: 
Line 263: When the charge is submitted to the credit-card processor.
Line 264: Then a charge declined status is received. 
Line 265: “With the manual system, if a charge is declined, the clerk asks for another 
Line 266: card. I guess that will be harder to do with this application. I’ll think about what 
Line 267: to do for the second condition and get back to you on that.” 
Line 268: Debbie says, “That’s ﬁne. It’ll take a little time to get the information I need 
Line 269: from the credit processor.” 
Line 270: Component Tests 
Line 271: After a while, the triad meets again. Debbie starts off, “The credit-card proces-
Line 272: sor has coding standards and protocols on how to submit a charge and what 
Line 273: messages are transmitted between a merchant’s system and a retailer’s system. 
Line 274: Once I understood some of the issues, I determined I needed a component that 
Line 275: 
Line 276: --- 페이지 132 ---
Line 277: External Interface Tests 
Line 278: 109
Line 279: would handle the charge submission. I created component tests that my code 
Line 280: needed to pass. Using your cases, they are as follows.” 
Line 281: Given a valid credit-card charge: 
Line 282: Card Charge 
Line 283: Customer
Line 284: Name
Line 285: Street
Line 286: Address City 
Line 287: State ZIP
Line 288: Charge
Line 289: Identiﬁer 
Line 290: CC
Line 291: Issuer
Line 292: CC
Line 293: Number 
Line 294: Expires 
Line 295: Amount
Line 296: James
Line 297: 36500
Line 298: Some-
Line 299: where
Line 300: Street
Line 301: Anchor
Line 302: Point
Line 303: AK
Line 304: 99556 Sam CD 
Line 305: Rental
Line 306: Return
Line 307: 1-23-
Line 308: 2011
Line 309: Visa
Line 310: 4005550
Line 311: 00000
Line 312: 0019
Line 313: 01/2020 $1.00
Line 314: When the charge is submitted to the credit-card processor: 
Line 315: •  (Contact website and submit properly formatted charge.) 
Line 316: Then the charge is accepted 
Line 317: •  and a message is received with this data. 
Line 318: Transaction Receipt 
Line 319: Transaction ID 
Line 320: Amount 
Line 321: Charge Identiﬁcation 
Line 322: Result
Line 323: 123456789012345 
Line 324: $1 
Line 325: Sam CD Rental Return 
Line 326: 1-23-2011
Line 327: Accepted
Line 328: “I made up one for charge declined: The input information includes a credit 
Line 329: number that should be declined.” 
Line 330: Invalid Card Response Is Charge Declined 
Line 331: Given a invalid credit-card charge: 
Line 332: Card Charge 
Line 333: Customer
Line 334: Name
Line 335: Street
Line 336: Address City 
Line 337: State 
Line 338: ZIP
Line 339: Charge
Line 340: Identiﬁer 
Line 341: CC
Line 342: Issuer
Line 343: CC
Line 344: Number 
Line 345: Expires Amount
Line 346: James
Line 347: 36500
Line 348: Some-
Line 349: where
Line 350: Street
Line 351: Anchor
Line 352: Point
Line 353: AK
Line 354: 99556
Line 355: Sam CD 
Line 356: Rental
Line 357: Return
Line 358: 1-23-
Line 359: 2011
Line 360: Visa
Line 361: 411111
Line 362: 11111
Line 363: 11111
Line 364: 1/2020
Line 365: $1.00
Line 366: 
Line 367: --- 페이지 133 ---
Line 368: Chapter 11 System Boundary
Line 369: 110
Line 370: “Now how all this information is formatted and transmitted is technical and 
Line 371: detailed. I’ll be using test-driven development with unit tests to design the code 
Line 372: that passes this component test. As you can see, the tests have a lot of detail for 
Line 373: the card charge. The reason I’m showing them to you is they bring up business 
Line 374: questions. A simple one is how do you want to phrase the Charge Identiﬁcation 
Line 375: that appears on the customer’s statement?” 
Line 376: Cathy replies, “That looks okay to me. What else?” 
Line 377: Debbie continues, “I found that there are a lot of reasons a card can be 
Line 378: rejected. Many of the rejections are for reasons such as the expiration date being 
Line 379: in a bad format. These types of issues I will handle in the component. They are 
Line 380: standard programming concerns. But I’ve come up with some results that call for 
Line 381: a business decision. I may come across a few more when I get into the details.” 
Line 382: Declined Reasons 
Line 383: Card number not on ﬁle 
Line 384: Contact the ﬁnancial institution 
Line 385: Expired credit card 
Line 386: Debbie says, “You need to decide what should be done in each of these cases.” 
Line 387: Cathy works through the options and comes up with the following actions. 
Line 388: Credit-Card Charge Declined Actions 
Line 389: Reasons 
Line 390: Action 
Line 391: Notes
Line 392: Card number
Line 393: not on ﬁle 
Line 394: Inform the customer. 
Line 395: Get information for another 
Line 396: card.
Line 397: Generate a dialog box on 
Line 398: check-in.
Line 399: Generate an e-mail to Cathy. 
Line 400: When the charge is submitted to the credit-card processor: 
Line 401: •  (Contact website and submit a properly formatted charge.) 
Line 402: Then the charge is declined. 
Line 403: •  and a message is received with this data. 
Line 404: Transaction Receipt 
Line 405: Transaction ID 
Line 406: Amount
Line 407: Charge
Line 408: Identiﬁcation 
Line 409: Result 
Line 410: Reason
Line 411: 123456789012346 
Line 412: $1 
Line 413: Sam CD Rental 
Line 414: Return 1-23-2011 
Line 415: Declined 
Line 416: Card not
Line 417: on ﬁle 
Line 418: continues
Line 419: 
Line 420: --- 페이지 134 ---
Line 421: External Interface Tests 
Line 422: 111
Line 423: Credit-Card Charge Declined Actions 
Line 424: Reasons 
Line 425: Action 
Line 426: Notes
Line 427: Contact the
Line 428: ﬁnancial 
Line 429: institution
Line 430: Do not inform the customer. 
Line 431: Make person look up at
Line 432: security camera. 
Line 433: Put up a message to call the 
Line 434: police.
Line 435: Card may be stolen. 
Line 436: Expired credit 
Line 437: card
Line 438: Inform the customer. 
Line 439: Get information for another 
Line 440: card.
Line 441: Generate a dialog box. 
Line 442: Generate an e-mail to Cathy. 
Line 443: Debbie continues, “Tom and I will come up with tests that generate all these 
Line 444: results to make sure the action occurs. Details will need to be gathered on the 
Line 445: wording of the dialog boxes and e-mail messages. But those are display con-
Line 446: cerns, not business rule issues.” 
Line 447: Tom asks, “Debbie, what happens if the network goes down in the middle 
Line 448: of processing a credit-card transaction? You and I both know that periodically 
Line 449: the Internet seems to come to a grinding halt, which is the equivalent of going 
Line 450: down.”
Line 451: Debbie replies, “I’ll just queue up the charges and submit them when it does 
Line 452: come back up. I’ll add a component test to make sure that is what happens.” 
Line 453: Tom answers, “What if it doesn’t come up for full day?” 
Line 454: Debbie counters, “I can send them when it does. But the date of the charge 
Line 455: will not match the date of the return. Cathy, will that work for you?” 
Line 456: Cathy replies, “We faced the same problem when the phone line was down. 
Line 457: The clerks had to write down the credit-card numbers and submit them the 
Line 458: next day. We did have one customer who knew the line was down, so he used 
Line 459: an invalid card. But you can only do so much. Submitting them when you can 
Line 460: sounds ﬁne to me.” 
Line 461: Test Doubles and Mocks 
Line 462: Cathy has a burning question. “How are you going to run all these tests? Are 
Line 463: you going to use your credit-card number? How can you make sure that a credit 
Line 464: card is rejected for a particular reason?” 
Line 465: Debbie answers, “One way to do it is to use Tom’s cards. He’s maxed out on 
Line 466: some of them. But the banks might get after Tom for trying to use those credit 
Line 467: cards. So we will use what many developers call a test double [Meszaros01]. A 
Line 468: test double is something that stands in for a real system when tests are being 
Line 469: run. It comes from the idea of a double who stands in for the real actor when 
Line 470: shooting a movie.” 
Line 471: , Continued
Line 472: 
Line 473: --- 페이지 135 ---
Line 474: Chapter 11 System Boundary
Line 475: 112
Line 476: “A test double encompasses a couple of other concepts that you might hear 
Line 477: Tom and me or other developers throw around. They are mock [Hillside01], 
Line 478: stub, and fake. [Craig01]. The mock term comes from Alice in Wonderland by 
Line 479: Lewis Carroll. You may remember the line:” 
Line 480: “Once,” said the Mock Turtle at last, with a deep sigh, “I was a real Turtle.” 
Line 481: Debbie continues, “I’m not going to get into the differences and details 
Line 482: between these three terms. That’s something that developers love to discuss on 
Line 483: blogs. The key is that using test doubles makes a system easier to test. The credit-
Line 484: card processor provides a test double. Instead of connecting to the real credit-
Line 485: card system, you connect to the test double that’s provided. The test double 
Line 486: accepts credit-card charges and returns conﬁrmations just like the real system.” 
Line 487: “To get the test double to return different results, you send it different com-
Line 488: binations of values. For example, with your processor, you send a charge for the 
Line 489: credit-card number 4111111111111111. This causes a charge to be declined.” 
Line 490: “If there wasn’t already a test double, I would write one myself. In fact, 
Line 491: whenever there is some external interface to a system, I usually create a test 
Line 492: double. In this case, as long as I can have all the different results sent back to 
Line 493: me, I don’t need my own test double. I haven’t checked, but I’m sure there is 
Line 494: some number I can send that would create a result that puts up a dialog to call 
Line 495: the police. If not, I’ll bet one of Tom’s cards would do that.” 
Line 496: “To test the complete system, we do need to make some credit-card charges 
Line 497: all the way from the return of a CD through seeing it on the credit charges proc-
Line 498: essed list. We’ll use your card for a good one and use an invalid number to see 
Line 499: if things are rejected.” 
Line 500: What Is Real? 
Line 501: A system in production—“the real world”—interacts with many things outside 
Line 502: itself. It may ask an external service for information or to do a calculation or 
Line 503: perform an action. Events may occur at random times and in random sequences 
Line 504: that require a response from the system. In production, there is usually no con-
Line 505: trol over these external interactions. But in testing, control is needed so that 
Line 506: the same test case can be performed over and over again and still get the same 
Line 507: expected result. 
Line 508: An external service may provide the same information every time it is 
Line 509: requested. (In programmers’ terms, it is idempotent.) Even so, the developer 
Line 510: may want to create a test double for it so the tests run faster. The context of our 
Line 511: system is shown in Figure 11.2.
Line 512: 
Line 513: --- 페이지 136 ---
Line 514: Story Map of Activities 
Line 515: 113
Line 516: Time
Line 517: System
Line 518: in
Line 519: Production
Line 520: Random
Line 521: Events
Line 522: External
Line 523: Service
Line 524: Figure 11.2 System Context 
Line 525: You often need control of time to get tests to run the same way. The test dou-
Line 526: ble that the credit-card processor provides allows for repeatable tests. If there 
Line 527: were random events that the system had to respond to, a test double for them 
Line 528: would be created. 
Line 529: As an example, suppose several clerks were doing check-outs and check-ins 
Line 530: at the same time. The developer could simulate a sequence of check-outs and 
Line 531: check-ins. A test double would generate a series of actions like the following 
Line 532: sequence to see if the implantation could handle it. 
Line 533: Rental Sequence 
Line 534: Operation 
Line 535: CD ID 
Line 536: Customer ID 
Line 537: Date 
Line 538: Time
Line 539: Check-out 
Line 540: CD7 
Line 541: 99 
Line 542: 1/21/2011 
Line 543: 11:01:01.001 p.m. 
Line 544: Check-out 
Line 545: CD4 
Line 546: 99 
Line 547: 1/21/2011 
Line 548: 11:01:01.002 p.m. 
Line 549: Check-out 
Line 550: CD5 
Line 551: 007 
Line 552: 1/21/2011 
Line 553: 11:01:01.003 p.m. 
Line 554: Check-out 
Line 555: CD2 
Line 556: 86 
Line 557: 1/21/2011 
Line 558: 11:01:01.004 p.m. 
Line 559: Check-in 
Line 560: CD7 
Line 561: 1/21/2011 
Line 562: 11:01:03.005 p.m. 
Line 563: Check-out 
Line 564: CD3 
Line 565: 007 
Line 566: 1/21/2011 
Line 567: 11:01:03.006 p.m. 
Line 568: Check-in 
Line 569: CD4 
Line 570: 1/21/2011 
Line 571: 11:01:03.007 p.m. 
Line 572: Story Map of Activities 
Line 573: As described in Chapter 7, “Collaborating on Scenarios,” a story map can or-
Line 574: ganize various stories into activities. For the stories so far, the map could look 
Line 575: like the following (see Figure 11.3). As soon as the top story for each activity is 
Line 576: 
Line 577: --- 페이지 137 ---
Line 578: Chapter 11 System Boundary
Line 579: 114
Line 580: completed, the entire workﬂow from check-in through seeing the entry in the 
Line 581: card processor’s report can be executed. 
Line 582: Handle
Line 583: Declined Credit
Line 584: Cards
Line 585: Submit Normal
Line 586: Charge
Line 587: List Card Charges
Line 588: Compute Rental
Line 589: Charge for Multiple
Line 590: Rates
Line 591: Check-In
Line 592: Workflow
Line 593: Compute
Line 594: Rental Charge 
Line 595: Check-In CD
Line 596: Compute Rental
Line 597: Charge for 
Line 598: Single Rate
Line 599: Submit
Line 600: Charge
Line 601: View Report
Line 602: Check-In
Line 603: Figure 11.3 Check-In Story Map 
Line 604: Summary
Line 605: • Create acceptance tests for external interfaces. 
Line 606: • Developers can create component tests for internal processing 
Line 607: functionality.
Line 608: • Details from lower levels may generate questions that need customer 
Line 609: answers.
Line 610: • Use test doubles or mocks for external interfaces to simplify testing. 
Line 611: • Create story maps to organize stories into workﬂows. 